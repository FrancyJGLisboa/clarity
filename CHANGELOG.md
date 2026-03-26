# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-03-13

### Added
- **Monorepo consolidation**: `/clarity`, `/agent-skill-creator`, and `/linear-walkthrough` now ship together in a single repository
- `LICENSE` file (MIT) in repo root
- `CONTRIBUTING.md` with contribution guidelines
- `ROADMAP.md` with public development roadmap
- `.github/workflows/` with CI for validation and security scanning
- `.github/ISSUE_TEMPLATE/` with bug report and skill showcase templates
- `.github/PULL_REQUEST_TEMPLATE.md`
- `shared/install.sh` — unified installer for the full pipeline
- `shared/skill-brief-schema.json` — formal schema for the clarity-to-agent-skill-creator handoff format
- `docs/architecture.md` — end-to-end pipeline documentation
- `docs/skill-brief-spec.md` — skill-brief format v1.0 specification
- `clarity/references/skill-brief-template.md` — formalized handoff template

### clarity skill
- 5-phase pipeline: INGEST → SPECIFY → SCENARIO → HANDOFF → EVALUATE
- Holdout scenario evaluation (scenarios kept secret from implementing agents)
- Support for repos, URLs, PDFs, local codebases, and free text as input
- Quick mode, resume capability, and `/clarity update` command

### agent-skill-creator skill
- 5-phase pipeline: DISCOVERY → DESIGN → ARCHITECTURE → DETECTION → IMPLEMENTATION
- 14-platform support with auto-detection and format adapters
- Quality gates: spec validation, security scanning, staleness detection
- Git-based team skill registry
- Cross-platform export system
- Template-based skill creation (financial, climate, e-commerce)

### linear-walkthrough skill
- Zero-hallucination codebase walkthroughs (all code extracted via shell commands)
- Quick mode for fast orientation
- Support for local and remote repositories

---

## Pre-consolidation history

### clarity (standalone)
- `217571f` Improve /clarity update discoverability in README
- `13e8fbf` Add /clarity update command for self-updating
- `d5f6b2c` Add /linear-walkthrough companion skill
- `5562529` Rewrite to autonomous spec generation
- `ee1304b` Initial commit

### agent-skill-creator (standalone)
- `0663e3e` Add "Don't Make Humans Be Clear" design principle
- `a70b5a5` Use ~/.agents/skills/ canonical path
- `518a153` Clarify global install
- 81 commits total — see git history for full details
