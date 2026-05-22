#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="korean-humanizer"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -f "$REPO_ROOT/SKILL.md" ]]; then
  echo "error: SKILL.md not found at $REPO_ROOT" >&2
  exit 1
fi

ACTIVE_SKILLS_DIR="${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"
LEGACY_SKILLS_DIR="$HOME/.codex/skills"

install_link() {
  local skills_dir="$1"
  local target="$skills_dir/$SKILL_NAME"

  mkdir -p "$skills_dir"

  if [[ -L "$target" ]]; then
    rm "$target"
  elif [[ -e "$target" ]]; then
    local backup="$target.backup.$(date +%Y%m%d%H%M%S)"
    mv "$target" "$backup"
    echo "moved existing install to $backup"
  fi

  ln -s "$REPO_ROOT" "$target"
  echo "linked $target -> $REPO_ROOT"
}

install_link "$ACTIVE_SKILLS_DIR"

if [[ "$LEGACY_SKILLS_DIR" != "$ACTIVE_SKILLS_DIR" ]]; then
  install_link "$LEGACY_SKILLS_DIR"
fi

"$REPO_ROOT/scripts/check-codex-skill.sh"
