import re
import asyncio
from dsplayer.utils.compat import discord_lib, commands
from dsplayer.player_system.queue import Queue
from dsplayer.plugin_system.plugin_loader import PluginLoader
from dsplayer.utils.lib_exceptions import TrackNotFound, TrackError
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.engines.ytmusic import YTMusicSearchEngine
from dsplayer.utils.events import event_emitter
from dsplayer.utils.debug import Debuger


class Player:
    def __init__(
            self,
            voice_id: int,
            text_id: int,
            inter,
            plugin_loader: PluginLoader = PluginLoader(),
            volume: float = 1.0,
            FFMPEG_OPTIONS: dict = {},
            deaf: bool = True,
            engine: EngineInterface = YTMusicSearchEngine,
            debug: bool = False):
        """
        Инициализирует объект Player с необходимыми атрибутами.

        :param voice_id: ID голосового канала.
        :param text_id: ID текстового канала.
        :param plugin_loader: Экземпляр PluginLoader для работы с плагинами.
        :param volume: Начальный уровень громкости.
        :param FFMPEG_OPTIONS: Параметры для FFMPEG.
        :param deaf: Глушить ли бота при подключенииы.
        :param engine: Движок, используемый для поиска треков.
        :param debug: Включить или отключить отладку
        """
        self.queue = Queue()
        self.plugin_loader = plugin_loader
        self.voice_channel = inter.guild.get_channel(voice_id)
        self.text_id = text_id
        self.voice_client: discord_lib.VoiceClient = None
        self.FFMPEG_OPTIONS = FFMPEG_OPTIONS
        self.deaf = deaf
        self.engine = engine
        self.debug = debug
        self.debug_print = Debuger(self.debug).debug_print
        self.volume = volume

        event_data = {
            "voice_channel": self.voice_channel,
            "text_id": self.text_id,
            "volume": self.volume,
            "FFMPEG_OPTIONS": self.FFMPEG_OPTIONS,
            "deaf": self.deaf,
            "engine": self.engine,
            "debug": self.debug,
        }

        event_emitter.emit("on_init", event_data=event_data)

    def get_player(self):
        """
        Возвращает объект Player.
        """
        return self

    async def connect(self):
        """
        Подключает бота к голосовому каналу. Если бот уже подключен к другому каналу, он переподключиться на другой голосовой канал.
        """
        if self.voice_client is None or not self.voice_client.is_connected():
            self.debug_print(
                f"Connecting to voice channel: {self.voice_channel}")
            self.voice_client = await self.voice_channel.connect()
            if self.deaf:
                await self.voice_client.guild.change_voice_state(channel=self.voice_client.channel, self_deaf=True)
        elif self.voice_client.channel != self.voice_channel:
            self.debug_print(f"Moving to voice channel: {self.voice_channel}")
            await self.voice_client.move_to(self.voice_channel)
            if self.deaf:
                await self.voice_client.guild.change_voice_state(channel=self.voice_client.channel, self_deaf=True)

        event_data = {
            "voice_client": self.voice_client,
            "text_id": self.text_id,
            "voice_channel": self.voice_channel,

        }
        event_emitter.emit("on_connect", event_data=event_data)

    async def disconnect(self):
        """
        Отключает бота от голосового канала и устанавливает для голосового клиента значение None.
        """
        if self.voice_client is not None:
            self.debug_print("Disconnecting from voice channel")
            await self.voice_client.disconnect()
            self.voice_client = None
            event_data = {
                "voice_client": self.voice_client,
                "text_id": self.text_id,
                "voice_channel": self.voice_channel,
    
            }
            event_emitter.emit("on_disconnect", event_data=event_data)

    async def stop(self):
        """
        Останавливает воспроизведение текущего тркека и очищает очередь.
        """
        if self.voice_client is not None:
            self.debug_print("Stopping playback and clearing the queue")
            self.voice_client.stop()
            self.queue.clear()
            event_data = {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client,
    
            }
            event_emitter.emit("on_stop", event_data=event_data)
            await self.disconnect()

    async def pause(self):
        """
        Приостанавливает воспроизведение текущего трека.
        """
        if self.voice_client is not None:
            self.voice_client.pause()
            event_data = {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client,
    
            }
            event_emitter.emit("on_pause", event_data=event_data)

    async def resume(self):
        """
        Возобновление приостановленного трека.
        """
        if self.voice_client is not None:
            self.voice_client.resume()
            event_data = {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client,
    
            }
            event_emitter.emit("on_resume", event_data=event_data)

    async def skip(self):
        """
        Пропускает текущую воспроизводимый трек и воспроизводит следующий трек в очереди.
        """
        if self.voice_client and self.voice_client.is_playing():
            self.debug_print("Skipping current track")
            self.voice_client.stop()
            await self._play_next()
            event_data = {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client,
    
            }
            event_emitter.emit("on_skip", event_data=event_data)
        else:
            self.debug_print("No track is currently playing")
            event_data = {
                "error": "No track is currently playing to skip",
                "text_id": self.text_id,
    
            }
            event_emitter.emit("on_error", event_data=event_data)
            raise TrackError("No track is currently playing to skip")

    async def previous(self):
        """
        Воспроизводит предыдущий трек в очереди.
        """
        if self.voice_client and self.voice_client.is_playing():
            self.debug_print("Returning to the previous track")
            self.voice_client.stop()
            await self._play_previous()
            event_data = {
                "queue": self.queue.get_all_tracks(),
                "text_id": self.text_id,
                "voice_client": self.voice_client,
    
            }
            event_emitter.emit("on_previous", event_data=event_data)
        else:
            self.debug_print("No track is currently playing")
            event_emitter.emit("on_error", {
                "error": "No track is currently playing to skip",
                "text_id": self.text_id,
    
            })
            raise TrackError("No track is currently playing to skip")

    async def set_volume(self, volume: float):
        """
        Устанавливает громкость для текущего воспроизводимого трека.

        :param volume: Уровень громкости, который необходимо установить.
        """
        if self.voice_client is not None and self.voice_client.source is not None:
            self.voice_client.source = discord_lib.PCMVolumeTransformer(
                self.voice_client.source, volume)
            event_data = {
                "volume": volume,
                "text_id": self.text_id,
                "voice_client": self.voice_client,
    
            }
            event_emitter.emit("on_volume_change", event_data=event_data)

    def update_plugin_settings(self, plugin_name: str, settings: dict) -> bool:
        """
        Обновляет настройки для указанного плагина.

        :param имя_плагина: имя плагина.
        :param settings: Словарь, содержащий настройки для обновления.
        :return: True, если настройки были успешно обновлены, False в противном случае.
        """
        result = self.plugin_loader.update_plugin_settings(
            plugin_name, settings)
        event_emitter.emit("on_update_plugin_settings", {
            "plugin_name": plugin_name,
            "settings": settings,
            "result": result,
            "text_id": self.text_id,

        })
        return result

    async def _play_track(self, track: dict):
        """
        Воспроизводит указанный трек. Если трек уже проигрывается, он ставится в очередь.

        :param track: Словарь, содержащий информацию о треке.
        :raises TrackNotFound: Если трек не найден для воспроизведения.
        :raises TrackError: Если при воспроизведении трека произошла ошибка.
        """
        if track:
            try:
                if self.voice_client is None:
                    self.debug_print("Voice client is not initialized.")
                    return

                if not self.voice_client.is_connected():
                    self.debug_print("Voice client is not connected.")
                    return

                if not self.voice_client.is_playing():
                    self.debug_print(f"Playing track: {track}")
                    event_data = {
                        "track": track,
                        "text_id": self.text_id,
                        "voice_client": self.voice_client,
            
                    }
                    event_emitter.emit("on_play_track", event_data=event_data)

                    self.debug_print("Event is emitted")

                    try:
                        audio_source = discord_lib.FFmpegPCMAudio(
                            track['url'], **self.FFMPEG_OPTIONS)
                    except BaseException:
                        try:
                            audio_source = discord_lib.FFmpegPCMAudio(
                                track.get('url'), **self.FFMPEG_OPTIONS)
                        except BaseException:
                            audio_source = None

                    if audio_source:
                        self.debug_print(
                            f"Audio source created: {audio_source}")
                        loop = asyncio.get_event_loop()
                        self.voice_client.play(
                            audio_source, after=lambda e: loop.call_soon_threadsafe(
                                asyncio.create_task, self._track_ended(e)))
                        await self.set_volume(self.volume)
                        self.debug_print("Play command sent")
                        self.queue.update_current_index()
                    else:
                        self.debug_print("Failed to create audio source.")

                else:
                    self.debug_print(f"Queueing track: {track}")
                    self.queue.add_track(track)
                    event_emitter.emit("on_track_queued", {
                        "track": track,
                        "text_id": self.text_id,
                        "queue": self.queue.get_all_tracks(),
            
                    })
            except Exception as e:
                self.debug_print(f"Error playing track: {e}")
                event_emitter.emit("on_error", {
                    "error": str(e),
                    "text_id": self.text_id,
        
                })
                raise TrackError(f"Error playing track: {e}")

    async def play(self, url_or_query: str):
        """
        Воспроизводит трек.

        :param url_or_query: URL или текст для поиска трека.
        """
        self.debug_print(
            f"Searching for track with URL or query: {url_or_query}")
        plugins = self.plugin_loader.get_plugins()
        if self.debug:
            self.plugin_loader.debug()

        track_found = False

        if url_or_query.startswith('http'):
            for plugin in plugins:
                patterns = plugin.get_url_patterns()
                for pattern in patterns:
                    if re.search(pattern, url_or_query):
                        try:
                            if self.debug:
                                plugin.debug()
                            track_generator = plugin.search(
                                data=url_or_query, engine=self.engine)
                            async for track_info in track_generator:
                                if not track_found:
                                    self.debug_print(
                                        f"Adding first track: {track_info}")
                                    self.queue.add_track(track_info)
                                    await self._play_track(track_info)
                                    track_found = True
                                else:
                                    self.queue.add_track(track_info)

                            if track_found:
                                return
                        except Exception as e:
                            self.debug_print(
                                f"Error finding track info with plugin: {plugin.get_plugin_name()} \n{e}")
                            event_emitter.emit("on_error", {
                                "error": str(e),
                                "text_id": self.text_id,
                    
                            })
        else:
            for plugin in plugins:
                if plugin.__class__.__name__ == 'QueryPlugin':
                    try:
                        if self.debug:
                            plugin.debug()
                        track_generator = plugin.search(
                            data=url_or_query, engine=self.engine)
                        async for track_info in track_generator:
                            if not track_found:
                                self.debug_print(
                                    f"Adding first track: {track_info}")
                                self.queue.add_track(track_info)
                                await self._play_track(track_info)
                                track_found = True
                            else:
                                self.queue.add_track(track_info)

                        if track_found:
                            return
                    except Exception as e:
                        self.debug_print(
                            f"Error finding track info with plugin: {plugin.get_plugin_name()} \n{e}")
                        event_emitter.emit("on_error", {
                            "error": str(e),
                            "text_id": self.text_id,
                
                        })
            else:
                if not track_found:
                    raise TrackNotFound(
                        f"No suitable plugin found to handle the provided data or track not played")

    async def _play_track_from_queue(self):
        if self.voice_client and self.voice_client.is_playing() and not self.queue.is_empty():
            self.debug_print("Playing track from queue")
            await self.play_next()

    async def _track_ended(self, error):
        """
        Обрабатывает событие окончания трека. Воспроизводит следующущий трек, если она доступна.
        """
        if error:
            self.debug_print(f"Track ended with error: {error}")
            event_emitter.emit("on_error", {
                "error": str(error),
                "text_id": self.text_id,
    
            })
        else:
            self.debug_print("Track ended successfully")
            await self._play_next()

    async def _play_next(self):
        """
        Воспроизводит следующий трек в очереди.
        """
        self.debug_print("Getting next track from queue")
        next_track = self.queue.get_next_track()
        if next_track:
            await self._play_track(next_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty", {
                "text_id": self.text_id,
                "queue": self.queue.get_all_tracks(),
    
            })
            await self.disconnect()

    async def _play_previous(self):
        """
        Воспроизводит предыдущий трек в очереди.
        """
        self.debug_print("Getting previous track from queue")
        back_track = self.queue.get_back_track()
        if back_track:
            await self._play_track(back_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty", {
                "text_id": self.text_id,
                "queue": self.queue.get_all_tracks(),
    
            })
            await self.disconnect()

    async def _play_current(self):
        """
        Воспроизводит текущий трек в очереди.
        """
        self.debug_print("Getting current track from queue")
        current_track = self.queue.get_current_track()
        if current_track:
            await self._play_track(current_track)
        else:
            self.debug_print("Queue is empty")
            event_emitter.emit("on_queue_empty", {
                "text_id": self.text_id,
                "queue": self.queue.get_all_tracks(),
    
            })
            await self.disconnect()
