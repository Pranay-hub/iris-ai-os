from __future__ import annotations

from app.memory.models import Message


class ConversationStore:
    """Stores recent conversation messages in memory."""

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""

        if not role.strip():
            raise ValueError("Message role cannot be empty.")

        if not content.strip():
            raise ValueError("Message content cannot be empty.")

        self._messages.append(
            Message(
                role=role.strip(),
                content=content.strip(),
            )
        )

    def get(self, limit: int | None = None) -> list[dict[str, str]]:
        """Return conversation messages in insertion order."""

        messages = self._messages

        if limit is not None:
            if limit < 0:
                raise ValueError("Conversation limit cannot be negative.")

            messages = messages[-limit:] if limit > 0 else []

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    def clear(self) -> None:
        """Remove all conversation messages."""

        self._messages.clear()