from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from yt_dlp import YoutubeDL
from typing import Dict, Any


class YoutubePlugin(PluginInterface):
    def __init__(self):
        self.name = "YouTube"
        self.url_patterns = [r"^(https?://)?(www\.)?youtube\.com/.*", r"https?://(?:www\.)?music\.youtube\.com/.", r"https?://youtu\.be/[\w-]{11}", r"https?://music\.youtube\.com/[\w-]{11}"]
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

    def search(self, data: str, engine: EngineInterface) -> Dict[str, Any]:
        """
        Параметр engine в данном плагине не используется! 
        Этоn параметр тут "заглушка" для избежания ошибок!
        """
        ydl_opts = {
            'format': 'bestaudio/best'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data, download=False)
            audio_url = info['url'] 
            thumbnail_url = info.get('thumbnail')
            title = info.get('title')
            duration = info.get('duration')
            artist = info.get('artist')

            out: Dict[str, Any] = {
                'url': audio_url,
                'thumbnail_url': thumbnail_url,
                'title': title,
                'artist': artist,
                'duration': duration
            }
            return [out]