# clarity

**From messy references to deployed agent skills — verified, not just plausible.**

[![Agent Skills Open Standard](https://img.shields.io/badge/Agent%20Skills-Open%20Standard-blue)](https://github.com/anthropics/agent-skills-spec)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## The problem

The specification gap is why AI agent workflows fail. Not model capability. Not implementation speed. Specification.

Humans cannot write specs detailed enough for agents to build from without ambiguity. The implementing agent fills in the gaps with plausible-sounding assumptions. The result looks right until it doesn't.

## What this is

Three companion skills that form a complete pipeline — from raw, messy references to a verified, production-ready agent skill deployed across 14 platforms.

```
Your messy inputs                                        Your deployed skill
(repos, URLs, PDFs,   →   /clarity   →   /agent-skill-creator   →   on 14 platforms
 docs, codebases,          Ingest          Build & distribute          instantly
 vague intentions)         Specify
                           Scenario (holdout)
                           Handoff
                           Evaluate
```

You provide sources and evaluate the outcome. The agents handle everything in between.

---

## The three skills

### /clarity — References → Verified Spec

Points at anything. Reads it. Thinks. Produces a structured spec and independently verifiable behavioral scenarios.

| Phase | What happens | Output |
|-------|-------------|--------|
| **INGEST** | Reads all your references — repos, URLs, code, docs, PDFs | `.clarity/context.md` |
| **SPECIFY** | Writes a structured spec with numbered requirements | `.clarity/spec.md` |
| **SCENARIO** | Generates Given/When/Then behavioral scenarios (holdout set) | `scenarios/SC-NNN-*.md` |
| **HANDOFF** | Creates implementation prompt + skill brief | `.clarity/handoff.md` `.clarity/skill-brief.md` |
| **EVALUATE** | Tests code against holdout scenarios | `.clarity/evaluations/eval-*.md` |

The key mechanism: **holdout evaluation**. Scenarios are generated before implementation and kept secret from the implementing agent. After implementation, `/clarity evaluate` tests the code against those scenarios — the only way to distinguish "the agent did what I asked" from "the agent did what I meant."

### /agent-skill-creator — Spec → Deployed Skill

Takes a workflow description, a skill-brief from `/clarity`, or any input — and produces a complete, production-ready agent skill installed on your platform.

```
your-skill/
├── SKILL.md          # Skill definition — activates with /your-skill
├── scripts/          # Functional Python code (no placeholders)
├── references/       # Detailed documentation, loaded on demand
├── assets/           # Templates, configs, data files
├── install.sh        # Cross-platform auto-detect installer
└── README.md         # Install instructions for all 14 platforms
```

Every skill passes automated validation and security scanning before delivery.

### /linear-walkthrough — Code → Walkthrough

The inverse of `/clarity`. Reads existing code and produces a file-by-file walkthrough where every code snippet is extracted via shell commands — zero hallucination risk.

---

## Install

### One-liner (recommended — installs all three skills)

```bash
# Claude Code + VS Code Copilot
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.claude/skills/clarity
cd ~/.claude/skills/clarity && ./shared/install.sh

# Universal path (Codex CLI, Gemini CLI, Kiro, Antigravity)
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.agents/skills/clarity
cd ~/.agents/skills/clarity && ./shared/install.sh
```

The installer auto-detects your platforms and symlinks all three skills.

### Manual (pick your tool)

```bash
# Claude Code
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.claude/skills/clarity
ln -s ~/.claude/skills/clarity/agent-skill-creator ~/.claude/skills/agent-skill-creator
ln -s ~/.claude/skills/clarity/linear-walkthrough ~/.claude/skills/linear-walkthrough

# Copilot CLI
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.copilot/skills/clarity
ln -s ~/.copilot/skills/clarity/agent-skill-creator ~/.copilot/skills/agent-skill-creator

# Per-project (all contributors get it)
git clone https://github.com/FrancyJGLisboa/clarity.git .github/skills/clarity
```

### VS Code Copilot (prompt file only)

```bash
mkdir -p .github/prompts
cp .github/skills/clarity/prompts/clarity.prompt.md .github/prompts/
```

Then type `/clarity` in Copilot Chat (agent mode).

### Platform support

| Tool | Install path | Invocation |
|------|-------------|------------|
| Claude Code | `~/.claude/skills/clarity/` | `/clarity` |
| Copilot CLI | `~/.copilot/skills/clarity/` | `/clarity` |
| Copilot VS Code | `.github/skills/clarity/` | `/clarity` in agent mode |
| Cursor | `.cursor/rules/clarity/` | `/clarity` |
| Windsurf | `.windsurf/rules/clarity/` | `/clarity` |
| Codex CLI | `~/.agents/skills/clarity/` | `/clarity` |
| Gemini CLI | `~/.gemini/skills/clarity/` | `/clarity` |
| Kiro | `.kiro/skills/clarity/` | `/clarity` |
| Cline / Roo Code / Trae | `.clinerules/clarity/` | `/clarity` |
| Goose | `~/.config/goose/skills/clarity/` | `/clarity` |
| OpenCode | `~/.config/opencode/skills/clarity/` | `/clarity` |

---

## Usage

### The full pipeline

```bash
# Step 1: Point clarity at your reference material
/clarity https://github.com/your-org/internal-api-docs

# Step 2: Review the spec at .clarity/spec.md
# Redirect, approve, or adjust before continuing

# Step 3: Hand off to agent-skill-creator
/agent-skill-creator .clarity/skill-brief.md

# Step 4: Your skill is installed and ready
# /your-skill is now available

# Step 5: Evaluate the implementation
/clarity evaluate
```

### Fast path — you already know what you want

```bash
# Skip clarity if you have a clear spec or workflow
/agent-skill-creator "weekly positions report for the latam grains desk"

# Or point it at existing code
/agent-skill-creator scripts/my_existing_pipeline.py
```

### Understand before building

```bash
# Use linear-walkthrough when the codebase is unfamiliar
/linear-walkthrough https://github.com/someone/complex-repo

# Then use clarity to build on top of it
/clarity https://github.com/someone/complex-repo "add webhook support"
```

### /clarity commands

```
/clarity https://github.com/someone/repo                   # Single repo
/clarity https://github.com/repo https://docs.example.com   # Repo + API docs
/clarity /path/to/codebase "add OAuth authentication"        # Local + goal
/clarity quick https://github.com/someone/repo               # Fast mode
/clarity resume                                              # Resume interrupted session
/clarity evaluate                                            # Test against holdout scenarios
/clarity update                                              # Pull latest version
```

### /agent-skill-creator commands

```
/agent-skill-creator .clarity/skill-brief.md                # From a clarity handoff
/agent-skill-creator "daily risk report for corn and soybeans" # From a description
/agent-skill-creator scripts/existing_pipeline.py            # From existing code
/agent-skill-creator meeting-transcript.md                   # From a transcript
```

### /linear-walkthrough commands

```
/linear-walkthrough ~/projects/billing-service               # Full codebase
/linear-walkthrough ~/projects/app "focus on auth"           # Focus on subsystem
/linear-walkthrough quick https://github.com/psf/black       # Quick orientation
```

---

## How it handles different sources

| Source type | What gets extracted |
|-------------|---------------------|
| GitHub repo | Architecture, tech stack, data models, API surface, test expectations, gaps |
| Local codebase | Same + git history, uncommitted work, env config |
| API docs URL | Endpoints, schemas, auth, rate limits, error codes |
| Product page | Features, target users, UX flows |
| Blog/tutorial | Architecture decisions, patterns, trade-offs |
| Free text | Intent, constraints, priorities, anti-goals |

---

## Quality gates

Every skill generated by `/agent-skill-creator` passes automated checks before delivery:

| Gate | What it checks |
|------|---------------|
| **Spec validation** | SKILL.md structure, frontmatter, naming rules, file references |
| **Security scan** | No hardcoded API keys, no credentials, no injection patterns |
| **Staleness check** | Review dates, dependency health, API schema drift |

Run them independently:

```bash
python3 agent-skill-creator/scripts/validate.py ./my-skill/
python3 agent-skill-creator/scripts/security_scan.py ./my-skill/
python3 agent-skill-creator/scripts/staleness_check.py ./my-skill/ --check-deps --check-drift
```

---

## Share skills across your team

After building a skill, share it with one `git clone`:

```bash
# Your colleague installs it
git clone https://github.com/your-org/sales-report-skill.git ~/.agents/skills/sales-report-skill
```

For larger teams, use the git-based skill registry:

```bash
python3 agent-skill-creator/scripts/skill_registry.py init --name "Acme Corp Skills"
python3 agent-skill-creator/scripts/skill_registry.py publish ./skill/ --tags sales,reports
python3 agent-skill-creator/scripts/skill_registry.py list
python3 agent-skill-creator/scripts/skill_registry.py search "sales"
python3 agent-skill-creator/scripts/skill_registry.py install sales-report-skill
```

No servers, no databases — just git.

---

## The skill-brief format

The **skill brief** is the interchange format between `/clarity` and `/agent-skill-creator`. It encodes everything the builder needs without re-reading original sources.

Any tool can produce or consume this format. See:
- Template: [`clarity/references/skill-brief-template.md`](clarity/references/skill-brief-template.md)
- JSON Schema: [`shared/skill-brief-schema.json`](shared/skill-brief-schema.json)
- Specification: [`docs/skill-brief-spec.md`](docs/skill-brief-spec.md)

---

## Updating

```
/clarity update
```

Or from the terminal:

```bash
cd ~/.claude/skills/clarity && git pull
./shared/install.sh
```

---

## Repository structure

```
clarity/                            # Repo root — IS the /clarity skill
├── SKILL.md                        # /clarity activation
├── prompts/                        # VS Code Copilot prompt file
├── references/                     # Templates and playbooks
├── scripts/                        # init_project.py, update.py
│
├── linear-walkthrough/             # /linear-walkthrough companion skill
│   ├── SKILL.md
│   └── references/
│
├── agent-skill-creator/            # /agent-skill-creator skill
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   └── registry/
│
├── shared/                         # Shared infrastructure
│   ├── install.sh                  # Unified pipeline installer
│   └── skill-brief-schema.json     # Skill brief format schema
│
├── docs/                           # Project documentation
│   ├── architecture.md             # End-to-end pipeline docs
│   └── skill-brief-spec.md         # Skill brief format v1.0
│
├── LICENSE                         # MIT
├── CONTRIBUTING.md                 # How to contribute
├── CHANGELOG.md                    # Version history
├── ROADMAP.md                      # Public development roadmap
└── README.md                       # This file
```

---

## Why this exists

Every agent workflow has the same failure mode. The spec is vague. The implementing agent fills gaps with plausible-sounding assumptions. The result looks right until it doesn't.

The root cause isn't the model. It's that humans are structurally bad at writing specifications — not because they lack intelligence, but because externalizing implicit knowledge into explicit, unambiguous instructions is genuinely cognitively demanding work.

This pipeline inverts that. The agent does the hard specification work. The human reviews artifacts at each phase. The holdout evaluation provides an independent measure of whether the implementation matches the intent.

The result: agent workflows that are **verifiable**, not just plausible.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

## Links

- [Agent Skills Open Standard](https://github.com/anthropics/agent-skills-spec)
- [Architecture docs](docs/architecture.md)
- [Skill brief specification](docs/skill-brief-spec.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
