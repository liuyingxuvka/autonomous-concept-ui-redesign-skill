## ADDED Requirements

### Requirement: Parent-owned integrated acceptance ledger
The autonomous redesign orchestrator SHALL build a final integrated acceptance
ledger before declaring the final verdict. The ledger MUST cover every
applicable child-skill gate and built-in QA phase that contributed to the run,
including FlowGuard UI structure, concept search/readiness, frontend
implementation, design iteration, deviation review, functional walkthrough,
geometry/screenshot QA, content/localization, motion/assets, and app-icon
realization when applicable.

#### Scenario: Complete run reaches final verdict
- **WHEN** an autonomous redesign run reaches final acceptance
- **THEN** the final verdict includes a ledger row for each required,
  conditional, skipped, partial, blocked, or accepted-deviation gate

#### Scenario: Child gate was not applicable
- **WHEN** a child gate is not applicable to the route or target surface
- **THEN** the ledger records `skipped_with_reason` with the route-specific
  reason instead of silently omitting the gate

### Requirement: Evidence status vocabulary
The final integrated acceptance ledger SHALL use explicit statuses:
`pass`, `accepted_deviation`, `skipped_with_reason`, `partial`, or `blocked`.
Each non-skipped row MUST name its evidence source, evidence freshness, and
impact on the final verdict.

#### Scenario: Deviation is accepted
- **WHEN** the implementation diverges from a concept or baseline for a recorded
  product, accessibility, content-density, or design-system reason
- **THEN** the ledger records `accepted_deviation` and states why the deviation
  does not weaken the final verdict

#### Scenario: Evidence is missing
- **WHEN** a required gate has no current evidence
- **THEN** the ledger records `partial` or `blocked`, not `pass`

### Requirement: Hard downgrade rules
The final integrated acceptance gate SHALL downgrade the final verdict from
`pass` to `partial` or `blocked` when required evidence is missing, stale,
contradictory, or structurally insufficient.

#### Scenario: FlowGuard evidence is missing
- **WHEN** the FlowGuard UI Structure Gate was triggered but lacks current model
  evidence, structure contract evidence, journey coverage for complete app-level
  UI claims, text hierarchy blueprint, implementation validation for
  implemented/runnable UI claims, revalidation notes after structural drift, or
  duplicate information/control decisions
- **THEN** the final verdict is `partial` or `blocked`

#### Scenario: Screenshot or geometry proof is insufficient
- **WHEN** rendered evidence is missing, untrusted, wrong-surface, stale, or
  shows unresolved overlap, clipping, unreachable controls, popup bounds
  failures, or hidden required controls
- **THEN** the final verdict is `partial` or `blocked`

#### Scenario: App icon identity is only in UI content
- **WHEN** an app/software icon gate applies but the selected identity is only
  shown inside the UI and not bound to platform identity surfaces
- **THEN** the final verdict is `partial` or `blocked`

### Requirement: Child-skill standards remain authoritative
The final integrated acceptance gate SHALL reference child-skill completion
standards without duplicating their full internal checklists. The parent skill
MUST decide composition and final verdict; child skills keep ownership of
detailed standards.

#### Scenario: Reviewer output exists
- **WHEN** `design-implementation-reviewer` reports visual alignment but the
  FlowGuard structure contract has stale or missing evidence
- **THEN** the final gate does not treat reviewer output alone as enough for
  overall `pass`

#### Scenario: FlowGuard passes
- **WHEN** FlowGuard structure evidence passes but concept, implementation,
  geometry, or screenshot evidence is missing
- **THEN** the final gate does not treat FlowGuard alone as enough for overall
  `pass`
