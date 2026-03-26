# Skill Brief Format — v1.0

## Purpose

The skill brief is the interchange format between specification tools (like `/clarity`) and skill builders (like `/agent-skill-creator`). It encodes everything an implementing agent needs to build a skill **without re-reading the original sources**.

The skill brief collapses the builder's research phase entirely. When `/agent-skill-creator` receives a skill brief, it skips Phase 1 (DISCOVERY) and Phase 2 (DESIGN) and proceeds directly to implementation.

## Design principles

1. **Decisions are final.** The brief contains decisions, not options. The API has been selected. The analyses have been defined. The builder implements them.
2. **Sources are summarized, not linked.** The brief contains key takeaways from each source. The builder must NOT re-read them.
3. **Holdout scenarios are hidden.** The brief includes a behavioral summary (what areas are covered) but never the scenarios themselves.
4. **Self-contained.** The brief plus the skill's SKILL.md specification is everything the builder needs. No additional context required.

## Format

The skill brief is a Markdown document with YAML-style sections. The canonical template is at `clarity/references/skill-brief-template.md`. A JSON Schema for programmatic validation is at `shared/skill-brief-schema.json`.

### Required sections

| Section | Purpose |
|---------|---------|
| **Identity** | Skill name, description, activation keywords, primary user |
| **Sources ingested** | Table of every reference read, with type and key takeaway |
| **API decision** | Selected API, auth, rate limits, pagination, quirks |
| **Priority analyses** | 4-6 analyses with objective, inputs, output, methodology, CLI examples |
| **Command structure** | Full CLI surface with nouns, verbs, and global flags |
| **Output design** | Default format, fields to surface/suppress, size limits, error message rules |
| **Domain context** | Terminology, filtering conventions, implicit requirements, anti-goals |
| **Environment** | Required env vars, Python dependencies, network requirements |

### Optional sections

| Section | Purpose |
|---------|---------|
| **Holdout summary** | Behavioral areas covered by holdout scenarios (NOT the scenarios) |
| **Clarity references** | Pointers to `.clarity/context.md`, `.clarity/spec.md`, `.clarity/handoff.md` |

## Producing a skill brief

Any tool that follows this format can produce a valid skill brief. Currently:

- **`/clarity`** generates it automatically in Phase 4 (HANDOFF) as `.clarity/skill-brief.md`

## Consuming a skill brief

Any tool that follows this format can consume a valid skill brief. Currently:

- **`/agent-skill-creator`** accepts it as input: `/agent-skill-creator .clarity/skill-brief.md`

## Versioning

This is **v1.0** of the skill brief format. Changes will be documented in `CHANGELOG.md` and the JSON Schema will be updated accordingly.

Breaking changes (removed or renamed required sections) will increment the major version. Additive changes (new optional sections) will increment the minor version.

## Validation

Validate a skill brief against the schema:

```bash
# Using Python (stdlib only)
python3 -c "
import json, sys
schema = json.load(open('shared/skill-brief-schema.json'))
# Basic structure check — full JSON Schema validation requires jsonschema package
brief = open(sys.argv[1]).read()
required = schema['required']
missing = [s for s in required if s.replace('_', ' ') not in brief.lower() and s not in brief.lower()]
if missing:
    print(f'Possibly missing sections: {missing}')
    sys.exit(1)
print('Basic structure check passed')
" .clarity/skill-brief.md
```

For full JSON Schema validation, use the `jsonschema` package or any JSON Schema validator.
