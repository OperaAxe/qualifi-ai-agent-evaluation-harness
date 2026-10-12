# Manual QA walkthrough: evaluating an AI agent

The goal is to test behavior, not to admire a confident final sentence.

## 1. Give the agent a concrete task

“Create a note titled `Release candidate checklist` with ID `note-1`.”

Point out that the expected action and expected result are explicit. If the task is vague, the evaluation is measuring ambiguity instead of agent quality.

## 2. Watch the action

The reference agent should choose `create_note` and provide the title and ID. The harness records that tool call.

Ask: **Did the agent choose a permitted tool, and did it supply the information the tool needs?**

## 3. Check the result independently

Open the environment state. Confirm the note exists with the expected title. The final text “created successfully” is not used as the only proof.

## 4. Show the four deliberate failures

Run the fault dataset and explain each failure:

- The wrong-tool agent tries to delete a protected note.
- The wrong-arguments agent omits the title.
- The false-claim agent says it succeeded without changing state.
- The looping agent repeats a failed lookup beyond the step budget.

The useful part is that the report names the failed dimension rather than only returning one mysterious score.

## 5. Show regression detection

Run the clean dataset once, save it as the baseline, then run the same cases with the wrong-arguments agent. The comparison should report the cases that changed from pass to fail.

## 6. Show the limits

“This repository proves that the graders and isolation work with local fixtures. It does not benchmark a commercial model, measure provider cost, or claim that a model is safe in production.”

## The line to use in an interview

“I evaluate what the agent actually changed, not just what it said. I keep each run isolated, check the tool transcript, inspect state, and compare with a baseline so a previously working behavior cannot quietly regress.”
