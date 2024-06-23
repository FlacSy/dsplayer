from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dsplayer.engines_system.engine_interface import EngineInterface

class SoundCloudSearchEngine(EngineInterface):
    def __init__(self):
        self.driver = None
        self._initialize_driver()

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if not self.driver:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def get_url_by_query(self, query: str):
        try:
            search_url = f"https://soundcloud.com/search?q={query}"
            self.driver.get(search_url)
            track_element = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.soundTitle__title'))
            )

            track_link = track_element.get_attribute('href')

            return track_link
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None