from app.plugins.system_plugin import SystemPlugin


class PluginManager:

    def __init__(self):
        self.plugins = {
            "system": SystemPlugin()
        }

    def execute(self, plugin_name, **kwargs):
        plugin = self.plugins.get(plugin_name)

        if not plugin:
            raise Exception(f"Plugin '{plugin_name}' not found")

        return plugin.execute(**kwargs)