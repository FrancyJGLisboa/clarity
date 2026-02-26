# Walkthrough Template

Use this structure for the generated `walkthrough.md` file. Adapt section depth and detail based on codebase size and whether quick mode is active.

---

```markdown
# Codebase Walkthrough: {project-name}

> Generated from: {source-path-or-url}
> Date: {YYYY-MM-DD}
> Focus: {user-specified focus or "full codebase"}

## Overview

{1-2 paragraph summary: what this project does, what problem it solves, tech stack, architecture style (monolith, library, CLI tool, microservice, etc.)}

## Project Structure

{Annotated file tree — include brief purpose for each file/directory}

```
project/
├── src/
│   ├── main.py          # Application entry point
│   ├── core/
│   │   ├── engine.py    # Core processing logic
│   │   └── models.py    # Data models
│   ├── handlers/
│   │   ├── auth.py      # Authentication
│   │   └── api.py       # API routes
│   └── utils/
│       └── helpers.py   # Shared utilities
├── tests/               # Test suite
├── config.py            # Configuration
└── Dockerfile           # Container setup
```

## Walkthrough

### 1. {File/Module Name} — {Role}

{Commentary paragraph: what this file does, why it exists, how it fits in the system. If this references a previously explained module, say so.}

```{language}
# $ {shell command that extracted this snippet}
{extracted code}
```

{Explanation of the extracted code: what it does, how it connects to other parts, notable patterns or decisions.}

{Repeat code extraction + explanation blocks as needed for the same file. Pick the most important parts — don't extract everything unless the file is small.}

---

### 2. {Next File/Module} — {Role}

{Same pattern: commentary → extracted code → explanation}

---

{Continue for all files in the walkthrough plan...}

## Architecture Summary

{How the pieces connect — describe the primary flows:}
- **Data flow**: How data moves through the system (input → processing → output)
- **Request lifecycle**: For web apps — request → middleware → handler → response
- **Key patterns**: Design patterns used (repository, factory, middleware chain, etc.)
- **Module coupling**: How tightly/loosely modules depend on each other

## Key Decisions & Patterns

{Notable architectural choices, conventions, and trade-offs observed in the code:}
- {Decision 1: what was chosen and why it likely was chosen}
- {Decision 2: ...}
- {Any gotchas, workarounds, or technical debt worth noting}
```

---

## Quick Mode Template

For quick mode, use this abbreviated structure:

```markdown
# Codebase Overview: {project-name}

> Generated from: {source-path-or-url}
> Date: {YYYY-MM-DD}
> Mode: Quick overview

## What This Project Does

{1 paragraph summary from README}

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | {language} |
| Framework | {framework} |
| ... | ... |

## Project Structure

{Annotated file tree}

## Entry Point

{Walkthrough of the main entry point only — same commentary → code → explanation pattern}

## Architecture at a Glance

{Brief summary of how the system is organized, based on structure and entry point analysis}
```
