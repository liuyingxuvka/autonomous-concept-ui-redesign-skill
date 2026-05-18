## Context

`autonomous-concept-ui-redesign` already has concept-led functional framing,
display-element review, concept search, implementation, iteration, deviation
review, geometry QA, and app-icon gates. The missing layer is an executable
model-first UI structure checkpoint before visual direction is chosen.

FlowGuard `v0.15.0` adds a dedicated UI Flow Structure route with interaction
models, structure derivations, duplicate information review, duplicate
same-level control review, stable region placement, overlays, and downstream
contracts. This change composes that route into the autonomous redesign
orchestrator without making FlowGuard responsible for visual style or frontend
implementation.

## Goals / Non-Goals

**Goals:**

- Add a conditional FlowGuard UI structure gate before concept search,
  imagegen, or frontend implementation.
- Make the gate produce a named UI interaction model, structure derivation, and
  downstream structure contract when triggered.
- Carry model-derived parent/child hierarchy, region ownership, menu level,
  stable placement, navigation ownership, display ownership, and redundancy
  rationale into later phases.
- Keep minor visual-only fixes lightweight by allowing a recorded skip reason.
- Add regression evidence that the skill text and references continue to expose
  this integration.

**Non-Goals:**

- Do not replace `frontend-design`, `design-iterator`,
  `design-implementation-reviewer`, Browser checks, image generation, or
  geometry QA.
- Do not require FlowGuard for pure spacing, color, typography, copy, or
  icon-only adjustments with no workflow or state risk.
- Do not add a new runtime dependency for users who only read the skill; the
  skill instructs Codex to use the installed FlowGuard capability when the gate
  is triggered.

## Decisions

1. Insert FlowGuard as a Stage 2.5 gate, after functional framing and before
   concept brief or implementation.

   Rationale: the gate needs product goals, actions, states, and display
   candidates from Stage 2, but it must run before visual concepts can lock in
   unstable structure.

   Alternative considered: run FlowGuard after implementation as QA. Rejected
   because it would catch structural mistakes after the expensive visual and
   code work already happened.

2. Make the gate conditional by route and risk, not universal.

   Rationale: large redesigns, multi-state workflows, menus, overlays, and
   duplicate-information concerns benefit from modeling. Tiny visual fixes do
   not.

   Alternative considered: always run the gate. Rejected because it would slow
   and over-formalize small visual work.

3. Treat FlowGuard output as a structure contract, not a visual direction.

   Rationale: FlowGuard should determine behavior topology, hierarchy,
   placement stability, event/control ownership, and information ownership.
   Visual language remains owned by the concept-led and frontend-design phases.

   Alternative considered: merge FlowGuard instructions into visual concept
   generation. Rejected because it would blur model obligations with aesthetic
   decisions and make failures harder to classify.

4. Add a local executable regression artifact for the skill text.

   Rationale: the repository is mostly Markdown, so regressions should check
   that required trigger rules, outputs, propagation targets, and final-report
   fields remain present.

   Alternative considered: rely on manual review only. Rejected because the
   change is a workflow contract and can silently regress through prose edits.

## Risks / Trade-offs

- [Risk] FlowGuard becomes a heavy step for small cosmetic work.
  -> Mitigation: specify skip conditions and require a recorded skip reason.
- [Risk] Downstream design phases ignore the model output.
  -> Mitigation: name the FlowGuard structure contract in the concept brief,
  implementation brief, iterator checklist, deviation review, geometry QA, and
  final verdict.
- [Risk] Users confuse FlowGuard with visual design generation.
  -> Mitigation: state that FlowGuard owns structure and redundancy checks, not
  palette, typography, bitmap concepts, or frontend code.
- [Risk] Installed skill drifts from the source repository.
  -> Mitigation: sync the edited skill directory into
  `$CODEX_HOME/skills/autonomous-concept-ui-redesign` and verify both copies.

## Migration Plan

1. Update source skill instructions and references.
2. Add focused FlowGuard-backed regression checks for the skill contract.
3. Update README, CHANGELOG, and VERSION.
4. Copy the source skill directory to the installed Codex skills directory.
5. Run OpenSpec, FlowGuard import, skill-text, and git-state validations.
6. Commit, tag, and push the repository after validation passes.
