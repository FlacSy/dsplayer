from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from yt_dlp import YoutubeDL
from typing import Dict, Any, List

class SoundCloudPlugin(PluginInterface):
    def __init__(self):
        self.name = "SoundCloud"
        self.url_patterns = [r"https?:\/\/(www\.)?soundcloud\.com\/.*"]
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

    def search(self, data: str, engine: EngineInterface):
        return self._search(data)

    def _search(self, url: str) -> List[Dict[str, Any]]:
        ydl_opts = {
            'format': 'bestaudio/best'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if 'entries' in info:
                tracks = []
                for entry in info['entries']:
                    track_info = self._extract_track_info(entry)
                    tracks.append(track_info)
                return tracks
            else:
                return [self._extract_track_info(info)]

    def _extract_track_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        audio_url = info['url']
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