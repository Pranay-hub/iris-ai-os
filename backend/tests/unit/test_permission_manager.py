from app.security.permission_manager import PermissionManager


def test_allowed_action() -> None:
    manager = PermissionManager()

    result = manager.authorize(
        capability="system",
        action="get_info",
    )

    assert result.allowed is True
    assert result.reason is None


def test_unknown_capability_is_denied() -> None:
    manager = PermissionManager()

    result = manager.authorize(
        capability="browser",
        action="open_url",
    )

    assert result.allowed is False
    assert result.reason is not None


def test_unknown_action_is_denied() -> None:
    manager = PermissionManager()

    result = manager.authorize(
        capability="system",
        action="shutdown",
    )

    assert result.allowed is False
    assert result.reason is not None