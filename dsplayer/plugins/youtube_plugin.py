from dsplayer.plugin_system.plugin_interface import PluginInterface
from yt_dlp import YoutubeDL
from typing import Dict, Any


class YoutubePlugin(PluginInterface):
    def __init__(self):
        self.name = "YouTube"
        self.url_patterns = [r"^(https?://)?(www\.)?youtube\.com/.*", r"https?://(?:www\.)?music\.youtube\.com/.", r"https?://youtu\.be/[\w-]{11}", r"https?://music\.youtube\.com/[\w-]{11}"]
    
    def on_plugin_load(self) -> Any:
        print(f"Plugin '{self.name}' loaded.")

    def on_plugin_unload(self) -> Any:
        print(f"Plugin '{self.name}' unloaded.")

    def get_url_paterns(self) -> list:
        return self.url_patterns

    def get_plugin_name(self) -> str:
        return self.name

    def search(self, url: str) -> Dict[str, Any]:
        ydl_opts = {
            'format': 'bestaudio/best'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
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