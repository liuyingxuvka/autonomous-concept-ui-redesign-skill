## Why

The autonomous UI redesign skill already propagates FlowGuard UI structure,
concept selection, implementation, iteration, deviation review, geometry QA, and
app-icon evidence, but final completion is still mostly a report summary. A
parent-level final acceptance gate is needed so child-skill hard gates cannot be
lost, stale, skipped without reason, or treated as passed only because a final
report field exists.

## What Changes

- Add a final integrated acceptance gate owned by the autonomous redesign
  orchestrator.
- Require the final gate to build an evidence ledger for every required,
  conditional, skipped, accepted-deviation, partial, or blocked child-skill
  check.
- Add downgrade rules that prevent `pass` when required child-skill evidence is
  missing, stale, unresolved, or only recorded as a summary field.
- Extend final reporting, visual QA, divergence review, and geometry QA
  references so final acceptance cannot be replaced by screenshot-only,
  reviewer-only, or FlowGuard-only evidence.
- Add focused FlowGuard-backed regression checks for the integrated acceptance
  contract and known-bad hazards.

## Capabilities

### New Capabilities

- `final-integrated-acceptance`: Parent-owned final acceptance for composed UI
  redesign runs, including child-skill evidence obligations, skip reasons,
  stale-evidence checks, downgrade rules, and final `pass` / `partial` /
  `blocked` verdict mapping.

### Modified Capabilities

- None.

## Impact

- Updates `autonomous-concept-ui-redesign/SKILL.md`.
- Updates references for final reporting, visual QA, divergence review, and
  layout geometry QA.
- Adds focused FlowGuard regression artifacts for the final acceptance gate and
  release-process evidence freshness.
- Updates README, CHANGELOG, and VERSION for the new release.
- Syncs the source skill directory into the installed Codex skill directory and
  known local shadow copies after validation.
