from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dsplayer.engines_system.engine_interface import EngineInterface

class SoundCloudSearchEngine(EngineInterface):
    def initialize_driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver    

    def get_url_by_query(query: str):
        try:
            driver = SoundCloudSearchEngine.initialize_driver()
            search_url = f"https://soundcloud.com/search?q={query}"
            driver.get(search_url)
            track_element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.soundTitle__title'))
            )

            track_link = track_element.get_attribute('href')
            driver.quit()

            return track_link
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return None