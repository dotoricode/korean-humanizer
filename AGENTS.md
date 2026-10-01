# Agent Instructions

This repository is the source of truth for the `korean-humanizer` Codex skill.

- Do not install this skill by copying files into `~/.codex/skills` manually.
- Use `scripts/install-codex-skill.sh`; it links the repo into the active `$CODEX_SKILLS_DIR` and the legacy `~/.codex/skills` path.
- Use `scripts/check-codex-skill.sh` after changing install behavior or `SKILL.md`.
- The active Codex home on this machine may be `~/.codex-personal`, so `~/.codex/skills` alone is not sufficient.

## Project terminology

- `korean-humanizer` is a Korean writing skill and prompt that preserves meaning while editing expressions. Editing rules live in `SKILL.md`; do not duplicate them here.
- Socialistic/Tinkerland is a third-party community demo. Describe it as externally operated, and disclose that the external operator processes submitted text.
- Current documentation starts at `docs/README.md`. Files under `docs/archive/` are historical records, not current instructions.
