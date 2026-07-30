from abc import ABC, abstractmethod
from typing import Any


class Capability(ABC):
    name: str
    description: str
    actions: dict
    permissions: list[str]

    def manifest(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "actions": self.actions,
            "permissions": self.permissions,
        }

    @abstractmethod
    def execute(self, action: str, parameters: dict[str, Any]) -> Any:
        pass