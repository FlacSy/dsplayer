import asyncio
import json
from typing import Dict, Any, List
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from yt_dlp import YoutubeDL
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from dsplayer.utils.debug import Debuger

class AppleMusicPlugin(PluginInterface):
    def __init__(self):
        self.name = "Apple Music"
        self.url_patterns = [r"https:\/\/music\.apple\.com\/.*"]
        self.settings = {}
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self.debug_print("AppleMusicPlugin initialized")

    def debug(self):
        self.debug_mode = True


    def on_plugin_load(self) -> None:
        self.debug_print("AppleMusicPlugin loaded")

    def on_plugin_unload(self) -> None:
        self.debug_print("AppleMusicPlugin unloaded")

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
        title, artist, thumbnail_url = await self._get_track_info(data)
        url = engine.get_url_by_query(f"{artist} {title}")
        audio_url, duration = await self._search_by_url(url)
        track_info_list = [{
            'title': title,
            'artist': artist,
            'thumbnail_url': thumbnail_url,
            'url': audio_url,
            'duration': duration
        }]
        for track_info in track_info_list:
            yield track_info

    async def _get_track_info(self, url: str) -> (str, str, str):
        async with ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()

        soup = BeautifulSoup(content, 'html.parser')
        
        title = soup.find('h1', class_='headings__title svelte-1la0y7y').find('span').text.strip()
        artist = soup.find('div', class_='headings__subtitles svelte-1la0y7y').text.strip()
        thumbnail_meta = soup.find('meta', property='og:image')

        thumbnail_url = thumbnail_meta['content']
        thumbnail_url = thumbnail_url.rsplit('/', 1)[0] + '/1080x1080bb.jpg'
        
        return title, artist, thumbnail_url

    async def _search_by_url(self, url: str) -> (str, float):
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
                raise RuntimeError(f"yt-dlp failed with return code {proc.returncode}: {stderr.decode()}")

            info = json.loads(stdout.decode())
            audio_url = info.get('url')
            duration = info.get('duration')

            if not audio_url:
                raise RuntimeError("No audio URL found in yt-dlp output")

            self.debug_print(f"Extracted audio URL: {audio_url}, duration: {duration}")
            return audio_url, duration
        except Exception as e:
            self.debug_print(f"Error extracting track info: {e}")
            raise
