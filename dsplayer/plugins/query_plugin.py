from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from yt_dlp import YoutubeDL
from typing import Dict, Any


class QueryPlugin(PluginInterface):
    def __init__(self):
        self.name = "Query"
        self.url_patterns = []
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
        url = engine.get_url_by_query(data)
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