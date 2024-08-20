import asyncio


class EventEmitter:
    def __init__(self):
        self.events = {}

    def event(self, name):
        def decorator(func):
            if hasattr(func, '__self__'):
                cls = func.__self__.__class__
                if not hasattr(cls, '_event_emitter'):
                    cls._event_emitter = EventEmitter()
                cls._event_emitter.event(name)(func)
            else:
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


def event(name):
    def decorator(func):
        event_emitter.event(name)(func)
        return func
    return decorator
