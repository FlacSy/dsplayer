import re
import requests
from yt_dlp import YoutubeDL
from typing import Dict, Any
from bs4 import BeautifulSoup
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.utils.user_agent import get_random_user_agent

class SpotifyPlugin(PluginInterface):
    def __init__(self):
        self.name = "Spotify"
        self.url_patterns = [r"https:\/\/open\.spotify\.com\/track\/[a-zA-Z0-9_-]+"]

    def on_plugin_load(self) -> Any:
        print(f"Plugin '{self.name}' loaded.")

    def on_plugin_unload(self) -> Any:
        print(f"Plugin '{self.name}' unloaded.")

    def get_url_paterns(self) -> list:
        return self.url_patterns

    def search(self, data: str) -> Dict[str, Any]:
        response = requests.get(data)

        soup = BeautifulSoup(response.content, 'html.parser')
        
        track_name = soup.title.get_text(strip=True).split(' - ')[0]
        artist_name = soup.find('meta', {'name': 'music:musician_description'}).get('content')
        track_image = soup.find('meta', {'property': 'og:image'}).get('content')

        url = self._search_by_query(f"{track_name} {artist_name}")
        audio_url, duration = self._search_by_url(url)

        out = {
            'url': audio_url,
            'thumbnail_url': track_image,
            'title': track_name,
            'artist': artist_name,
            'duration': duration
        }

        return out

    def _search_by_query(self, query: str):
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

        return url

    def _search_by_url(self, url: str) -> Dict[str, Any]:
        if not isinstance(url, str):
            url = str(url)

        ydl_opts = {
            'format': 'bestaudio/best'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            duration = info.get('duration')

        return audio_url, duration
