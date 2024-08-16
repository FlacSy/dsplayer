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