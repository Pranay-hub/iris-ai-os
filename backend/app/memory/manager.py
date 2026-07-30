from __future__ import annotations

from typing import Any

from app.memory.conversation_store import ConversationStore
from app.memory.session_store import SessionStore
from app.memory.user_store import UserStore


class MemoryManager:
    """Provides a single interface to IRIS runtime memory."""

    def __init__(
        self,
        session_store: SessionStore | None = None,
        conversation_store: ConversationStore | None = None,
        user_store: UserStore | None = None,
    ) -> None:
        self._session = session_store or SessionStore()
        self._conversation = conversation_store or ConversationStore()
        self._user = user_store or UserStore()

    def set_session(self, key: str, value: Any) -> None:
        """Store session-scoped state."""

        self._session.set(key, value)

    def get_session(self, key: str) -> Any | None:
        """Retrieve session-scoped state."""

        return self._session.get(key)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation memory."""

        self._conversation.add(role, content)

    def get_conversation(
        self,
        limit: int | None = None,
    ) -> list[dict[str, str]]:
        """Retrieve recent conversation messages."""

        return self._conversation.get(limit=limit)

    def set_user_preference(self, key: str, value: Any) -> None:
        """Store a user preference."""

        self._user.set_preference(key, value)

    def get_user_preference(self, key: str) -> Any | None:
        """Retrieve a user preference."""

        return self._user.get_preference(key)

    def clear_session(self) -> None:
        """Clear all session memory."""

        self._session.clear()

    def clear_conversation(self) -> None:
        """Clear conversation history."""

        self._conversation.clear()

    def clear_user_preferences(self) -> None:
        """Clear user preferences."""

        self._user.clear()