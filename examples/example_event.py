import disnake
from disnake.ext import commands
from dsplayer import Player, event_emitter

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

players = {}

@event_emitter.event("on_play_track")
async def on_play_track(event_data: dict):
    """Отправляет сообщение, когда начинается воспроизведение трека."""
    track = track_info['track']
    channel_id = event_data['text_id']
    channel = bot.get_channel(channel_id)
    await channel.send(f"Начинается воспроизведение трека: {track['url']}")


bot.run('YOUR_BOT_TOKEN')