# Документация
---

## Навигация

- [Для пользователей библиотеки](#для-пользователей-библиотеки)
  - [Описание](#описание)
  - [Установка](#установка)
  - [Player](#player)
    - [Атрибуты](#атрибуты)
    - [Методы](#методы)
  - [Queue](#queue)
    - [Атрибуты](#атрибуты)
    - [Методы](#методы)
  - [Плагины](#плагины)
  - [Поисковые движки](#поисковые-движки)
  - [Список событий](#список-событий)
  - [Примеры использования](#примеры-использования)
- [Для разработчиков библиотеки и плагинов](#для-разработчиков-библиотеки-и-плагинов)
  - [Структура проекта](#структура-проекта)
  - [Создание плагинов](#создание-плагинов)
  - [Создание поисковых движков](#создание-поисковых-движков)
  - [Обработка исключений](#обработка-исключений)

<div id="search-container">
    <input type="text" id="search-input" placeholder="Поиск..." oninput="searchInDocs()">
</div>

<script>
function searchInDocs() {
    let input = document.getElementById('search-input');
    let filter = input.value.toLowerCase();
    let sections = document.querySelectorAll('section, h2, h3, h4, p, code');

    sections.forEach((section) => {
        if (section.innerText.toLowerCase().includes(filter)) {
            section.style.display = '';
        } else {
            section.style.display = 'none';
        }
    });
}
</script>

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

- **debug (bool):**
  Режим отладки.   

### Методы

### `async` `connect(self)`

Подключает плеер к указанному голосовому каналу. Если плеер уже подключен к другому каналу, он перемещается в новый.

- **Вызывает:** Событие `on_connect` после подключения.

### `async` `disconnect(self)`

Отключает плеер от голосового канала и очищает клиент голосового канала.

- **Вызывает:** Событие `on_disconnect` после отключения.

### `async` `stop(self)`

Останавливает воспроизведение треков и очищает очередь.

- **Вызывает:** Событие `on_stop`.

### `async` `pause(self)`

Приостанавливает текущий воспроизводимый трек.

- **Вызывает:** Событие `on_pause`.

### `async` `resume(self)`

Возобновляет воспроизведение приостановленного трека.

- **Вызывает:** Событие `on_resume`.

### `async` `skip(self)`

Пропускает текущий трек и начинает воспроизведение следующего в очереди.

- **Вызывает:** Событие `on_skip`.

### `async` `set_volume(self, volume: float)`

Устанавливает громкость плеера.

- **Параметры:**
  - `volume (float)`: Уровень громкости (от 0.0 до 1.0).

- **Вызывает:** Событие `on_volume_change`.

### `update_plugin_settings(self, plugin_name: str, settings: dict) -> bool`

Обновляет настройки для указанного плагина.

- **Параметры:**
  - `plugin_name (str)`: Имя плагина, для которого обновляются настройки.
  - `settings (dict)`: Новые настройки для плагина.

- **Возвращает:** `bool`: `True`, если настройки были успешно обновлены, `False` в противном случае.

- **Вызывает:** Событие `on_update_plugin_settings`.

### `async` `play_track(self, track: dict)`

Запускает воспроизведение указанного трека.

- **Параметры:**
  - `track (dict)`: Словарь, содержащий информацию о треке для воспроизведения, включая URL аудиопотока.

- **Вызывает:** Событие `on_play`.

### `async` `play_next(self)`

Воспроизводит следующий трек в очереди. Если очередь пуста, ничего не воспроизводится.

- **Вызывает:** Событие `on_play_next`.

### `async` `add_and_play(self, track: dict)`

Добавляет трек в очередь и начинает его воспроизведение, если ничего не воспроизводится в данный момент.

- **Параметры:**
  - `track (dict)`: Словарь, содержащий информацию о треке для добавления в очередь.

- **Вызывает:** Событие `on_add_to_queue`.

### `async` `play_previous(self)`

Возвращает воспроизведение к предыдущему треку в очереди.

- **Вызывает:** Событие `on_play_previous`.

### `async` `find_track_info(self, query: str) -> dict`

Выполняет поиск информации о треке на основе заданного запроса.

- **Параметры:**
  - `query (str)`: Строка, содержащая запрос для поиска трека.

- **Возвращает:** `dict`: Словарь с информацией о найденном треке.

- **Вызывает:** События `on_track_search_start` и `on_track_search_end`.

### `async` `play(self, track: dict)`

Запускает воспроизведение трека, заданного в параметре `track`, если ничего не воспроизводится в данный момент. Если трек уже воспроизводится, обновляет его.

- **Параметры:**
  - `track (dict)`: Словарь с информацией о треке, который нужно воспроизвести, включая URL аудиопотока.

- **Вызывает:** Событие `on_play`.

## Queue

Класс `Queue` управляет списком треков, предназначенных для воспроизведения в плеере. Этот класс позволяет добавлять, удалять и управлять треками в очереди, а также предоставляет историю воспроизведенных треков. Ниже приведены основные атрибуты и методы, которые можно использовать для работы с очередью.

### Атрибуты

- **_queue (List[Any]):**  
  Список текущих треков в очереди.

- **_history (List[Any]):**  
  Список треков, которые уже были воспроизведены.

- **_current_index (Optional[int]):**  
  Индекс текущего воспроизводимого трека в очереди. Если нет воспроизводимого трека, значение будет `None`.

- **_repeat (bool):**  
  Флаг, указывающий, включена ли функция повторения треков.

### Методы

#### `set_repeat(self, repeat: bool) -> None`

Устанавливает флаг повторения треков.

- **Параметры:**
  - `repeat (bool)`: Значение флага повторения (включить или отключить).

#### `is_repeat_enabled(self) -> bool`

Возвращает `True`, если функция повторения включена.

#### `get_current_index(self) -> Optional[int]`

Возвращает индекс текущего трека. Если индекс отсутствует, возвращает `None`.

#### `remove_track(self, index: int) -> Optional[Any]`

Удаляет трек из очереди по указанному индексу и возвращает его. Если индекс некорректен, возвращает `None`.

- **Параметры:**
  - `index (int)`: Индекс трека в очереди, который нужно удалить.

#### `add_track(self, track: Any) -> None`

Добавляет трек в конец очереди. Если очередь пуста, устанавливает текущий индекс на первый трек.

- **Параметры:**
  - `track (Any)`: Трек, который нужно добавить в очередь.

#### `get_last(self) -> Optional[Any]`

Возвращает последний трек в очереди. Если очередь пуста, возвращает `None`.

#### `get_first(self) -> Optional[Any]`

Возвращает первый трек в очереди. Если очередь пуста, возвращает `None`.

#### `get_next_track(self) -> Optional[Any]`

Возвращает следующий трек после текущего в очереди. Если следующего трека нет, возвращает `None`.

#### `get_queue(self) -> List[Any]`

Возвращает список всех треков в очереди.

#### `get_history(self) -> List[Any]`

Возвращает список всех треков из истории.

#### `is_empty(self) -> bool`

Проверяет, пуста ли очередь.

#### `clear(self) -> None`

Очищает очередь.

#### `clear_history(self) -> None`

Очищает историю воспроизведения.

#### `update_current_index(self) -> None`

Обновляет индекс текущего трека после завершения воспроизведения. Если текущий трек был последним, устанавливает индекс на `None`.

#### `__len__(self) -> int`

Возвращает количество треков в очереди.

#### `__iter__(self) -> Iterable`

Возвращает итератор по очереди треков.

#### `__getitem__(self, index: int) -> Any`

Возвращает трек по указанному индексу.

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


### Обработка исключений

`dsplayer` предоставляет систему обработки исключений, которая позволяет гибко реагировать на различные ошибки, возникающие в процессе работы библиотеки. Для обработки ошибок рекомендуется использовать исключения из модуля `dsplayer.utils.exceptions.lib_exceptions`.

#### Основные исключения

- **VoiceChaneNotConnected**  
  Возникает, если бот пытается воспроизвести трек, не подключившись к голосовому каналу.

- **TrackNotFound**  
  Возникает, если указанный трек не найден во время поиска.

- **TrackError**  
  Общая ошибка, связанная с воспроизведением трека.

#### Пример использования

```python
from dsplayer.utils.exceptions.lib_exceptions import VoiceChaneNotConnected, TrackNotFound, TrackError

try:
    # Ваш код
except VoiceChaneNotConnected as e:
    print(f"Ошибка подключения: {e}")
except TrackNotFound as e:
    print(f"Трек не найден: {e}")
except TrackError as e:
    print(f"Ошибка воспроизведения трека: {e}")
```

### Список доступных исключений

- **VoiceChaneError**  
  - **VoiceChaneNotConnected**: Бот не подключен к голосовому каналу.
  - **VoiceChaneNotFound**: Указанный голосовой канал не найден.
  - **VoiceChaneNotPlaying**: Бот не воспроизводит трек в текущий момент.

- **ConnectionError**  
  - Возникает при проблемах с подключением к голосовому каналу.

- **TrackError**  
  - **TrackNotFound**: Трек не найден.
  - **TrackError**: Общая ошибка воспроизведения трека.

---

Для расширения раздела "Примеры использования" с примерами использования `dsplayer`, можно добавить более детализированные примеры, которые охватывают различные сценарии использования библиотеки, такие как управление плеером, взаимодействие с плагинами и обработка событий. Вот как это можно сделать:

---

### Примеры использования

#### Пример 1: Подключение и воспроизведение трека

В этом примере показано, как подключиться к голосовому каналу и начать воспроизведение трека:

```python
import disnake
from disnake.ext import commands
from dsplayer import Player
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.engines_system.ytmusic import YTMusicSearchEngine

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

plugin_loader = PluginLoader()
players = {}

@bot.command()
async def play(ctx, url):
    """Добавить трек в очередь и воспроизвести его."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
    else:
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            player = Player(
                voice_channel=voice_channel,
                bot=bot,
                plugin_loader=plugin_loader,
                engine=YTMusicSearchEngine,
                debug=True
            )
            players[ctx.guild.id] = player
            await player.connect()
        else:
            await ctx.send('Вы не подключены к голосовому каналу.')
            return

    await player.play_track({'url': url})
    await ctx.send(f'Трек добавлен в очередь: {url}')

    # Если трек только добавлен, воспроизводим его
    if not player.voice_client.is_playing() and not player.queue.is_empty():
        await player.play_next()

bot.run('YOUR_BOT_TOKEN')
```

#### Пример 2: Управление очередью треков

В этом примере демонстрируется, как управлять очередью треков с помощью команд для добавления треков, пропуска и отображения текущей очереди:

```python
import disnake
from disnake.ext import commands
from dsplayer import Player
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.engines_system.ytmusic import YTMusicSearchEngine

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

plugin_loader = PluginLoader()
players = {}

@bot.command()
async def skip(ctx):
    """Пропустить текущий трек."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
        await player.skip()
        await ctx.send('Трек пропущен.')
    else:
        await ctx.send("Нет активного плеера для этого сервера.")

@bot.command()
async def queue(ctx):
    """Показать текущую очередь треков."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
        queue = player.queue.get_queue()
        if queue:
            queue_list = "\n".join([f"{idx + 1}. {track['url']}" for idx, track in enumerate(queue)])
            await ctx.send(f"Очередь:\n{queue_list}")
        else:
            await ctx.send("Очередь пуста.")
    else:
        await ctx.send("Нет активного плеера для этого сервера.")

bot.run('YOUR_BOT_TOKEN')
```

#### Пример 3: Обработка событий

Этот пример показывает, как использовать события для выполнения действий при изменении состояния плеера:

```python
import disnake
from disnake.ext import commands
from dsplayer import Player, event_emitter

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

players = {}

@event_emitter.event("on_play")
async def on_play(track_info):
    """Отправляет сообщение, когда начинается воспроизведение трека."""
    channel = track_info[1]
    track = track_info[0]
    await channel.send(f"Начинается воспроизведение трека: {track['url']}")

@bot.command()
async def play(ctx, url):
    """Добавить трек в очередь и воспроизвести его."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
    else:
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            player = Player(
                voice_channel=voice_channel,
                bot=bot,
                plugin_loader=PluginLoader(),
                engine=YTMusicSearchEngine,
                debug=True
            )
            players[ctx.guild.id] = player
            await player.connect()
        else:
            await ctx.send('Вы не подключены к голосовому каналу.')
            return

    await player.play_track({'url': url})
    await ctx.send(f'Трек добавлен в очередь: {url}')

bot.run('YOUR_BOT_TOKEN')
```

В этих примерах охватываются основные функции библиотеки `dsplayer`, включая подключение и воспроизведение треков, управление очередью, обработку событий и взаимодействие с плагинами. Эти примеры помогут пользователям быстро освоиться с библиотекой и интегрировать её в свои проекты.


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
    ├───debug.py
    ├───events.py
    ├───lib_exceptions.py
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