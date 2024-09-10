# Документация

## Навигация

- [Для пользователей библиотеки](#для-пользователей-библиотеки)
  - [Описание](#описание)
  - [Установка](#установка)
  - [Player](#player)
    - [Атрибуты Player](#атрибуты-player)
    - [Методы Player](#методы-player)
  - [Queue](#queue)
    - [Атрибуты Queue](#атрибуты-queue)
    - [Методы Queue](#методы-queue)
  - [PluginLoader](#pluginloader)
    - [Атрибуты PluginLoader](#атрибуты-pluginloader)
    - [Методы PluginLoader](#методы-pluginloader)
  - [Плагины](#плагины)
  - [Поисковые движки](#поисковые-движки)
  - [Список событий](#список-событий)
  - [Примеры использования](#примеры-использования)

## Для пользователей библиотеки

### Описание

`dsplayer` — это библиотека для Discord-ботов, которая позволяет подключаться к голосовым каналам, воспроизводить треки и управлять очередью воспроизведения. Библиотека также поддерживает плагины, расширяющие количество платформ для воспроизведения.

`dsplayer` совместим с такими библиотеками, как disnake, discord.py, и nextcord.

### Установка

Установите библиотеку с помощью pip из PyPi:

```bash
pip install dsplayer
```

Или установите последнюю версию с GitHub:

```bash
pip install git+https://github.com/FlacSy/dsplayer
```

**Примечание:** Установка через PyPi обеспечивает стабильность, тогда как на GitHub можно получить последние изменения.

--- 

### Класс `Player`
- **Player Attributes:**
  1. **`queue: Queue`** — объект класса `Queue`, представляющий очередь треков для воспроизведения.
  2. **`plugin_loader: PluginLoader`** — объект класса `PluginLoader`, загружающий плагины.
  3. **`voice_channel: Optional[disnake.VoiceChannel]`** — объект канала голосовой связи.
  4. **`text_id: int`** — идентификатор текстового канала.
  5. **`voice_client: Optional[disnake.VoiceClient]`** — объект клиента голосовой связи.
  6. **`FFMPEG_OPTIONS: dict`** — опции для FFMPEG.
  7. **`bot: commands.Bot`** — объект бота.
  8. **`deaf: bool`** — флаг, указывающий, должен ли бот быть заглушен при подключении.
  9. **`engine: EngineInterface`** — объект интерфейса поискового движка для треков.
  10. **`debug: bool`** — флаг, включающий или выключающий режим отладки.
  11. **`debug_print: Callable`** — функция для печати отладочных сообщений.
  12. **`volume: float`** — громкость плеера.

- **Player Methods:**
  1. **`__init__(self, voice_id: int, text_id: int, bot: commands.Bot, plugin_loader: PluginLoader, volume: float = 1.0, FFMPEG_OPTIONS: dict = {}, deaf: bool = True, engine: EngineInterface = YTMusicSearchEngine, debug: bool = False)`** — инициализирует объект плеера с необходимыми атрибутами.
  2. **`connect(self)`** — подключает бота к голосовому каналу.
  3. **`disconnect(self)`** — отключает бота от голосового канала.
  4. **`stop(self)`** — останавливает текущий трек и очищает очередь.
  5. **`pause(self)`** — ставит воспроизведение на паузу.
  6. **`resume(self)`** — возобновляет воспроизведение.
  7. **`skip(self)`** — пропускает текущий трек и воспроизводит следующий в очереди.
  8. **`previous(self)`** — воспроизводит предыдущий трек в очереди.
  9. **`set_volume(self, volume: float)`** — устанавливает громкость для текущего трека.
  10. **`update_plugin_settings(self, plugin_name: str, settings: dict) -> bool`** — обновляет настройки для указанного плагина.
  11. **`play_track(self, track: dict)`** — воспроизводит указанный трек.
  12. **`_track_ended(self, error)`** — обрабатывает событие окончания трека.
  13. **`_play_next(self)`** — воспроизводит следующий трек в очереди.
  14. **`_play_previous(self)`** — воспроизводит предыдущий трек в очереди.
  15. **`_play_current(self)`** — воспроизводит текущий трек в очереди.

### Класс `Queue`
- **Queue Attributes:**
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

### Класс `PluginLoader`
- **Pluginloader Attributes:**
  1. **`plugin_packages: List[str]`** — список пакетов плагинов.
  2. **`plugin_classes: List[Type[PluginInterface]]`** — список классов плагинов.
  3. **`plugins: List[PluginInterface]`** — список экземпляров плагинов.
  4. **`debug_mode: bool`** — флаг, указывающий, включен ли режим отладки.
  5. **`debug_print: Callable`** — функция для печати отладочных сообщений.

- **Pluginloader Methods:**
  1. **`__init__(self, plugin_packages: List[str] = ['dsplayer.plugin_system'])`** — инициализирует загрузчик плагинов и загружает плагины.
  2. **`debug(self)`** — включает режим отладки.
  3. **`load_plugins_from_classes(self, plugin_classes: List[Type[PluginInterface]]) -> None`** — загружает плагины из переданных классов.
  4. **`_load_plugins(self) -> None`** — загружает плагины из указанных пакетов и точек входа.
  5. **`get_plugins(self) -> List[PluginInterface]`** — возвращает список загруженных плагинов.
  6. **`get_plugin_by_name(self, plugin_name: str) -> Optional[PluginInterface]`** — возвращает плагин по его имени.
  7. **`update_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]) -> bool`** — обновляет настройки указанного плагина.


### Плагины 
В `dsplayer` предусмотрены следующие плагины:
- **[Query](dsplayer/plugins/query_plugin.py)** - этот плагин позволяет производить поиск музыки по ее названию, он уже часть корабля :)


- **[Spotify](https://github.com/FlacSy/dsplayer-spotify)** - этот плагин позволяет искать треки, плейлисты и авторов из Spotify.
    ```bash
    pip3 install dsplayer-spotify
    ```
- **[YouTube](https://github.com/FlacSy/dsplayer-youtube)** - этот плагин позволяет искать треки из YouTube, YouTube Music, YouTube Shorts.
    ```bash
    pip3 install dsplayer-youtube
    ```
- **[SoundCloud](https://github.com/FlacSy/dsplayer-soundcloud)** - этот плагин позволяет искать треки, плейлисты и авторов из SoundCloud.
    ```bash
    pip3 install dsplayer-soundcloud
    ```
- **[Apple Music](https://github.com/FlacSy/dsplayer-applemusic)** - этот плагин позволяет искать треки из Apple Music.
    ```bash
    pip3 install dsplayer-applemusic
    ```

### Поисковые движки 
В `dsplayer` предусмотрены следующие поисковые движки:
- **[YouTube Music](dsplayer/engines_system/ytmusic.py)** - он имеет более низкую точность, но он быстрее, чем `SoundCloud`.
- **[SoundCloud](dsplayer/engines_system/soundcloud.py)** - он имеет точность выше, чем `YouTube Music`, но поиск может занимать 2-3+ секунды вместо 1-2.
- **[Bandcamp](dsplayer/engines_system/bandcamp.py)** - он имеет достаточно высокую точность и производительность как у `YouTube Music`

***⚠️ SoundCloud работает на Selenium! Если вы хотите его использовать то вам нужно иметь Chrome браузер и chrome driver под ваш браузер!***

### Список событий 

Класс `Player` генерирует несколько событий через `event_emitter`. Эти события можно использовать для выполнения пользовательских действий в ответ на различные состояния воспроизведения. Ниже приведен список событий и когда они генерируются:

1. **`on_init`**
   - **Когда вызывается:** При инициализации объекта `Player`.
   - **Что возвращает:** Данные о начальных настройках плеера.
   - **Возвращаемые данные:**
     ```json
     {
       "voice_channel": <voice_channel_object>,
       "text_id": <text_channel_id>,
       "volume": <volume_level>,
       "FFMPEG_OPTIONS": <ffmpeg_options_dict>,
       "deaf": <deaf_status>,
       "engine": <engine_object>,
       "debug": <debug_status>
     }
     ```

2. **`on_connect`**
   - **Когда вызывается:** При подключении бота к голосовому каналу.
   - **Что возвращает:** Данные о подключении.
   - **Возвращаемые данные:**
     ```json
     {
       "voice_client": <voice_client_object>,
       "text_id": <text_channel_id>,
       "voice_channel": <voice_channel_object>
     }
     ```

3. **`on_disconnect`**
   - **Когда вызывается:** При отключении бота от голосового канала.
   - **Что возвращает:** Данные о состоянии после отключения.
   - **Возвращаемые данные:**
     ```json
     {
       "voice_client": <voice_client_object>,
       "text_id": <text_channel_id>,
       "voice_channel": <voice_channel_object>
     }
     ```

4. **`on_stop`**
   - **Когда вызывается:** При остановке воспроизведения трека и очистке очереди.
   - **Что возвращает:** Данные о состоянии очереди и плеере после остановки.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

5. **`on_pause`**
   - **Когда вызывается:** При паузе текущего трека.
   - **Что возвращает:** Данные о состоянии очереди и плеере после паузы.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

6. **`on_resume`**
   - **Когда вызывается:** При возобновлении воспроизведения трека.
   - **Что возвращает:** Данные о состоянии очереди и плеере после возобновления.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

7. **`on_skip`**
   - **Когда вызывается:** При пропуске текущего трека и переходе к следующему.
   - **Что возвращает:** Данные о состоянии очереди и плеере после пропуска.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

8. **`on_previous`**
   - **Когда вызывается:** При возврате к предыдущему треку в очереди.
   - **Что возвращает:** Данные о состоянии очереди и плеере после возврата.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

9. **`on_update_plugin_settings`**
   - **Когда вызывается:** При обновлении настроек плагина.
   - **Что возвращает:** Данные о результатах обновления настроек.
   - **Возвращаемые данные:**
     ```json
     {
       "plugin_name": <plugin_name>,
       "settings": <plugin_settings>,
       "result": <update_success_or_failure>,
       "text_id": <text_channel_id>
     }
     ```

10. **`on_play_track`**
    - **Когда вызывается:** При начале воспроизведения нового трека.
    - **Что возвращает:** Данные о треке и состоянии плеера.
    - **Возвращаемые данные:**
      ```json
      {
        "track": <track_info>,
        "text_id": <text_channel_id>,
        "voice_client": <voice_client_object>
      }
      ```

11. **`on_track_queued`**
    - **Когда вызывается:** При добавлении трека в очередь.
    - **Что возвращает:** Данные о добавленном треке и состоянии очереди.
    - **Возвращаемые данные:**
      ```json
      {
        "track": <track_info>,
        "text_id": <text_channel_id>,
        "queue": <all_tracks_in_queue>
      }
      ```

12. **`on_error`**
    - **Когда вызывается:** При возникновении ошибки во время выполнения команды.
    - **Что возвращает:** Данные об ошибке.
    - **Возвращаемые данные:**
      ```json
      {
        "error": <error_message>,
        "text_id": <text_channel_id>
      }
      ```

13. **`on_queue_empty`**
    - **Когда вызывается:** При отсутствии треков в очереди.
    - **Что возвращает:** Данные о состоянии очереди после проверки.
    - **Возвращаемые данные:**
      ```json
      {
        "text_id": <text_channel_id>,
        "queue": <all_tracks_in_queue>
      }
      ```

14. **`on_track_end`**
    - **Когда вызывается:** Когда трек завершает воспроизведение.
    - **Что возвращает:** Данные о завершении трека.
    - **Возвращаемые данные:**
      ```json
      {
        "text_id": <text_channel_id>
      }
      ```

15. **`on_volume_change`**
    - **Когда вызывается:** Когда изменяеться громкость.
    - **Что возвращает:** Громкость трека.
    - **Возвращаемые данные:**
      ```json
      {
        "volume": <volume>,
        "text_id": <text_channel_id>,
        "voice_client": <voice_client>
      }
      ```



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

### Примеры использования

### Использование `Player` и `Queue`
#### Пример 1: Подключение и воспроизведение трека

В этом примере показано, как подключиться к голосовому каналу и начать воспроизведение трека:

```python
import disnake
from disnake.ext import commands
from dsplayer import Player, event_emitter

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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
                plugin_loader=PluginLoader(),
                engine=YTMusicSearchEngine,
                debug=True
            )
            players[ctx.guild.id] = player
            await player.connect()
        else:
            await ctx.send('Вы не подключены к голосовому каналу.')
            return

    await player.play(url)
    await ctx.send(f'Трек добавлен в очередь: {url}')

bot.run('YOUR_BOT_TOKEN')
```

#### Пример 2: Управление очередью треков

В этом примере демонстрируется, как управлять очередью треков с помощью команд для добавления треков, пропуска и отображения текущей очереди:

```python
import disnake
from disnake.ext import commands
from dsplayer import Player
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.engines.ytmusic import YTMusicSearchEngine

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
        await ctx.send('Играет следущий трек.')
    else:
        await ctx.send("Нет активного плеера для этого сервера.")

@bot.command()
async def previous(ctx):
    """Вернуться к преведущему треку."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
        await player.previous()
        await ctx.send('Играет преведущий трек.')
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
from dsplayer import Player, event

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

players = {}

@event("on_play_track")
async def on_play_track(event_data: dict):
    """Отправляет сообщение, когда начинается воспроизведение трека."""
    track = track_info['track']
    channel_id = event_data['text_id']
    channel = bot.get_channel(channel_id)
    await channel.send(f"Начинается воспроизведение трека: {track['title']}")


bot.run('YOUR_BOT_TOKEN')
```

### `PluginLoader`

#### 1. Загрузка плагинов из деректории

```python
from dsplayer import PluginLoader


plugins_list = ["custom_plugins.plugins"]
loader = PluginLoader(plugins)

```

#### 2. Загрузка плагинов используя класс 

```python
from dsplayer import PluginLoader
from dsplayer import PluginInterface


loader = PluginLoader()
loader.load_plugins_from_classes(plugins_list)

class MyCastomPlugin1(PluginInterface):
    ...

class MyCastomPlugin2(PluginInterface):
    ...

plugins_list = [MyCastomPlugin1, MyCastomPlugin2]

```

**Пример бота можно найти в [***examples/example_bot.py***](examples/example_bot.py)**

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

### Создание плагинов

Скачайте шаблон плагина:
```bash
git clone https://github.com/FlacSy/dsplayer-example
``` 
В данном шаблоне уже реализовано всё необходимое для создания плагинов. Вам нужно только реализовать свою логику в `plugin/plugin.py` и отредактировать `setup.py`. 

### Создание поисковых движков 

```python 
from dsplayer.engines_system.engine_interface import EngineInterface

class YourEngine(EngineInterface):
    def get_url_by_query(query: str):
        # Ваша реализация 
        pass        
```