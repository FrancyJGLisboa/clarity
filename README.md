# /clarity

An agent skill that generates implementable specs from reference material — repos, URLs, codebases, docs. You point it at sources. It does the hard thinking.

Works with **Claude Code**, **GitHub Copilot CLI**, **Copilot in VS Code**, and any tool that supports the [Agent Skills standard](https://agentskills.io).

The bottleneck in AI-assisted development isn't implementation speed — it's spec quality. Most people can't write specs detailed enough for autonomous AI implementation. This skill removes that bottleneck: you provide references, the AI generates the spec.

## What it does

5 phases, each producing a concrete artifact:

| Phase | What happens | Output |
|-------|-------------|--------|
| **1. INGEST** | Reads all your references (repos, URLs, code, docs) and extracts everything | `.clarity/context.md` |
| **2. SPECIFY** | Writes a structured spec from what it ingested | `.clarity/spec.md` |
| **3. SCENARIO** | Generates Given/When/Then behavioral scenarios (holdout set) | `scenarios/SC-NNN-*.md` |
| **4. HANDOFF** | Creates a self-contained prompt for any AI coding agent | `.clarity/handoff.md` |
| **5. EVALUATE** | After implementation, tests code against holdout scenarios | `.clarity/evaluations/eval-*.md` |

The key trick: scenarios are a **holdout set** — the implementing agent never sees them. This lets you independently verify whether the implementation matches the spec.

## Install

### Claude Code (personal skill)

```bash
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.claude/skills/clarity
```

Then use `/clarity` in any project.

### GitHub Copilot CLI (personal skill)

```bash
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.copilot/skills/clarity
```

Then use `/clarity` in any project.

### Per-project (any tool)

Copy into your repo so all contributors get it:

```bash
# Works with Copilot, Claude Code, and other agentskills.io-compatible tools
git clone https://github.com/FrancyJGLisboa/clarity.git .github/skills/clarity
```

Or add as a submodule:

```bash
git submodule add https://github.com/FrancyJGLisboa/clarity.git .github/skills/clarity
```

### VS Code — Copilot prompt file

For VS Code users who prefer prompt files, copy just the prompt:

```bash
mkdir -p .github/prompts
cp .github/skills/clarity/prompts/clarity.prompt.md .github/prompts/
```

Then type `/clarity` in Copilot Chat (agent mode).

## Usage

Point it at anything — GitHub repos, local codebases, URLs, docs:

**Claude Code / Copilot CLI:**
```
/clarity https://github.com/someone/repo
/clarity /path/to/codebase
/clarity https://github.com/someone/repo https://docs.example.com/api "add payment processing"
/clarity quick https://github.com/someone/repo
/clarity resume
/clarity evaluate
/clarity update
```

**VS Code Copilot (agent mode):**
Type `/clarity` in chat, then describe your references in the input prompt.

On first run, it creates two directories in your project:

```
your-project/
├── .clarity/        # specs, context, handoff, evaluations
└── scenarios/       # holdout test scenarios (agents must not read these)
```

You can also initialize these manually:

```bash
python scripts/init_project.py
```

## Updating

Already have clarity installed? Pull the latest version and pick up new companion skills:

```
/clarity update
```

This pulls the latest from GitHub, shows what changed, and automatically links any new companion skills (like `/linear-walkthrough`).

You can also run it directly from the terminal:

```bash
python ~/.claude/skills/clarity/scripts/update.py
```

## Getting Started — VS Code + GitHub Copilot

### Prerequisites

1. **VS Code** — [Download](https://code.visualstudio.com/) if you don't have it
2. **GitHub Copilot extension** — Install from the Extensions sidebar (`Ctrl+Shift+X` / `Cmd+Shift+X`), search "GitHub Copilot"
3. **GitHub Copilot Chat** — Installed automatically with the Copilot extension
4. **Active Copilot subscription** — Free, Pro, or Enterprise (agent mode requires Copilot Chat)

### Step 1: Enable Agent Mode

Agent mode lets Copilot use skills, run commands, and edit files autonomously.

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for `chat.agent.enabled`
3. Check the box to enable it
4. Restart VS Code

You'll know it's working when the Copilot Chat panel shows a mode dropdown at the top — switch it from **"Ask"** or **"Edit"** to **"Agent"**.

### Step 2: Install /clarity (once, works in every project)

You only need to do this once. After setup, `/clarity` is available in any VS Code project.

**Option A — No terminal needed (recommended)**

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open the Command Palette
2. Type **"Chat: New Prompt File"** and select it
3. Choose **"User"** (not "Workspace") — this makes it global
4. Name the file `clarity`
5. VS Code opens the new file. Replace its contents with the prompt from:
   `https://raw.githubusercontent.com/FrancyJGLisboa/clarity/main/prompts/clarity.prompt.md`
6. Save (`Ctrl+S`)

Done. `/clarity` now works in every project you open.

> The file is saved to your VS Code user data folder. You don't need to know where — VS Code manages it. If you use [Settings Sync](https://code.visualstudio.com/docs/editor/settings-sync), it syncs across your machines automatically.

**Option B — Terminal install (full skill with all reference files)**

This gives Copilot access to the complete skill including analysis playbooks, templates, and examples.

First, open a terminal in VS Code (`` Ctrl+` ``).

> **Windows terminal tip:** Your terminal prompt tells you which shell you're in:
> - `PS C:\Users\...>` → **PowerShell** (default, works fine)
> - `C:\Users\...>` → **Command Prompt** (also works)
> - `user@machine:` → **Git Bash / WSL** (also works)
>
> All three work for the commands below. If `git` is not recognized, [download Git for Windows](https://git-scm.com/download/win) and restart VS Code.

Clone to a permanent location on your machine:

```bash
# Windows (PowerShell or Command Prompt)
git clone https://github.com/FrancyJGLisboa/clarity.git %USERPROFILE%\.clarity-skill

# macOS / Linux
git clone https://github.com/FrancyJGLisboa/clarity.git ~/.clarity-skill
```

Then tell VS Code where to find the prompt files. Open your user settings JSON (`Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)") and add:

```json
{
  "chat.promptFilesLocations": {
    ".github/prompts": true,
    "C:\\Users\\YourName\\.clarity-skill\\prompts": true
  }
}
```

Replace `YourName` with your actual Windows username. On macOS/Linux use `"/Users/you/.clarity-skill/prompts"` or `"/home/you/.clarity-skill/prompts"`.

> **Why Option B?** The prompt file in Option A is lightweight — it tells Copilot the 5-phase workflow. Option B also gives Copilot the full reference files (analysis playbooks, spec templates, scenario templates, examples) which produce richer specs.

### Step 3: Use /clarity

Open any project in VS Code, then:

1. Open the **Copilot Chat** panel (`Ctrl+Shift+I` / `Cmd+Shift+I`)
2. Switch to **Agent** mode using the dropdown at the top of the chat panel
3. Type `/clarity` followed by your references

**Example prompts:**

```
/clarity https://github.com/someone/repo
```
Generates a full spec from a GitHub repository.

```
/clarity https://github.com/someone/repo https://docs.example.com/api
```
Combines a repo and its API docs into one spec.

```
/clarity C:\Users\YourName\projects\my-app "add user authentication with OAuth"
```
Analyzes a local project and generates a spec for a new feature. On macOS/Linux use `/path/to/project` instead.

```
/clarity quick https://github.com/someone/repo
```
Fast mode — less analysis depth, more assumptions, same output structure.

### Step 4: Review the outputs

After /clarity runs, you'll find these files in your project:

```
your-project/
├── .clarity/
│   ├── context.md      ← What was extracted from your references
│   ├── spec.md          ← The structured specification (FR-001, NFR-001, ...)
│   └── handoff.md       ← Ready-to-use prompt for any AI coding agent
└── scenarios/
    └── SC-001-*.md      ← Holdout test scenarios (don't share with coding agents)
```

The skill pauses after each phase so you can review and give feedback before it continues.

### Step 5: Hand off to implementation

Copy the contents of `.clarity/handoff.md` and paste it into a new Copilot Agent chat (or any AI coding tool). The handoff is self-contained — it has everything the implementing agent needs.

After implementation, come back and run:

```
/clarity evaluate
```

This tests the code against the holdout scenarios the implementing agent never saw.

### Tips

- **Resume interrupted sessions** — Type `/clarity resume` to pick up where you left off
- **Add to .gitignore** — You may want to add `.clarity/` and `scenarios/` to `.gitignore` if you don't want specs in version control
- **Share with your team** — If you used Option A (skill folder), commit `.github/skills/clarity/` so all contributors get `/clarity` automatically
- **Keep scenarios secret** — The `scenarios/` folder is a holdout set. Never include it in implementation prompts — that's what makes evaluation meaningful

## How it handles different sources

| Source type | What gets extracted |
|-------------|---------------------|
| **GitHub repo** | Architecture, tech stack, data models, API surface, test expectations, gaps |
| **Local codebase** | Same + git history, uncommitted work, env config |
| **API docs URL** | Endpoints, schemas, auth, rate limits, error codes |
| **Product page URL** | Features, target users, UX flows |
| **Blog/tutorial URL** | Architecture decisions, patterns, trade-offs |
| **Free text** | Intent, constraints, priorities, anti-goals |

## Compatibility

This skill follows the [Agent Skills standard](https://agentskills.io) and works with:

| Tool | Install path | Invocation |
|------|-------------|------------|
| Claude Code | `~/.claude/skills/clarity/` | `/clarity` |
| Copilot CLI | `~/.copilot/skills/clarity/` | `/clarity` |
| Copilot VS Code | `.github/skills/clarity/` or `.github/prompts/` | `/clarity` in chat |
| Cursor | `.github/skills/clarity/` | `/clarity` |
| Gemini CLI | `~/.agents/skills/clarity/` | `/clarity` |
| Any agentskills.io tool | `.github/skills/clarity/` | Varies |

## Companion Skills

### /linear-walkthrough

The opposite of `/clarity`: while clarity turns references into specs for *building*, linear-walkthrough reads existing code and produces a walkthrough for *understanding*.

Based on Simon Willison's "Linear Walkthroughs" pattern — the key innovation is that **every code snippet is extracted via shell commands**, never manually typed, eliminating hallucination risk.

**Install (one extra symlink):**

```bash
# If clarity is already installed at ~/.claude/skills/clarity:
ln -s ~/.claude/skills/clarity/linear-walkthrough ~/.claude/skills/linear-walkthrough
```

Or install companions automatically:

```bash
uv run ~/.claude/skills/clarity/scripts/init_project.py --install-companions
```

**Usage:**

```
/linear-walkthrough /path/to/codebase
/linear-walkthrough https://github.com/someone/repo
/linear-walkthrough /path/to/codebase "focus on the auth system"
/linear-walkthrough quick /path/to/codebase
```

**Examples:**

Onboard yourself to an unfamiliar repo:
```
/linear-walkthrough ~/projects/billing-service
```
→ Produces `billing-service/walkthrough.md` — a file-by-file explanation starting from the entry point, through core domain logic, down to config and infrastructure.

Understand just one subsystem:
```
/linear-walkthrough ~/projects/billing-service "focus on the webhook handlers"
```
→ Same format, but scoped to webhook-related files only.

Quick orientation on a GitHub repo before contributing:
```
/linear-walkthrough quick https://github.com/psf/black
```
→ Clones to `/tmp`, produces a high-level overview (README summary, tech stack, entry point walkthrough) in your current directory, then cleans up.

Every code block in the output includes a provenance comment showing the shell command that extracted it:
```python
# $ sed -n '42,58p' src/core/engine.py
def process(self, event: Event) -> Result:
    validated = self.validator.check(event)
    ...
```
You can re-run any command to verify the snippet is real — zero hallucination risk.

| Skill | Direction | Use when |
|-------|-----------|----------|
| `/clarity` | References → Spec | You want to build something new |
| `/linear-walkthrough` | Code → Walkthrough | You want to understand existing code |

## Troubleshooting

### SSL certificate error when cloning

If you get:
```
fatal: unable to access 'https://github.com/...': SSL certificate problem: unable to get local issuer certificate
```

**Update CA certificates (recommended fix):**

```bash
# macOS
brew install ca-certificates

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ca-certificates

# Windows
git update-git-for-windows
```

**Point Git to the correct CA bundle:**

```bash
# macOS with Homebrew
git config --global http.sslCAInfo /usr/local/etc/openssl/cert.pem

# Linux
git config --global http.sslCAInfo /etc/ssl/certs/ca-certificates.crt
```

**Behind a corporate proxy/VPN:**

Your proxy may intercept HTTPS with its own certificate. Add the corporate CA cert:
```bash
git config --global http.sslCAInfo /path/to/corporate-ca-bundle.crt
```

**Quick workaround (temporary only):**

```bash
git config --global http.sslVerify false
```

> ⚠️ This disables SSL verification entirely. Use only to unblock yourself, then fix the root cause above.

## Files

```
clarity/
├── SKILL.md                    # Main skill prompt (agentskills.io format)
├── prompts/
│   └── clarity.prompt.md       # VS Code Copilot prompt file
├── references/
│   ├── analysis-playbook.md    # How to extract info from each source type
│   ├── spec-template.md        # Spec structure (numbered FRs/NFRs)
│   ├── scenario-template.md    # Given/When/Then format
│   ├── handoff-template.md     # Implementation prompt template
│   ├── evaluation-template.md  # Pass/fail report template
│   └── examples.md             # Reference in → spec out examples
├── linear-walkthrough/         # Companion skill: /linear-walkthrough
│   ├── SKILL.md                # Skill prompt
│   └── references/
│       └── walkthrough-template.md
└── scripts/
    └── init_project.py         # Project initializer (stdlib only, idempotent)
```
