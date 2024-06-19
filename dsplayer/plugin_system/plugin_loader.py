import pkgutil
import importlib
from dsplayer.plugin_system.plugin_interface import PluginInterface
from typing import List

class PluginLoader:
    def __init__(self, plugin_package: str = 'dsplayer.plugins'):
        self.plugin_package = plugin_package
        self.plugins = self._load_plugins()

    def _load_plugins(self) -> List:
        plugins = []
        package = importlib.import_module(self.plugin_package)
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            if not is_pkg:
                module = importlib.import_module(f"{self.plugin_package}.{name}")
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, PluginInterface) and cls is not PluginInterface:
                        plugins.append(cls())
        return plugins

    def get_plugins(self):
        return self.plugins