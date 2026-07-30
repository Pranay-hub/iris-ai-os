from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class PermissionDenied(Exception):
    """Raised when an action is not permitted."""


@dataclass(frozen=True)
class PermissionResult:
    allowed: bool
    reason: str | None = None


class PermissionManager:
    """
    Central authorization service.

    Every capability execution must pass through here.
    """

    def __init__(self) -> None:
        self._rules: dict[str, set[str]] = {
            "system": {
                "get_info",
            }
        }

    def authorize(
        self,
        capability: str,
        action: str,
        parameters: dict[str, Any] | None = None,
    ) -> PermissionResult:

        allowed_actions = self._rules.get(capability)

        if allowed_actions is None:
            return PermissionResult(
                allowed=False,
                reason=f"Unknown capability '{capability}'.",
            )

        if action not in allowed_actions:
            return PermissionResult(
                allowed=False,
                reason=(
                    f"Action '{action}' is not allowed "
                    f"for capability '{capability}'."
                ),
            )

        return PermissionResult(True)