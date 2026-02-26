#!/usr/bin/env python3
"""Update clarity to the latest version from GitHub.

Usage:
    python ~/.claude/skills/clarity/scripts/update.py

Or via the skill trigger:
    /clarity update

What it does:
    1. Detects where clarity is installed
    2. Pulls the latest from origin/main
    3. Installs/updates companion skill symlinks
    4. Reports what changed
"""

import subprocess
import sys
from pathlib import Path

# The repo root is one level up from scripts/
CLARITY_DIR = Path(__file__).resolve().parent.parent


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=CLARITY_DIR, **kwargs)


def current_head() -> str:
    r = run(["git", "rev-parse", "HEAD"])
    return r.stdout.strip() if r.returncode == 0 else ""


def is_git_repo() -> bool:
    return (CLARITY_DIR / ".git").exists()


def has_local_changes() -> bool:
    r = run(["git", "status", "--porcelain"])
    return bool(r.stdout.strip())


def detect_install_type() -> str:
    """Detect how clarity was installed based on its path."""
    path = str(CLARITY_DIR)
    if "/.claude/skills/" in path:
        return "Claude Code"
    if "/.copilot/skills/" in path:
        return "Copilot CLI"
    if "/.agents/skills/" in path:
        return "Gemini CLI"
    if "/.github/skills/" in path or "/.github\\skills\\" in path:
        return "per-project"
    return "custom"


def find_companion_skills() -> dict[str, Path]:
    """Find companion skill directories (contain SKILL.md)."""
    companions = {}
    for child in CLARITY_DIR.iterdir():
        if child.is_dir() and (child / "SKILL.md").exists() and child.name != ".git":
            companions[child.name] = child
    return companions


def install_companions(companions: dict[str, Path]) -> list[str]:
    """Create symlinks for companion skills. Returns list of newly linked names."""
    skills_dir = CLARITY_DIR.parent
    linked = []

    for name, source in companions.items():
        target = skills_dir / name

        if target.is_symlink() and target.resolve() == source.resolve():
            continue  # already correct
        if target.exists():
            print(f"  skip: {target} already exists (not a clarity symlink)")
            continue

        if target.is_symlink():
            # broken symlink — remove and re-create
            target.unlink()

        target.symlink_to(source)
        linked.append(name)

    return linked


def update() -> None:
    print(f"Clarity installed at: {CLARITY_DIR}")
    print(f"Install type: {detect_install_type()}\n")

    if not is_git_repo():
        print("Error: clarity directory is not a git repo.", file=sys.stderr)
        print("       Cannot update — was it installed via git clone?", file=sys.stderr)
        sys.exit(1)

    if has_local_changes():
        print("Warning: you have local changes in the clarity directory.")
        print("         Stashing them before pulling...\n")
        run(["git", "stash"])

    before = current_head()

    # Fetch and pull
    print("Fetching latest from origin...")
    r = run(["git", "pull", "--rebase", "origin", "main"])
    if r.returncode != 0:
        print(f"Error pulling: {r.stderr}", file=sys.stderr)
        sys.exit(1)

    after = current_head()

    if before == after:
        print("Already up to date.\n")
    else:
        # Show what changed
        r = run(["git", "log", "--oneline", f"{before[:12]}..{after[:12]}"])
        count = len(r.stdout.strip().splitlines())
        print(f"Updated ({count} new commit{'s' if count != 1 else ''}):\n")
        for line in r.stdout.strip().splitlines():
            print(f"  {line}")
        print()

    # Install companion skills
    companions = find_companion_skills()
    if companions:
        linked = install_companions(companions)
        if linked:
            print(f"New companion skills linked: {', '.join(linked)}")
            print("Restart Claude Code to pick them up.\n")
        else:
            print(f"Companion skills up to date: {', '.join(companions.keys())}")
    else:
        print("No companion skills found.")

    print("\nDone.")


if __name__ == "__main__":
    update()
