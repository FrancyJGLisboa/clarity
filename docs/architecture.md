# Pipeline Architecture

## Overview

The clarity pipeline turns messy references into deployed, verified agent skills. Three skills form a sequential pipeline with a clean handoff point between each stage.

```
Your references          Verified spec           Deployed skill
(repos, URLs, PDFs,  →   /clarity   →   /agent-skill-creator   →   on 14 platforms
 docs, vague ideas)                                                  instantly
```

## The Three Skills

### /clarity — References → Verified Spec

Reads anything you point it at. Produces a structured specification and independently verifiable behavioral scenarios.

**5 phases:**

| Phase | Output | Purpose |
|-------|--------|---------|
| INGEST | `.clarity/context.md` | Extract everything from all references |
| SPECIFY | `.clarity/spec.md` | Structured spec with numbered requirements |
| SCENARIO | `scenarios/SC-NNN-*.md` | Holdout test set (never shown to implementer) |
| HANDOFF | `.clarity/handoff.md` + `.clarity/skill-brief.md` | Implementation prompt + skill-brief for agent-skill-creator |
| EVALUATE | `.clarity/evaluations/eval-*.md` | Pass/fail against holdout scenarios |

**Key mechanism**: Holdout evaluation. Scenarios are generated before implementation and kept secret from the implementing agent. After implementation, `/clarity evaluate` tests the code against those scenarios. This is the only way to distinguish "the agent did what I asked" from "the agent did what I meant."

### /agent-skill-creator — Spec → Deployed Skill

Takes a workflow description, a skill-brief from `/clarity`, or any input — and produces a complete, production-ready agent skill installed on your platform.

**5 phases:**

| Phase | Purpose |
|-------|---------|
| DISCOVERY | Research APIs, select data sources |
| DESIGN | Define 4-6 priority analyses covering 80% of use cases |
| ARCHITECTURE | Plan directory structure, caching, rate limiting |
| DETECTION | Generate activation keywords and description |
| IMPLEMENTATION | Write all code, validate, security scan, install |

**Key mechanism**: Quality gates. Every skill passes spec validation and security scanning before delivery. Skills that fail are blocked.

### /linear-walkthrough — Code → Walkthrough

The inverse of `/clarity`: reads existing code and produces a file-by-file walkthrough for understanding.

**Key mechanism**: Zero hallucination. Every code snippet is extracted via shell commands (`grep`, `sed`, `cat`), never manually typed. Each snippet includes a provenance comment showing the command that extracted it.

## The Handoff Format

The **skill-brief** is the interchange format between `/clarity` and `/agent-skill-creator`. It's a structured Markdown document that collapses agent-skill-creator's Phase 1 (API research) entirely.

```
.clarity/skill-brief.md
├── Identity (name, description, keywords, user persona)
├── Sources ingested (what /clarity read — agent-skill-creator must NOT re-read)
├── API decision (selected API, auth, rate limits, quirks)
├── Priority analyses (4-6 analyses with methodology and examples)
├── Command structure (CLI surface)
├── Output design (formats, default fields, size limits)
├── Domain context (terminology, filtering conventions, anti-goals)
├── Environment (env vars, dependencies, network)
└── Holdout summary (behavioral areas, NOT the scenarios themselves)
```

A JSON Schema for this format is at `shared/skill-brief-schema.json`.

## Data Flow

```
User provides references
        │
        ▼
   ┌─────────┐
   │ /clarity │
   │  INGEST  │──→ .clarity/context.md
   │ SPECIFY  │──→ .clarity/spec.md
   │ SCENARIO │──→ scenarios/SC-*.md (HOLDOUT — secret)
   │ HANDOFF  │──→ .clarity/skill-brief.md
   └────┬─────┘
        │
        ▼
┌──────────────────────┐
│ /agent-skill-creator │
│     DISCOVERY        │ (skipped — skill-brief has API decision)
│     DESIGN           │ (skipped — skill-brief has analyses)
│     ARCHITECTURE     │──→ directory structure
│     DETECTION        │──→ activation keywords
│     IMPLEMENTATION   │──→ complete skill package
└──────────┬───────────┘
           │
           ▼
   Skill installed on platform
           │
           ▼
   ┌─────────────────┐
   │ /clarity        │
   │ EVALUATE        │──→ Tests against holdout scenarios
   └─────────────────┘
           │
           ▼
   Pass/fail report with root cause analysis
```

## Quality Gates

| Gate | Tool | What it checks | When it runs |
|------|------|---------------|-------------|
| Spec validation | `validate.py` | SKILL.md structure, naming, metadata | Before skill delivery, on every PR |
| Security scan | `security_scan.py` | Hardcoded keys, credentials, injection patterns | Before skill delivery, on every PR |
| Staleness check | `staleness_check.py` | Review dates, dependency health, schema drift | On demand, in registry audits |
| Holdout evaluation | `/clarity evaluate` | Implementation vs. behavioral scenarios | After implementation |

## Repository Structure

```
clarity/                              ← repo root (IS the /clarity skill)
├── SKILL.md                          ← /clarity activation
├── prompts/                          ← VS Code Copilot prompt file
├── references/                       ← clarity templates and playbooks
├── scripts/                          ← init_project.py, update.py
├── linear-walkthrough/               ← /linear-walkthrough companion skill
│   ├── SKILL.md
│   └── references/
├── agent-skill-creator/              ← /agent-skill-creator skill
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   └── registry/
├── shared/                           ← shared infrastructure
│   ├── install.sh
│   └── skill-brief-schema.json
├── docs/                             ← project documentation
├── .github/                          ← CI/CD, issue templates
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── ROADMAP.md
└── README.md
```
