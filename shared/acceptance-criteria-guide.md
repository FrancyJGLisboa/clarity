# Acceptance Criteria Guide

When generating `priority_analyses` in the skill brief, populate `acceptance_criteria` for each command so the BUILD evaluator can verify scripts immediately after generation.

## Rules

- **smoke_input**: A minimal valid CLI invocation. Use the simplest possible input that exercises the command's core path. Example: `./skill-name price --commodity soybean --date 2024-01-15`
- **smoke_output_contains**: List 1-3 strings the output must contain (field names, expected JSON keys, format markers). Keep it structural, not value-dependent. Example: `["commodity", "price", "date"]`
- **smoke_output_is_json**: Set `true` for any command that promises JSON output to stdout.
- **smoke_exit_code**: Default 0 (success). Set to 1 when the smoke test deliberately triggers an expected error (e.g., missing API key) to verify graceful failure.

## When API keys are unavailable at build time

If a command requires an API key that won't be present during BUILD:
- Set `smoke_exit_code: 1`
- Set `smoke_output_contains: ["error", "hint"]`
- This verifies the command fails gracefully with a structured error, not a crash.

## What NOT to put in acceptance criteria

- Domain logic correctness (that belongs in holdout scenarios)
- Exact output values (outputs change with data)
- Holdout scenario content (sacred separation)

Acceptance criteria verify the script **runs**. Holdout scenarios verify the script **does the right thing**.
