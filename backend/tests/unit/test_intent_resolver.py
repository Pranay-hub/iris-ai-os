import pytest

from app.executor.intent_resolver import (
    IntentResolutionError,
    IntentResolver,
)


def test_resolves_valid_intent() -> None:
    resolver = IntentResolver()

    result = resolver.resolve(
        {
            "capability": "System",
            "action": "Get Info",
            "parameters": {},
            "confidence": 0.95,
        }
    )

    assert result.capability == "system"
    assert result.action == "get_info"
    assert result.parameters == {}
    assert result.confidence == 0.95


def test_defaults_missing_parameters() -> None:
    resolver = IntentResolver()

    result = resolver.resolve(
        {
            "capability": "system",
            "action": "get_info",
        }
    )

    assert result.parameters == {}
    assert result.confidence == 1.0


def test_rejects_missing_capability() -> None:
    resolver = IntentResolver()

    with pytest.raises(IntentResolutionError):
        resolver.resolve(
            {
                "action": "get_info",
            }
        )


def test_rejects_invalid_parameters() -> None:
    resolver = IntentResolver()

    with pytest.raises(IntentResolutionError):
        resolver.resolve(
            {
                "capability": "system",
                "action": "get_info",
                "parameters": [],
            }
        )


def test_rejects_invalid_confidence() -> None:
    resolver = IntentResolver()

    with pytest.raises(IntentResolutionError):
        resolver.resolve(
            {
                "capability": "system",
                "action": "get_info",
                "confidence": 1.5,
            }
        )