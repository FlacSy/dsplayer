from abc import ABC, abstractmethod

class EngineInterface(ABC):

    @abstractmethod
    def get_url_by_query(self, query: str) -> str:
        """Возвращает ссылку на трек"""
        pass