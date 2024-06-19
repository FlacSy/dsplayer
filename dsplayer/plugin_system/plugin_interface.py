from abc import ABC, abstractmethod
from typing import List, Dict, Any

class PluginInterface(ABC):
    @abstractmethod
    def on_plugin_load(self) -> None:
        """Вызывается при загрузке плагина"""
        pass

    @abstractmethod
    def on_plugin_unload(self) -> None:
        """Вызывается при выгрузке плагина"""
        pass

    @abstractmethod
    def search(self, data: str) -> Dict[str, Any]:
        """Ищет трек по запросу или url и возвращает информацию о треке"""
        pass

    @abstractmethod
    def get_url_paterns(self) -> List:
        """Возвращает список паттернов для url"""
        pass