import re
import requests
from dsplayer.utils.user_agent import get_random_user_agent
from dsplayer.engines_system.engine_interface import EngineInterface

class YTMusicSearchEngine(EngineInterface):

    def get_url_by_query(query: str):
        try:
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
                  
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None