from harness.runner import compare_baseline, evaluate, load_cases


def test_baseline_comparison_flags_pass_to_fail_regression():
    baseline = evaluate(load_cases("data/cases.jsonl"))
    current = evaluate(load_cases("data/cases.jsonl"), agent_name="wrong_arguments")
    comparison = compare_baseline(current, baseline)
    assert comparison["regression"] is True
    assert {item["case_id"] for item in comparison["changes"]} == {
        "create-note-basic",
        "create-note-second",
    }
