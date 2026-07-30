from __future__ import annotations

from typing import Any


class UserStore:
    """Stores user preferences for the current runtime."""

    def __init__(self) -> None:
        self._preferences: dict[str, Any] = {}

    def set_preference(self, key: str, value: Any) -> None:
        """Store a user preference."""

        self._preferences[key] = value

    def get_preference(self, key: str) -> Any | None:
        """Return a user preference, or None when it does not exist."""

        return self._preferences.get(key)

    def delete_preference(self, key: str) -> bool:
        """Delete a user preference and report whether it existed."""

        if key not in self._preferences:
            return False

        del self._preferences[key]
        return True

    def clear(self) -> None:
        """Remove all user preferences."""

        self._preferences.clear()