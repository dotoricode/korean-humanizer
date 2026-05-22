# Agent Instructions

This repository is the source of truth for the `korean-humanizer` Codex skill.

- Do not install this skill by copying files into `~/.codex/skills` manually.
- Use `scripts/install-codex-skill.sh`; it links the repo into the active `$CODEX_SKILLS_DIR` and the legacy `~/.codex/skills` path.
- Use `scripts/check-codex-skill.sh` after changing install behavior or `SKILL.md`.
- The active Codex home on this machine may be `~/.codex-personal`, so `~/.codex/skills` alone is not sufficient.
