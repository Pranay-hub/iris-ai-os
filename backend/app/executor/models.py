from typing import Any
from pydantic import BaseModel


class ActionRequest(BaseModel):
    capability: str
    action: str
    parameters: dict[str, Any] = {}


class ExecutionPlan(BaseModel):
    task: str
    actions: list[ActionRequest]