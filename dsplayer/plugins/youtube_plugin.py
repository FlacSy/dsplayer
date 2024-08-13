import asyncio
import json
from typing import Dict, Any
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.utils.debug import Debuger


class YoutubePlugin(PluginInterface):
    def __init__(self):
        self.name = "YouTube"
        self.url_patterns = [
            r"^(https?://)?(www\.)?youtube\.com/.*",
            r"https?://(?:www\.)?music\.youtube\.com/.*",
            r"https?://youtu\.be/[\w-]{11}",
            r"https?://music\.youtube\.com/[\w-]{11}"
        ]
        self.settings = {}
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self.debug_print("YouTubePlugin initialized")

    def debug(self):
        self.debug_mode = True

    def on_plugin_load(self) -> None:
        self.debug_print("YouTubePlugin loaded")

    def on_plugin_unload(self) -> None:
        self.debug_print("YouTubePlugin unloaded")

    def get_url_patterns(self) -> list:
        self.debug_print(f"URL patterns: {self.url_patterns}")
        return self.url_patterns

    def get_plugin_name(self) -> str:
        self.debug_print(f"Plugin name: {self.name}")
        return self.name

    def get_settings(self) -> Dict[str, Any]:
        print(f"Current settings: {self.settings}")
        return self.settings

    def update_settings(self, settings: Dict[str, Any]) -> None:
        print(f"Updating settings: {settings}")
        self.settings.update(settings)

    async def search(self, data: str, engine: EngineInterface) -> Dict[str, Any]:
        print(f"Searching with data: {data}")
        track_info = await self._search_by_url(data)
        for track_info in track_info_list:
            yield track_info
            
    async def _search_by_url(self, url: str) -> Dict[str, Any]:
        print(f"Searching by URL: {url}")
        if not isinstance(url, str):
            url = str(url)

        command = [
            'yt-dlp',
            '--format', 'bestaudio/best',
            '--dump-json',
            url
        ]

        try:
            proc = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                raise RuntimeError(f"yt-dlp failed with return code {proc.returncode}: {stderr.decode()}")

            info = json.loads(stdout.decode())
            audio_url = info.get('url')
            duration = info.get('duration')
            thumbnail_url = info.get('thumbnail')
            title = info.get('title')
            artist = info.get('artist')

            if not audio_url:
                raise RuntimeError("No audio URL found in yt-dlp output")

            track_info = {
                'url': audio_url,
                'thumbnail_url': thumbnail_url,
                'title': title,
                'artist': artist,
                'duration': duration
            }

            print(f"Track info: {track_info}")
            return track_info
        except Exception as e:
            print(f"Error extracting track info: {e}")
            raise
