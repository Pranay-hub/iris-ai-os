import platform
from typing import Any

from app.capabilities.base import Capability


class SystemCapability(Capability):
    name = "system"
    description = "Provides system-level information and diagnostics."

    actions = {
        "info": {
            "description": "Get operating system information.",
            "parameters": {},
            "dangerous": False,
        }
    }

    permissions = ["system:read"]

    def execute(self, action: str, parameters: dict[str, Any]) -> Any:
        if action == "info":
            return {
                "os": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
            }

        raise ValueError(f"Unknown system action: {action}")