from typing import Any, Optional, List, Iterable


class Queue:
    def __init__(self) -> None:
        self._queue: List[Any] = []
        self._history: List[Any] = []
        self._current_index: Optional[int] = None
        self._repeat: bool = False

    def set_repeat(self, repeat: bool) -> None:
        """Устанавливает флаг повторения треков."""
        self._repeat = repeat

    def is_repeat_enabled(self) -> bool:
        """Возвращает True, если функция повторения включена."""
        return self._repeat

    def get_current_index(self) -> Optional[int]:
        """Возвращает индекс текущего трека."""
        return self._current_index

    def remove_track(self, index: int) -> Optional[Any]:
        """Удаляет трек из очереди по индексу и возвращает его, если индекс корректен."""
        if 0 <= index < len(self._queue):
            return self._queue.pop(index)
        return None
    
    def add_track(self, track: Any) -> None:
        """Добавляет трек в конец очереди."""
        self._queue.append(track)
        if self._current_index is None:
            self._current_index = 0

    def get_last(self) -> Optional[Any]:
        """Возвращает последний трек в очереди."""
        if self._queue:
            return self._queue[-1]
        return None

    def get_first(self) -> Optional[Any]:
        """Возвращает первый трек в очереди."""
        if self._queue:
            return self._queue[0]
        return None

    def get_next_track(self) -> Optional[Any]:
        """Возвращает следующий трек после текущего."""
        if self._current_index is not None and 0 <= self._current_index + 1 < len(self._queue):
            return self._queue[self._current_index + 1]
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
    def clear_history(self) -> None:
        """Очищает историю."""
        self._history = []

    def update_current_index(self) -> None:
        """Обновляет индекс текущего трека после завершения воспроизведения."""
        if self._current_index is not None:
            self._current_index += 1
            if self._current_index >= len(self._queue):
                self._current_index = None

    def __len__(self) -> int:
        return len(self._queue)
    
    def __iter__(self) -> Iterable:
        return iter(self._queue)
    
    def __getitem__(self, index: int) -> Any:
        return self._queue[index]