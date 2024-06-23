# Документация для библиотеки dsplayer

## Для пользователей библиотеки

### Описание

`dsplayer` - это библиотека для Discord ботов. Она позволяет подключаться к голосовым каналам, воспроизводить треки из различных источников и управлять очередью воспроизведения. Также она имеет плагины которые способны роширить количество платформ

### Установка

Установите библиотеку с помощью pip:

```bash
pip install dsplayer
```

### Быстрый старт

Ниже приведен пример использования `dsplayer` для создания бота, который может воспроизводить треки из плозадок которые предусмотрены в заргуженых плагинах:

```python
import disnake
from disnake.ext import commands
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.player_system.player import Player

intents = disnake.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

plugin_loader = PluginLoader()
players = {}

@bot.command()
async def play(ctx, *, query: str):
    voice_channel = ctx.author.voice.channel
    if ctx.guild.id not in players:
        players[ctx.guild.id] = Player(voice_channel, bot)
    player = players[ctx.guild.id]

    await player.connect()
    track_info = player.find_track_info(plugin_loader, query)
    await player.add_and_play(track_info)
    await ctx.send(f'Now playing: {track_info["title"]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

bot.run('YOUR_BOT_TOKEN')
```

### Блоее подробный пример создания бота

В директории `examples/` вы найдете пример создания бота, использующего `dsplayer`.

## Для разработчиков библиотеки и плагинов

### Структура проекта

```
dsplayer/
│   __init__.py
├───player_system/
│   ├───__init__.py
│   ├───player.py
│   └───queue.py
├───plugin_system/
│   ├───__init__.py
│   ├───plugin_interface.py
│   └───plugin_loader.py
├───plugins/
│   ├───__init__.py
│   ├───query_plugin.py
│   ├───spotify_plugin.py
│   └───youtube_plugin.py
├───utils/
│   ├───__init__.py
│   ├───user_agent.py
│   ├───exceptions/
│   │   ├───lib_exceptions.py
│   └───local/
│       └───user_agents.txt
└───examples/
    └───example.py
```

### Создание плагинов

Для создания плагинов необходимо реализовать интерфейс `PluginInterface`.

```python
from dsplayer.plugin_system.plugin_interface import PluginInterface
from typing import List, Dict, Any

class YourPlugin(PluginInterface):
    def __init__(self):
        self.name = "YourPlugin"
        self.url_patterns = []

    def on_plugin_load(self) -> None:
        pass

    def on_plugin_unload(self) -> None:
        pass

    def search(self, data: str) -> Dict[str, Any]:
        # Реализуйте поиск трека
        pass

    def get_url_paterns(self) -> list:
        return self.url_patterns
```

### Загрузка плагинов

Используйте `PluginLoader` для загрузки всех доступных плагинов.

```python
from dsplayer.plugin_system.plugin_loader import PluginLoader

plugin_loader = PluginLoader()
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