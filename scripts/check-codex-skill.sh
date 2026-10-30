#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="${1:-korean-humanizer}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "$SKILL_NAME" in
  korean-humanizer) SOURCE_ROOT="$REPO_ROOT" ;;
  korean-humanizer-deep) SOURCE_ROOT="$REPO_ROOT/skills/$SKILL_NAME" ;;
  *) echo "usage: $0 [korean-humanizer|korean-humanizer-deep]" >&2; exit 1 ;;
esac
ACTIVE_SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.agents/skills}"
ACTIVE_LINK="$ACTIVE_SKILLS_DIR/$SKILL_NAME"

fail() { echo "error: $*" >&2; exit 1; }
[[ -f "$SOURCE_ROOT/SKILL.md" ]] || fail "SKILL.md not found at $SOURCE_ROOT"
[[ -f "$ACTIVE_LINK/SKILL.md" ]] || fail "$ACTIVE_LINK/SKILL.md does not exist"
resolved="$(cd "$ACTIVE_LINK" && pwd -P)"
source_resolved="$(cd "$SOURCE_ROOT" && pwd -P)"
[[ "$resolved" == "$source_resolved" ]] || fail "$ACTIVE_LINK resolves to $resolved, expected $source_resolved"
sed -n '1,8p' "$ACTIVE_LINK/SKILL.md" | grep -qx "name: $SKILL_NAME" || fail "frontmatter is missing name: $SKILL_NAME"
active_resolved="$(cd "$ACTIVE_SKILLS_DIR" && pwd -P)"
for skills_dir in "$HOME/.agents/skills" "${CODEX_HOME:-$HOME/.codex}/skills" "$HOME/.codex/skills"; do
  [[ -d "$skills_dir" ]] || continue
  skills_dir="$(cd "$skills_dir" && pwd -P)"
  if [[ "$skills_dir" != "$active_resolved" ]]; then
    duplicate="$skills_dir/$SKILL_NAME"
    [[ ! -e "$duplicate" && ! -L "$duplicate" ]] || fail "duplicate install remains at $duplicate"
  fi
done
echo "ok: $SKILL_NAME has one development install at $ACTIVE_LINK -> $resolved"
