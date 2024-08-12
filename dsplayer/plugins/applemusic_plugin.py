from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from yt_dlp import YoutubeDL
from typing import Dict, Any
from bs4 import BeautifulSoup
import requests

class AppleMusicPlugin(PluginInterface):
    def __init__(self):
        self.name = "Apple Music"
        self.url_patterns = [r"https:\/\/music\.apple\.com\/.*"]
        self.settings = {}
        
    def on_plugin_load(self) -> None:
        pass

    def on_plugin_unload(self) -> None:
        pass

    def get_url_patterns(self) -> list:
        return self.url_patterns

    def get_plugin_name(self) -> str:
        return self.name

    def get_settings(self) -> Dict[str, Any]:
        return self.settings

    def update_settings(self, settings: Dict[str, Any]) -> None:
        self.settings.update(settings)

    def search(self, data: str, engine: EngineInterface) -> list:
        title, artist, thumbnail_url = self._get_track_info(data)
        url = engine.get_url_by_query(f"{artist} {title}")
        audio_url, duration = self._search_by_url(url)
        track_info_list = [{
            'title': title,
            'artist': artist,
            'thumbnail_url': thumbnail_url,
            'url': audio_url,
            'duration': duration
        }]
        return track_info_list

    def _get_track_info(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('h1', class_='headings__title svelte-1la0y7y').find('span').text.strip()
        artist = soup.find('div', class_='headings__subtitles svelte-1la0y7y').text.strip()
        thumbnail_meta = soup.find('meta', property='og:image')

        thumbnail_url = thumbnail_meta['content']
        thumbnail_url = thumbnail_url.rsplit('/', 1)[0] + '/1080x1080bb.jpg'
        
        return title, artist, thumbnail_url


    def _search_by_url(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'format': 'bestaudio/best'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url'] 
            duration = info.get('duration')

            return audio_url, duration