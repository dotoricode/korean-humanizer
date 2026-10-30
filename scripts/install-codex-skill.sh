#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="${1:-korean-humanizer}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "$SKILL_NAME" in
  korean-humanizer) SOURCE_ROOT="$REPO_ROOT" ;;
  korean-humanizer-deep) SOURCE_ROOT="$REPO_ROOT/skills/$SKILL_NAME" ;;
  *) echo "usage: $0 [korean-humanizer|korean-humanizer-deep]" >&2; exit 1 ;;
esac
[[ -f "$SOURCE_ROOT/SKILL.md" ]] || { echo "error: SKILL.md not found at $SOURCE_ROOT" >&2; exit 1; }
source_resolved="$(cd "$SOURCE_ROOT" && pwd -P)"

ACTIVE_SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.agents/skills}"
BACKUP_ROOT="$HOME/.local/share/korean-humanizer/backups"

# Keep backups outside every skills search root, where they cannot become duplicate entries.
backup_install() {
  local target="$1"
  local backup
  [[ -e "$target" || -L "$target" ]] || return 0
  if [[ -d "$target" && ! -L "$target" ]]; then
    local target_resolved
    target_resolved="$(cd "$target" && pwd -P)"
    if [[ "$source_resolved" == "$target_resolved" || "$source_resolved" == "$target_resolved/"* ]]; then
      echo "error: refusing to move source checkout inside $target" >&2
      return 1
    fi
  fi
  mkdir -p "$BACKUP_ROOT"
  backup="$(mktemp -d "$BACKUP_ROOT/$SKILL_NAME.XXXXXXXX")"
  mv "$target" "$backup/$SKILL_NAME"
  echo "backed up $target -> $backup/$SKILL_NAME"
}

mkdir -p "$ACTIVE_SKILLS_DIR"
ACTIVE_SKILLS_DIR="$(cd "$ACTIVE_SKILLS_DIR" && pwd -P)"
target="$ACTIVE_SKILLS_DIR/$SKILL_NAME"
if [[ -d "$target" && "$(cd "$target" && pwd -P)" == "$(cd "$SOURCE_ROOT" && pwd -P)" ]]; then
  echo "kept existing install at $target"
else
  backup_install "$target"
  ln -s "$SOURCE_ROOT" "$target"
  echo "linked $target -> $SOURCE_ROOT"
fi

# Retire old account-specific and legacy installs rather than creating more search entries.
for skills_dir in "$HOME/.agents/skills" "${CODEX_HOME:-$HOME/.codex}/skills" "$HOME/.codex/skills"; do
  [[ -d "$skills_dir" ]] || continue
  skills_dir="$(cd "$skills_dir" && pwd -P)"
  if [[ "$skills_dir" != "$ACTIVE_SKILLS_DIR" ]]; then
    # An existing source checkout is the same skill, not a disposable installed copy.
    if [[ -d "$skills_dir/$SKILL_NAME" && ! -L "$skills_dir/$SKILL_NAME" && "$(cd "$skills_dir/$SKILL_NAME" && pwd -P)" == "$source_resolved" ]]; then
      echo "kept source checkout at $skills_dir/$SKILL_NAME"
      continue
    fi
    backup_install "$skills_dir/$SKILL_NAME"
  fi
done

"$REPO_ROOT/scripts/check-codex-skill.sh" "$SKILL_NAME"
