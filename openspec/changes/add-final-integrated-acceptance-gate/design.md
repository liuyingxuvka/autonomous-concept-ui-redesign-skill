## Context

`autonomous-concept-ui-redesign` composes several child skills and built-in
references. The previous release added a conditional FlowGuard UI Structure Gate
and propagates its structure contract through concept, implementation,
iteration, deviation review, geometry QA, and final reporting. That propagation
is necessary but not sufficient: the final stage must also decide whether each
child gate has current evidence and whether missing or skipped evidence should
downgrade the overall verdict.

## Goals / Non-Goals

**Goals:**

- Add a parent-owned final integrated acceptance gate before the final verdict.
- Make child-skill evidence obligations explicit without copying every child
  skill's full checklist into the parent skill.
- Require final acceptance to distinguish passed evidence, accepted deviations,
  justified skips, partial gaps, and blockers.
- Prevent `pass` when required FlowGuard, concept, implementation, iteration,
  deviation, geometry/screenshot, functional walkthrough, or app-icon evidence
  is missing or stale.
- Add executable regression evidence for the final acceptance contract and
  known-bad failure cases.

**Non-Goals:**

- Do not replace `flowguard-ui-flow-structure`, `frontend-design`,
  `design-iterator`, `design-implementation-reviewer`, Browser checks, or
  screenshot/geometry QA.
- Do not force full modeling for small visual-only work with a recorded safe
  skip reason.
- Do not introduce a runtime application, UI, or package dependency; this is a
  skill contract and regression-check update.
- Do not archive older OpenSpec changes unless separately requested.

## Decisions

1. Add the final integrated acceptance gate as a new stage after Geometry and
   Screenshot QA and before Final Verdict.

   Rationale: every child gate and every screenshot/geometry artifact should be
   final before the parent can decide completion.

   Alternative considered: fold this into the existing Final Verdict section.
   Rejected because report fields alone can look complete while child evidence
   remains stale, skipped, or unverified.

2. Use an acceptance ledger instead of duplicating all child-skill checklists.

   Rationale: child skills keep ownership of their detailed standards, while
   the parent skill owns final composition, evidence freshness, and downgrade
   rules.

   Alternative considered: paste FlowGuard, iterator, reviewer, and geometry
   checklists into the parent skill. Rejected because duplicated standards will
   drift and make maintenance harder.

3. Treat `pass`, `accepted_deviation`, `skipped_with_reason`, `partial`, and
   `blocked` as the only final ledger statuses.

   Rationale: these statuses force explicit distinction between true evidence,
   deliberate product/design decisions, safe skips, evidence gaps, and blockers.

   Alternative considered: simple yes/no fields. Rejected because "yes" can
   hide accepted deviations, stale evidence, or unrun checks.

4. Add hard downgrade rules.

   Rationale: a final `pass` must not be available when FlowGuard was triggered
   but not evidenced, when screenshots are untrusted, when geometry fails, when
   a concept is missing required workflows, or when app-icon identity is only
   shown inside the UI.

   Alternative considered: leave downgrade judgment to the agent. Rejected
   because the skill exists to make these checks repeatable.

5. Add focused FlowGuard-backed regression artifacts for the final acceptance
   gate and release-process evidence freshness.

   Rationale: this repository is mostly Markdown, so text-contract regressions
   and known-bad final acceptance cases need executable checks.

   Alternative considered: rely only on OpenSpec validation and manual review.
   Rejected because those checks do not prove child-gate evidence obligations
   remain present.

## Risks / Trade-offs

- [Risk] The final gate becomes too heavy for small visual-only edits.
  -> Mitigation: allow justified skips and make visual-only FlowGuard skips
  explicit.
- [Risk] The parent skill starts owning child-skill internals.
  -> Mitigation: the parent owns evidence status and final verdict only; child
  skills keep detailed standards.
- [Risk] Agents treat a filled ledger as proof even when evidence is stale.
  -> Mitigation: require evidence freshness and downgrade stale evidence to
  `partial` or `blocked`.
- [Risk] Release sync updates an old shadow copy incorrectly.
  -> Mitigation: sync whole skill directories after source validation and verify
  hashes for source, installed, and shadow copies.

## Migration Plan

1. Update OpenSpec specs and tasks for the new final acceptance capability.
2. Add the final acceptance gate and downgrade rules to the source skill.
3. Update reference files so final reporting, visual QA, divergence review, and
   geometry QA point to the integrated ledger.
4. Add FlowGuard-backed final acceptance and release-process regression checks
   with known-bad probes.
5. Update README, CHANGELOG, and VERSION.
6. Run OpenSpec, FlowGuard import, regression, text sync, and git-state checks.
7. Sync the source skill directory into installed and shadow local copies.
8. Commit, tag, push, and create the GitHub release.
