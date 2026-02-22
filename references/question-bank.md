# Question Bank — /clarity Skill

Use these questions progressively. Never ask more than 2-3 per message.
After each round, summarize understanding and ask "Did I get that right?"

> The user can answer in any language. System prompts stay in English.

---

## Greenfield Projects (nothing exists yet)

### Round 1 — The Spark
1. **One-liner**: "In one sentence, what does this thing do?"
2. **Who benefits**: "Who is the primary user or beneficiary?"

#### Probes for vague answers
| Vague signal | Probe |
|---|---|
| "It's like X but better" | "What specifically is wrong with X that this solves?" |
| "It manages/handles Y" | "Walk me through one concrete example of someone using it." |
| "It's for everyone" | "If you had to pick ONE person to build this for first, who?" |

### Round 2 — The Happy Path
3. **Core workflow**: "Walk me through the #1 thing a user does, step by step."
4. **Input/Output**: "What goes in and what comes out?"

#### Probes
| Vague signal | Probe |
|---|---|
| "The user just clicks a button" | "What happens between the click and the result? What data moves?" |
| "It automatically does X" | "What triggers it? On a schedule? An event? User action?" |
| Hand-waves at the middle | "Pretend I'm the computer. Tell me what to do at each step." |

### Round 3 — Boundaries & Rules
5. **Must NOT do**: "What should this system explicitly NOT do?"
6. **Constraints**: "Are there hard constraints? (budget, latency, compliance, existing tech stack)"

#### Probes
| Vague signal | Probe |
|---|---|
| "It should be fast" | "What's the maximum acceptable response time in seconds?" |
| "It needs to be secure" | "Secure against what? Unauthorized access? Data leaks? Specific compliance?" |
| "No constraints really" | "If I built it as a 100GB desktop app requiring Windows, would that be fine?" |

### Round 4 — Data & State
7. **Data model**: "What are the key 'things' (entities) in the system and how do they relate?"

#### Probes
| Vague signal | Probe |
|---|---|
| "Just normal user data" | "List the fields you'd put on a user's profile page." |
| "It stores the results" | "What exactly is in a 'result'? Give me a concrete example." |
| "Standard stuff" | "Humor me — name the 3-5 most important data objects." |

### Round 5 — Success & Failure
8. **Success looks like**: "How will you know this is working correctly?"
9. **Failure looks like**: "What's the worst thing that could go wrong?"

#### Probes
| Vague signal | Probe |
|---|---|
| "Users are happy" | "What specific action would a happy user take that an unhappy one wouldn't?" |
| "It just works" | "Describe a test you'd run to prove it works." |
| "Nothing can really go wrong" | "What if the database is down? What if a user enters garbage?" |

---

## Brownfield Projects (modifying existing code)

Before asking questions, auto-scan the codebase:
- Read README, CLAUDE.md, package.json/pyproject.toml
- Identify tech stack, architecture patterns, entry points
- Map relevant modules/files

Then ask:

### Round 1 — The Delta
1. **What changes**: "What specific behavior should be different after this work?"
2. **What stays**: "What existing behavior must NOT change?"

#### Probes
| Vague signal | Probe |
|---|---|
| "Just add a small feature" | "Which screens/endpoints/files does it touch?" |
| "Fix the bug" | "What's the exact current behavior vs. expected behavior?" |
| "Refactor the code" | "What measurable improvement should the refactor produce?" |

### Round 2 — Impact & Risk
3. **Blast radius**: "What other parts of the system could this change affect?"
4. **Migration**: "Does this change require data migration or backwards compatibility?"

#### Probes
| Vague signal | Probe |
|---|---|
| "It's isolated" | "Does anything else import/call/depend on the code being changed?" |
| "No migration needed" | "Are there existing records in the database that would be affected?" |

### Round 3 — Acceptance
5. **Done means**: "How will you verify this change is complete and correct?"

---

## Quick Mode (fast rough spec)

Ask only:
1. One-liner (Round 1, Q1)
2. Core workflow (Round 2, Q3)

Then proceed directly to Phase 2 with explicit `[ASSUMPTION]` tags for everything else.
