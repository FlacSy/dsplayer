import pkgutil
import importlib
from dsplayer.plugin_system.plugin_interface import PluginInterface
from typing import List

class PluginLoader:
    def __init__(self, plugin_packages: List[str] = ['dsplayer.plugins']):
        self.plugin_packages = plugin_packages
        self.plugins = self._load_plugins()

    def _load_plugins(self) -> List[PluginInterface]:
        plugins = []
        for plugin_package in self.plugin_packages:
            package = importlib.import_module(plugin_package)
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                if not is_pkg:
                    module = importlib.import_module(f"{plugin_package}.{name}")
                    for attr in dir(module):
                        cls = getattr(module, attr)
                        if isinstance(cls, type) and issubclass(cls, PluginInterface) and cls is not PluginInterface:
                            plugin_instance = cls()  
                            plugins.append(plugin_instance)
                            plugin_instance.on_plugin_load()  
        return plugins

    def get_plugins(self) -> List[PluginInterface]:
        return self.plugins