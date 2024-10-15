# Очередь 

В `dsplayer` есть система очереди треков, реализована она в классе `Queue`. Ниже будут атрибуты и методы класса `Queue`

## Класс `Queue`
- **Атрибуты:**
  1. **`_queue: List[Any]`** — список треков в очереди.
  2. **`_history: List[Any]`** — список треков в истории воспроизведения.
  3. **`_current_index: Optional[int]`** — индекс текущего трека.
  4. **`_repeat: bool`** — флаг повторения треков.

- **Методы:** {queue-methods}
  1. **`__init__(self)`** — инициализирует очередь.
  2. **`set_repeat(self, repeat: bool) -> None`** — устанавливает флаг повторения треков.
  3. **`is_repeat_enabled(self) -> bool`** — возвращает `True`, если функция повторения включена.
  4. **`get_current_index(self) -> Optional[int]`** — возвращает индекс текущего трека.
  5. **`remove_track(self, index: int) -> Optional[Any]`** — удаляет трек по индексу и возвращает его.
  6. **`add_track(self, track: Any) -> None`** — добавляет трек в очередь.
  7. **`get_last(self) -> Optional[Any]`** — возвращает последний трек в очереди.
  8. **`get_first(self) -> Optional[Any]`** — возвращает первый трек в очереди.
  9. **`get_next_track(self) -> Optional[Any]`** — возвращает следующий трек после текущего.
  10. **`get_queue(self) -> List[Any]`** — возвращает список всех треков в очереди.
  11. **`get_history(self) -> List[Any]`** — возвращает список всех треков из истории.
  12. **`is_empty(self) -> bool`** — проверяет, пустая ли очередь.
  13. **`clear(self) -> None`** — очищает очередь.
  14. **`clear_history(self) -> None`** — очищает историю.
  15. **`update_current_index(self) -> None`** — обновляет индекс текущего трека после завершения воспроизведения.
  16. **`__len__(self) -> int`** — возвращает количество треков в очереди.
  17. **`__iter__(self) -> Iterable`** — возвращает итератор для очереди.
  18. **`__getitem__(self, index: int) -> Any`** — возвращает трек по индексу. 