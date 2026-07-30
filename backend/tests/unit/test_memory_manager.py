from app.memory.manager import MemoryManager


def test_session_memory():
    memory = MemoryManager()

    memory.set_session("cwd", "/Users/pranay")

    assert memory.get_session("cwd") == "/Users/pranay"


def test_unknown_session_returns_none():
    memory = MemoryManager()

    assert memory.get_session("missing") is None


def test_conversation_memory():
    memory = MemoryManager()

    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi!")

    history = memory.get_conversation()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_user_preferences():
    memory = MemoryManager()

    memory.set_user_preference("theme", "dark")

    assert memory.get_user_preference("theme") == "dark"