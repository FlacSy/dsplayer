import re
import spotipy
import requests
from yt_dlp import YoutubeDL
from typing import Dict, Any
from spotipy.oauth2 import SpotifyClientCredentials
from dsplayer.utils.user_agent import get_random_user_agent
from dsplayer.plugin_system.plugin_interface import PluginInterface


class SpotifyPlugin(PluginInterface):
    def __init__(self):
        self.name = "Spotify"
        self.url_patterns = [r"https:\/\/open\.spotify\.com\/.*"]
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id="92136b939d6d435e854780b1c90955a8",
            client_secret="150a4bc5afee4cba8c85495c91691a27"
            )
        )
        
    def on_plugin_load(self) -> Any:
        print(f"Plugin '{self.name}' loaded.")

    def on_plugin_unload(self) -> Any:
        print(f"Plugin '{self.name}' unloaded.")

    def get_url_paterns(self) -> list:
        return self.url_patterns

    def get_plugin_name(self) -> str:
        return self.name

    def search(self, data: str) -> Dict[str, Any]:
        if "track" in data:
            return [self._search_track(data)]
        elif "playlist" in data:
            return self._search_playlist(data)
    
    def _search_playlist(self, data: str) -> list[Dict[str, Any]]:
        spotify_data = self.sp.playlist(data)
        spotify_urls = [item['track']['external_urls']['spotify'] for item in spotify_data['tracks']['items']]

        track_info_list = []

        for url in spotify_urls:
            track_info_list.append(self._search_track(url))

        return track_info_list

    def _search_track(self, data: str) -> list[Dict[str, Any]]:
        spotify_data = self.sp.track(data)
        artist_name = spotify_data['artists'][0]['name']
        track_name = spotify_data['name']
        track_image = spotify_data['album']['images'][0]['url']
        url = self._search_by_query(f"{artist_name} {track_name}")
        audio_url, duration = self._search_by_url(url)

        track_info_list = {
            'url': audio_url,
            'thumbnail_url': track_image,
            'title': track_name,
            'artist': artist_name,
            'duration': duration
        }

        return track_info_list

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
