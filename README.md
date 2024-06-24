# Документация для библиотеки dsplayer

## Для пользователей библиотеки

### Описание

`dsplayer` - это библиотека для Discord ботов. Она позволяет подключаться к голосовым каналам, воспроизводить треки из различных источников и управлять очередью воспроизведения. Также она имеет плагины которые способны роширить количество платформ

### Установка

Установите библиотеку с помощью pip:

```bash
pip install dsplayer
```

### Подробный пример создания бота

**В [example.py](examples/example.py) вы найдете пример создания бота, использующего `dsplayer`.**

## Для разработчиков библиотеки и плагинов

### Структура проекта

```
dsplayer/
├───engines_system
│   ├───engine_interface.py
│   ├───soundсloud.py
│   └───ytmusic.py
├───player_system
│   ├───player.py
│   ├───queue.py
│   └───__init__.py
├───plugins
│   ├───query_plugin.py
│   ├───spotify_plugin.py
│   └───youtube_plugin.py
├───plugin_system
│   ├───plugin_interface.py
│   ├───plugin_loader.py
│   └───__init__.py
└───utils
    ├───user_agent.py
    └───__init__.py
```

### Создание плагинов

Для создания плагинов необходимо реализовать интерфейс `PluginInterface`.

```python
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from typing import List, Dict, Any

class YourPlugin(PluginInterface):
    def __init__(self):
        self.name = "YourPlugin"
        self.url_patterns = []

    def on_plugin_load(self) -> None:
        pass

    def on_plugin_unload(self) -> None:
        pass

    def search(self, data: str, engine: EngineInterface) -> Dict[str, Any]:
        # Ваша реализация 
        pass

    def get_url_paterns(self) -> list:
        return self.url_patterns
```

### Создание поисковых движков 

```python 
from dsplayer.engines_system.engine_interface import EngineInterface

class YourEngine(EngineInterface):
    def get_url_by_query(query: str):
        # Ваша реализация 
        pass        
```

### Обработка исключений

Для обработки различных ошибок используйте исключения из `dsplayer.utils.exceptions.lib_exceptions`.

```python
from dsplayer.utils.exceptions.lib_exceptions import VoiceChaneNotConnected, TrackNotFound, TrackError

try:
    # Ваш код
except VoiceChaneNotConnected as e:
    print(e)
except TrackNotFound as e:
    print(e)
except TrackError as e:
    print(e)
```

## TODO

- SoundCloud плагин 
- Apple Music поисковый движок 
- Рефакторинг структуры проекта  