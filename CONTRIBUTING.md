# Contributing to clarity

Thanks for your interest in contributing. This project aims to become the go-to pipeline for building verified agent skills across all platforms.

## Ways to contribute

### 1. Report bugs

Found something broken? [Open an issue](https://github.com/FrancyJGLisboa/clarity/issues/new?template=bug-report.yml) with:
- Which skill (`/clarity`, `/agent-skill-creator`, or `/linear-walkthrough`)
- What platform you're using (Claude Code, Copilot, Cursor, etc.)
- What you tried and what happened

### 2. Improve the skills

The skills are prompt-based — improvements to templates, references, and SKILL.md files have high impact.

**Before submitting a PR:**

```bash
# Validate SKILL.md files (run from repo root)
python3 agent-skill-creator/scripts/validate.py .
python3 agent-skill-creator/scripts/validate.py agent-skill-creator/
python3 agent-skill-creator/scripts/validate.py linear-walkthrough/

# Security scan
python3 agent-skill-creator/scripts/security_scan.py .
python3 agent-skill-creator/scripts/security_scan.py agent-skill-creator/
```

Both must pass with exit code 0.

### 3. Share skills you built

Built a skill with this pipeline? Share it with the community:
- [Open a skill showcase issue](https://github.com/FrancyJGLisboa/clarity/issues/new?template=skill-showcase.yml)
- We'll feature it in the community skills index

### 4. Improve documentation

Typos, unclear instructions, missing platform guides — all welcome. Documentation PRs don't need validation checks.

## Development setup

```bash
git clone https://github.com/FrancyJGLisboa/clarity.git
cd clarity
```

No build step. The skills are Markdown + Python scripts. Edit and test directly.

## Pull request process

1. Fork and create a feature branch from `main`
2. Make your changes
3. Run validation and security checks (see above)
4. Submit a PR with a clear description of what changed and why

## Repository structure

```
clarity/
├── clarity/                  # /clarity skill
├── agent-skill-creator/      # /agent-skill-creator skill
├── shared/                   # Shared infrastructure
└── docs/                     # Project-level documentation
```

Each skill is self-contained. Changes to one skill should not break the others.

## Code style

- Python: follow existing patterns, use type hints, no external dependencies (stdlib only)
- Markdown: no line length limit, use ATX headings (`#`), use fenced code blocks
- Shell: POSIX-compatible (bash, dash, zsh, ash)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
