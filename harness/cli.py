from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runner import compare_baseline, evaluate, load_cases, write_reports

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic local AI-agent evaluations.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run a case dataset")
    run.add_argument("--dataset", default=str(ROOT / "data/cases.jsonl"))
    run.add_argument(
        "--agent",
        default=None,
        choices=["good", "wrong_tool", "wrong_arguments", "false_claim", "looping"],
    )
    run.add_argument("--json-out", default="reports/evaluation.json")
    run.add_argument("--md-out", default="reports/evaluation.md")
    run.add_argument("--baseline", default=None)
    args = parser.parse_args()
    if args.command == "run":
        result = evaluate(load_cases(args.dataset), args.agent)
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        write_reports(result, args.json_out, args.md_out)
        if args.baseline:
            baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
            comparison = compare_baseline(result, baseline)
            regression_path = Path(args.json_out).with_name("regression.json")
            regression_path.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
            if comparison["regression"]:
                return 1
        return 0 if result["summary"]["failed"] == 0 else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
