import requests
from bs4 import BeautifulSoup
from dsplayer.engines_system.engine_interface import EngineInterface

class BandcampSearchEngine(EngineInterface):
    def get_url_by_query(query: str):
        try:
            search_url = f"https://bandcamp.com/search?q={query}&item_type=t"
            response = requests.get(search_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            })

            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            url = soup.find("li", class_="searchresult data-search").find("a")["href"]   
                  
            return url   
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None