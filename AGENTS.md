# Agent Instructions

This repository is the source of truth for the `korean-humanizer` Codex skill.

- End-user installation uses the Skills CLI command documented in `README.md`.
- For local development on this machine, use `scripts/install-codex-skill.sh [korean-humanizer|korean-humanizer-deep]` to link the selected source into `$CODEX_SKILLS_DIR` (default `~/.agents/skills`). Keep that link pointing at the repository. The installer backs up duplicate account-specific and legacy installs outside skill search roots so each name appears once.
- For a repository-linked development install, use `scripts/check-codex-skill.sh` after changing install behavior or `SKILL.md`. For a copied end-user install, compare every installed runtime file with the package manifest; the development checker requires repository links.

## Project terminology

- `korean-humanizer` is a Korean writing skill and prompt that preserves meaning while editing expressions. Editing rules live in `SKILL.md`; do not duplicate them here.
- `korean-humanizer-deep` is an independent skill for revising tone, structure, and verified facts using document context. Its editing rules live in `skills/korean-humanizer-deep/SKILL.md`.
- Socialistic/Tinkerland is a third-party community demo. Describe it as externally operated, and disclose that the external operator processes submitted text.
- Current documentation starts at `docs/README.md`. Files under `docs/archive/` are historical records, not current instructions.
