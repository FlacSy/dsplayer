import asyncio
import json
from typing import Dict, Any, List
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.utils.debug import Debuger


class SoundCloudPlugin(PluginInterface):
    def __init__(self):
        self.name = "SoundCloud"
        self.url_patterns = [r"https?:\/\/(www\.)?soundcloud\.com\/.*"]
        self.settings = {}
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self.debug_print("SoundCloudPlugin initialized")

    def debug(self):
        self.debug_mode = True

    def on_plugin_load(self) -> None:
        self.debug_print("SoundCloudPlugin loaded")

    def on_plugin_unload(self) -> None:
        self.debug_print("SoundCloudPlugin unloaded")

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

    async def search(self, data: str, engine: EngineInterface) -> List[Dict[str, Any]]:
        self.debug_print(f"Searching with data: {data}")
        track_info = await self._search(data)
        for track_info in track_info_list:
            yield track_info

    async def _search(self, url: str) -> List[Dict[str, Any]]:
        self.debug_print(f"Searching by URL: {url}")
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'dumpjson': True
        }

        command = [
            'yt-dlp',
            *['--' + k if v is True else '--' + k + '=' + str(v) for k, v in ydl_opts.items()],
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
            tracks = []

            if 'entries' in info:
                for entry in info['entries']:
                    track_info = self._extract_track_info(entry)
                    tracks.append(track_info)
            else:
                tracks.append(self._extract_track_info(info))

            self.debug_print(f"Found tracks: {tracks}")
            return tracks
        except Exception as e:
            self.debug_print(f"Error extracting track info: {e}")
            raise

    def _extract_track_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        audio_url = info.get('url')
        thumbnail_url = info.get('thumbnail')
        title = info.get('title')
        duration = info.get('duration')
        artist = info.get('artist')

        return {
            'url': audio_url,
            'thumbnail_url': thumbnail_url,
            'title': title,
            'artist': artist,
            'duration': duration
        }
