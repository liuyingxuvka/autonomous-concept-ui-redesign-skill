# Changelog

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
