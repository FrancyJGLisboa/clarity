# /clarity

A Claude Code skill that generates implementable specs from reference material — repos, URLs, codebases, docs. You point it at sources. It does the hard thinking.

The bottleneck in AI-assisted development isn't implementation speed — it's spec quality. Most people can't write specs detailed enough for autonomous AI implementation. This skill removes that bottleneck: you provide references, Claude generates the spec.

## What it does

5 phases, each producing a concrete artifact:

| Phase | What happens | Output |
|-------|-------------|--------|
| **1. INGEST** | Claude reads all your references (repos, URLs, code, docs) and extracts everything | `.clarity/context.md` |
| **2. SPECIFY** | Claude writes a structured spec from what it ingested | `.clarity/spec.md` |
| **3. SCENARIO** | Claude generates Given/When/Then behavioral scenarios (holdout set) | `scenarios/SC-NNN-*.md` |
| **4. HANDOFF** | Claude creates a self-contained prompt for any AI coding agent | `.clarity/handoff.md` |
| **5. EVALUATE** | After implementation, Claude tests code against holdout scenarios | `.clarity/evaluations/eval-*.md` |

The key trick: scenarios are a **holdout set** — the implementing agent never sees them. This lets you independently verify whether the implementation matches the spec.

## Install

```bash
cp -r clarity/ ~/.claude/skills/clarity/
```

No dependencies.

## Usage

Point it at anything — GitHub repos, local codebases, URLs, docs:

```
/clarity https://github.com/someone/repo
/clarity /path/to/codebase
/clarity https://github.com/someone/repo https://docs.example.com/api "add payment processing"
/clarity quick https://github.com/someone/repo
/clarity resume
/clarity evaluate
```

You can mix and match references. Claude reads everything, synthesizes, and generates the spec. You just review.

On first run, it creates two directories in your project:

```
your-project/
├── .clarity/        # specs, context, handoff, evaluations
└── scenarios/       # holdout test scenarios (agents must not read these)
```

You can also initialize these manually:

```bash
uv run ~/.claude/skills/clarity/scripts/init_project.py
```

## How it handles different sources

| Source type | What Claude extracts |
|-------------|---------------------|
| **GitHub repo** | Architecture, tech stack, data models, API surface, test expectations, gaps |
| **Local codebase** | Same + git history, uncommitted work, env config |
| **API docs URL** | Endpoints, schemas, auth, rate limits, error codes |
| **Product page URL** | Features, target users, UX flows |
| **Blog/tutorial URL** | Architecture decisions, patterns, trade-offs |
| **Free text** | Intent, constraints, priorities, anti-goals |

## Files

```
~/.claude/skills/clarity/
├── SKILL.md                    # Main skill prompt (5-phase autonomous workflow)
├── references/
│   ├── analysis-playbook.md    # How to extract info from each source type
│   ├── spec-template.md        # Spec structure (numbered FRs/NFRs)
│   ├── scenario-template.md    # Given/When/Then format
│   ├── handoff-template.md     # Implementation prompt template
│   ├── evaluation-template.md  # Pass/fail report template
│   └── examples.md             # Reference in → spec out examples
└── scripts/
    └── init_project.py         # Project initializer (stdlib only, idempotent)
```
