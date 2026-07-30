from __future__ import annotations
from app.memory.manager import MemoryManager
from typing import Any

from app.executor.intent_resolver import (
    IntentResolutionError,
    IntentResolver,
    ResolvedIntent,
)
from app.registry.capability_registry import CapabilityRegistry
from app.security.permission_manager import PermissionManager


class ExecutionEngine:
    """Executes validated and authorized intents."""

    def __init__(
        self,
        registry: CapabilityRegistry,
        intent_resolver: IntentResolver | None = None,
        permission_manager: PermissionManager | None = None,
        memory_manager: MemoryManager | None = None,
    ) -> None:
       self._registry = registry
       self._intent_resolver = intent_resolver or IntentResolver()
       self._permission_manager = (
        permission_manager or PermissionManager()
    )
       self._memory_manager = memory_manager or MemoryManager()

    async def execute(
        self,
        planner_output: dict[str, Any],
    ) -> dict[str, Any]:
        """Resolve, authorize, and execute planner output."""

        # 1. Validate and normalize the planner response.
        try:
            intent = self._intent_resolver.resolve(planner_output)
        except IntentResolutionError as exc:
            return self._error_response(
                error_code="INVALID_INTENT",
                message=str(exc),
            )

        # 2. Check permission before accessing the capability.
        permission = self._permission_manager.authorize(
            capability=intent.capability,
            action=intent.action,
            parameters=intent.parameters,
        )

        if not permission.allowed:
            return self._error_response(
                error_code="PERMISSION_DENIED",
                message=permission.reason or "Permission denied.",
                intent=intent,
            )

        # 3. Find the requested capability.
        try:
          capability = self._registry.get(intent.capability)
        except ValueError as exc:
           return self._error_response(
        error_code="CAPABILITY_NOT_FOUND",
        message=str(exc),
        intent=intent,
    )

        # 4. Execute the capability action.
        try:
            result = await capability.execute(
                action=intent.action,
                parameters=intent.parameters,
            )
        except Exception as exc:
            return self._error_response(
                error_code="EXECUTION_FAILED",
                message=str(exc),
                intent=intent,
            )
        self._memory_manager.set_session(
    "last_intent",
    self._serialize_intent(intent),
)
        self._memory_manager.set_session(
    "last_result",
    result,
)

        return {
            "success": True,
            "intent": self._serialize_intent(intent),
            "result": result,
            "error": None,
        }

    def _error_response(
        self,
        error_code: str,
        message: str,
        intent: ResolvedIntent | None = None,
    ) -> dict[str, Any]:
        """Create a consistent execution error response."""

        return {
            "success": False,
            "intent": (
                self._serialize_intent(intent)
                if intent is not None
                else None
            ),
            "result": None,
            "error": {
                "code": error_code,
                "message": message,
            },
        }

    def _serialize_intent(
        self,
        intent: ResolvedIntent,
    ) -> dict[str, Any]:
        """Convert a resolved intent into JSON-safe data."""

        return {
            "capability": intent.capability,
            "action": intent.action,
            "parameters": intent.parameters,
            "confidence": intent.confidence,
        }