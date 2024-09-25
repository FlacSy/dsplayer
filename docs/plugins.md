# Плагины

В `dsplayer` предусмотрена система плагинов за которую отвечает класс `PluginLoader`. 

## Класс `PluginLoader`
- **Pluginloader Attributes:**
  1. **`plugin_packages: List[str]`** — список пакетов плагинов.
  2. **`plugin_classes: List[Type[PluginInterface]]`** — список классов плагинов.
  3. **`plugins: List[PluginInterface]`** — список экземпляров плагинов.
  4. **`debug_mode: bool`** — флаг, указывающий, включен ли режим отладки.
  5. **`debug_print: Callable`** — функция для печати отладочных сообщений.

- **Pluginloader Methods:**
  1. **`__init__(self, plugin_packages: List[str] = ['dsplayer.plugin_system'])`** — инициализирует загрузчик плагинов и загружает плагины.
  2. **`debug(self)`** — включает режим отладки.
  3. **`load_plugins_from_classes(self, plugin_classes: List[Type[PluginInterface]]) -> None`** — загружает плагины из переданных классов.
  4. **`_load_plugins(self) -> None`** — загружает плагины из указанных пакетов и точек входа.
  5. **`get_plugins(self) -> List[PluginInterface]`** — возвращает список загруженных плагинов.
  6. **`get_plugin_by_name(self, plugin_name: str) -> Optional[PluginInterface]`** — возвращает плагин по его имени.
  7. **`update_plugin_settings(self, plugin_name: str, settings: Dict[str, Any]) -> bool`** — обновляет настройки указанного плагина.

