import disnake
from disnake.ext import commands
from dsplayer import Player, PluginLoader, YTMusicSearchEngine, event
import asyncio

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@event("on_play_track")
async def on_play_track(event_data):
    """Отправляет сообщение, когда начинается воспроизведение трека."""
    track = event_data['track']
    channel_id = event_data['text_id']
    channel = bot.get_channel(channel_id)
    await channel.send(f"Начинается воспроизведение трека: {track['title']}")


@event("on_queue_empty")
async def on_queue_empty(event_data):
    """Отправляет сообщение, когда очередь пуста."""
    channel_id = event_data['text_id']
    channel = bot.get_channel(channel_id)
    await channel.send("Очередь пуста.")


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @commands.command()
    async def play(self, ctx, url):
        """Добавить трек в очередь и воспроизвести его."""
        if ctx.guild.id in self.players:
            player = self.players[ctx.guild.id]
        else:
            if ctx.author.voice:
                channel_id = ctx.author.voice.channel.id
                player = Player(
                    voice_id=channel_id,
                    text_id=channel_id,
                    bot=bot,
                    FFMPEG_OPTIONS={
                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': '-vn'},
                    plugin_loader=PluginLoader(),
                    engine=YTMusicSearchEngine,
                    debug=True,
                    deaf=True)
                self.players[ctx.guild.id] = player
                await player.connect()
            else:
                await ctx.send('Вы не подключены к голосовому каналу.')
                return

        await player.play(url)
        await ctx.send(f'Трек добавлен в очередь: {url}')

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Пропустить текущий трек."""
        if ctx.guild.id in self.players:
            player = self.players[ctx.guild.id]
            await player.skip()
            await ctx.send('Играет следущий трек.')
        else:
            await ctx.send("Нет активного плеера для этого сервера.")

    @commands.command()
    async def previous(self, ctx):
        """Вернуться к преведущему треку."""
        if ctx.guild.id in self.players:
            player = self.players[ctx.guild.id]
            await player.previous()
            await ctx.send('Играет преведущий трек.')
        else:
            await ctx.send("Нет активного плеера для этого сервера.")

    @commands.command()
    async def queue(self, ctx):
        """Показать текущую очередь треков."""
        if ctx.guild.id in self.players:
            player = self.players[ctx.guild.id]
            queue = player.queue.get_all_tracks()
            if queue:
                queue_list = "\n".join(
                    [f"{idx + 1}. {track['title']}" for idx, track in enumerate(queue)])
                await ctx.send(f"Очередь:\n{queue_list}")
            else:
                await ctx.send("Очередь пуста.")
        else:
            await ctx.send("Нет активного плеера для этого сервера.")


bot.add_cog(Music(bot))

bot.run('TOKEN')
