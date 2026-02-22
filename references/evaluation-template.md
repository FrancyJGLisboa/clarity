# Evaluation Template

Use this structure for `.clarity/evaluations/eval-YYYY-MM-DD.md`.

---

```markdown
# Evaluation Report: {Project Name}

> Date: {YYYY-MM-DD}
> Spec version: {date of spec}
> Evaluator: /clarity Phase 5

## Summary

| Metric | Value |
|--------|-------|
| Total scenarios | {N} |
| Passed | {N} ({%}) |
| Failed | {N} ({%}) |
| Blocked | {N} ({%}) |

---

## Results

### ✅ Passed

| Scenario | Requirement | Notes |
|----------|-------------|-------|
| SC-001 | FR-001 | {brief note} |

### ❌ Failed

| Scenario | Requirement | Root Cause | Details |
|----------|-------------|------------|---------|
| SC-XXX | FR-XXX | {Spec Gap / Implementation Gap / Scenario Gap} | {explanation} |

### ⏸️ Blocked

| Scenario | Reason |
|----------|--------|
| SC-XXX | {why it couldn't be tested} |

---

## Root Cause Analysis

### Spec Gaps
{Requirements that were missing or ambiguous in the spec, causing implementation to diverge}

- **SC-XXX**: {what the spec should have said}

### Implementation Gaps
{Requirements that were clear in the spec but not correctly implemented}

- **SC-XXX**: {what the implementation got wrong}

### Scenario Gaps
{Scenarios that were poorly written, testing the wrong thing, or based on incorrect assumptions}

- **SC-XXX**: {what the scenario should have been}

---

## Recommendations

### Spec Updates Needed
- [ ] {spec change 1}
- [ ] {spec change 2}

### Implementation Fixes Needed
- [ ] {fix 1}
- [ ] {fix 2}

### Scenario Updates Needed
- [ ] {scenario change 1}

---

## Next Steps
{What should happen next — re-implement, update spec, re-evaluate, ship}
```

---

## Root Cause Classification Guide

| Category | Meaning | Action |
|----------|---------|--------|
| **Spec Gap** | The spec didn't cover this case or was ambiguous | Update spec, then re-implement |
| **Implementation Gap** | The spec was clear but code doesn't match | Fix the code |
| **Scenario Gap** | The scenario tested wrong behavior or had bad assumptions | Update the scenario |

### Decision Tree
1. Is the expected behavior described in the spec?
   - **No** → Spec Gap
   - **Yes** → continue
2. Does the code match what the spec says?
   - **No** → Implementation Gap
   - **Yes** → continue
3. Does the scenario accurately test what the spec says?
   - **No** → Scenario Gap
   - **Yes** → Investigate deeper (possible integration issue)
