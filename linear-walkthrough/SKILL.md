---
name: linear-walkthrough
description: >
  Generates a linear, file-by-file walkthrough of an existing codebase that explains
  how the code works in detail. Code snippets are extracted via shell commands (grep,
  sed, cat, head) — never manually copied — to eliminate hallucination risk. Use when
  asked to explain, document, or walk through a codebase, repo, or project. Triggers:
  "walk me through this code", "explain this codebase", "how does this project work",
  "create a walkthrough", "onboard me to this repo".
metadata:
  author: FrancyJGLisboa
  version: "1.0"
  license: MIT
---

# /linear-walkthrough — Zero-Hallucination Codebase Walkthroughs

You are an expert code reader. Your job is to consume an entire codebase and produce a structured, linear walkthrough document that explains how the code works. The critical constraint: **every code snippet is extracted by executing shell commands against the actual source files** — you never manually type or copy code.

This technique is based on Simon Willison's "Linear Walkthroughs" agentic engineering pattern.

## Trigger

User invokes `/linear-walkthrough` followed by a target codebase:

```
/linear-walkthrough /path/to/codebase
/linear-walkthrough https://github.com/someone/repo
/linear-walkthrough /path/to/codebase "focus on the auth system"
/linear-walkthrough quick /path/to/codebase
```

Arguments:
- **First arg**: Path to a local directory OR a GitHub URL
- **Optional quoted text**: Focus area — limits the walkthrough to specific modules/concerns
- **`quick` modifier**: Produces a high-level overview instead of file-by-file detail

## Core Principles

1. **Shell-extracted code only.** Every code snippet in the output MUST come from executing a shell command (`grep`, `sed`, `cat`, `head`, `tail`, `awk`) against the actual source files. NEVER manually type, copy, or reconstruct code from memory.
2. **Logical order, not alphabetical.** Walk through code in the order a human would explain it: entry point → core logic → supporting modules → config/infra.
3. **Commentary drives, code supports.** Write prose that explains the *why*. Extract code to show the *what*. Don't dump code without explanation.
4. **Single output file.** Produce one `walkthrough.md` — portable, reviewable, shareable.
5. **Bilingual.** Templates and system logic in English. If the user writes in another language, respond in that language.

## Reference Files

Load as needed:
- `references/walkthrough-template.md` — Document structure template

---

## Phase 1: SCAN

**Goal**: Map the codebase to understand its shape, tech stack, and boundaries.

### Step 1: Resolve the Target

**Local path:**
- Verify the directory exists
- Use it directly for all subsequent operations

**GitHub URL:**
- Clone to `/tmp/walkthrough-{repo-name}`
- Use the cloned path for all subsequent operations
- Note: clean up after Phase 3 completes

### Step 2: Map the Codebase

Execute these discovery commands (adapt as needed):

```bash
# File tree (respect .gitignore, skip heavy directories)
find {path} -type f \
  ! -path '*/.git/*' \
  ! -path '*/node_modules/*' \
  ! -path '*/__pycache__/*' \
  ! -path '*/venv/*' \
  ! -path '*/.venv/*' \
  ! -path '*/dist/*' \
  ! -path '*/build/*' \
  ! -path '*/.tox/*' \
  ! -path '*/target/*' \
  | head -200

# Tech stack signals
ls {path}/package.json {path}/pyproject.toml {path}/Cargo.toml \
  {path}/go.mod {path}/Gemfile {path}/pom.xml 2>/dev/null

# Entry points
ls {path}/main.* {path}/app.* {path}/index.* {path}/cli.* \
  {path}/src/main.* {path}/src/app.* {path}/src/index.* 2>/dev/null

# README for high-level context
head -100 {path}/README.md 2>/dev/null || head -100 {path}/README.rst 2>/dev/null
```

### Step 3: Build Internal Map

From the scan results, build a mental model (internal working memory, not written to disk):
- **Tech stack**: Language(s), framework(s), key dependencies
- **Architecture style**: Monolith, microservices, CLI tool, library, etc.
- **Module boundaries**: What are the logical groupings of files?
- **Entry points**: Where does execution start?
- **Dependency graph**: Which modules depend on which?
- **Focus filter**: If the user specified a focus area, identify the relevant subset of files

---

## Phase 2: PLAN

**Goal**: Determine the walkthrough order and get user approval.

### Step 1: Determine Order

Arrange files/modules in the order a human would explain the system. General pattern:

1. **Entry point** — Where execution begins (main, app, index, CLI)
2. **Core domain** — The primary logic/models that define what the system does
3. **Data layer** — Storage, schemas, migrations, external data access
4. **API/Interface layer** — HTTP routes, CLI commands, UI components
5. **Supporting utilities** — Helpers, middleware, decorators, shared code
6. **Configuration & infrastructure** — Config files, CI/CD, Docker, deployment

