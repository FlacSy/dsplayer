from typing import Callable, Dict, List, Any

class EventEmitter:
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}

    def event(self, event: str):
        def decorator(func: Callable):
            if event not in self._events:
                self._events[event] = []
            self._events[event].append(func)
            return func
        return decorator

    def emit(self, event: str, *args: Any, **kwargs: Any):
        if event in self._events:
            for handler in self._events[event]:
                handler(*args, **kwargs)

event_emitter = EventEmitter()