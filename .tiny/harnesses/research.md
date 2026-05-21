# research

## When to use
Compare options, read docs, or collect grounded facts.

## Ask first
- What decision should this support?
- Which sources or constraints matter?
- How current does the answer need to be?

## Plan
1. Define the question.
2. Collect sources.
3. Separate facts from guesses.
4. Summarize tradeoffs.
5. Recommend the next action.

## Checks
- Use only the context needed for this task.
- Do not repeat questions already answered in `.tiny/current/answers.md`.
- Do not store raw logs, full diffs, secrets, or one-off state in memory.

## Done means
- Sources are linked.
- Uncertainty is labeled.
- Recommendation follows from evidence.

## If it fails, Tink back
Return to the last safe step. State what failed, the last safe point, and the next single action.
