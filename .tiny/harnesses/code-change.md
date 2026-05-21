# code-change

## When to use
Add, change, or refactor code with a clear scope.

## Ask first
- What is the target behavior?
- What files or areas are in scope?
- What must not change?

## Plan
1. Inspect before editing.
2. Make the smallest useful change.
3. Avoid unrelated cleanup.
4. Run the relevant check.
5. Report changed files and evidence.

## Checks
- Use only the context needed for this task.
- Do not repeat questions already answered in `.tiny/current/answers.md`.
- Do not store raw logs, full diffs, secrets, or one-off state in memory.

## Done means
- Only related files changed.
- Tests/build pass, or reason not run is stated.
- Diff evidence is available.

## If it fails, Tink back
Return to the last safe step. State what failed, the last safe point, and the next single action.
