import random
from typing import Any, Optional, List, Iterable
from dsplayer.utils.events import EventEmitter
from dsplayer.utils.debug import Debuger


class Queue:
    def __init__(self) -> None:
        self._queue: List[Any] = []
        self._history: List[Any] = []
        self._current_index: Optional[int] = None
        self._repeat: bool = False
        self._repeat_queue: bool = False
        self.event_emitter = EventEmitter()
        self.debug_print = Debuger().debug_print

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
        """Возвращает следующий трек после текущего или повторяет текущий трек."""
        if self._current_index is not None:
            if self._repeat:
                return self._queue[self._current_index]
            elif 0 <= self._current_index + 1 < len(self._queue):
                self.update_current_index()
                return self._queue[self._current_index]
        return None

    def get_all_tracks(self) -> List[Any]:
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
            self._history.append(self._queue[self._current_index])
            self._current_index += 1
            if self._current_index >= len(self._queue):
                self._current_index = None

    def set_repeat_queue(self, repeat: bool) -> None:
        """Устанавливает флаг повторения очереди."""
        self._repeat_queue = repeat

    def is_repeat_queue_enabled(self) -> bool:
        """Возвращает True, если функция повторения очереди включена."""
        return self._repeat_queue

    def shuffle(self) -> None:
        """Перемешивает очередь, исключая уже проигранные треки."""
        if self._current_index is not None:
            unplayed_tracks = self._queue[self._current_index + 1:]
            random.shuffle(unplayed_tracks)
            self._queue = self._queue[:self._current_index +
                                      1] + unplayed_tracks

    def get_next_track(self) -> Optional[Any]:
        """Возвращает следующий трек после текущего или повторяет текущий/очередь."""
        if self._current_index is not None:
            if self._repeat:
                return self._queue[self._current_index]
            elif 0 <= self._current_index + 1 < len(self._queue):
                self.update_current_index()
                return self._queue[self._current_index]
            elif self._repeat_queue:
                self._current_index = 0
                return self._queue[self._current_index]
        return None

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterable:
        return iter(self._queue)

    def __getitem__(self, index: int) -> Any:
        return self._queue[index]
