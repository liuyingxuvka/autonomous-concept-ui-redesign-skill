## Why

The autonomous UI redesign pipeline can currently preserve workflows through
functional framing and later visual QA, but it does not require a model-first
UI interaction structure before concept selection or implementation. Complex
redesigns need an upstream gate that turns buttons, states, displayed
information, hierarchy, and redundancy into an explicit contract before visual
work starts.

## What Changes

- Add a conditional FlowGuard UI Flow Structure gate between product/design
  framing and concept or implementation work.
- Require the gate to produce a UI interaction model and a model-derived UI
  structure contract when substantial UI behavior, hierarchy, state, menu, or
  information-ownership risk exists.
- Carry FlowGuard outputs into the concept brief, final concept evaluation
  package, frontend implementation brief, iterator checklist, deviation review,
  geometry QA, and final report.
- Define skip behavior for minor visual-only fixes so the pipeline does not
  over-model spacing, color, copy, or icon-only changes.
- Treat duplicate displayed information and duplicate same-level controls as
  explicit review obligations, allowing intentional redundancy only with a
  recorded rationale.

## Capabilities

### New Capabilities

- `flowguard-ui-structure-gate`: Conditional FlowGuard-backed UI interaction
  modeling, structure derivation, redundancy review, and downstream contract
  propagation for the autonomous redesign pipeline.

### Modified Capabilities

- None.

## Impact

- Updates `autonomous-concept-ui-redesign/SKILL.md`.
- Updates built-in references for functional framing, dependency mapping, and
  final reporting.
- Adds an OpenSpec change record and a focused FlowGuard model/check artifact
  for the skill-level workflow change.
- Updates README, CHANGELOG, and VERSION so the public repository and installed
  skill describe the new capability.
