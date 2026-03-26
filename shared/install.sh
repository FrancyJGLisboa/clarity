#!/bin/sh
# Unified installer for the clarity pipeline.
# Installs /clarity, /agent-skill-creator, and /linear-walkthrough together.
#
# Usage:
#   ./shared/install.sh                    # Auto-detect platform
#   ./shared/install.sh --dry-run          # Preview without changes
#   ./shared/install.sh --uninstall        # Remove symlinks
#
# This script is POSIX-compatible (bash, dash, zsh, ash).

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DRY_RUN=0
UNINSTALL=0

for arg in "$@"; do
    case "$arg" in
        --dry-run)  DRY_RUN=1 ;;
        --uninstall) UNINSTALL=1 ;;
        --help|-h)
            echo "Usage: $0 [--dry-run] [--uninstall]"
            echo ""
            echo "Installs the clarity pipeline (clarity + agent-skill-creator + linear-walkthrough)"
            echo "to all detected agent platforms."
            exit 0
            ;;
    esac
done

# Platform detection — check which tools have skills directories
detect_platforms() {
    platforms=""

    # Claude Code (also works for VS Code Copilot)
    if [ -d "$HOME/.claude" ]; then
        platforms="$platforms claude"
    fi

    # Copilot CLI
    if [ -d "$HOME/.copilot" ]; then
        platforms="$platforms copilot"
    fi

    # Universal path (Codex CLI, Gemini CLI, Kiro, Antigravity)
    if [ -d "$HOME/.agents" ] || command -v codex >/dev/null 2>&1 || command -v gemini >/dev/null 2>&1; then
        platforms="$platforms universal"
    fi

    # Gemini CLI
    if [ -d "$HOME/.gemini" ]; then
        platforms="$platforms gemini"
    fi

    # Goose
    if [ -d "$HOME/.config/goose" ]; then
        platforms="$platforms goose"
    fi

    # OpenCode
    if [ -d "$HOME/.config/opencode" ]; then
        platforms="$platforms opencode"
    fi

    # Default to Claude Code if nothing detected
    if [ -z "$platforms" ]; then
        platforms="claude"
    fi

    echo "$platforms"
}

# Create a symlink (or report what would happen)
link() {
    src="$1"
    dst="$2"
    name="$3"

    if [ "$UNINSTALL" = 1 ]; then
        if [ -L "$dst" ]; then
            if [ "$DRY_RUN" = 1 ]; then
                echo "  would remove: $dst"
            else
                rm "$dst"
                echo "  removed: $dst"
            fi
        fi
        return
    fi

    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
        echo "  ok: $name (already linked)"
        return
    fi

    if [ -e "$dst" ]; then
        echo "  skip: $dst exists (not a symlink from this installer)"
        return
    fi

    # Remove broken symlinks
    if [ -L "$dst" ]; then
        rm "$dst"
    fi

    if [ "$DRY_RUN" = 1 ]; then
        echo "  would link: $dst -> $src"
    else
        mkdir -p "$(dirname "$dst")"
        ln -s "$src" "$dst"
        echo "  linked: $name -> $dst"
    fi
}

install_to_platform() {
    platform="$1"
    case "$platform" in
        claude)
            base="$HOME/.claude/skills"
            ;;
        copilot)
            base="$HOME/.copilot/skills"
            ;;
        universal)
            base="$HOME/.agents/skills"
            ;;
        gemini)
            base="$HOME/.gemini/skills"
            ;;
        goose)
            base="$HOME/.config/goose/skills"
            ;;
        opencode)
            base="$HOME/.config/opencode/skills"
            ;;
    esac

    echo "  Platform: $platform ($base)"
    # The repo root IS the clarity skill (SKILL.md is at root)
    link "$REPO_DIR"                               "$base/clarity"               "clarity"
    link "$REPO_DIR/agent-skill-creator"           "$base/agent-skill-creator"   "agent-skill-creator"
    link "$REPO_DIR/linear-walkthrough"            "$base/linear-walkthrough"    "linear-walkthrough"
}

# Main
echo "clarity pipeline installer"
echo "========================="
echo ""
echo "Repository: $REPO_DIR"
echo ""

if [ "$DRY_RUN" = 1 ]; then
    echo "Mode: dry run (no changes will be made)"
    echo ""
fi

if [ "$UNINSTALL" = 1 ]; then
    echo "Mode: uninstall"
    echo ""
fi

platforms=$(detect_platforms)

for platform in $platforms; do
    install_to_platform "$platform"
    echo ""
done

if [ "$UNINSTALL" = 0 ] && [ "$DRY_RUN" = 0 ]; then
    echo "Done. Restart your agent tool to pick up the skills."
    echo ""
    echo "Available commands:"
    echo "  /clarity                  — Generate specs from references"
    echo "  /agent-skill-creator      — Build skills from specs or workflows"
    echo "  /linear-walkthrough       — Understand existing codebases"
fi
