import disnake
from disnake.ext import commands
from dsplayer import Player, PluginLoader, YTMusicSearchEngine, event_emitter

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
            channel_id = ctx.author.voice.channel.id
            player = Player(
                voice_id=channel_id,
                text_id=channel_id,
                bot=bot,
                plugin_loader=PluginLoader(),
                engine=YTMusicSearchEngine,
                debug=True, 
                deaf=True
            )
            players[ctx.guild.id] = player
            await player.connect()
        else:
            await ctx.send('Вы не подключены к голосовому каналу.')
            return

    await player.play(url)
    await ctx.send(f'Трек добавлен в очередь: {url}')

bot.run('YOUR_BOT_TOKEN')