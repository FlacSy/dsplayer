import re
import disnake
import asyncio
from disnake.ext import commands
from dsplayer.player_system.queue import Queue
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.utils.lib_exceptions import TrackNotFound, TrackError
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.engines.ytmusic import YTMusicSearchEngine
from dsplayer.utils.events import event_emitter


class Player:
    """                                                                                
    Attributes:
        queue (Queue): A queue for managing tracks to be played.
        plugin_loader (PluginLoader): Manages loading and interacting with plugins.
        voice_channel (disnake.VoiceChannel): The voice channel where the player is connected.
        voice_client (disnake.VoiceClient): The client handling voice connections.
        FFMPEG_OPTIONS (dict): Options to customize FFmpeg audio stream.
        bot (commands.Bot): The Discord bot instance.
        deaf (bool): Indicates if the bot should be deafened when connected.
        engine (EngineInterface): The search engine used to find track information.

    Methods:
        __init__(self, voice_channel, bot, plugin_loader, FFMPEG_OPTIONS={}, deaf=True, engine=YTMusicSearchEngine):
            Initializes a new Player instance.
        async connect(self):
            Connects the player to the voice channel.
        async disconnect(self):
            Disconnects the player from the voice channel.
        async play_next(self):
            Plays the next track in the queue.
        track_ended(self, error):
            Handles actions when a track ends, triggering the next track to play.
        async get_player(self):
            Returns the current voice client instance.
        async create_event(self, event_name, *args, **kwargs):
            Dynamically triggers an event with the provided name.
        async add_and_play(self, track_info):
            Adds a track to the queue and starts playing if no track is currently playing.
        async stop(self):
            Stops playing tracks.
        async pause(self):
            Pauses the currently playing track.
        async resume(self):
            Resumes playback of the paused track.
        async skip(self):
            Skips the current track and starts playing the next one in the queue.
        async add_to_queue(self, track_info):
            Adds a track to the queue.
        async set_volume(self, volume: float):
            Sets the volume of the player.
        is_playing(self):
            Checks if the player is currently playing a track.
        is_connected(self):
            Checks if the player is connected to a voice channel.
        update_plugin_settings(self, plugin_name: str, settings: dict) -> bool:
            Updates settings for a specified plugin.
        find_track_info(self, plugin_loader: PluginLoader, data: str):
            Searches for track information based on provided data using available plugins.
    """
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
                except Exception as e:
                    event_emitter.emit("on_error", e)
                    raise TrackError(f"Error playing track: {e}")
            else:
                raise TrackNotFound("No track found to play")
        else:
            raise TrackNotFound("The queue is empty")

    async def play_previous(self):
        back_track = self.queue.get_back_track()
        if back_track:
            try:
                if not self.voice_client.is_playing():
                    event_emitter.emit("on_play_previous", back_track)
                    if self.FFMPEG_OPTIONS == {}:
                        self.voice_client.play(disnake.FFmpegPCMAudio(back_track['url']), after=lambda e: self.track_ended(e))
                    else:
                        self.voice_client.play(disnake.FFmpegPCMAudio(back_track['url'], **self.FFMPEG_OPTIONS), after=lambda e: self.track_ended(e))
                else:
                    await self.stop()
                    await self.play_previous()
            except Exception as e:
                event_emitter.emit("on_error", e)
                raise TrackError(f"Error playing previous track: {e}")
        else:
            raise TrackNotFound("No previous track found to play")

    def track_ended(self, error):
        if error:
            event_emitter.emit("on_error", error)
        
        if self.bot.loop.is_closed():
            event_emitter.emit("on_error", RuntimeError("Event loop is closed."))
            return
        
        if self.is_connected() and self.voice_client:
            asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
        else:
            event_emitter.emit("on_error", RuntimeError("Bot is not connected or voice client is unavailable."))
        
        event_emitter.emit("on_track_end")

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
            self.voice_client.stop()
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
        if self.voice_client is not None and self.voice_client.source is not None:
            self.voice_client.source = disnake.PCMVolumeTransformer(self.voice_client.source, volume)
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
