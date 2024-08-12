from typing import Any, Optional, List, Iterable

class Queue:
    def __init__(self) -> None:
        self._queue: List[Any] = []
        self._history: List[Any] = []
        self._repeat: bool = False

    def remove_track(self, index: int) -> Optional[Any]:
        """Удаляет трек из очереди по индексу и возвращает его, если индекс корректен."""
        if 0 <= index < len(self._queue):
            return self._queue.pop(index)
        return None
    
    def add_track(self, track: Any) -> None:
        """Добавляет трек в конец очереди."""
        self._queue.append(track)

    def add_next(self, track: Any) -> None:
        """Добавляет трек в начало очереди (после текущего трека)."""
        self._queue.insert(1, track)

    def get_next_track(self) -> Optional[Any]:
        """Получает и удаляет следующий трек в очереди."""
        if self._queue:
            track = self._queue.pop(0)
            self._history.append(track)
            return track
        return None

    def get_current_track(self) -> Optional[Any]:
        """Возвращает текущий трек без удаления его из истории."""
        if self._history:
            return self._history[-1]
        return None

    def get_back_track(self) -> Optional[Any]:
        """Получает и удаляет последний трек из истории."""
        if self._history:
            track = self._history.pop()
            self._queue.insert(0, track)
            return track
        return None

    def get_queue(self) -> List[Any]:
        """Возвращает список всех треков в очереди."""
        return self._queue

    def get_history(self) -> List[Any]:
        """Возвращает список всех треков из истории."""
        return self._history

    def is_empty(self) -> bool:
        """Проверяет, пустая ли очередь."""
        return len(self._queue) == 0
    
    def clear(self) -> None:
        """Очищает очередь."""
        self._queue = []
    def toggle_repeat(self) -> None:
        """Переключает режим повтора."""
        self._repeat = not self._repeat

    def get_next_track(self) -> Optional[Any]:
        """Получает и удаляет следующий трек в очереди."""
        if self._repeat and self._history:
            return self._history[-1]  # Возвращаем текущий трек, если включен режим повтора
        if self._queue:
            track = self._queue.pop(0)
            self._history.append(track)
            return track
        return None
        
    def is_repeat_enabled(self) -> bool:
        """Возвращает состояние режима повтора."""
        return self._repeat
    def clear_history(self) -> None:
        """Очищает историю."""
        self._history = []

    def __len__(self) -> int:
        return len(self._queue)
    
    def __iter__(self) -> Iterable:
        return iter(self._queue)
    
    def __getitem__(self, index: int) -> Any:
        return self._queue[index]
