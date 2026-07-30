import platform

from app.plugins.base import Plugin


class SystemPlugin(Plugin):

    name = "system"

    description = "Returns system information."

    def execute(self, **kwargs):
        return {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine()
        }