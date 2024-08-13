import asyncio

class EventEmitter:
    def __init__(self):
        self.events = {}

    def event(self, name):
        def decorator(func):
            self.events.setdefault(name, []).append(func)
            return func
        return decorator

    def emit(self, name, *args, **kwargs):
        handlers = self.events.get(name, [])
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                asyncio.create_task(handler(*args, **kwargs))
            else:
                handler(*args, **kwargs)

event_emitter = EventEmitter()