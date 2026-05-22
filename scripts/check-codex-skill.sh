#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="korean-humanizer"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ACTIVE_SKILLS_DIR="${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"
ACTIVE_LINK="$ACTIVE_SKILLS_DIR/$SKILL_NAME"
LEGACY_LINK="$HOME/.codex/skills/$SKILL_NAME"

fail() {
  echo "error: $*" >&2
  exit 1
}

[[ -f "$REPO_ROOT/SKILL.md" ]] || fail "SKILL.md not found at $REPO_ROOT"
[[ -e "$ACTIVE_LINK" ]] || fail "$ACTIVE_LINK does not exist"
[[ -f "$ACTIVE_LINK/SKILL.md" ]] || fail "$ACTIVE_LINK/SKILL.md does not exist"

resolved="$(cd "$ACTIVE_LINK" && pwd -P)"
repo_resolved="$(cd "$REPO_ROOT" && pwd -P)"

[[ "$resolved" == "$repo_resolved" ]] || fail "$ACTIVE_LINK resolves to $resolved, expected $repo_resolved"

if ! sed -n '1,8p' "$ACTIVE_LINK/SKILL.md" | rg -q '^name: korean-humanizer$'; then
  fail "$ACTIVE_LINK/SKILL.md frontmatter is missing name: korean-humanizer"
fi

echo "ok: $SKILL_NAME is installed at $ACTIVE_LINK"
echo "ok: active install resolves to $repo_resolved"

if [[ "$LEGACY_LINK" != "$ACTIVE_LINK" ]]; then
  [[ -e "$LEGACY_LINK" ]] || fail "$LEGACY_LINK does not exist"
  legacy_resolved="$(cd "$LEGACY_LINK" && pwd -P)"
  [[ "$legacy_resolved" == "$repo_resolved" ]] || fail "$LEGACY_LINK resolves to $legacy_resolved, expected $repo_resolved"
  echo "ok: legacy install also resolves to $repo_resolved"
fi
