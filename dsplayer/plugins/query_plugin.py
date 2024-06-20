from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.utils.user_agent import get_random_user_agent
from yt_dlp import YoutubeDL
from typing import Dict, Any
import requests
import re


class QueryPlugin(PluginInterface):
    def __init__(self):
        self.name = "Query"
        self.url_patterns = []

    def on_plugin_load(self) -> Any:
        print(f"Plugin '{self.name}' loaded.")

    def on_plugin_unload(self) -> Any:
        print(f"Plugin '{self.name}' unloaded.")

    def get_url_paterns(self) -> list:
        return self.url_patterns

    def get_plugin_name(self) -> str:
        return self.name

    def search(self, query: str):
        headers: dict = {"User-Agent": get_random_user_agent()}

        response = requests.get(f"https://music.youtube.com/search?q={query}", headers=headers, timeout=None)
        page: str = response.content.decode("unicode_escape")

        if "consent.youtube.com" in page or "<title>Consent</title>" in page:
            response = requests.get(f"https://www.youtube.com/results?search_query={query}", headers=headers, timeout=None)
            page = response.content.decode("unicode_escape")

        trackId_match = re.search('"videoId":"(.*?)"', page)
        if not trackId_match:
            return {}

        trackId: str = eval(f"{{{trackId_match.group()}}}")["videoId"]
        url=f"https://music.youtube.com/watch?v={trackId}"

        return self._search_by_url(url)

        
    def _search_by_url(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'format': 'bestaudio/best'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url'] 
            thumbnail_url = info.get('thumbnail')
            title = info.get('title')
            artist = info.get('artist')
            duration = info.get('duration')

            track_info_list = [{
                'url': audio_url,
                'thumbnail_url': thumbnail_url,
                'title': title,
                'artist': artist,
                'duration': duration
            }]

            return track_info_list