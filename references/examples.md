# Examples — Before & After

These show how `/clarity` transforms vague ideas into implementable specs.

---

## Example 1: "I want a weather alert system"

### Before (what the user says)
> "I want something that sends weather alerts to ship captains before they arrive at port."

### After Phase 1 (extracted context)
- **One-liner**: A system that emails maritime weather forecasts to vessel operators 24-48h before port arrival
- **Primary user**: Port operations coordinators and ship captains
- **Core workflow**: System ingests vessel schedule (ETA) → fetches weather forecast for port coordinates at ETA time → generates PDF report → emails to captain and operations team
- **Key constraints**: Must use free weather APIs; emails via Resend; deployed on Render
- **Must NOT do**: Real-time tracking, route optimization, cargo management
- **Success**: Captain receives accurate forecast PDF 24h before arrival
- **Failure**: Alert not sent (silent failure), forecast wildly inaccurate

### After Phase 2 (spec excerpt)

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System accepts vessel schedule with port, ETA, and recipient email | MUST |
| FR-002 | System fetches 48h weather forecast for port coordinates from Open-Meteo API | MUST |
| FR-003 | System generates PDF summary with wind speed, wave height, visibility, precipitation | MUST |
| FR-004 | System sends email with PDF attachment 24h before ETA | MUST |
| FR-005 | System retries failed email delivery up to 3 times with exponential backoff | SHOULD |
| NFR-001 | Forecast fetch completes in < 5 seconds | SHOULD |
| NFR-002 | PDF generation completes in < 10 seconds | SHOULD |

### After Phase 3 (scenario excerpt)
```
# SC-001: Successful weather alert delivery

> Covers: FR-001, FR-002, FR-003, FR-004
> Type: Happy Path

## Given
- Vessel "MV Example" has ETA at Port of Santos (lat: -23.95, lon: -46.30) on 2024-03-15 08:00 UTC
- Recipient email is captain@example.com
- Open-Meteo API is available and returning data

## When
- System checks for upcoming arrivals within 24-48h window
- Current time is 2024-03-14 08:00 UTC (24h before ETA)

## Then
- Email is sent to captain@example.com
- Email subject contains "MV Example" and "Santos"
- Email has PDF attachment
- PDF contains wind speed, wave height, visibility for 2024-03-15 06:00-12:00 UTC

## Verification Method
**Method**: API call + email inspection
**Steps**:
1. Insert test vessel schedule via API
2. Trigger the check job manually
3. Verify email was sent via Resend dashboard or API logs
**Expected evidence**: Resend API shows delivered email with PDF attachment > 0 bytes
```

---

## Example 2: "Add dark mode to the dashboard"

### Before (what the user says)
> "Can you add dark mode to our admin dashboard?"

### After Phase 1 (extracted context — brownfield)

**Codebase scan reveals**: React 18 + Tailwind CSS + shadcn/ui dashboard. Theme currently hardcoded to light. No CSS custom properties for colors. 47 components in `src/components/`.

- **What changes**: All UI components support light/dark theme toggle
- **What stays**: All existing functionality, layout, data display
- **Blast radius**: Every component that uses hardcoded colors (32 of 47)
- **Migration**: None (UI-only change)
- **Done means**: User can toggle dark/light mode; preference persists across sessions

### After Phase 2 (spec excerpt — brownfield delta)

**Current State**: Colors hardcoded via Tailwind classes (`bg-white`, `text-gray-900`). No theme provider.

**Delta**:

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Add theme toggle button in the top navigation bar | MUST |
| FR-002 | Implement dark color palette using Tailwind's `dark:` variant | MUST |
| FR-003 | Persist theme preference in localStorage | MUST |
| FR-004 | Respect OS-level color scheme preference on first visit | SHOULD |
| FR-005 | Theme transition uses 150ms fade (no flash of wrong theme) | SHOULD |

**Must NOT change**: Component layout, data fetching logic, routing, API calls.

---

## Example 3: Quick Mode

### Before
> "A CLI tool that converts CSV to JSON"

### After Quick Mode (2 questions only)
**One-liner**: CLI tool that reads a CSV file and outputs JSON
**Core workflow**: User runs `csv2json input.csv` → tool reads CSV → outputs JSON to stdout (or `-o file.json`)

**Spec** (with explicit assumptions):

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | Accept CSV file path as positional argument | MUST | |
| FR-002 | Output JSON array of objects to stdout | MUST | |
| FR-003 | Support `-o` flag for file output | MUST | [ASSUMPTION] |
| FR-004 | Auto-detect CSV delimiter (comma, semicolon, tab) | SHOULD | [ASSUMPTION] |
| FR-005 | Handle UTF-8 encoding | MUST | [ASSUMPTION] |
| FR-006 | Exit with error code 1 and message on invalid CSV | MUST | [ASSUMPTION] |

> 4 assumptions flagged — user can review and adjust before handoff.
