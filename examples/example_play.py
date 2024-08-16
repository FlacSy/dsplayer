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