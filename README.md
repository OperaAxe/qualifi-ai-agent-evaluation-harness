# QualiFi AI-Agent Evaluation Harness

[![CI](https://github.com/OperaAxe/qualifi-ai-agent-evaluation-harness/actions/workflows/ci.yml/badge.svg)](https://github.com/OperaAxe/qualifi-ai-agent-evaluation-harness/actions/workflows/ci.yml)

A small evaluation harness for checking whether a tool-using agent actually completed a task. It checks the actions an agent took and the state left behind, rather than treating a confident final message as proof.

The agents and environment are deterministic local fixtures. This makes the examples repeatable, but it does **not** measure the performance of GPT, Claude, Gemini, or another hosted model.

## What it checks

- **Tool choice:** did the agent use an allowed tool?
- **Arguments:** did it provide the required inputs?
- **Final state:** does the requested note or other result actually exist?
- **State integrity:** did it touch protected data?
- **Recovery:** did it handle a failed action or keep looping?
- **Regression:** did a previously passing case stop passing?

The sample task asks an agent to create a note titled “Release candidate checklist.” The grader checks the note and verifies that protected state remains unchanged.

## Run locally

Requires Python 3.13.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest
```

Run the clean reference cases and write a report:

```bash
qa-eval run --json-out reports/evaluation.json --md-out reports/evaluation.md
```

Run the deliberately faulty agents:

```bash
qa-eval run --dataset data/fault_cases.jsonl --json-out reports/faults.json --md-out reports/faults.md
```

The faulty dataset is supposed to expose failures, so a non-zero exit is expected when those cases are detected.

## Useful files

- `data/cases.jsonl` — clean reference cases
- `data/fault_cases.jsonl` — agents with deliberate mistakes
- `harness/grading.py` — grading checks
- `harness/runner.py` — execution and baseline comparison
- `docs/grading-rules.md` — pass/fail rules
- `docs/evaluation-methodology.md` — how the cases are designed

## Current limits

**Status: in development.** The harness does not call external model providers, collect real token usage, or measure provider latency and cost. Those fields remain unavailable unless they are actually measured. The fixtures demonstrate how the evaluation works; they are not a commercial-model benchmark.
