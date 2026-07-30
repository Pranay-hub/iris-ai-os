from __future__ import annotations

from typing import Any

import pytest

from app.executor.engine import ExecutionEngine
from app.memory.manager import MemoryManager


class FakeCapability:
    async def execute(
        self,
        action: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "action": action,
            "parameters": parameters,
        }


class FakeRegistry:
    def get(self, name: str) -> FakeCapability:
        if name == "system":
            return FakeCapability()

        raise ValueError(f"Capability not found: {name}")


@pytest.mark.asyncio
async def test_engine_stores_last_successful_intent_and_result() -> None:
    memory = MemoryManager()

    engine = ExecutionEngine(
        registry=FakeRegistry(),
        memory_manager=memory,
    )

    response = await engine.execute(
        {
            "capability": "system",
            "action": "get_info",
            "parameters": {},
            "confidence": 1.0,
        }
    )

    assert response["success"] is True

    assert memory.get_session("last_intent") == {
        "capability": "system",
        "action": "get_info",
        "parameters": {},
        "confidence": 1.0,
    }

    assert memory.get_session("last_result") == {
        "action": "get_info",
        "parameters": {},
    }


@pytest.mark.asyncio
async def test_engine_does_not_store_failed_execution() -> None:
    memory = MemoryManager()

    engine = ExecutionEngine(
        registry=FakeRegistry(),
        memory_manager=memory,
    )

    response = await engine.execute(
        {
            "capability": "system",
            "action": "shutdown",
            "parameters": {},
        }
    )

    assert response["success"] is False
    assert memory.get_session("last_intent") is None
    assert memory.get_session("last_result") is None