Within each group, order by dependency: a module should be explained before modules that depend on it.

If the user specified a focus area, limit the plan to relevant files only.

### Step 2: Present the Plan

Show the user the planned walkthrough order:

```
I've scanned {project-name} and plan to walk through it in this order:

1. src/main.py — Application entry point
2. src/core/engine.py — Core processing engine
3. src/core/models.py — Data models
4. src/handlers/auth.py — Authentication handler
5. src/handlers/api.py — API route handlers
6. src/utils/helpers.py — Shared utilities
7. config.py — Configuration
8. Dockerfile — Container setup

Does this order work? Want me to add, remove, or reorder anything?
```

Wait for user approval before proceeding.

---

## Phase 3: WRITE

**Goal**: Produce the walkthrough document. Read `references/walkthrough-template.md` for the output structure.

### Step 1: Write the Header

- Project name, source path/URL, date, focus area (if any)
- 1-2 paragraph overview: what the project does, tech stack, architecture style
- Annotated file tree

### Step 2: Walk Through Each File/Module

For each item in the approved plan:

**a) Write commentary** — A paragraph explaining:
  - What this file/module does
  - Why it exists (its role in the system)
  - How it connects to previously explained parts

**b) Extract code snippets** — Use shell commands to pull relevant sections:

```bash
# Show a function definition (by line range)
sed -n '15,45p' src/main.py

# Show a specific class or function (by pattern match)
grep -A 30 'class AuthHandler' src/handlers/auth.py

# Show imports to explain dependencies
head -20 src/core/engine.py

# Show a specific block (function + body)
grep -A 15 'def process_request' src/core/engine.py

# Show a pattern across files
grep -rn 'def handle_' src/handlers/

# Show configuration
cat config.py

# Show the last section of a file
tail -30 src/utils/helpers.py
```

Choose the extraction method that best shows the relevant code. Don't extract entire files unless they're short — pick the important parts.

**c) Explain the extracted code** — After each snippet, explain:
  - What the code does
  - How it connects to other parts of the system
  - Any notable patterns, design decisions, or gotchas

### Step 3: Write Architecture Summary

After walking through all files:
- How the pieces connect (data flow, request lifecycle, event flow)
- Key architectural patterns used (and why)
- Notable design decisions and trade-offs

### Step 4: Write the Output File

Write the complete walkthrough to `walkthrough.md` in the target directory.

If the target was a GitHub URL (cloned to /tmp), write `walkthrough.md` to the **current working directory** instead, then clean up the cloned repo.

Tell the user where the file was written.

---

## THE CRITICAL CONSTRAINT

This is the most important rule in this entire skill:

> **NEVER manually type or copy code into the walkthrough.**
>
> Every code snippet MUST be extracted by executing a shell command (`grep`, `sed`, `cat`, `head`, `tail`, `awk`) against the actual source files. If you cannot extract a snippet via shell command, describe it in prose instead — do NOT fabricate or reconstruct the code from memory.
>
> This ensures **zero hallucination risk** — every line of code shown in the walkthrough is verified to exist in the actual source files.

When writing the walkthrough document, format extracted code as fenced code blocks with the appropriate language tag. Include a comment showing which command produced the snippet:

````markdown
```python
# $ sed -n '15,30p' src/main.py
def main():
    config = load_config()
    app = create_app(config)
    app.run(host="0.0.0.0", port=config.port)
```
````

The `# $ command` comment serves as provenance — a reader can re-run it to verify.

---

## Quick Mode

When invoked with `quick`:

- **Phase 1**: Scan README + entry points only (skip deep file tree exploration)
- **Phase 2**: Skip user approval — go straight to writing
- **Phase 3**: Produce a high-level overview:
  - Project summary (from README)
  - Tech stack
  - Annotated file tree
  - Entry point walkthrough only (not every file)
  - Architecture summary based on structure and entry points

Quick mode is useful for getting a fast orientation before diving deeper.

---

## Remote Repository Handling

For GitHub URLs:

1. Clone to `/tmp/walkthrough-{repo-name}` (shallow clone with `--depth 1` for speed)
2. Run all phases using the cloned path
3. Write `walkthrough.md` to the **user's current working directory** (not inside /tmp)
4. Remove the cloned repo after writing

```bash
git clone --depth 1 https://github.com/someone/repo /tmp/walkthrough-repo
# ... all extraction commands use /tmp/walkthrough-repo/...
# ... write walkthrough.md to $PWD ...
rm -rf /tmp/walkthrough-repo
```

---

## Error Handling

- If a file can't be read, note it in the walkthrough and skip it
- If the codebase is very large (>200 source files), suggest the user specify a focus area
- If a GitHub URL is unreachable, tell the user and stop
- If the user provides no target, ask what codebase they want walked through
- If a shell extraction command fails, describe the intended content in prose — never fabricate code
