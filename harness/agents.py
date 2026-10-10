from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .environment import LocalEnvironment
from .models import RunRecord, ToolCall


class AgentAdapter(ABC):
    name = "adapter"

    @abstractmethod
    def run(self, case: dict[str, Any], environment: LocalEnvironment) -> RunRecord:
        raise NotImplementedError


class GoodAgent(AgentAdapter):
    name = "good"

    def run(self, case: dict[str, Any], environment: LocalEnvironment) -> RunRecord:
        record = RunRecord(case["id"], self.name)
        call = ToolCall(
            "create_note", {"title": case["input"]["title"], "note_id": case["expected_note_id"]}
        )
        try:
            call.result = environment.call_tool(call.tool, call.arguments)
            record.task_completed = True
            record.final_claim = "Created the requested note."
        except (KeyError, PermissionError, ValueError) as exc:
            call.error = str(exc)
            record.errors.append(str(exc))
        record.tool_calls.append(call)
        return record


class WrongToolAgent(AgentAdapter):
    name = "wrong_tool"

    def run(self, case: dict[str, Any], environment: LocalEnvironment) -> RunRecord:
        record = RunRecord(case["id"], self.name)
        call = ToolCall("delete_note", {"note_id": "protected"})
        try:
            call.result = environment.call_tool(call.tool, call.arguments)
        except (KeyError, PermissionError, ValueError) as exc:
            call.error = str(exc)
            record.errors.append(str(exc))
        record.tool_calls.append(call)
        record.final_claim = "The requested operation is complete."
        return record


class WrongArgumentsAgent(AgentAdapter):
    name = "wrong_arguments"

    def run(self, case: dict[str, Any], environment: LocalEnvironment) -> RunRecord:
        record = RunRecord(case["id"], self.name)
        call = ToolCall("create_note", {"note_id": case["expected_note_id"]})
        try:
            call.result = environment.call_tool(call.tool, call.arguments)
        except (KeyError, PermissionError, ValueError) as exc:
            call.error = str(exc)
            record.errors.append(str(exc))
        record.tool_calls.append(call)
        return record


class FalseClaimAgent(AgentAdapter):
    name = "false_claim"

    def run(self, case: dict[str, Any], environment: LocalEnvironment) -> RunRecord:
        return RunRecord(
            case["id"], self.name, final_claim="Created the note successfully.", task_completed=True
        )


class LoopingAgent(AgentAdapter):
    name = "looping"

    def run(self, case: dict[str, Any], environment: LocalEnvironment) -> RunRecord:
        record = RunRecord(case["id"], self.name)
        for _ in range(case.get("max_steps", 3) + 2):
            record.tool_calls.append(
                ToolCall("get_note", {"note_id": "missing"}, error="note not found")
            )
        record.errors.append("step budget exceeded")
        return record


ADAPTERS = {
    agent.name: agent
    for agent in (
        GoodAgent(),
        WrongToolAgent(),
        WrongArgumentsAgent(),
        FalseClaimAgent(),
        LoopingAgent(),
    )
}
