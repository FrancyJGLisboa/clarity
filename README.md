# /clarity

A Claude Code skill that turns vague ideas into implementable specs through structured questioning. You answer questions, Claude writes the spec.

Based on the "Five Levels of Vibe Coding" insight: the bottleneck isn't implementation speed — it's spec quality.

## What it does

5 phases, each producing a concrete artifact:

| Phase | What happens | Output |
|-------|-------------|--------|
| **1. EXTRACT** | Claude asks you progressive questions (max 2-3 at a time) | `.clarity/context.md` |
| **2. SPECIFY** | Claude writes a structured spec, you review section by section | `.clarity/spec.md` |
| **3. SCENARIO** | Claude generates Given/When/Then behavioral scenarios (holdout set) | `scenarios/SC-NNN-*.md` |
| **4. HANDOFF** | Claude creates a self-contained prompt for any AI coding agent | `.clarity/handoff.md` |
| **5. EVALUATE** | After implementation, Claude tests code against holdout scenarios | `.clarity/evaluations/eval-*.md` |

The key trick: scenarios are a **holdout set** — the implementing agent never sees them. This lets you independently verify whether the implementation matches the spec.

## Install

Copy the skill folder into your Claude Code skills directory:

```bash
cp -r clarity/ ~/.claude/skills/clarity/
```

That's it. No dependencies.

## Usage

In any project, just type:

```
/clarity                                  # start from scratch
/clarity a weather alert system for ports # start with a one-liner
/clarity quick a CSV to JSON tool         # fast mode (2 questions, liberal assumptions)
/clarity resume                           # continue where you left off
/clarity evaluate                         # run holdout scenarios after implementation
```

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

## How it works for brownfield projects

If you run `/clarity` in a project that already has code, it auto-scans the codebase first (README, config files, entry points), summarizes what it found, then asks targeted delta questions: what changes, what stays, blast radius.

## Files

```
~/.claude/skills/clarity/
├── SKILL.md                    # Main skill prompt (the 5-phase workflow)
├── references/
│   ├── question-bank.md        # Questions + probes for vague answers
│   ├── spec-template.md        # Spec structure (numbered FRs/NFRs)
│   ├── scenario-template.md    # Given/When/Then format
│   ├── handoff-template.md     # Implementation prompt template
│   ├── evaluation-template.md  # Pass/fail report template
│   └── examples.md             # Before/after examples
└── scripts/
    └── init_project.py         # Project initializer (stdlib only, idempotent)
```
