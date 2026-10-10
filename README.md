# QualiFi AI-Agent Evaluation Harness

A **local, model-independent evaluation harness** for testing whether an agent selects tools correctly, supplies valid arguments, respects authorization, changes the intended state, recovers from failures, stays within a step budget, and regresses against a saved baseline.

The default workflow uses a deterministic local reference agent. The faulty agents are test fixtures; they are not real model evaluations and their results must not be presented as benchmark scores.

## Why it matters

An agent saying “done” is not evidence that the task happened. This harness grades the environment after the run, checks the tool transcript, and compares current behavior with a baseline. It uses deterministic code-based graders by default, keeping the workflow free and reproducible.

## Setup

### Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Bash

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## CLI

Run the clean regression suite:

```bash
qa-eval run --json-out reports/evaluation.json --md-out reports/evaluation.md
```

Compare it to the saved baseline:

```bash
qa-eval run --json-out reports/regression.json --md-out reports/regression.md --baseline baseline.json
```

Run the deliberately faulty fixtures. A non-zero exit code is expected because the graders should detect the failures:

```bash
qa-eval run --dataset data/fault_cases.jsonl --json-out reports/faults.json --md-out reports/faults.md
```

The CLI writes JSON and Markdown reports. It returns non-zero when configured critical checks fail.

## Architecture

- `harness/models.py` — run and tool-call records
- `harness/environment.py` — isolated local state and tool interface
- `harness/agents.py` — adapter contract, deterministic reference agent, and faulty fixtures
- `harness/grading.py` — independent code-based graders
- `harness/runner.py` — isolated case execution and baseline comparison
- `harness/cli.py` — command-line interface
- `data/` — version-controlled regression and fault datasets

Each case starts with a clean environment. Metrics that are not supplied by an adapter remain unavailable; local fixture duration is not model latency and no cost is invented.

## Grading categories

The harness checks task success, tool selection, tool arguments, authorization, state integrity, failure recovery, and execution budgets. The report exposes each case and failed dimension rather than hiding everything in one score.

## Limitations

This repository does not benchmark a real model, measure provider token usage, or establish production performance. The local tools and agents are deliberately small. A provider adapter would need to implement the same `AgentAdapter` contract and document actual runs before any model-specific claim could be made. Model-based or human graders may be added later for tasks where deterministic checks are insufficient.

See `docs/evaluation-methodology.md`, `docs/grading-rules.md`, `docs/limitations.md`, `docs/learning-guide.md`, and `docs/demo-script.md`.
