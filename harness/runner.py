from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .agents import ADAPTERS
from .environment import LocalEnvironment
from .grading import grade


def load_cases(path: str | Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def evaluate(cases: list[dict[str, Any]], agent_name: str | None = None) -> dict[str, Any]:
    results = []
    for case in cases:
        selected = agent_name or case.get("agent", "good")
        agent = ADAPTERS[selected]
        environment = LocalEnvironment()
        before = environment.snapshot()
        started = time.perf_counter()
        record = agent.run(case, environment)
        record.duration_ms = round((time.perf_counter() - started) * 1000, 3)
        after = environment.snapshot()
        results.append(
            {"case": case, "run": record.to_dict(), "grading": grade(case, record, before, after)}
        )
    passed = sum(item["grading"]["passed"] for item in results)
    return {
        "summary": {"total": len(results), "passed": passed, "failed": len(results) - passed},
        "results": results,
    }


def compare_baseline(current: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    changes = []
    old = {item["case"]["id"]: item["grading"]["passed"] for item in baseline["results"]}
    for item in current["results"]:
        case_id = item["case"]["id"]
        if case_id in old and old[case_id] and not item["grading"]["passed"]:
            changes.append({"case_id": case_id, "change": "regression"})
    return {"regression": bool(changes), "changes": changes}


def write_reports(result: dict[str, Any], json_path: str, markdown_path: str) -> None:
    Path(json_path).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# QualiFi AI-agent evaluation report",
        "",
        f"**Passed:** {result['summary']['passed']} / {result['summary']['total']}",
        "",
        "## Cases",
    ]
    for item in result["results"]:
        status = "PASS" if item["grading"]["passed"] else "FAIL"
        failed = ", ".join(item["grading"]["failed_checks"]) or "none"
        lines.append(
            f"- **{status}** `{item['case']['id']}` via `{item['run']['agent_name']}` — failed checks: {failed}"
        )
    lines += [
        "",
        "Metrics marked unavailable are not silently replaced with zero. Local fixture timings are not model latency.",
    ]
    Path(markdown_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
