import platform
from typing import Any

from app.capabilities.base import Capability


class SystemCapability(Capability):
    name = "system"
    description = "Provides system-level information and diagnostics."

    actions = {
        "get_info": {
            "description": "Get operating system information.",
            "parameters": {},
            "dangerous": False,
        }
    }

    permissions = ["system:read"]

    async def execute(
        self,
        action: str,
        parameters: dict[str, Any],
    ) -> Any:
        if action == "get_info":
            return {
                "os": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python_version": platform.python_version(),
            }

        raise ValueError(f"Unknown system action: {action}")