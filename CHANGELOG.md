# Changelog

## 0.1.3 - 2026-05-19

Added parent-owned final integrated acceptance.

- Added a final integrated acceptance gate before the final verdict so the
  orchestrator maps child-skill gates to evidence, freshness, status, and final
  verdict impact.
- Added explicit ledger statuses: `pass`, `accepted_deviation`,
  `skipped_with_reason`, `partial`, and `blocked`.
- Added hard downgrade rules so reviewer-only, FlowGuard-only, stale,
  untrusted screenshot, unresolved geometry, and in-UI-only app icon evidence
  cannot produce a final `pass`.
- Updated final reporting, visual QA, divergence review, and layout geometry QA
  references to feed the integrated acceptance ledger.
- Added a focused `.flowguard` regression check for final acceptance ledger
  behavior and known-bad downgrade hazards.
- Added a release-process FlowGuard check to keep validation evidence fresh
  before install sync, commit, tag, and GitHub release.

## 0.1.2 - 2026-05-18

Added conditional FlowGuard UI Flow Structure integration.

- Added a FlowGuard UI Structure Gate before concept search, image generation,
  or frontend implementation when behavior, hierarchy, state, overlay,
  navigation, display ownership, or duplicate-information/control risk exists.
- Required triggered runs to produce a UI interaction model, model-derived UI
  structure contract, duplicate information review, and duplicate same-level
  control review before visual work proceeds.
- Propagated the FlowGuard structure contract into concept briefs, final
  concept evaluation packages, frontend implementation briefs, iteration,
  deviation review, geometry QA, and final reporting.
- Added a focused `.flowguard` regression check for the skill contract and
  FlowGuard duplicate-detection behavior.

## 0.1.1 - 2026-05-11

Refined the concept-led UI workflow before implementation.

- Added explicit concept diagnosis and refinement gates for generated UI
  concept candidates.
- Added a reusable final concept evaluation package that carries function,
  hierarchy, density, color, background/foreground, accent/status, typography,
  spacing, state, and implementation-simplification decisions into UI
  iteration.
- Required screenshot comparison and deviation review to reuse the final
  concept evaluation package instead of relying only on bitmap similarity.
- Expanded color QA for background surfaces, foreground text, muted text,
  accents, selected/hover/focus states, success/warning/error states, and
  contrast risks.

## 0.1.0 - 2026-05-04

Initial standalone release of `autonomous-concept-ui-redesign`.

- Built the concept-led product/design front half directly into this skill.
- Included functional framing, concept brief, design search, divergence review,
  platform notes, visual QA, layout geometry QA, and final report references.
- Added app/software icon realization guidance and the transparent icon helper
  script.
- Preserved non-interactive orchestration with `frontend-design`,
  `design-iterator`, and `design-implementation-reviewer` companion skills.
- Removed any requirement for the older `concept-led-ui-redesign` skill.
