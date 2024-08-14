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
from dsplayer.utils.debug import Debuger

class Player:
    def __init__(self, voice_channel: disnake.VoiceChannel, text_channel: disnake.TextChannel, bot: commands.Bot, plugin_loader: PluginLoader, FFMPEG_OPTIONS: dict = {}, deaf: bool = True, engine: EngineInterface = YTMusicSearchEngine, debug: bool = False):
        self.queue = Queue()
        self.plugin_loader = plugin_loader
        self.voice_channel = voice_channel
        self.text_channel = text_channel
        self.voice_client = None
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS 
        self.bot = bot
        self.deaf = deaf
        self.engine = engine
        self.debug = debug
        self.debug_print = Debuger(self.debug).debug_print

    async def connect(self):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.debug_print(f"Connecting to voice channel: {self.voice_channel}")
            self.voice_client = await self.voice_channel.connect()    
        elif self.voice_client.channel != self.voice_channel:
            self.debug_print(f"Moving to voice channel: {self.voice_channel}")
            await self.voice_client.move_to(self.voice_channel)
        event_emitter.emit("on_connect", self.voice_client)

    async def disconnect(self):
        if self.voice_client is not None:
            self.debug_print("Disconnecting from voice channel")
            await self.voice_client.disconnect()
            self.voice_client = None
            event_emitter.emit("on_disconnect", self.voice_client)

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
        if self.voice_client and self.voice_client.is_playing():
            self.debug_print("Skipping current track")
            self.voice_client.stop()
            await self.play_next()
            event_emitter.emit("on_skip", self.queue)
        else:
            self.debug_print("No track is currently playing")
            event_emitter.emit("on_error", TrackError)
            raise TrackError("No track is currently playing to skip")

    async def set_volume(self, volume: float):
        if self.voice_client is not None and self.voice_client.source is not None:
            self.voice_client.source = disnake.PCMVolumeTransformer(self.voice_client.source, volume)
            event_emitter.emit("on_volume_change", volume)

    def update_plugin_settings(self, plugin_name: str, settings: dict) -> bool:
        event_emitter.emit("on_update_plugin_settings")
        return self.plugin_loader.update_plugin_settings(plugin_name, settings)

    async def play_track(self, track: dict):
        if track:
            try:
                if self.voice_client is None:
                    self.debug_print("Voice client is not initialized.")
                    return

                if not self.voice_client.is_connected():
                    self.debug_print("Voice client is not connected.")
                    return

                if not self.voice_client.is_playing():
                    self.debug_print(f"Playing track: {track}")
                    event_emitter.emit("on_play_track", [track, self.text_channel])
                    self.debug_print("Event is emitted")
                    audio_source = disnake.FFmpegPCMAudio(track['url'], **self.FFMPEG_OPTIONS)
                    
                    if audio_source:
                        self.debug_print(f"Audio source created: {audio_source}")
                        self.voice_client.play(audio_source, after=lambda e: self._track_ended(e))
                        self.debug_print("Play command sent")
                        self.queue.update_current_index()
                    else:
                        self.debug_print("Failed to create audio source.")
                        
                else:
                    self.debug_print(f"Queueing track: {track}")
                    self.queue.add_track(track)
                    event_emitter.emit("on_track_queued", track)
            except Exception as e:
                self.debug_print(f"Error playing track: {e}")
                event_emitter.emit("on_error", e)
                raise TrackError(f"Error playing track: {e}")
        else:
            self.debug_print("No track found to play")
            raise TrackNotFound("No track found to play")


    def _track_ended(self, error):
        if error:
            self.debug_print(f"Track ended with error: {error}")
            event_emitter.emit("on_error", error)

        if self.bot.loop.is_closed():
            self.debug_print("Event loop is closed")
            event_emitter.emit("on_error", RuntimeError("Event loop is closed."))
            return

        if self.voice_client and self.voice_client.is_connected():
            if self.queue.is_repeat_enabled() and self.queue.get_current_index() is not None:
                self.debug_print("Repeating current track")
                current_track_index = self.queue.get_current_index()
                if current_track_index is not None:
                    track_to_repeat = self.queue[current_track_index]
                    asyncio.run_coroutine_threadsafe(self.play_track(track_to_repeat), self.bot.loop)
            else:
                self.debug_print("Playing next track")
                self.queue.update_current_index()
                next_track = self.queue.get_next_track()
                if next_track:
                    asyncio.run_coroutine_threadsafe(self.play_track(next_track), self.bot.loop)
                else:
                    self.debug_print("Queue is empty")
                    event_emitter.emit("on_queue_empty")
        else:
            self.debug_print("Bot is not connected or voice client is unavailable")
            event_emitter.emit("on_error", RuntimeError("Bot is not connected or voice client is unavailable."))

        event_emitter.emit("on_track_end")


    async def play_next(self):
        self.debug_print("Getting next track from queue")
        next_track = self.queue.get_first()
        if next_track:
            await self.play_track(next_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty")
            await self.disconnect()

    async def play_previous(self):
        self.debug_print("Getting previous track from queue")
        back_track = self.queue.get_back_track()
        if back_track:
            await self.play_track(back_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty")
            await self.disconnect()

    async def _play_track_from_queue(self):
        if self.voice_client and self.voice_client.is_playing() and not self.queue.is_empty():
            self.debug_print("Playing track from queue")
            await self.play_next()

    async def play(self, plugin_loader: PluginLoader, url_or_query: str):
        self.debug_print(f"Searching for track with URL or query: {url_or_query}")
        plugins = plugin_loader.get_plugins()
        if self.debug:
            plugin_loader.debug()

        track_found = False
        
        if url_or_query.startswith('http'):
            for plugin in plugins:    
                patterns = plugin.get_url_patterns()
                for pattern in patterns:
                    if re.search(pattern, url_or_query):
                        try:
                            if self.debug:
                                plugin.debug()
                            track_generator = plugin.search(data=url_or_query, engine=self.engine)
                            async for track_info in track_generator:
                                if not track_found:
                                    self.debug_print(f"Adding first track: {track_info}")
                                    self.queue.add_track(track_info)
                                    await self.play_next()
                                    track_found = True
                                else:
                                    self.queue.add_track(track_info)
                                    event_emitter.emit("on_track_add_to_queue", track_info)
                            event_emitter.emit("on_track_search_end", track_generator)
                            if track_found:
                                return
                        except Exception as e:
                            self.debug_print(f"Error finding track info with plugin: {plugin.get_plugin_name()} \n{e}")
                            event_emitter.emit("on_error", e)

        for plugin in plugins:
            if plugin.__class__.__name__ == 'QueryPlugin':
                try:
                    if self.debug:
                        plugin.debug()
                    track_generator = plugin.search(data=url_or_query, engine=self.engine)
                    async for track_info in track_generator:
                        if not track_found:
                            self.debug_print(f"Adding first track: {track_info}")
                            self.queue.add_track(track_info)
                            await self.play_next()
                            track_found = True
                        else:
                            self.queue.add_track(track_info)
                            event_emitter.emit("on_track_add_to_queue", track_info)
                    event_emitter.emit("on_track_search_end", track_generator)
                    if track_found:
                        return
                except Exception as e:
                    self.debug_print(f"Error finding track info with plugin: {plugin.get_plugin_name()} \n{e}")
                    event_emitter.emit("on_error", e)

        if not track_found:
            raise TrackNotFound(f"No suitable plugin found to handle the provided data")