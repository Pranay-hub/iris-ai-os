from __future__ import annotations
from typing import Any

import pytest

from app.executor.engine import ExecutionEngine
from app.executor.intent_resolver import IntentResolver
from app.security.permission_manager import PermissionManager


class FakeCapability:
    """Test capability that records whether it was executed."""

    def __init__(self) -> None:
        self.executed = False

    async def execute(
        self,
        action: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        self.executed = True

        return {
            "action": action,
            "parameters": parameters,
        }


class FakeRegistry:
    """Minimal registry used to test the execution pipeline."""

    def __init__(self, capability: FakeCapability) -> None:
        self._capability = capability

    def get(self, name: str) -> FakeCapability | None:
        if name == "system":
            return self._capability

        return None


@pytest.mark.asyncio
async def test_engine_executes_authorized_action() -> None:
    capability = FakeCapability()
    registry = FakeRegistry(capability)

    engine = ExecutionEngine(
        registry=registry,
        intent_resolver=IntentResolver(),
        permission_manager=PermissionManager(),
    )

    response = await engine.execute(
        {
            "capability": "system",
            "action": "get_info",
            "parameters": {},
        }
    )

    assert response["success"] is True
    assert response["error"] is None
    assert capability.executed is True


@pytest.mark.asyncio
async def test_engine_blocks_unauthorized_action() -> None:
    capability = FakeCapability()
    registry = FakeRegistry(capability)

    engine = ExecutionEngine(
        registry=registry,
        intent_resolver=IntentResolver(),
        permission_manager=PermissionManager(),
    )

    response = await engine.execute(
        {
            "capability": "system",
            "action": "shutdown",
            "parameters": {},
        }
    )

    assert response["success"] is False
    assert response["error"]["code"] == "PERMISSION_DENIED"
    assert capability.executed is False