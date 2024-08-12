# Документация
---

## Навигация

- [Для пользователей библиотеки](#для-пользователей-библиотеки)
  - [Описание](#описание)
  - [Установка](#установка)
  - [Player](#player)
    - [Атрибуты](#атрибуты)
    - [Методы](#методы)
    - [Подробный пример создания бота](#подробный-пример-создания-бота)
  - [Плагины](#плагины)
  - [Поисковые движки](#поисковые-движки)
  - [Список событий](#список-событий)
- [Для разработчиков библиотеки и плагинов](#для-разработчиков-библиотеки-и-плагинов)
  - [Структура проекта](#структура-проекта)
  - [Создание плагинов](#создание-плагинов)
  - [Создание поисковых движков](#создание-поисковых-движков)
  - [Обработка исключений](#обработка-исключений)


## Для пользователей библиотеки

### Описание

`dsplayer` - это библиотека для Discord ботов. Она позволяет подключаться к голосовым каналам, воспроизводить треки из различных источников и управлять очередью воспроизведения. Также она имеет плагины, которые способны расширить количество платформ.

### Установка

Установить библиотеку с помощью pip из PyPi:

```bash
pip install dsplayer
```

Еще можно установить библиотеку с помощью pip из GitHub:
```bash
pip install git+https://github.com/FlacSy/dsplayer
```

Преймущества установки через PyPi это стабильность, на GitHub выкладываються последние изменения

# Player 

Класс `Player` управляет воспроизведением аудиотреков, включая подключение к голосовым каналам, управление очередью треков, взаимодействие с плагинами. Он интегрируется с библиотекой `disnake` для взаимодействия с Discord и использует собственную систему очереди и плагинов для расширения функциональности.


## Атрибуты

- **queue (Queue):**  
  Экземпляр класса `Queue`, который управляет списком треков для воспроизведения в голосовом канале.

- **plugin_loader (PluginLoader):**  
  Отвечает за загрузку и взаимодействие с различными плагинами, которые могут расширять функциональность плеера.

- **voice_channel (disnake.VoiceChannel):**  
  Голосовой канал Discord, к которому подключен плеер.

- **voice_client (disnake.VoiceClient):**  
  Клиент, управляющий голосовыми соединениями в Discord.

- **FFMPEG_OPTIONS (dict):**  
  Словарь с опциями для настройки аудиопотока FFmpeg, используемого для воспроизведения треков.

- **bot (commands.Bot):**  
  Экземпляр Discord-бота, с которым связан плеер.

- **deaf (bool):**  
  Указывает, должен ли бот отключать звук у самого себя при подключении к голосовому каналу.

- **engine (EngineInterface):**  
  Поисковый движок, используемый для получения информации о треках. По умолчанию используется `YTMusicSearchEngine`.

## Методы

### `__init__(self, voice_channel: disnake.VoiceChannel, bot: commands.Bot, plugin_loader: PluginLoader, FFMPEG_OPTIONS: dict = {}, deaf: bool = True, engine: EngineInterface = YTMusicSearchEngine)`

Инициализирует новый экземпляр `Player`.

- **Параметры:**
  - `voice_channel (disnake.VoiceChannel)`: Голосовой канал для подключения.
  - `bot (commands.Bot)`: Экземпляр Discord-бота.
  - `plugin_loader (PluginLoader)`: Экземпляр загрузчика плагинов.
  - `FFMPEG_OPTIONS (dict)`: Необязательно; опции FFmpeg для воспроизведения аудио.
  - `deaf (bool)`: Необязательно; указывает, должен ли бот отключать звук у самого себя.
  - `engine (EngineInterface)`: Необязательно; поисковый движок для информации о треках, по умолчанию `YTMusicSearchEngine`.

### `async connect(self)`

Подключает плеер к указанному голосовому каналу. Если плеер уже подключен к другому каналу, он перемещается в новый.

- **Вызывает:** Событие `on_connect` после подключения.

### `async disconnect(self)`

Отключает плеер от голосового канала и очищает клиент голосового канала.

- **Вызывает:** Событие `on_disconnect` после отключения.

### `async play_next(self)`

Воспроизводит следующий трек в очереди. Если треков нет, вызывает ошибку.

- **Исключения:**
  - `TrackNotFound`: Если очередь пуста или трек не найден.
  - `TrackError`: Если произошла ошибка во время воспроизведения.
  - Вызывает события `on_play` и `on_error`.

### `asymc play_previous(self)`

Воспроизводит преведущий трек в очереди. Если треков нет, вызывает ошибку.

- **Исключения:**
  - `TrackNotFound`: Если очередь пуста или трек не найден.
  - `TrackError`: Если произошла ошибка во время воспроизведения.
  - Вызывает события `on_play` и `on_error`.

### `track_ended(self, error)`

Обрабатывает событие, когда трек завершает воспроизведение, и запускает следующий трек.

- **Параметры:**
  - `error (Exception)`: Необязательная ошибка, произошедшая во время воспроизведения.

- **Вызывает:** События `on_error` и `on_track_end`.

### `async get_player(self)`

Возвращает текущий экземпляр `disnake.VoiceClient`.

- **Возвращает:** `disnake.VoiceClient`: Текущий голосовой клиент.

### `async create_event(self, event_name, *args, **kwargs)`

Динамически вызывает событие с указанным именем.

- **Параметры:**
  - `event_name (str)`: Имя вызываемого события.
  - `*args, **kwargs`: Аргументы и именованные аргументы для события.

### `async add_and_play(self, track_info)`

Добавляет трек в очередь и начинает его воспроизведение, если в данный момент ничего не воспроизводится.

- **Параметры:**
  - `track_info (dict)`: Информация о добавляемом треке.

- **Вызывает:** Событие `on_add_to_queue`.

### `async stop(self)`

Останавливает воспроизведение треков и очищает очередь.

- **Вызывает:** Событие `on_stop`.

### `async pause(self)`

Приостанавливает текущий воспроизводимый трек.

- **Вызывает:** Событие `on_pause`.

### `async resume(self)`

Возобновляет воспроизведение приостановленного трека.

- **Вызывает:** Событие `on_resume`.

### `async skip(self)`

Пропускает текущий трек и начинает воспроизведение следующего в очереди.

- **Вызывает:** Событие `on_skip`.

### `async add_to_queue(self, track_info)`

Добавляет трек в очередь без начала воспроизведения.

- **Параметры:**
  - `track_info (dict)`: Информация о добавляемом треке.

### `async set_volume(self, volume: float)`

Устанавливает громкость плеера.

- **Параметры:**
  - `volume (float)`: Уровень громкости (от 0.0 до 1.0).

- **Вызывает:** Событие `on_volume_change`.

### `is_playing(self)`

Проверяет, воспроизводит ли плеер в данный момент трек.

- **Возвращает:** `bool`: `True`, если трек воспроизводится, `False` в противном случае.

### `is_connected(self)`

Проверяет, подключен ли плеер к голосовому каналу.

- **Возвращает:** `bool`: `True`, если подключен, `False` в противном случае.

### `update_plugin_settings(self, plugin_name: str, settings: dict) -> bool`

Обновляет настройки для указанного плагина.

- **Параметры:**
  - `plugin_name (str)`: Имя плагина, для которого обновляются настройки.
  - `settings (dict)`: Новые настройки для плагина.

- **Возвращает:** `bool`: `True`, если настройки были успешно обновлены, `False` в противном случае.

- **Вызывает:** Событие `on_update_plugin_settings`.

### `find_track_info(self, plugin_loader: PluginLoader, data: str)`

Ищет информацию о треке на основе предоставленных данных с использованием доступных плагинов.

- **Параметры:**
  - `plugin_loader (PluginLoader)`: Экземпляр загрузчика плагинов.
  - `data (str)`: Поисковый запрос или URL для поиска трека.

- **Возвращает:** `dict` или `list`: Найденная информация о треке.

- **Исключения:**
  - `TrackNotFound`: Если информация о треке не найдена.
  - `TrackError`: Если произошла ошибка при поиске трека.
  
- **Вызывает:** События `on_track_search_start`, `on_track_search_end`, и `on_error`.


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
- **[YouTube Music](dsplayer/engines_system/ytmusic.py)** - он имеет более низкую точность, но он быстрее, чем `SoundCloud`.
- **[SoundCloud](dsplayer/engines_system/soundcloud.py)** - он имеет точность выше, чем `YouTube Music`, но поиск может занимать 2-3+ секунды вместо 1-2.
- **[Bandcamp](dsplayer/engines_system/bandcamp.py)** - он имеет достаточно высокую точность и производительность как у `YouTube Music`

***⚠️ SoundCloud работает на Selenium! Если вы хотите его использовать то вам нужно иметь Chrome браузер и chrome driver под ваш браузер!***

### Список событий 

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

10. **on_track_end**
    - **Описание**: Генерируется, когда трек заканчивает воспроизводиться.
    - **Метод**: `play_next`

11. **on_volume_change**
    - **Описание**: Генерируется при изменении уровня громкости.
    - **Метод**: `set_volume`

12. **on_error**
    - **Описание**: Генерируется при возникновении ошибки.
    - **Метод**: `play_next`, `find_track_info`

13. **on_track_search_start**
    - **Описание**: Генерируется при начале поиска трека.
    - **Метод**: `find_track_info`

14. **on_track_search_end**
    - **Описание**: Генерируется при завершении поиска трека.
    - **Метод**: `find_track_info`

15. **on_play_previous**
    - **Описание**: Генерируеться при проигровании преведущего трека.
    - **Метод**: `play_previous`

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