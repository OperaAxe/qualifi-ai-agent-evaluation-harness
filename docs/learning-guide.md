# Learning guide

## Important choices

The harness grades outcomes and state, not only the agent's final text. Each case gets a fresh environment so one trial cannot benefit from another trial's state. Independent graders make the failure reason visible.

## Difficult scenarios

1. A tool is selected that is not allowed: the authorization and selection graders catch it.
2. Required arguments are omitted: the argument grader catches the invalid call and task failure.
3. The agent claims success without changing state: outcome verification catches the false claim.
4. The agent repeats calls: budget and recovery graders catch non-progress.
5. A known-good case later fails: baseline comparison reports a regression.

## Interview questions

- Why not use one aggregate score? — Individual dimensions explain what failed and prevent a high score from hiding a critical authorization error.
- Why keep fault fixtures? — They validate the graders themselves and provide reproducible examples.
- Why are missing metrics not zero? — Zero would falsely imply measured usage or cost.
- What is the difference between capability and regression evals? — Capability tests what an agent can learn to do; regression tests protect behavior that already worked.
