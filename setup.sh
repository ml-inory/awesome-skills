#!/bin/bash
set -e
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

find "$REPO_DIR" -mindepth 3 -maxdepth 3 -type d -path "*/skills/*" | while read -r skill; do
    name="$(basename "$skill")"
    ln -sfn "$skill" "$SKILLS_DIR/$name"
    echo "Linked: $name"
done
