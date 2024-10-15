import asyncio
import json
from typing import Dict, Any, List

from eel import start
from numpy import source
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.utils.debug import Debuger


class QueryPlugin(PluginInterface):
    def __init__(self):
        self.name = "Query"
        self.url_patterns = []
        self.settings = {}
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self.debug_print("QueryPlugin initialized")

    def debug(self):
        self.debug_mode = True

    def on_plugin_load(self) -> None:
        self.debug_print("QueryPlugin loaded")

    def on_plugin_unload(self) -> None:
        self.debug_print("QueryPlugin unloaded")

    def get_url_patterns(self) -> list:
        self.debug_print(f"URL patterns: {self.url_patterns}")
        return self.url_patterns

    def get_plugin_name(self) -> str:
        self.debug_print(f"Plugin name: {self.name}")
        return self.name

    def get_settings(self) -> Dict[str, Any]:
        self.debug_print(f"Current settings: {self.settings}")
        return self.settings

    def update_settings(self, settings: Dict[str, Any]) -> None:
        self.debug_print(f"Updating settings: {settings}")
        self.settings.update(settings)

    def get_plugin_type(self) -> str:
        return "extractor"

    async def search(self, data: str, engine: EngineInterface):
        self.debug_print(f"Searching with data: {data}")
        url = engine.get_url_by_query(data)
        source_name = 
        track_info_list = await self._search_by_url(url)
        for track_info in track_info_list:
            track_info['source_name'] = engine.__class__.__name__
            yield track_info

    async def _search_by_url(self, url: str) -> List[Dict[str, Any]]:
        self.debug_print(f"Searching by URL: {url}")
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
                raise RuntimeError(
                    f"yt-dlp failed with return code {proc.returncode}: {stderr.decode()}")

            info = json.loads(stdout.decode())
            track_info_list = []

            if 'entries' in info:
                for entry in info['entries']:
                    track_info_list.append(self._extract_track_info(entry))
            else:
                track_info_list.append(self._extract_track_info(info))

            self.debug_print(f"Found tracks: {track_info_list}")
            return track_info_list
        except Exception as e:
            self.debug_print(f"Error extracting track info: {e}")
            raise

    def _extract_track_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        audio_url = info.get('url')
        thumbnail_url = info.get('thumbnail')
        title = info.get('title')
        artist = info.get('artist')
        duration = info.get('duration')

        return {
            'url': audio_url,
            'thumbnail_url': thumbnail_url,
            'title': title,
            'artist': artist,
            'duration': duration,
        }
