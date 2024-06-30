# Документация
---
## Для пользователей библиотеки

### Описание

`dsplayer` - это библиотека для Discord ботов. Она позволяет подключаться к голосовым каналам, воспроизводить треки из различных источников и управлять очередью воспроизведения. Также она имеет плагины, которые способны расширить количество платформ.

### Установка

Установите библиотеку с помощью pip:

```bash
pip install dsplayer
```

### Подробный пример создания бота

**В [example.py](examples/example.py) вы найдете пример создания бота, использующего `dsplayer`.**

### Плагины 
В `dsplayer` предусмотрены следующие плагины:
- **[Query](dsplayer/plugins/query_plugin.py)** - этот плагин позволяет производить поиск музыки по ее названию.
- **[Spotify](dsplayer/plugins/spotify_plugin.py)** - этот плагин позволяет искать треки, плейлисты и авторов из Spotify.
- **[YouTube](dsplayer/plugins/youtube_plugin.py)** - этот плагин позволяет искать треки из YouTube, YouTube Music, YouTube Shorts.
- **[SoundCloud](dsplayer/plugins/soundcloud_plugin.py)** - этот плагин позволяет искать треки, плейлисты и авторов из SoundCloud.
- **[Apple Music](dsplayer/plugins/applemusic_plugin.py)** - этот плагин позволяет искать треки из Apple Music.

### Поисковые движки 
В `dsplayer` предусмотрены следующие поисковые движки:
- **[SoundCloud](dsplayer/engines_system/soundcloud.py)** - он имеет точность выше, чем `YouTube Music`, но поиск может занимать 2-3+ секунды вместо 1-2.
- **[YouTube Music](dsplayer/engines_system/ytmusic.py)** - он имеет более низкую точность, но он быстрее, чем `SoundCloud`.


### События

Класс `Player` генерирует несколько событий через `event_emitter`. Эти события можно использовать для выполнения пользовательских действий в ответ на различные состояния воспроизведения. Ниже приведен список событий и когда они генерируются:

1. **on_connect**
   - **Описание**: Генерируется, когда бот успешно подключается к голосовому каналу.
   - **Метод**: `connect`

2. **on_disconnect**
   - **Описание**: Генерируется, когда бот отключается от голосового канала.
   - **Метод**: `disconnect`

3. **on_play**
   - **Описание**: Генерируется, когда начинается воспроизведение трека.
   - **Метод**: `play_next`

4. **on_add_to_queue**
   - **Описание**: Генерируется, когда трек добавляется в очередь.
   - **Метод**: `add_and_play`

5. **on_stop**
   - **Описание**: Генерируется, когда воспроизведение останавливается и очередь очищается.
   - **Метод**: `stop`

6. **on_pause**
   - **Описание**: Генерируется, когда воспроизведение приостанавливается.
   - **Метод**: `pause`

7. **on_resume**
   - **Описание**: Генерируется, когда воспроизведение возобновляется после паузы.
   - **Метод**: `resume`

8. **on_skip**
   - **Описание**: Генерируется, когда текущий трек пропускается.
   - **Метод**: `skip`

9. **on_update_plugin_settings**
   - **Описание**: Генерируется, когда настройки плагинов обновляются.
   - **Метод**: `update_plugin_settings`

10. **on_track_start**
    - **Описание**: Генерируется, когда трек начинает воспроизводиться.
    - **Метод**: `play_next`

11. **on_track_end**
    - **Описание**: Генерируется, когда трек заканчивает воспроизводиться.
    - **Метод**: `play_next`

12. **on_volume_change**
    - **Описание**: Генерируется при изменении уровня громкости.
    - **Метод**: `set_volume`

13. **on_error**
    - **Описание**: Генерируется при возникновении ошибки.
    - **Метод**: `play_next`, `find_track_info`

14. **on_track_search_start**
    - **Описание**: Генерируется при начале поиска трека.
    - **Метод**: `find_track_info`

15. **on_track_search_end**
    - **Описание**: Генерируется при завершении поиска трека.
    - **Метод**: `find_track_info`

---
## Для разработчиков библиотеки и плагинов

### Структура проекта

```
dsplayer/
├───engines_system
│   ├───engine_interface.py
│   ├───soundcloud.py
│   └───ytmusic.py
├───player_system
│   ├───player.py
│   ├───queue.py
│   └───__init__.py
├───plugins
│   ├───query_plugin.py
│   ├───spotify_plugin.py
│   ├───youtube_plugin.py
│   └───soundcloud_plugin.py
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

    def get_url_patterns(self) -> list:
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