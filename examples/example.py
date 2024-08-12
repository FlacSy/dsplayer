from dsplayer import PluginLoader
from dsplayer import Player
import disnake
from disnake.ext import commands
import logging
import asyncio
from typing import Dict
from dsplayer import SoundCloudSearchEngine
from dsplayer import event_emitter as emitter

# Настройка базового уровня логирования на INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка намерений (intents) бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Инициализация загрузчика плагинов и словаря игроков
plugin_loader = PluginLoader()
players: Dict[int, Player] = {}

# Событие при начале воспроизведения трека
@emitter.event('on_play')
def on_play(track: dict) -> None:
    """
    Обработчик события при воспроизведении трека.
    Логирует информацию о воспроизводимом треке.
    
    :param track: Словарь с информацией о треке.
    :type track: dict
    """
    logger.info(track)

# Событие при пропуске трека
@emitter.event('on_skip')
def on_skip(queue: dict) -> None:
    """
    Обработчик события при пропуске трека.
    Логирует информацию о текущей очереди воспроизведения.
    
    :param queue: Словарь с информацией о текущей очереди.
    :type queue: dict
    """
    logger.info(queue)

# Команда для воспроизведения трека
@bot.slash_command()
async def play(inter: disnake.ApplicationCommandInteraction, query: str) -> None:
    """
    Воспроизводит трек, найденный по запросу в голосовом канале пользователя.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    :param query: Строка запроса для поиска трека.
    :type query: str
    """
    await inter.response.defer()
    voice_channel = inter.author.voice.channel

    if inter.guild.id in players:
        player = players[inter.guild.id]
        player.voice_channel = voice_channel
    else:
        player = Player(
            voice_channel=voice_channel,
            plugin_loader=plugin_loader,
            bot=bot, 
            FFMPEG_OPTIONS={
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                'options': '-vn'
            },
            deaf=True,
            engine=SoundCloudSearchEngine
        )
        players[inter.guild.id] = player

    if not player.is_connected():
        await player.connect()

    track_info_list = player.find_track_info(plugin_loader, query)
    if track_info_list:
        for track_info in track_info_list:
            embed = disnake.Embed(title=f"{track_info['title']}", color=0x490DDD)
            embed.add_field(name=track_info['title'], value=track_info['artist'])
            formatted_duration = divmod(round(track_info['duration']), 60)
            embed.add_field(name='Duration', value=f'{formatted_duration[0]}:{formatted_duration[1]}')
            embed.set_image(url=track_info['thumbnail_url'])
            await inter.send(embed=embed)

            while player.is_playing():
                await asyncio.sleep(0.1)
            await player.add_and_play(track_info)

    else:
        await inter.edit_original_response(content='Трек не найден.')

# Команда для паузы текущего трека
@bot.slash_command(description="Поставить трек на паузу.")
async def pause(inter: disnake.ApplicationCommandInteraction) -> None:
    """
    Ставит на паузу текущий воспроизводимый трек.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    """
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.is_playing():
            await player.pause()
            await inter.response.send_message("Трек поставлен на паузу.")
        else:
            await inter.response.send_message("Трек в данный момент не воспроизводится.")
    else:
        await inter.response.send_message("Плеер не подключен.")

# Команда для возобновления трека
@bot.slash_command(description="Возобновить трек.")
async def resume(inter: disnake.ApplicationCommandInteraction) -> None:
    """
    Возобновляет воспроизведение трека, если он был на паузе.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    """
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.voice_client.is_paused():
            await player.resume()
            await inter.response.send_message("Воспроизведение трека возобновлено.")
        else:
            await inter.response.send_message("Трек в данный момент не приостановлен.")
    else:
        await inter.response.send_message("Плеер не подключен.")

# Команда для пропуска текущего трека
@bot.slash_command(description="Пропустить трек.")
async def skip(inter: disnake.ApplicationCommandInteraction) -> None:
    """
    Пропускает текущий воспроизводимый трек.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    """
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.is_playing():
            await player.skip()
            await inter.response.send_message("Трек пропущен.")
        else:
            await inter.response.send_message("Трек в данный момент не воспроизводится.")
    else:
        await inter.response.send_message("Плеер не подключен.")

# Команда для воспроизведения предыдущего трека
@bot.slash_command()
async def back(inter: disnake.ApplicationCommandInteraction) -> None:
    """
    Воспроизводит предыдущий трек из истории.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    """
    if inter.guild.id in players:
        player = players[inter.guild.id]
        await player.play_previous()
        await inter.response.send_message("Воспроизводится предыдущий трек.")
    else:
        await inter.response.send_message("Плеер не подключен.")

# Команда для отображения текущей очереди воспроизведения
@bot.slash_command(description="Показать очередь.")
async def queue(inter: disnake.ApplicationCommandInteraction) -> None:
    """
    Отображает текущую очередь воспроизведения, включая текущий трек и историю треков.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    """
    if inter.guild.id in players:
        player = players[inter.guild.id]
        queue = player.queue.get_queue()
        current_track = player.queue.get_current_track()
        history = player.queue.get_history()
        
        if current_track:
            current_track_text = f"**Сейчас играет:** {current_track['title']} - {current_track['artist']}\n"
        else:
            current_track_text = "Сейчас ничего не играет.\n"

        if history:
            history_text = '\n'.join([f"{idx+1}. {track['title']} - {track['artist']}" for idx, track in enumerate(history)])
        else:
            history_text = "История пуста."

        await inter.response.send_message(f"{current_track_text}\n\n**История воспроизведения:**\n{history_text}")
    else:
        await inter.response.send_message("Плеер не подключен.")

# Команда для очистки очереди воспроизведения
@bot.slash_command(description="Очистить очередь.")
async def clear(inter: disnake.ApplicationCommandInteraction) -> None:
    """
    Очищает текущую очередь воспроизведения.
    
    :param inter: Взаимодействие с командой.
    :type inter: disnake.ApplicationCommandInteraction
    """
    if inter.guild.id in players:
        player = players[inter.guild.id]
        player.queue.clear()
        await inter.response.send_message("Очередь очищена.")
    else:
        await inter.response.send_message("Плеер не подключен.")

# Событие при готовности бота к работе
@bot.event
async def on_ready() -> None:
    """
    Логирует сообщение о подключении бота к Discord.
    """
    logger.info(f'{bot.user} подключен к Discord!')

# Запуск бота
if __name__ == '__main__':
    bot.run('')