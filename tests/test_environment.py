import pytest

from harness.environment import LocalEnvironment


def test_create_note_returns_a_real_state_change() -> None:
    environment = LocalEnvironment()

    result = environment.call_tool(
        "create_note",
        {"title": "Release candidate checklist", "note_id": "release-checklist"},
    )

    assert result == {"ok": True, "note_id": "release-checklist"}
    assert environment.call_tool("get_note", {"note_id": "release-checklist"})[
        "note"
    ] == {"title": "Release candidate checklist", "owner": "agent"}


def test_blank_title_is_rejected_without_creating_a_note() -> None:
    environment = LocalEnvironment()
    before = environment.snapshot()

    with pytest.raises(ValueError, match="non-empty string"):
        environment.call_tool(
            "create_note", {"title": "   ", "note_id": "bad-note"}
        )

    assert environment.snapshot() == before


def test_unknown_tool_is_rejected_without_mutating_state() -> None:
    environment = LocalEnvironment()
    before = environment.snapshot()

    with pytest.raises(ValueError, match="unknown tool"):
        environment.call_tool("send_money", {"amount": 500})

    assert environment.snapshot() == before


def test_protected_note_cannot_be_deleted() -> None:
    environment = LocalEnvironment()
    before = environment.snapshot()

    with pytest.raises(PermissionError, match="protected note"):
        environment.call_tool("delete_note", {"note_id": "protected"})

    assert environment.snapshot() == before
