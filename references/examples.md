# Examples — Reference In, Spec Out

These show how `/clarity` transforms raw references into implementable specs autonomously.

---

## Example 1: GitHub repo + intent

### Input
```
/clarity https://github.com/someone/port-scheduler "add weather alerts before vessel arrival"
```

### What INGEST produces (context.md summary)

**Sources analyzed:**
- GitHub repo `someone/port-scheduler`: Python 3.12, FastAPI, PostgreSQL. Manages vessel ETAs per port. Has `models/vessel.py`, `models/port.py`, `routes/schedule.py`. No weather integration. Tests cover CRUD for schedules.
- Free text: user wants weather alerts before vessel arrival.

**Inferred intent:** Add a weather forecasting feature that sends email alerts to vessel operators 24-48h before their scheduled port arrival, leveraging the existing vessel schedule data.

**Assumptions:**
- [ASSUMPTION] Weather data from Open-Meteo API (free, no key required)
- [ASSUMPTION] Alerts via email (not SMS, not push)
- [ASSUMPTION] 24h before ETA is the alert trigger window
- [ASSUMPTION] Alert includes wind speed, wave height, visibility, precipitation
- [ASSUMPTION] PDF attachment for the forecast summary

### What SPECIFY produces (spec.md excerpt)

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-001 | Fetch 48h weather forecast for port coordinates from Open-Meteo API | MUST | Inferred from intent + existing port model has lat/lon |
| FR-002 | Generate PDF summary with wind, waves, visibility, precipitation | MUST | [ASSUMPTION] |
| FR-003 | Send email with PDF attachment 24h before vessel ETA | MUST | Inferred from intent |
| FR-004 | Retry failed email delivery 3x with exponential backoff | SHOULD | [ASSUMPTION] |
| FR-005 | Log all alert attempts with delivery status | SHOULD | Inferred from existing logging patterns in codebase |

---

## Example 2: Two repos (reference implementation + target)

### Input
```
/clarity https://github.com/someone/auth-service-v1 /path/to/our-api "rebuild auth like v1 but with JWT"
```

### What INGEST produces

**Sources analyzed:**
- GitHub repo `someone/auth-service-v1`: Node.js, Express, session-based auth with Redis. Has login, logout, password reset, role-based access (admin/user/viewer). 23 endpoints.
- Local codebase `/path/to/our-api`: Python, FastAPI, currently no auth. Has 12 endpoints, PostgreSQL, deployed on Render.
- Free text: rebuild auth like v1 but with JWT instead of sessions.

**Inferred intent:** Implement JWT-based authentication in the existing FastAPI app, replicating the feature set of the reference Node.js auth service (login, logout, password reset, RBAC) but using JWT tokens instead of server-side sessions.

**Key delta from reference:**
- Session + Redis → JWT + refresh tokens (no server-side state)
- Express middleware → FastAPI dependencies
- 3 roles preserved: admin, user, viewer

---

## Example 3: URL + codebase (API docs as reference)

### Input
```
/clarity https://stripe.com/docs/api/charges /path/to/my-saas "integrate Stripe payments"
```

### What INGEST produces

**Sources analyzed:**
- Stripe API docs: Charges API — create, retrieve, list, update charges. Requires API key. Supports idempotency keys. Webhooks for async events (charge.succeeded, charge.failed).
- Local codebase: Next.js SaaS app with user accounts, subscription tiers (free/pro/enterprise) defined in `config/plans.ts`, no payment integration yet.

**Inferred intent:** Integrate Stripe Charges API to handle payments for the existing subscription tiers, including checkout flow, webhook handling for payment confirmation, and subscription status tracking.

---

## Example 4: Quick mode

### Input
```
/clarity quick https://github.com/someone/csv-toolkit
```

### What happens
- Reads only: README + `pyproject.toml` + `src/main.py`
- Generates spec in ~2 minutes with 8+ `[ASSUMPTION]` tags
- User reviews assumptions, confirms or corrects
- Scenarios and handoff generated immediately after

---

## Example 5: Multiple URLs (research-driven spec)

### Input
```
/clarity https://linear.app https://github.com/makeplane/plane https://docs.github.com/en/issues "build a simpler project tracker"
```

### What INGEST produces

**Sources analyzed:**
- linear.app product page: Features — issues, cycles, projects, roadmaps, views, Git integration. Fast keyboard-driven UI. Opinionated workflow.
- Plane (open-source): Similar feature set, React + Django, modular architecture. Has cycles, modules, pages, analytics.
- GitHub Issues docs: Simple issue tracking with labels, milestones, assignees, projects. Limited workflow automation.
- Free text: "simpler" — user wants a subset, not a clone.

**Inferred intent:** Build a lightweight project tracker inspired by Linear's UX philosophy but scoped down — issues, labels, and a kanban board. No cycles, roadmaps, or Git integration in v1.

**Assumptions:**
- [ASSUMPTION] Web app (not desktop, not CLI)
- [ASSUMPTION] Single-team use (no multi-workspace)
- [ASSUMPTION] Core entities: Issue, Label, Board, Column
- [ASSUMPTION] "Simpler" means ~20% of Linear's feature set
