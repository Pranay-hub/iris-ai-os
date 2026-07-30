from fastapi import APIRouter

from app.registry.capability_registry import CapabilityRegistry
from app.executor.engine import ExecutionEngine

router = APIRouter(prefix="/capabilities", tags=["Capabilities"])

registry = CapabilityRegistry()
engine = ExecutionEngine()


@router.get("")
def list_capabilities():
    return registry.list_capabilities()


@router.post("/execute")
def execute_plan(plan: dict):
    return engine.execute_plan(plan)