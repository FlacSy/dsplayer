# Плеер

В `dsplayer` для проигрования музыки используеться класс `Player`. Ниже будет перечислены атрибуты и методы класса `Player`.

- **Атрибуты**
  1. **`queue: Queue`** — объект класса `Queue`, представляющий очередь треков для воспроизведения.
  2. **`plugin_loader: PluginLoader`** — объект класса `PluginLoader`, загружающий плагины.
  3. **`voice_channel: Optional[disnake.VoiceChannel]`** — объект канала голосовой связи.
  4. **`text_id: int`** — идентификатор текстового канала.
  5. **`voice_client: Optional[disnake.VoiceClient]`** — объект клиента голосовой связи.
  6. **`FFMPEG_OPTIONS: dict`** — опции для FFMPEG.
  7. **`bot: commands.Bot`** — объект бота.
  8. **`deaf: bool`** — флаг, указывающий, должен ли бот быть заглушен при подключении.
  9. **`engine: EngineInterface`** — объект интерфейса поискового движка для треков.
  10. **`debug: bool`** — флаг, включающий или выключающий режим отладки.
  11. **`debug_print: Callable`** — функция для печати отладочных сообщений.
  12. **`volume: float`** — громкость плеера.

- **Методы**
  1. **`__init__(self, voice_id: int, text_id: int, bot: commands.Bot, plugin_loader: PluginLoader, volume: float = 1.0, FFMPEG_OPTIONS: dict = {}, deaf: bool = True, engine: EngineInterface = YTMusicSearchEngine, debug: bool = False)`** — инициализирует объект плеера с необходимыми атрибутами.
  2. **`connect(self)`** — подключает бота к голосовому каналу.
  3. **`disconnect(self)`** — отключает бота от голосового канала.
  4. **`stop(self)`** — останавливает текущий трек и очищает очередь.
  5. **`pause(self)`** — ставит воспроизведение на паузу.
  6. **`resume(self)`** — возобновляет воспроизведение.
  7. **`skip(self)`** — пропускает текущий трек и воспроизводит следующий в очереди.
  8. **`previous(self)`** — воспроизводит предыдущий трек в очереди.
  9. **`set_volume(self, volume: float)`** — устанавливает громкость для текущего трека.
  10. **`update_plugin_settings(self, plugin_name: str, settings: dict) -> bool`** — обновляет настройки для указанного плагина.
  11. **`play_track(self, track: dict)`** — воспроизводит указанный трек.
  12. **`_track_ended(self, error)`** — обрабатывает событие окончания трека.
  13. **`_play_next(self)`** — воспроизводит следующий трек в очереди.
  14. **`_play_previous(self)`** — воспроизводит предыдущий трек в очереди.
  15. **`_play_current(self)`** — воспроизводит текущий трек в очереди.
