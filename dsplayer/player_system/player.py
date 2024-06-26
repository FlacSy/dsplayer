import re
import disnake
import asyncio
from disnake.ext import commands
from dsplayer.player_system.queue import Queue
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.utils.lib_exceptions import TrackNotFound, TrackError
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.engines_system.ytmusic import YTMusicSearchEngine
from dsplayer.utils.events import event_emitter


class Player:
    def __init__(self, voice_channel: disnake.VoiceChannel, bot: commands.Bot, plugin_loader: PluginLoader, FFMPEG_OPTIONS: dict = {}, deaf: bool = True, engine: EngineInterface = YTMusicSearchEngine):
        self.queue = Queue()
        self.plugin_loader = plugin_loader
        self.voice_channel = voice_channel
        self.voice_client = None
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS 
        self.bot = bot
        self.deaf = deaf
        self.engine = engine

    async def connect(self):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.voice_client = await self.voice_channel.connect()    
        elif self.voice_client.channel != self.voice_channel:
            await self.voice_client.move_to(self.voice_channel)
        event_emitter.emit("on_connect", self.voice_client)

    async def disconnect(self):
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
        event_emitter.emit("on_disconnect", self.voice_client)

    async def play_next(self):
        await self.voice_client.guild.change_voice_state(channel=self.voice_channel, self_deaf=True, self_mute=False)
        if not self.queue.is_empty():
            track = self.queue.get_next_track()
            if track:
                try:
                    if not self.voice_client.is_playing():
                        event_emitter.emit("on_play", track)
                        if self.FFMPEG_OPTIONS == {}:
                            self.voice_client.play(disnake.FFmpegPCMAudio(track['url']), after=lambda e: self.track_ended(e))
                        else:
                            self.voice_client.play(disnake.FFmpegPCMAudio(track['url'], **self.FFMPEG_OPTIONS), after=lambda e: self.track_ended(e))
                        
                        await self.bot.change_presence(activity=disnake.Game(name=track['title']))                
                except Exception as e:
                    event_emitter.emit("on_error", e)
                    raise TrackError(f"Error playing track: {e}")
            else:
                raise TrackNotFound("No track found to play")
        else:
            raise TrackNotFound("The queue is empty")

    def track_ended(self, error):
        if error:
            event_emitter.emit("on_error", error)
        event_emitter.emit("on_track_end", self.queue.current_track)
        asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)

    async def get_player(self):
        return self.voice_client

    async def create_event(self, event_name, *args, **kwargs):
        event = getattr(self, event_name)
        if event:
            await event(*args, **kwargs)

    async def add_and_play(self, track_info):
        self.queue.add_track(track_info)
        if not self.voice_client.is_playing():
            await self.play_next()
        event_emitter.emit("on_add_to_queue", track_info)

    async def stop(self):
        if self.voice_client is not None:
            self.queue.clear()
            self.voice_client.stop()
            await self.bot.change_presence(activity=None)
        event_emitter.emit("on_stop", self.queue)

    async def pause(self):
        if self.voice_client is not None:
            self.voice_client.pause()
        event_emitter.emit("on_pause", self.queue)

    async def resume(self):
        if self.voice_client is not None:
            self.voice_client.resume()
        event_emitter.emit("on_resume", self.queue)

    async def skip(self):
        if self.voice_client is not None:
            self.voice_client.stop()
            await self.play_next()
        event_emitter.emit("on_skip", self.queue)

    async def add_to_queue(self, track_info):
        self.queue.add_track(track_info)

    async def set_volume(self, volume: float):
        if self.voice_client is not None:
            if self.voice_client.source.volume > 1:
                volume = 1
            self.voice_client.source.volume = volume
            event_emitter.emit("on_volume_change", volume)

    def is_playing(self):
        return self.voice_client is not None and self.voice_client.is_playing()

    def is_connected(self):
        return self.voice_client is not None and self.voice_client.is_connected()

    def update_plugin_settings(self, plugin_name: str, settings: dict) -> bool:
        event_emitter.emit("on_update_plugin_settings")
        return self.plugin_loader.update_plugin_settings(plugin_name, settings)

    def find_track_info(self, plugin_loader: PluginLoader, data: str):
        event_emitter.emit("on_track_search_start", data)
        plugins = plugin_loader.get_plugins()
        if data.startswith('http'):
            for plugin in plugins:
                patterns = plugin.get_url_patterns()
                for pattern in patterns:
                    if re.search(pattern, data):
                        try:
                            track_info_list = plugin.search(data=data, engine=self.engine)
                            event_emitter.emit("on_track_search_end", track_info_list)
                            return track_info_list
                        except Exception as e:
                            event_emitter.emit("on_error", e)
                            raise TrackError(f"Plugin: {plugin.get_plugin_name()} \nError finding track info: {e}")

        else:
            for plugin in plugins:
                if plugin.__class__.__name__ == 'QueryPlugin':
                    try:
                        track_info = plugin.search(data, engine=self.engine)
                        if track_info:
                            event_emitter.emit("on_track_search_end", track_info)
                            return track_info
                        else:
                            raise TrackNotFound(f"Plugin: {plugin.get_plugin_name()} \nNo track info found with the provided query")
                    except Exception as e:
                        event_emitter.emit("on_error", e)
                        raise TrackError(f"Plugin: {plugin.get_plugin_name()} \nError finding track info: {e}")

        raise TrackNotFound(f"Plugin: {plugin.get_plugin_name()} \nNo suitable plugin found to handle the provided data")
