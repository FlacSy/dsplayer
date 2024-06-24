from dsplayer import PluginLoader
from dsplayer import Player
import disnake
from disnake.ext import commands
import logging
import asyncio
from typing import Dict
from dsplayer.engines_system.soundcloud import SoundCloudSearchEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

plugin_loader = PluginLoader()
players: Dict[int, Player] = {}

@bot.slash_command()
async def play(inter: disnake.ApplicationCommandInteraction, query: str) -> None:
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
            while player.is_playing():
                await asyncio.sleep(0.1)
            await player.add_and_play(track_info)
            embed = disnake.Embed(title=f"{track_info['title']}", color=0x490DDD, url=query)
            embed.add_field(name=track_info['title'], value=track_info['artist'])
            formatted_duration = divmod(track_info['duration'], 60)
            embed.add_field(name='Duration', value=f'{formatted_duration[0]}:{formatted_duration[1]}')
            embed.set_image(url=track_info['thumbnail_url'])
            await inter.send(embed=embed)
    else:
        await inter.edit_original_response(content='Track not found.')

@bot.slash_command(description="Pause the current track.")
async def pause(inter: disnake.ApplicationCommandInteraction) -> None:
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.is_playing():
            await player.pause()
            await inter.response.send_message("Track paused.")
        else:
            await inter.response.send_message("No track is currently playing.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Resume the paused track.")
async def resume(inter: disnake.ApplicationCommandInteraction) -> None:
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.voice_client.is_paused():
            await player.resume()
            await inter.response.send_message("Track resumed.")
        else:
            await inter.response.send_message("No track is currently paused.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Skip the current track.")
async def skip(inter: disnake.ApplicationCommandInteraction) -> None:
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.is_playing():
            await player.skip()
            await inter.response.send_message("Track skipped.")
        else:
            await inter.response.send_message("No track is currently playing.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Show the current queue.")
async def queue(inter: disnake.ApplicationCommandInteraction) -> None:
    if inter.guild.id in players:
        player = players[inter.guild.id]
        queue = player.queue.get_queue()
        if queue:
            queue_text = '\n'.join([track['title'] for track in queue])
            await inter.response.send_message(f"Current queue:\n{queue_text}")
        else:
            await inter.response.send_message("Queue is empty.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Clear the queue.")
async def clear(inter: disnake.ApplicationCommandInteraction) -> None:
    if inter.guild.id in players:
        player = players[inter.guild.id]
        player.queue.clear()
        await inter.response.send_message("Queue cleared.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.event
async def on_ready() -> None:
    logger.info(f'{bot.user} has connected to Discord!')

if __name__ == '__main__':
    bot.run('TOKEN')