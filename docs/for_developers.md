# Для разработчиков библиотеки и плагинов

## Структура проекта

```
dsplayer/
├───engines_system
│   ├───engine_interface.py
│   ├───soundcloud.py
│   └───ytmusic.py
├───player_system
│   ├───player.py
│   ├───query_plugin.py
│   ├───queue.py
│   └───__init__.py
├───plugin_system
│   ├───plugin_interface.py
│   ├───plugin_loader.py
│   └───__init__.py
└───utils
    ├───debug.py
    ├───events.py
    ├───lib_exceptions.py
    ├───user_agent.py
    └───__init__.py
```

## Создание плагинов

Скачайте шаблон плагина:
```bash
git clone https://github.com/FlacSy/dsplayer-example
``` 
В данном шаблоне уже реализовано всё необходимое для создания плагинов. Вам нужно только реализовать свою логику в `plugin/plugin.py` и отредактировать `setup.py`. 

## Создание поисковых движков 

```python 
from dsplayer.engines_system.engine_interface import EngineInterface

class YourEngine(EngineInterface):
    def get_url_by_query(query: str):
        # Ваша реализация 
        pass        
```