# bug-fix

## When to use
Something is broken and needs a minimal fix.

## Ask first
- How can the bug be reproduced?
- What is expected vs actual?
- Is there a failing test, log, or screenshot?

## Plan
1. Reproduce or explain why reproduction is not possible.
2. Identify the likely root cause.
3. Make the smallest fix.
4. Run a regression check.
5. Report the evidence.

## Checks
- Use only the context needed for this task.
- Do not repeat questions already answered in `.tiny/current/answers.md`.
- Do not store raw logs, full diffs, secrets, or one-off state in memory.

## Done means
- Bug no longer reproduces or risk is stated.
- Root cause is explained.
- Regression check is complete.

## If it fails, Tink back
Return to the last safe step. State what failed, the last safe point, and the next single action.
