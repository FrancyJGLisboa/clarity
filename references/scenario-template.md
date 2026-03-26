# Scenario Template

Use this structure for each file in `scenarios/SC-NNN-slug.scenario.md`.

---

```markdown
# SC-{NNN}: {Short Title}

> Covers: {FR-XXX, NFR-XXX} — {requirement summary}
> Type: Happy Path | Edge Case | Failure | Security | Performance | Invalid Input | Missing Prerequisite

## Given
{Preconditions — system state before the action}
- {precondition 1}
- {precondition 2}

## When
{The action or trigger}
- {action 1}

## Then
{Expected outcomes — observable, testable}
- {outcome 1}
- {outcome 2}

## Verification Method
{Concrete, executable way to check this scenario — NOT abstract}

**Method**: {Manual test | Automated test | API call | CLI command | UI check | Log inspection}

**Steps**:
1. {Exact step to verify}
2. {Exact step to verify}

**Expected evidence**: {What you should see — exact output, status code, UI state, log line}
```

---

## Guidelines

### Coverage Rules
- Every `MUST` requirement → at least 1 happy path + 1 failure scenario
- Every `SHOULD` requirement → at least 1 happy path scenario
- Every edge case in the spec → 1 scenario
- Group related scenarios with consecutive numbers

### Harness Scenarios (mandatory)
Every skill must include at least:
- **2 Invalid Input scenarios** — pass malformed, negative, or out-of-bounds input. Expected: structured JSON error to stderr with `error_type: validation` and field-level details. NOT a stack trace.
- **1 Missing Prerequisite scenario** — simulate missing API key, unreachable network, or missing data source. Expected: structured JSON error with `error_type: runtime` and a `hint` field suggesting how to fix it.

These scenarios verify the skill's harness layer, not its business logic. They ensure the skill fails gracefully instead of crashing.

### Naming Convention
- `SC-001-user-login-success.scenario.md`
- `SC-002-user-login-wrong-password.scenario.md`
- `SC-003-user-login-account-locked.scenario.md`

### Writing Good Scenarios
- **Given**: Be specific about data state. Use concrete values, not "some data".
- **When**: One clear action. If you need multiple actions, split into multiple scenarios.
- **Then**: Observable outcomes only. Never "the system internally updates X" — instead "the API returns 200 with field Y = Z".
- **Verification**: Must be executable by someone with no context. Include exact commands, URLs, or UI paths.

### Anti-patterns to Avoid
- "Then the system works correctly" — not testable
- "Given a user exists" — which user? what attributes?
- "Verify it works" — how, specifically?
- Verification methods that require reading source code
