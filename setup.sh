#!/bin/bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: ./setup.sh [--claude|--codex]

Default target is Claude Code:
  --claude  install into ~/.claude/{skills,workflows}
  --codex   install into ${CODEX_HOME:-~/.codex}/{skills,workflows}
EOF
}

target="${1:---codex}"
case "$target" in
    --claude)
        TARGET_ROOT="$HOME/.claude"
        ;;
    --codex)
        TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}"
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac

SKILLS_DIR="$TARGET_ROOT/skills"
WORKFLOWS_DIR="$TARGET_ROOT/workflows"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$SKILLS_DIR" "$WORKFLOWS_DIR"

find "$REPO_DIR" -mindepth 4 -maxdepth 4 -type f -path "*/skills/*/SKILL.md" | sort | while IFS= read -r skill_file; do
    skill_dir="$(dirname "$skill_file")"
    name="$(basename "$skill_dir")"
    ln -sfn "$skill_dir" "$SKILLS_DIR/$name"
    echo "Linked skill: $name"
done

find "$REPO_DIR" -mindepth 3 -maxdepth 3 -type f \( -name "*.yaml" -o -name "*.yml" \) -path "*/workflows/*" | sort | while IFS= read -r workflow_file; do
    name="$(basename "$workflow_file")"
    ln -sfn "$workflow_file" "$WORKFLOWS_DIR/$name"
    echo "Linked workflow: $name"
done

# grill-me is a top-level skill (not inside skills/ subdirectory)
if [ -f "$REPO_DIR/grill-me/SKILL.md" ]; then
    ln -sfn "$REPO_DIR/grill-me" "$SKILLS_DIR/grill-me"
    echo "Linked skill: grill-me"
fi
