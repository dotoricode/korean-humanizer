# review

## When to use
Review changes, risks, or a PR/diff.

## Ask first
- What should be reviewed?
- What is the base or expected behavior?
- Which risks matter most?

## Plan
1. Inspect changed files.
2. Prioritize correctness, security, data, and UX risks.
3. Check tests or evidence.
4. Write actionable findings only.
5. Avoid unsupported style noise.

## Checks
- Use only the context needed for this task.
- Do not repeat questions already answered in `.tiny/current/answers.md`.
- Do not store raw logs, full diffs, secrets, or one-off state in memory.

## Done means
- Findings are reproducible or evidence-based.
- Severity is clear.
- No speculative blockers.

## If it fails, Tink back
Return to the last safe step. State what failed, the last safe point, and the next single action.
