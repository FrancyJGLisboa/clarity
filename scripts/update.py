#!/usr/bin/env python3
"""Update clarity pipeline to the latest version from GitHub.

Usage:
    python ~/.claude/skills/clarity/scripts/update.py

Or via the skill trigger:
    /clarity update

What it does:
    1. Detects where the clarity repo is installed
    2. Pulls the latest from origin/main
    3. Installs/updates companion skill symlinks (agent-skill-creator, linear-walkthrough)
    4. Reports what changed
"""

import subprocess
import sys
from pathlib import Path

# scripts/ is at the repo root, so repo root is one level up from scripts/
# The repo root IS the clarity skill (SKILL.md at root)
REPO_DIR = Path(__file__).resolve().parent.parent

# Fallback: walk up until we find .git (handles different install structures)
if not (REPO_DIR / ".git").exists():
    candidate = REPO_DIR
    while candidate != candidate.parent:
        if (candidate / ".git").exists():
            REPO_DIR = candidate
            break
        candidate = candidate.parent


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_DIR, **kwargs)


def current_head() -> str:
    r = run(["git", "rev-parse", "HEAD"])
    return r.stdout.strip() if r.returncode == 0 else ""


def is_git_repo() -> bool:
    return (REPO_DIR / ".git").exists()


def has_local_changes() -> bool:
    r = run(["git", "status", "--porcelain"])
    return bool(r.stdout.strip())


def detect_install_type() -> str:
    """Detect how clarity was installed based on its path."""
    path = str(REPO_DIR)
    if "/.claude/skills/" in path:
        return "Claude Code"
    if "/.copilot/skills/" in path:
        return "Copilot CLI"
    if "/.agents/skills/" in path:
        return "Universal (Codex/Gemini/Kiro)"
    if "/.github/skills/" in path or "/.github\\skills\\" in path:
        return "per-project"
    return "custom"


def find_skills_to_link() -> dict[str, Path]:
    """Find all skills in the monorepo that should be symlinked.

    The repo root IS the /clarity skill (SKILL.md at root).
    Subdirectories with SKILL.md are companion skills that need symlinks:
    - agent-skill-creator/ → /agent-skill-creator
    - linear-walkthrough/ → /linear-walkthrough
    """
    skills = {}

    for child in REPO_DIR.iterdir():
        if child.is_dir() and (child / "SKILL.md").exists() and child.name != ".git":
            skills[child.name] = child

    return skills


def install_skill_links(skills: dict[str, Path]) -> list[str]:
    """Create symlinks for skills in the parent skills directory.
    Returns list of newly linked names."""
    skills_dir = REPO_DIR.parent
    linked = []

    for name, source in skills.items():
        target = skills_dir / name

        if target.is_symlink() and target.resolve() == source.resolve():
            continue  # already correct
        if target.exists() and not target.is_symlink():
            print(f"  skip: {target} already exists (not a symlink)")
            continue

        if target.is_symlink():
            # broken or outdated symlink — remove and re-create
            target.unlink()

        target.symlink_to(source)
        linked.append(name)

    return linked


def update() -> None:
    print(f"Clarity pipeline at: {REPO_DIR}")
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

    # Install/update skill symlinks
    skills = find_skills_to_link()
    if skills:
        linked = install_skill_links(skills)
        if linked:
            print(f"New skills linked: {', '.join(linked)}")
            print("Restart your agent tool to pick them up.\n")
        else:
            print(f"Skills up to date: {', '.join(skills.keys())}")
    else:
        print("No skills found to link.")

    print("\nDone.")


if __name__ == "__main__":
    update()
