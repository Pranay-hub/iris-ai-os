from typing import Any

from fastapi import APIRouter

from app.executor.engine import ExecutionEngine
from app.registry.capability_registry import CapabilityRegistry


router = APIRouter(
    prefix="/capabilities",
    tags=["Capabilities"],
)

registry = CapabilityRegistry()
engine = ExecutionEngine(registry=registry)


@router.get("")
def list_capabilities() -> list[dict[str, Any]]:
    """Return the manifests of all registered capabilities."""

    return registry.list_capabilities()


@router.post("/execute")
async def execute_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Resolve, authorize, and execute a planner-generated plan."""

    return await engine.execute(plan)