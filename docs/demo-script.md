# Demo script

1. Show `data/cases.jsonl` and explain the task contract.
2. Run `qa-eval run` and open the Markdown report showing the reference agent passing.
3. Run the fault dataset and show the distinct failed checks for wrong tool, wrong arguments, false claim, and looping behavior.
4. Open `harness/grading.py` and map each check to a concrete state or transcript oracle.
5. Run the baseline comparison with the wrong-arguments adapter and show the regression report.
6. Explain that no real model or provider was evaluated.
