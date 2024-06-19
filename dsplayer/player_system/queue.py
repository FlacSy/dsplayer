from typing import Any, Optional, Iterable

class Queue:
    def __init__(self) -> None:
        self.queue: list = []

    def add_track(self, track: Any) -> None:
        self.queue.append(track)

    def get_next_track(self) -> Optional[Any]:
        if self.queue:
            return self.queue.pop(0)
        return None

    def get_back_track(self) -> Optional[Any]:
        if self.queue:
            return self.queue.pop()
        return None

    def get_queue(self) -> list:
        return self.queue

    def is_empty(self) -> bool:
        return len(self.queue) == 0
    
    def clear(self) -> None:
        self.queue = []

    def __len__(self) -> int:
        return len(self.queue)
    
    def __iter__(self) -> Iterable:
        return iter(self.queue)
    
    def __getitem__(self, index: int) -> Any:
        return self.queue[index]