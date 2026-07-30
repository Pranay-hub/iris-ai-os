from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class IntentResolutionError(Exception):
    """Raised when a planner response cannot be resolved into an executable intent."""


@dataclass(frozen=True)
class ResolvedIntent:
    """Normalized executable intent produced from a planner response."""

    capability: str
    action: str
    parameters: dict[str, Any]
    confidence: float = 1.0


class IntentResolver:
    """Validates and normalizes planner output before execution."""

    REQUIRED_FIELDS = ("capability", "action")

    def resolve(self, planner_output: dict[str, Any]) -> ResolvedIntent:
        """
        Convert raw planner output into a validated ResolvedIntent.

        Expected planner format:

        {
            "capability": "system",
            "action": "get_info",
            "parameters": {},
            "confidence": 0.95
        }
        """

        if not isinstance(planner_output, dict):
            raise IntentResolutionError(
                "Planner output must be a dictionary."
            )

        self._validate_required_fields(planner_output)

        capability = self._normalize_identifier(
            planner_output["capability"],
            field_name="capability",
        )

        action = self._normalize_identifier(
            planner_output["action"],
            field_name="action",
        )

        parameters = planner_output.get("parameters", {})

        if parameters is None:
            parameters = {}

        if not isinstance(parameters, dict):
            raise IntentResolutionError(
                "Intent parameters must be a dictionary."
            )

        confidence = self._normalize_confidence(
            planner_output.get("confidence", 1.0)
        )

        return ResolvedIntent(
            capability=capability,
            action=action,
            parameters=parameters,
            confidence=confidence,
        )

    def _validate_required_fields(
        self,
        planner_output: dict[str, Any],
    ) -> None:
        """Ensure all required planner fields are present."""

        missing_fields = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in planner_output
        ]

        if missing_fields:
            fields = ", ".join(missing_fields)

            raise IntentResolutionError(
                f"Planner output is missing required fields: {fields}."
            )

    def _normalize_identifier(
        self,
        value: Any,
        field_name: str,
    ) -> str:
        """Normalize capability and action identifiers."""

        if not isinstance(value, str):
            raise IntentResolutionError(
                f"Intent field '{field_name}' must be a string."
            )

        normalized = value.strip().lower().replace(" ", "_")

        if not normalized:
            raise IntentResolutionError(
                f"Intent field '{field_name}' cannot be empty."
            )

        return normalized

    def _normalize_confidence(self, value: Any) -> float:
        """Validate and normalize intent confidence."""

        if not isinstance(value, (int, float)):
            raise IntentResolutionError(
                "Intent confidence must be a number."
            )

        confidence = float(value)

        if not 0.0 <= confidence <= 1.0:
            raise IntentResolutionError(
                "Intent confidence must be between 0.0 and 1.0."
            )

        return confidence