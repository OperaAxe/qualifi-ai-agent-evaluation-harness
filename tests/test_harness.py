import json

from harness.agents import ADAPTERS
from harness.runner import evaluate, load_cases


def test_reference_agent_passes_regression_cases():
    result = evaluate(load_cases("data/cases.jsonl"))
    assert result["summary"] == {"total": 2, "passed": 2, "failed": 0}


def test_fault_fixtures_are_detected_by_independent_graders():
    result = evaluate(load_cases("data/fault_cases.jsonl"))
    assert result["summary"]["failed"] == 4
    by_id = {item["case"]["id"]: item for item in result["results"]}
    assert "tool_selection" in by_id["fault-wrong-tool"]["grading"]["failed_checks"]
    assert "tool_arguments" in by_id["fault-wrong-arguments"]["grading"]["failed_checks"]
    assert "task_success" in by_id["fault-false-claim"]["grading"]["failed_checks"]
    assert "execution_budget" in by_id["fault-loop"]["grading"]["failed_checks"]


def test_all_adapters_have_a_stable_name():
    assert set(ADAPTERS) == {"good", "wrong_tool", "wrong_arguments", "false_claim", "looping"}


def test_report_can_be_serialized():
    result = evaluate(load_cases("data/cases.jsonl"))
    json.dumps(result)
