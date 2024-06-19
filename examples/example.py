from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.player_system.player import Player
import disnake
from disnake.ext import commands
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

plugin_loader = PluginLoader()
players = {}

@bot.slash_command(description="Play a track from YouTube.")
async def play(inter: disnake.ApplicationCommandInteraction, query: str):
    await inter.response.defer()
    voice_channel = inter.author.voice.channel

    if inter.guild.id in players:
        player = players[inter.guild.id]
        player.voice_channel = voice_channel
    else:
        player = Player(voice_channel, bot)
        players[inter.guild.id] = player

    if not player.is_connected():
        await player.connect()

    track_info = player.find_track_info(plugin_loader, query)
    if track_info:
        await player.add_and_play(track_info)
        if player.queue.is_empty():
            await inter.edit_original_response(content=f'Now playing: {track_info["title"]}') 
        else:
            await inter.edit_original_response(content=f'Added to queue: {track_info["title"]}')
    else:
        await inter.edit_original_response(content='Track not found.')

@bot.slash_command(description="Pause the current track.")
async def pause(inter: disnake.ApplicationCommandInteraction):
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.is_playing():
            player.voice_client.pause()
            await inter.response.send_message("Track paused.")
        else:
            await inter.response.send_message("No track is currently playing.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Resume the paused track.")
async def resume(inter: disnake.ApplicationCommandInteraction):
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.voice_client.is_paused():
            player.voice_client.resume()
            await inter.response.send_message("Track resumed.")
        else:
            await inter.response.send_message("No track is currently paused.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Skip the current track.")
async def skip(inter: disnake.ApplicationCommandInteraction):
    if inter.guild.id in players:
        player = players[inter.guild.id]
        if player.is_playing():
            player.voice_client.stop()
            await inter.response.send_message("Track skipped.")
        else:
            await inter.response.send_message("No track is currently playing.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.slash_command(description="Show the current queue.")
async def queue(inter: disnake.ApplicationCommandInteraction):
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
async def clear(inter: disnake.ApplicationCommandInteraction):
    if inter.guild.id in players:
        player = players[inter.guild.id]
        player.queue.clear()
        await inter.response.send_message("Queue cleared.")
    else:
        await inter.response.send_message("Player is not connected.")

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

if __name__ == '__main__':
    bot.run('YOUR_BOT_TOKEN')