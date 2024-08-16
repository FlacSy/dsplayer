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
    def __init__(self, voice_id: int, text_id: int, bot: commands.Bot, plugin_loader: PluginLoader, volume: float = 1.0, FFMPEG_OPTIONS: dict = {}, deaf: bool = True, engine: EngineInterface = YTMusicSearchEngine, debug: bool = False):
        """
        Initializes the Player object with necessary attributes.

        :param voice_id: ID of the voice channel.
        :param text_id: ID of the text channel.
        :param bot: The bot instance.
        :param plugin_loader: PluginLoader instance for handling plugins.
        :param volume: Initial volume level.
        :param FFMPEG_OPTIONS: Options for FFMPEG.
        :param deaf: Whether to deafen the bot on connect.
        :param engine: Engine used for searching tracks.
        :param debug: Enable or disable debugging.
        """
        self.queue = Queue()
        self.plugin_loader = plugin_loader
        self.voice_channel = bot.get_channel(voice_id)
        self.text_id = text_id
        self.voice_client = None
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS 
        self.bot = bot
        self.deaf = deaf
        self.engine = engine
        self.debug = debug
        self.debug_print = Debuger(self.debug).debug_print
        self.volume = volume

        event_emitter.emit("on_init", {
            "voice_channel": self.voice_channel,
            "text_id": self.text_id,
            "volume": self.volume,
            "FFMPEG_OPTIONS": self.FFMPEG_OPTIONS,
            "deaf": self.deaf,
            "engine": self.engine,
            "debug": self.debug
        })

    async def connect(self):
        """
        Connects the bot to the voice channel. If the bot is already connected to another channel,
        it will move to the specified voice channel.
        """
        if self.voice_client is None or not self.voice_client.is_connected():
            self.debug_print(f"Connecting to voice channel: {self.voice_channel}")
            self.voice_client = await self.voice_channel.connect(deaf=self.deaf)
        elif self.voice_client.channel != self.voice_channel:
            self.debug_print(f"Moving to voice channel: {self.voice_channel}")
            await self.voice_client.move_to(self.voice_channel)

        event_emitter.emit("on_connect", {
            "voice_client": self.voice_client,
            "text_id": self.text_id,
            "voice_channel": self.voice_channel
        })

    async def disconnect(self):
        """
        Disconnects the bot from the voice channel and sets the voice client to None.
        """
        if self.voice_client is not None:
            self.debug_print("Disconnecting from voice channel")
            await self.voice_client.disconnect()
            self.voice_client = None

            event_emitter.emit("on_disconnect", {
                "voice_client": self.voice_client,
                "text_id": self.text_id,
                "voice_channel": self.voice_channel
            })

    async def stop(self):
        """
        Stops the currently playing track and clears the queue. 
        """
        if self.voice_client is not None:
            self.debug_print("Stopping playback and clearing the queue")
            self.voice_client.stop()
            self.queue.clear()
            event_emitter.emit("on_stop", {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client
            })
            await self.disconnect()

    async def pause(self):
        """
        Pauses the currently playing track.
        """
        if self.voice_client is not None:
            self.voice_client.pause()
            event_emitter.emit("on_pause", {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client
            })

    async def resume(self):
        """
        Resumes the paused track.
        """
        if self.voice_client is not None:
            self.voice_client.resume()
            event_emitter.emit("on_resume", {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client
            })

    async def skip(self):
        """
        Skips the currently playing track and plays the next track in the queue.
        """
        if self.voice_client and self.voice_client.is_playing():
            self.debug_print("Skipping current track")
            self.voice_client.stop()
            await self._play_next()
            event_emitter.emit("on_skip", {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client
            })
        else:
            self.debug_print("No track is currently playing")
            event_emitter.emit("on_error", {
                "error": "No track is currently playing to skip",
                "text_id": self.text_id
            })
            raise TrackError("No track is currently playing to skip")

    async def previous(self):
        """
        Plays the previous track in the queue.
        """
        if self.voice_client and self.voice_client.is_playing():
            self.debug_print("Returning to the previous track")
            self.voice_client.stop()
            await self._play_previous()
            event_emitter.emit("on_previous", {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client
            })
        else:
            self.debug_print("No track is currently playing")
            event_emitter.emit("on_error", {
                "error": "No track is currently playing to skip",
                "text_id": self.text_id
            })
            raise TrackError("No track is currently playing to skip")

    async def set_volume(self, volume: float):
        """
        Sets the volume for the currently playing track.

        :param volume: Volume level to set.
        """
        if self.voice_client is not None and self.voice_client.source is not None:
            self.voice_client.source = disnake.PCMVolumeTransformer(self.voice_client.source, volume)
            event_emitter.emit("on_volume_change", {
                "volume": volume,
                "text_id": self.text_id,
                "voice_client": self.voice_client
            })

    def update_plugin_settings(self, plugin_name: str, settings: dict) -> bool:
        """
        Updates the settings for a specified plugin.

        :param plugin_name: Name of the plugin.
        :param settings: Dictionary containing the settings to update.
        :return: True if settings were updated successfully, False otherwise.
        """
        result = self.plugin_loader.update_plugin_settings(plugin_name, settings)
        event_emitter.emit("on_update_plugin_settings", {
            "plugin_name": plugin_name,
            "settings": settings,
            "result": result,
            "text_id": self.text_id
        })
        return result

    async def play_track(self, track: dict):
        """
        Plays a specified track. If a track is already playing, the track is queued.

        :param track: Dictionary containing track information.
        :raises TrackNotFound: If no track is found to play.
        :raises TrackError: If there is an error playing the track.
        """
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
                    event_emitter.emit("on_play_track", {
                        "track": track,
                        "text_id": self.text_id,
                        "voice_client": self.voice_client
                    })
                    self.debug_print("Event is emitted")
                    audio_source = disnake.FFmpegPCMAudio(track['url'], **self.FFMPEG_OPTIONS)
                    
                    if audio_source:
                        self.debug_print(f"Audio source created: {audio_source}")
                        self.voice_client.play(audio_source, after=lambda e: self._track_ended(e))
                        await self.set_volume(self.volume)
                        self.debug_print("Play command sent")
                        self.queue.update_current_index()
                    else:
                        self.debug_print("Failed to create audio source.")
                        
                else:
                    self.debug_print(f"Queueing track: {track}")
                    self.queue.add_track(track)
                    event_emitter.emit("on_track_queued", {
                        "track": track,
                        "text_id": self.text_id,
                        "queue": self.queue.get_all_tracks()
                    })
            except Exception as e:
                self.debug_print(f"Error playing track: {e}")
                event_emitter.emit("on_error", {
                    "error": str(e),
                    "text_id": self.text_id
                })
                raise TrackError(f"Error playing track: {e}")

    async def _track_ended(self, error):
        """
        Handles the event when a track ends. Plays the next track if available.
        """
        if error:
            self.debug_print(f"Track ended with error: {error}")
            event_emitter.emit("on_error", {
                "error": str(error),
                "text_id": self.text_id
            })
        else:
            self.debug_print("Track ended successfully")
            await self._play_next()

    async def _play_next(self):
        """
        Plays the next track in the queue.
        """
        self.debug_print("Getting next track from queue")
        next_track = self.queue.get_first()
        if next_track:
            await self.play_track(next_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty", {
                "text_id": self.text_id,
                "queue": self.queue.get_all_tracks()
            })
            await self.disconnect()

    async def _play_previous(self):
        """
        Plays the previous track in the queue.
        """
        self.debug_print("Getting previous track from queue")
        back_track = self.queue.get_back_track()
        if back_track:
            await self.play_track(back_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty", {
                "text_id": self.text_id,
                "queue": self.queue.get_all_tracks()
            })
            await self.disconnect()

    async def _play_current(self):
        """
        Plays the current track in the queue.
        """
        self.debug_print("Getting current track from queue")
        current_track = self.queue.get_current_track()
        if current_track:
            await self.play_track(current_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty", {
                "text_id": self.text_id,
                "queue": self.queue.get_all_tracks()
            })
            await self.disconnect()
