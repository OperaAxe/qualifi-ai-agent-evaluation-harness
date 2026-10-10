# Evaluation methodology

Each JSONL case defines an input, expected note ID, and maximum step budget. The runner creates a fresh local environment for every case, runs one adapter, captures the tool transcript and final state, and passes both to independent graders.

The clean dataset is a regression suite: a known-good reference adapter should pass. The fault dataset contains deliberately faulty fixtures that should fail specific graders. This demonstrates grader sensitivity without claiming anything about a real model.

The design follows current agent-evaluation guidance: prefer objective outcome and tool-call checks where possible, isolate trials, write unambiguous cases, and use regression comparisons to catch pass-to-fail changes.
