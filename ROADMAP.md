# Roadmap

> From messy references to deployed agent skills — verified, not just plausible.

## v1.0 — Pipeline Foundation (current)

- [x] `/clarity`: references → verified spec with holdout scenarios
- [x] `/agent-skill-creator`: spec → deployed skill on 14 platforms
- [x] `/linear-walkthrough`: codebase → zero-hallucination walkthrough
- [x] Monorepo consolidation
- [x] LICENSE, CONTRIBUTING, CI/CD
- [x] Skill-brief format v1.0 specification
- [x] Unified installer

## v1.1 — Pipeline Automation

- [ ] `--build` flag: `/clarity` auto-invokes `/agent-skill-creator` after spec generation
- [ ] `--fix` flag: `/clarity evaluate` failures auto-generate targeted fix prompts
- [ ] Shared validation across both skills (validate specs, handoffs, and skills)
- [ ] Skill-brief JSON Schema validation as a standalone command

## v1.2 — Community

- [ ] GitHub Discussions enabled
- [ ] 5+ example skills in the registry (seeded by authors)
- [ ] Skill showcase issue template for community submissions
- [ ] Docs site on GitHub Pages
- [ ] Community skills index

## v1.3 — Ecosystem

- [ ] Skill-brief format submitted to agentskills.io as proposed extension
- [ ] Community registry with 20+ published skills
- [ ] Template library expansion beyond financial/climate/e-commerce
- [ ] Third-party tools producing or consuming the skill-brief format

## v2.0 — Continuous Verification

- [ ] Staleness-triggered re-evaluation (source material changed → re-ingest → re-evaluate)
- [ ] Dependency health monitoring feeding back into spec updates
- [ ] Schema drift detection as evaluation trigger
- [ ] Multi-agent suite orchestration with clarity specs

## What we will not build

- A SaaS platform — the value is in the open standard and CLI tools
- A plugin marketplace with gatekeeping — the git-based registry stays open
- Configurable phase ordering or plugin hooks — the pipeline is simple by design
- Support for every new platform that appears — depth over breadth
