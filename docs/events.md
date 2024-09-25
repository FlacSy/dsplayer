# События

Класс `Player` генерирует события через `event_emitter`. Эти события можно использовать для выполнения пользовательских действий в ответ на различные состояния воспроизведения. Ниже приведен список событий и когда они генерируются:

## Список событий 

1. **`on_init`**
   - **Когда вызывается:** При инициализации объекта `Player`.
   - **Что возвращает:** Данные о начальных настройках плеера.
   - **Возвращаемые данные:**
     ```json
     {
       "voice_channel": <voice_channel_object>,
       "text_id": <text_channel_id>,
       "volume": <volume_level>,
       "FFMPEG_OPTIONS": <ffmpeg_options_dict>,
       "deaf": <deaf_status>,
       "engine": <engine_object>,
       "debug": <debug_status>
     }
     ```

2. **`on_connect`**
   - **Когда вызывается:** При подключении бота к голосовому каналу.
   - **Что возвращает:** Данные о подключении.
   - **Возвращаемые данные:**
     ```json
     {
       "voice_client": <voice_client_object>,
       "text_id": <text_channel_id>,
       "voice_channel": <voice_channel_object>
     }
     ```

3. **`on_disconnect`**
   - **Когда вызывается:** При отключении бота от голосового канала.
   - **Что возвращает:** Данные о состоянии после отключения.
   - **Возвращаемые данные:**
     ```json
     {
       "voice_client": <voice_client_object>,
       "text_id": <text_channel_id>,
       "voice_channel": <voice_channel_object>
     }
     ```

4. **`on_stop`**
   - **Когда вызывается:** При остановке воспроизведения трека и очистке очереди.
   - **Что возвращает:** Данные о состоянии очереди и плеере после остановки.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

5. **`on_pause`**
   - **Когда вызывается:** При паузе текущего трека.
   - **Что возвращает:** Данные о состоянии очереди и плеере после паузы.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

6. **`on_resume`**
   - **Когда вызывается:** При возобновлении воспроизведения трека.
   - **Что возвращает:** Данные о состоянии очереди и плеере после возобновления.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

7. **`on_skip`**
   - **Когда вызывается:** При пропуске текущего трека и переходе к следующему.
   - **Что возвращает:** Данные о состоянии очереди и плеере после пропуска.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

8. **`on_previous`**
   - **Когда вызывается:** При возврате к предыдущему треку в очереди.
   - **Что возвращает:** Данные о состоянии очереди и плеере после возврата.
   - **Возвращаемые данные:**
     ```json
     {
       "queue": <all_tracks_in_queue>,
       "text_id": <text_channel_id>,
       "voice_client": <voice_client_object>
     }
     ```

9. **`on_update_plugin_settings`**
   - **Когда вызывается:** При обновлении настроек плагина.
   - **Что возвращает:** Данные о результатах обновления настроек.
   - **Возвращаемые данные:**
     ```json
     {
       "plugin_name": <plugin_name>,
       "settings": <plugin_settings>,
       "result": <update_success_or_failure>,
       "text_id": <text_channel_id>
     }
     ```

10. **`on_play_track`**
    - **Когда вызывается:** При начале воспроизведения нового трека.
    - **Что возвращает:** Данные о треке и состоянии плеера.
    - **Возвращаемые данные:**
      ```json
      {
        "track": <track_info>,
        "text_id": <text_channel_id>,
        "voice_client": <voice_client_object>
      }
      ```

11. **`on_track_queued`**
    - **Когда вызывается:** При добавлении трека в очередь.
    - **Что возвращает:** Данные о добавленном треке и состоянии очереди.
    - **Возвращаемые данные:**
      ```json
      {
        "track": <track_info>,
        "text_id": <text_channel_id>,
        "queue": <all_tracks_in_queue>
      }
      ```

12. **`on_error`**
    - **Когда вызывается:** При возникновении ошибки во время выполнения команды.
    - **Что возвращает:** Данные об ошибке.
    - **Возвращаемые данные:**
      ```json
      {
        "error": <error_message>,
        "text_id": <text_channel_id>
      }
      ```

13. **`on_queue_empty`**
    - **Когда вызывается:** При отсутствии треков в очереди.
    - **Что возвращает:** Данные о состоянии очереди после проверки.
    - **Возвращаемые данные:**
      ```json
      {
        "text_id": <text_channel_id>,
        "queue": <all_tracks_in_queue>
      }
      ```

14. **`on_track_end`**
    - **Когда вызывается:** Когда трек завершает воспроизведение.
    - **Что возвращает:** Данные о завершении трека.
    - **Возвращаемые данные:**
      ```json
      {
        "text_id": <text_channel_id>
      }
      ```

15. **`on_volume_change`**
    - **Когда вызывается:** Когда изменяеться громкость.
    - **Что возвращает:** Громкость трека.
    - **Возвращаемые данные:**
      ```json
      {
        "volume": <volume>,
        "text_id": <text_channel_id>,
        "voice_client": <voice_client>
      }
      ```

