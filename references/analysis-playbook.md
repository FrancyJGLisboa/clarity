# Analysis Playbook — Source Type Extraction Guide

How to extract spec-relevant information from each type of reference the user provides.

---

## GitHub Repositories

### Priority Reading Order
1. `README.md` — project purpose, setup, usage
2. Config files — `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `requirements.txt`
3. `CLAUDE.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md` — conventions, structure
4. Entry points — `main.*`, `app.*`, `index.*`, `src/main.*`, `cmd/`
5. Directory structure — `ls -la`, understand the module layout
6. Core source files — follow imports from entry points
7. Data models / schemas — `models/`, `schema/`, `types/`, `migrations/`, database files
8. API definitions — `routes/`, `handlers/`, `controllers/`, OpenAPI specs
9. Tests — `tests/`, `__tests__/`, `*_test.*`, `*.spec.*` — reveal behavioral expectations
10. CI/CD — `.github/workflows/`, `Dockerfile`, `render.yaml`, `docker-compose.yml`

### What to Extract
- **Purpose**: What does this project do? (from README)
- **Tech stack**: Languages, frameworks, databases, deployment (from config)
- **Architecture**: How is the code organized? What patterns? (from structure + source)
- **Data model**: What entities exist? What are their relationships? (from models/schemas)
- **API surface**: What endpoints/commands/interfaces exist? (from routes/handlers)
- **Behavioral expectations**: What should happen in key scenarios? (from tests)
- **Constraints**: What's locked in? (dependencies, deployment target, compatibility)
- **Gaps**: What's missing, incomplete, or marked TODO?

### For Brownfield (user wants to modify this codebase)
Also extract:
- Current behavior that must be preserved
- Modules most likely to be affected
- Test coverage of affected areas
- Dependency graph of affected modules

---

## GitHub Issues & PRs

Use `gh` CLI to read:
```
gh issue list --repo owner/repo --limit 20
gh issue view NUMBER --repo owner/repo
gh pr list --repo owner/repo --limit 10
gh pr view NUMBER --repo owner/repo
```

### What to Extract
- **User intent**: What problem are they trying to solve?
- **Requirements**: Requested features, acceptance criteria
- **Constraints**: Mentioned limitations, compatibility needs
- **Edge cases**: Reported bugs reveal boundary conditions
- **Priorities**: Labels, milestones, assignment patterns

---

## Web URLs

### Processing Strategy by Content Type

**API Documentation**:
- Extract: endpoints, methods, request/response schemas, auth requirements, rate limits
- Look for: OpenAPI/Swagger specs, example requests, error codes
- Output: API contracts section in spec

**Product Pages / Landing Pages**:
- Extract: features list, value propositions, target users, pricing tiers
- Look for: screenshots (describe what they show), feature comparisons
- Output: Goals, non-goals, user personas

**Blog Posts / Tutorials**:
- Extract: architectural decisions, patterns used, trade-offs discussed
- Look for: code examples, configuration snippets, deployment instructions
- Output: Technical constraints, architecture decisions

**Documentation Sites**:
- Extract: concepts, terminology, configuration options, best practices
- Look for: getting started guides, architecture overviews, migration guides
- Output: System understanding, constraints, glossary

**Competitor / Reference Products**:
- Extract: features, UX flows, data models (inferred from UI)
- Look for: what works well, what's missing, pricing/limits
- Output: Functional requirements (inspired by), non-goals (differentiation)

---

## Local Codebases

Same as GitHub repos but accessed directly via file system. Additional steps:

1. Check for `.env.example` or `.env.template` — reveals required configuration
2. Check for `docker-compose.yml` — reveals service dependencies
3. Check for database migrations — reveals data model evolution
4. Check git log (`git log --oneline -20`) — reveals recent development focus
5. Check for uncommitted changes (`git status`) — reveals work in progress

---

## Documents & Files

**PDF files**: Read and extract key content, tables, diagrams (described)
**Markdown/text files**: Read directly
**Images/screenshots**: Describe what you see — UI layouts, diagrams, workflows
**Spreadsheets**: Extract data structure, relationships, sample data

---

## Free Text from User

Parse for:
- **Intent signals**: "I want...", "Build me...", "Something that..."
- **Constraints**: "Must use...", "Can't use...", "Budget is..."
- **Comparisons**: "Like X but...", "Similar to..."
- **Priorities**: "The most important thing is...", "Nice to have..."
- **Anti-goals**: "I don't want...", "Not like..."

---

## Synthesis Rules

After processing all sources:

1. **Cross-reference**: If multiple sources mention the same concept, merge and note consistency
2. **Conflicts**: If sources contradict, note both positions and state which you're favoring (tagged `[ASSUMPTION]`)
3. **Gaps**: If a critical area has no source coverage, make an assumption and tag it
4. **Confidence levels**: For each major section in context.md, note whether it's:
   - **Derived** — directly stated in sources
   - **Inferred** — logically follows from sources
   - **Assumed** — no source coverage, best guess
