from __future__ import annotations

from typing import Any


class SessionStore:
    """Stores short-lived state for the current IRIS session."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Store a session value."""

        self._data[key] = value

    def get(self, key: str) -> Any | None:
        """Return a session value, or None when it does not exist."""

        return self._data.get(key)

    def delete(self, key: str) -> bool:
        """Delete a session value and report whether it existed."""

        if key not in self._data:
            return False

        del self._data[key]
        return True

    def clear(self) -> None:
        """Remove all session values."""

        self._data.clear()