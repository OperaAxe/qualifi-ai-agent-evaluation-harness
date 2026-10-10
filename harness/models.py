from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    tool: str
    arguments: dict[str, Any]
    result: dict[str, Any] | None = None
    error: str | None = None


@dataclass
class RunRecord:
    task_id: str
    agent_name: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    final_claim: str = ""
    task_completed: bool = False
    duration_ms: float | None = None
    token_usage: int | None = None
    estimated_cost: float | None = None
    metric_source: str = "unavailable"
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent_name": self.agent_name,
            "tool_calls": [call.__dict__ for call in self.tool_calls],
            "final_claim": self.final_claim,
            "task_completed": self.task_completed,
            "duration_ms": self.duration_ms,
            "token_usage": self.token_usage,
            "estimated_cost": self.estimated_cost,
            "metric_source": self.metric_source,
            "errors": self.errors,
        }
