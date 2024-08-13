import spotipy
import asyncio
import json
from typing import Dict, Any
from spotipy.oauth2 import SpotifyClientCredentials
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.utils.debug import Debuger


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
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self.debug_print("SpotifyPlugin initialized")

    def debug(self):
        self.debug_mode = True

    def on_plugin_load(self) -> None:
        self.debug_print("SpotifyPlugin loaded")

    def on_plugin_unload(self) -> None:
        self.debug_print("SpotifyPlugin unloaded")

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

    async def search(self, data: str, engine: EngineInterface):
        self.debug_print(f"Searching with data: {data}")
        if "track" in data:
            yield await self._search_track(data, engine)
        elif "playlist" in data:
            async for track in self._search_playlist(data, engine):
                yield track
        elif "artist" in data:
            async for track in self._search_artist(data, engine):
                yield track
        elif "album" in data:
            async for track in self._search_album(data, engine):
                yield track

    async def _search_playlist(self, data: str, engine: EngineInterface):
        self.debug_print(f"Searching playlist: {data}")
        spotify_data = self.sp.playlist(data)
        spotify_urls = [item['track']['external_urls']['spotify'] for item in spotify_data['tracks']['items']]
        self.debug_print(f"Found playlist URLs: {spotify_urls}")
        for url in spotify_urls:
            yield await self._search_track(url, engine)

    async def _search_artist(self, data: str, engine: EngineInterface):
        self.debug_print(f"Searching artist: {data}")
        spotify_data = self.sp.artist_top_tracks(data)
        spotify_urls = [item['external_urls']['spotify'] for item in spotify_data['tracks']]
        self.debug_print(f"Found artist URLs: {spotify_urls}")
        for url in spotify_urls:
            yield await self._search_track(url, engine)

    async def _search_album(self, data: str, engine: EngineInterface):
        self.debug_print(f"Searching album: {data}")
        spotify_data = self.sp.album_tracks(data)
        spotify_urls = [item['external_urls']['spotify'] for item in spotify_data['items']]
        self.debug_print(f"Found album URLs: {spotify_urls}")
        for url in spotify_urls:
            yield await self._search_track(url, engine)

    async def _search_track(self, data: str, engine: EngineInterface) -> Dict[str, Any]:
        self.debug_print(f"Searching track: {data}")
        spotify_data = self.sp.track(data)
        artist_name = spotify_data['artists'][0]['name']
        track_name = spotify_data['name']
        track_image = spotify_data['album']['images'][0]['url']
        url = self._search_by_query(f"{artist_name} {track_name}", engine)
        audio_url, duration = await self._search_by_url(url)

        track_info = {
            'url': audio_url,
            'thumbnail_url': track_image,
            'title': track_name,
            'artist': artist_name,
            'duration': duration
        }

        self.debug_print(f"Track info: {track_info}")
        return track_info

    def _search_by_query(self, query: str, engine: EngineInterface):
        self.debug_print(f"Searching by query: {query}")
        url = engine.get_url_by_query(query)
        self.debug_print(f"Found URL: {url}")
        return url      

    async def _search_by_url(self, url: str) -> Dict[str, Any]:
        self.debug_print(f"Searching by URL: {url}")
        if not isinstance(url, str):
            url = str(url)

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

