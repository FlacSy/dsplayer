# DSPlayer

## Описание

`dsplayer` — это библиотека для создания Discord-ботов, которая позволяет подключаться к голосовым каналам, воспроизводить музыкальные треки и управлять очередями воспроизведения. Библиотека также поддерживает плагины, что позволяет расширять количество доступных платформ для воспроизведения.

**Совместимость:** `dsplayer` работает с библиотеками `disnake`, `discord.py` и `nextcord`.

## Установка

Установите библиотеку с помощью `pip` из PyPI:

```bash
pip install dsplayer
```

Или установите последнюю версию с GitHub:

```bash
pip install git+https://github.com/FlacSy/dsplayer
```

> **Примечание:** Установка через PyPI гарантирует стабильную версию, тогда как установка с GitHub предоставляет последние изменения и улучшения.

---

---

## Список изменений

Ниже представлен список изменений для библиотеки, начиная с версии **2.0.0**.

- **2.0.0** | Глобальное обновление:
  - Обновлены компоненты: плеер, очередь, система плагинов.
  - Оптимизирован код для лучшей производительности.

- **2.0.1** | Исправления и улучшения:
  - Исправлены ошибки при инициализации некоторых классов.
  - Удалены ненужные части кода.
  - Добавлен новый метод в очередь: `get_current_track`.

- **2.1.0** | Новая система плагинов:
  - Добавлена поддержка двух типов плагинов: `addon` и `extractor`.
  - Частичная обратная совместимость с плагинами старых версий. Для работы старых плагинов необходимо реализовать метод `get_plugin_type`.

- **2.2.0** | Исправления и улучшения:
  - Удалены лишние фрагменты кода.
  - Обновлен стандарт возвращаемых данных плагинов. В этой версии плагины типа `extractor` совместимы только с версиями выше **1.4.0**!

## Плагины

В `dsplayer` предусмотрены следующие плагины:

- **[Query](dsplayer/plugins/query_plugin.py)** - Плагин для поиска музыки по названию (включен по умолчанию).
- **[Spotify](https://github.com/FlacSy/dsplayer-spotify)** - Плагин для поиска треков, плейлистов и авторов из Spotify.
    ```bash
    pip install dsplayer-spotify
    ```
- **[YouTube](https://github.com/FlacSy/dsplayer-youtube)** - Плагин для поиска треков из YouTube, YouTube Music и YouTube Shorts.
    ```bash
    pip install dsplayer-youtube
    ```
- **[SoundCloud](https://github.com/FlacSy/dsplayer-soundcloud)** - Плагин для поиска треков, плейлистов и авторов из SoundCloud.
    ```bash
    pip install dsplayer-soundcloud
    ```
- **[Apple Music](https://github.com/FlacSy/dsplayer-applemusic)** - Плагин для поиска треков из Apple Music.
    ```bash
    pip install dsplayer-applemusic
    ```

## Поисковые движки

В `dsplayer` предусмотрены следующие поисковые движки:

- **[YouTube Music](dsplayer/engines_system/ytmusic.py)** - Более быстрая, но менее точная поисковая система.
- **[SoundCloud](dsplayer/engines_system/soundcloud.py)** - Более точный поиск, но время отклика 2-3+ секунды.
- **[Bandcamp](dsplayer/engines_system/bandcamp.py)** - Высокая точность с хорошей производительностью.

> ⚠️ **Важно:** SoundCloud работает на Selenium! Для его использования необходимо установить Chrome и соответствующий Chrome Driver.

## Примеры использования

### Использование `Player` и `Queue`

#### Пример 1: Подключение и воспроизведение трека

```python
import disnake
from disnake.ext import commands
from dsplayer import Player, PluginLoader, YTMusicSearchEngine

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

```python
@bot.command()
async def skip(ctx):
    """Пропустить текущий трек."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
        await player.skip()
        await ctx.send('Играет следующий трек.')
    else:
        await ctx.send("Нет активного плеера для этого сервера.")

@bot.command()
async def previous(ctx):
    """Вернуться к предыдущему треку."""
    if ctx.guild.id in players:
        player = players[ctx.guild.id]
        await player.previous()
        await ctx.send('Играет предыдущий трек.')
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

```python
from dsplayer import event

@event("on_play_track")
async def on_play_track(event_data: dict):
    """Отправляет сообщение, когда начинается воспроизведение трека."""
    track = event_data['track']
    channel_id = event_data['text_id']
    channel = bot.get_channel(channel_id)
    await channel.send(f"Начинается воспроизведение трека: {track['title']}")
```

## `PluginLoader`

### 1. Загрузка плагинов из директории

```python
from dsplayer import PluginLoader

plugins_list = ["custom_plugins.plugins"]
loader = PluginLoader(plugins_list)
```

### 2. Загрузка плагинов используя класс 

```python
from dsplayer import PluginLoader, PluginInterface

loader = PluginLoader()
loader.load_plugins_from_classes(plugins_list)

class MyCustomPlugin1(PluginInterface):
    # Реализация плагина
    ...

class MyCustomPlugin2(PluginInterface):
    # Реализация плагина
    ...

plugins_list = [MyCustomPlugin1, MyCustomPlugin2]
```

> **Пример бота можно найти в [examples/example_bot.py](examples/example_bot.py)**

## Обработка исключений

`dsplayer` предоставляет систему обработки исключений, позволяющую гибко реагировать на ошибки. Для этого рекомендуется использовать исключения из модуля `dsplayer.utils.exceptions.lib_exceptions`.

### Основные исключения

- **VoiceChaneNotConnected**  
  Возникает, если бот пытается воспроизвести трек, не подключившись к голосовому каналу.

- **TrackNotFound**  
  Возникает, если указанный трек не найден.

- **TrackError**  
  Общая ошибка, связанная с воспроизведением трека.

### Пример обработки исключений

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
  - **VoiceChaneNotPlaying**: Бот не воспроизводит трек.

- **ConnectionError**  
  - Проблемы с подключением к голосовому каналу.

- **TrackError**  
  - **TrackNotFound**: Трек не найден.
  - **TrackError**: Ошибка воспроизведения трека.
