import re
import disnake
import asyncio
from disnake.ext import commands
from dsplayer.player_system.queue import Queue
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.utils.exceptions.lib_exceptions import VoiceChaneNotConnected, TrackNotFound, TrackError

class Player:
    def __init__(self, voice_channel: disnake.VoiceChannel, bot: commands.Bot, FFMPEG_OPTIONS: dict = {}, plugin_loader: PluginLoader = PluginLoader("dsplayer.plugin_system")):
        self.queue = Queue()
        self.plugin_loader = plugin_loader
        self.voice_channel = voice_channel
        self.voice_client = None
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS 
        self.bot = bot

    async def connect(self):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.voice_client = await self.voice_channel.connect()
        elif self.voice_client.channel != self.voice_channel:
            await self.voice_client.move_to(self.voice_channel)
    
    async def disconnect(self):
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None

    async def play_next(self):
        if not self.queue.is_empty():
            track = self.queue.get_next_track()
            if track:
                try:
                    if self.FFMPEG_OPTIONS == {}:
                        self.voice_client.play(disnake.FFmpegPCMAudio(track['url']), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
                    else:
                        self.voice_client.play(disnake.FFmpegPCMAudio(track['url'], **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
                    
                    await self.bot.change_presence(activity=disnake.Game(name=track['title']))
                except Exception as e:
                    raise TrackError(f"Error playing track: {e}")
            else:
                raise TrackNotFound("No track found to play")
        else:
            raise TrackNotFound("The queue is empty")

    async def add_and_play(self, track_info):
        self.queue.add_track(track_info)
        if not self.voice_client.is_playing():
            await self.play_next()

    def is_playing(self):
        return self.voice_client is not None and self.voice_client.is_playing()
    
    def is_connected(self):
        return self.voice_client is not None and self.voice_client.is_connected()

    def find_track_info(self, plugin_loader: PluginLoader, data: str):
        plugins = plugin_loader.get_plugins()
        if data.startswith('http'):
            for plugin in plugins:
                patterns = plugin.get_url_paterns()
                for pattern in patterns:
                    if re.search(pattern, data):
                        try:
                            track_info = plugin.search(data)
                            if track_info:
                                return track_info
                            else:
                                raise TrackNotFound("No track info found with the provided URL")
                        except Exception as e:
                            raise TrackError(f"Error finding track info: {e}")
        else:
            for plugin in plugins:
                if plugin.__class__.__name__ == 'QueryPlugin':
                    try:
                        track_info = plugin.search(data)
                        if track_info:
                            return track_info
                        else:
                            raise TrackNotFound("No track info found with the provided query")
                    except Exception as e:
                        raise TrackError(f"Error finding track info: {e}")
        raise TrackNotFound("No suitable plugin found to handle the provided data")