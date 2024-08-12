import spotipy
from yt_dlp import YoutubeDL
from typing import Dict, Any
from spotipy.oauth2 import SpotifyClientCredentials
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface

class SpotifyPlugin(PluginInterface):
    def __init__(self):
        self.name = "Spotify"
        self.url_patterns = [r"https:\/\/open\.spotify\.com\/.*"]
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id="92136b939d6d435e854780b1c90955a8",
            client_secret="150a4bc5afee4cba8c85495c91691a27"
            )
        )
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
        if "track" in data:
            return [self._search_track(data, engine)]
        elif "playlist" in data:
            return self._search_playlist(data, engine)
        elif "artist" in data:
            return self._search_artist(data, engine)
        elif "album" in data:
            return self._search_album(data, engine)
        
    def _search_playlist(self, data: str, engine: EngineInterface):
        spotify_data = self.sp.playlist(data)
        spotify_urls = [item['track']['external_urls']['spotify'] for item in spotify_data['tracks']['items']]
        for url in spotify_urls:
            yield self._search_track(url, engine)

    def _search_artist(self, data: str, engine: EngineInterface):
        spotify_data = self.sp.artist_top_tracks(data)
        spotify_urls = [item['external_urls']['spotify'] for item in spotify_data['tracks']]
        for url in spotify_urls:
            yield self._search_track(url, engine)
    
    def _search_album(self, data: str, engine: EngineInterface):
        spotify_data = self.sp.album_tracks(data)
        spotify_urls = [item['external_urls']['spotify'] for item in spotify_data['items']]
        for url in spotify_urls:
            yield self._search_track(url, engine)

    def _search_track(self, data: str, engine: EngineInterface) -> Dict[str, Any]:
        spotify_data = self.sp.track(data)
        artist_name = spotify_data['artists'][0]['name']
        track_name = spotify_data['name']
        track_image = spotify_data['album']['images'][0]['url']
        url = self._search_by_query(f"{artist_name} {track_name}", engine)
        audio_url, duration = self._search_by_url(url)

        track_info = {
            'url': audio_url,
            'thumbnail_url': track_image,
            'title': track_name,
            'artist': artist_name,
            'duration': duration
        }

        return track_info

    def _search_by_query(self, query: str, engine: EngineInterface):
        url = engine.get_url_by_query(query)
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
