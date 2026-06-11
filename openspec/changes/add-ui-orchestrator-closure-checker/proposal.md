## Why

The autonomous UI redesign skill already requires a parent-owned final
acceptance ledger, but agents still need a small executable checker to catch
missing, stale, skipped, or downgrading rows before they claim completion.

## What Changes

- Add a lightweight closure checker for the final integrated acceptance ledger.
- Update the skill guidance so a structured ledger is checked before the final
  verdict when it exists.
- Extend the run report template with the checker output fields.

## Capabilities

### New Capabilities
- `ui-orchestrator-closure-checker`: Machine-readable final acceptance ledger
  checking for the autonomous UI redesign orchestrator.

### Modified Capabilities
- `final-integrated-acceptance`: Require checker use when a structured ledger is
  available.

## Impact

- Updates `autonomous-concept-ui-redesign/SKILL.md`.
- Updates `autonomous-concept-ui-redesign/references/run-report-template.md`.
- Adds `autonomous-concept-ui-redesign/scripts/ui_redesign_closure_check.py`.
