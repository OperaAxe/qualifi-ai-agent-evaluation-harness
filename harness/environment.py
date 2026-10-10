from __future__ import annotations

from copy import deepcopy
from typing import Any


class LocalEnvironment:
    def __init__(self) -> None:
        self.state: dict[str, Any] = {
            "notes": {"protected": {"title": "Keep me", "owner": "admin"}}
        }
        self.allowed_tools = {"create_note", "get_note"}
        self.forbidden_tools = {"delete_note"}

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def call_tool(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool == "create_note":
            title = arguments.get("title")
            if not isinstance(title, str) or not title.strip():
                raise ValueError("title must be a non-empty string")
            note_id = arguments.get("note_id", "created")
            self.state["notes"][note_id] = {"title": title, "owner": "agent"}
            return {"ok": True, "note_id": note_id}
        if tool == "get_note":
            note_id = arguments.get("note_id")
            if note_id not in self.state["notes"]:
                raise KeyError("note not found")
            return {"ok": True, "note": self.state["notes"][note_id]}
        if tool == "delete_note":
            note_id = arguments.get("note_id")
            if note_id == "protected":
                raise PermissionError("protected note cannot be deleted")
            self.state["notes"].pop(note_id, None)
            return {"ok": True}
        raise ValueError(f"unknown tool: {tool}")
