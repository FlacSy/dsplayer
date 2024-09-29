import importlib
import importlib.metadata
import pkgutil
from dsplayer.plugin_system.plugin_interface import PluginInterface
from typing import List, Optional, Dict, Any, Type
from dsplayer.utils.debug import Debuger


class PluginLoader:
    def __init__(self, plugin_packages: List[str] = [], debug: bool = False):
        plugin_packages.append('dsplayer.plugin_system')
        self.plugin_packages = plugin_packages
        self.plugin_classes: List[Type[PluginInterface]] = []
        self.plugins: List[PluginInterface] = []
        self.addon_plugins: List[PluginInterface] = []
        self.extractor_plugins: List[PluginInterface] = []
        self.debug_mode = debug
        self.debug_print = Debuger(self.debug_mode).debug_print
        self._load_plugins()

    def _load_plugins(self) -> None:
        for plugin_package in self.plugin_packages:
            package = importlib.import_module(plugin_package)
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                if not is_pkg and name.endswith('_plugin'):
                    module = importlib.import_module(f"{plugin_package}.{name}")
                    for attr in dir(module):
                        cls = getattr(module, attr)
                        if isinstance(cls, type) and issubclass(cls, PluginInterface) and cls is not PluginInterface:
                            plugin_instance = cls()
                            self.plugins.append(plugin_instance)
                            plugin_instance.on_plugin_load()

                            self._categorize_plugin(plugin_instance)

        entry_points = importlib.metadata.entry_points()
        dsplayer_plugins = entry_points.select(group='dsplayer.plugins')
        for entry_point in dsplayer_plugins:
            plugin_class = entry_point.load()
            if issubclass(plugin_class, PluginInterface):
                plugin_instance = plugin_class()
                self.plugins.append(plugin_instance)
                plugin_instance.on_plugin_load()

                self._categorize_plugin(plugin_instance)

        self.debug_print("All plugins are loaded!")

    def _categorize_plugin(self, plugin: PluginInterface) -> None:
        plugin_type = plugin.get_plugin_type()
        if plugin_type == "addon":
            self.addon_plugins.append(plugin)
        elif plugin_type == "extractor":
            self.extractor_plugins.append(plugin)

    def get_addon_plugins(self) -> List[PluginInterface]:
        return self.addon_plugins

    def get_extractor_plugins(self) -> List[PluginInterface]:
        return self.extractor_plugins

    def debug(self):
        self.debug_mode = True