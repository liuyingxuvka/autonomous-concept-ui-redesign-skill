"""Regression checks for the final integrated acceptance gate."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

import flowguard


ROOT = Path(__file__).resolve().parents[2]

STATUS_PASS = "pass"
STATUS_ACCEPTED_DEVIATION = "accepted_deviation"
STATUS_SKIPPED_WITH_REASON = "skipped_with_reason"
STATUS_PARTIAL = "partial"
STATUS_BLOCKED = "blocked"

VERDICT_PASS = "pass"
VERDICT_PARTIAL = "partial"
VERDICT_BLOCKED = "blocked"


@dataclass(frozen=True)
class GateRequirement:
    gate_id: str
    required_when_triggered: bool
    triggered: bool
    skip_allowed: bool = False


@dataclass(frozen=True)
class GateEvidence:
    gate_id: str
    status: str
    evidence_ref: str = ""
    fresh: bool = True
    rationale: str = ""
    affects_final: bool = True


@dataclass(frozen=True)
class AcceptanceState:
    requirements: tuple[GateRequirement, ...]
    evidence: tuple[GateEvidence, ...] = ()


@dataclass(frozen=True)
class EvidenceInput:
    gate_id: str
    status: str
    evidence_ref: str = ""
    fresh: bool = True
    rationale: str = ""
    affects_final: bool = True


@dataclass(frozen=True)
class AcceptanceOutput:
    gate_id: str
    accepted: bool
    finding: str


VALID_STATUSES = {
    STATUS_PASS,
    STATUS_ACCEPTED_DEVIATION,
    STATUS_SKIPPED_WITH_REASON,
    STATUS_PARTIAL,
    STATUS_BLOCKED,
}


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _require_snippets(relative: str, snippets: tuple[str, ...]) -> None:
    text = _read(relative)
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        joined = "\n".join(f"- {snippet}" for snippet in missing)
        raise AssertionError(f"{relative} is missing required snippets:\n{joined}")


def apply_evidence(
    event: EvidenceInput, state: AcceptanceState
) -> set[tuple[AcceptanceOutput, AcceptanceState]]:
    """Model block: EvidenceInput x AcceptanceState -> Set(Output x State)."""

    if event.status not in VALID_STATUSES:
        output = AcceptanceOutput(event.gate_id, False, "unknown_status")
        return {(output, state)}

    requirement = next(
        (item for item in state.requirements if item.gate_id == event.gate_id),
        None,
    )
    if requirement is None:
        output = AcceptanceOutput(event.gate_id, False, "unknown_gate")
        return {(output, state)}

    evidence = GateEvidence(
        event.gate_id,
        event.status,
        event.evidence_ref,
        event.fresh,
        event.rationale,
        event.affects_final,
    )
    next_evidence = tuple(
        item for item in state.evidence if item.gate_id != event.gate_id
    ) + (evidence,)
    output = AcceptanceOutput(event.gate_id, True, "recorded")
    return {(output, replace(state, evidence=next_evidence))}


def _evidence_for(state: AcceptanceState, gate_id: str) -> GateEvidence | None:
    return next((item for item in state.evidence if item.gate_id == gate_id), None)


def final_verdict(state: AcceptanceState) -> str:
    blocking = False
    partial = False

    for requirement in state.requirements:
        evidence = _evidence_for(state, requirement.gate_id)
        gate_required = requirement.triggered and requirement.required_when_triggered

        if evidence is None:
            if gate_required:
                partial = True
            continue

        if not evidence.affects_final:
            continue

        if evidence.status == STATUS_BLOCKED:
            blocking = True
            continue
        if evidence.status == STATUS_PARTIAL:
            partial = True
            continue
        if evidence.status == STATUS_SKIPPED_WITH_REASON:
            if gate_required and not requirement.skip_allowed:
                partial = True
            if not evidence.rationale:
                partial = True
            continue
        if evidence.status == STATUS_ACCEPTED_DEVIATION:
            if not evidence.evidence_ref or not evidence.rationale or not evidence.fresh:
                partial = True
            continue
        if evidence.status == STATUS_PASS:
            if not evidence.evidence_ref or not evidence.fresh:
                partial = True

    if blocking:
        return VERDICT_BLOCKED
    if partial:
        return VERDICT_PARTIAL
    return VERDICT_PASS


def _base_requirements() -> tuple[GateRequirement, ...]:
    return (
        GateRequirement("flowguard_ui_structure", True, True),
        GateRequirement("concept_readiness", True, True),
        GateRequirement("frontend_implementation", True, True),
        GateRequirement("design_iteration", False, True, skip_allowed=True),
        GateRequirement("deviation_review", True, True),
        GateRequirement("functional_walkthrough", True, True),
        GateRequirement("geometry_screenshot_qa", True, True),
        GateRequirement("content_localization", False, True, skip_allowed=True),
        GateRequirement("motion_assets", False, True, skip_allowed=True),
        GateRequirement("app_icon_realization", True, False, skip_allowed=True),
    )


def _apply_all(
    state: AcceptanceState, events: Iterable[EvidenceInput]
) -> AcceptanceState:
    current = state
    for event in events:
        transitions = apply_evidence(event, current)
        if len(transitions) != 1:
            raise AssertionError("Acceptance model must be deterministic")
        output, current = next(iter(transitions))
        if not output.accepted:
            raise AssertionError(output.finding)
    return current


def _pass_events() -> tuple[EvidenceInput, ...]:
    return (
        EvidenceInput("flowguard_ui_structure", STATUS_PASS, "fg-model-v1"),
        EvidenceInput("concept_readiness", STATUS_PASS, "concept-package-v1"),
        EvidenceInput("frontend_implementation", STATUS_PASS, "first-render.png"),
        EvidenceInput(
            "design_iteration",
            STATUS_SKIPPED_WITH_REASON,
            rationale="first render already met the contract",
        ),
        EvidenceInput("deviation_review", STATUS_PASS, "review-report.md"),
        EvidenceInput("functional_walkthrough", STATUS_PASS, "walkthrough-matrix"),
        EvidenceInput("geometry_screenshot_qa", STATUS_PASS, "geometry-report.json"),
        EvidenceInput(
            "content_localization",
            STATUS_SKIPPED_WITH_REASON,
            rationale="no real copy or localization surface changed",
        ),
        EvidenceInput(
            "motion_assets",
            STATUS_SKIPPED_WITH_REASON,
            rationale="no motion or asset surface changed",
        ),
        EvidenceInput(
            "app_icon_realization",
            STATUS_SKIPPED_WITH_REASON,
            rationale="web component has no app identity surface",
        ),
    )


def check_acceptance_model() -> None:
    good_state = _apply_all(AcceptanceState(_base_requirements()), _pass_events())
    if final_verdict(good_state) != VERDICT_PASS:
        raise AssertionError("Complete fresh evidence should pass")

    missing_flowguard = _apply_all(
        AcceptanceState(_base_requirements()),
        (
            event
            for event in _pass_events()
            if event.gate_id != "flowguard_ui_structure"
        ),
    )
    if final_verdict(missing_flowguard) == VERDICT_PASS:
        raise AssertionError("Missing triggered FlowGuard evidence must not pass")

    stale_flowguard = _apply_all(
        AcceptanceState(_base_requirements()),
        (
            replace(event, fresh=False)
            if event.gate_id == "flowguard_ui_structure"
            else event
            for event in _pass_events()
        ),
    )
    if final_verdict(stale_flowguard) == VERDICT_PASS:
        raise AssertionError("Stale FlowGuard evidence must not pass")

    reviewer_only = _apply_all(
        AcceptanceState(_base_requirements()),
        (EvidenceInput("deviation_review", STATUS_PASS, "review-report.md"),),
    )
    if final_verdict(reviewer_only) == VERDICT_PASS:
        raise AssertionError("Reviewer-only evidence must not pass")

    untrusted_screenshot = _apply_all(
        AcceptanceState(_base_requirements()),
        (
            replace(event, status=STATUS_PARTIAL, rationale="wrong foreground app")
            if event.gate_id == "geometry_screenshot_qa"
            else event
            for event in _pass_events()
        ),
    )
    if final_verdict(untrusted_screenshot) == VERDICT_PASS:
        raise AssertionError("Partial screenshot/geometry evidence must not pass")

    app_icon_blocked = _apply_all(
        AcceptanceState(
            tuple(
                replace(item, triggered=True)
                if item.gate_id == "app_icon_realization"
                else item
                for item in _base_requirements()
            )
        ),
        (
            replace(
                event,
                status=STATUS_BLOCKED,
                evidence_ref="in-ui-logo-only",
                rationale="identity not bound to platform surfaces",
            )
            if event.gate_id == "app_icon_realization"
            else event
            for event in _pass_events()
        ),
    )
    if final_verdict(app_icon_blocked) != VERDICT_BLOCKED:
        raise AssertionError("App icon identity blocker should block final pass")


def check_skill_text() -> None:
    _require_snippets(
        "autonomous-concept-ui-redesign/SKILL.md",
        (
            "### 6.5 Final Integrated Acceptance Gate",
            "final acceptance ledger",
            "implementation validation when implemented/runnable",
            "accepted_deviation",
            "skipped_with_reason",
            "Reviewer output alone is not enough",
            "FlowGuard output alone is not enough",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/run-report-template.md",
        (
            "Integrated Acceptance:",
            "flowguard_journey_coverage:",
            "flowguard_text_hierarchy_blueprint:",
            "flowguard_implementation_validation:",
            "status: pass | accepted_deviation | skipped_with_reason | partial | blocked",
            "final_verdict_downgrades:",
            "evidence_version_or_timestamp:",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/visual-qa-loop.md",
        (
            "Visual QA feeds the final integrated acceptance ledger",
            "does not replace FlowGuard",
            "app-icon, or functional-walkthrough evidence",
            "wrong-window or cropped screenshots",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/divergence-review.md",
        (
            "Record each accepted difference in the final integrated acceptance ledger",
            "accepted_deviation",
            "does not weaken the final user outcome",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/layout-geometry-qa.md",
        (
            "Geometry QA feeds the final integrated acceptance ledger",
            "downgrade final acceptance to `partial` or `blocked`",
            "stales affected geometry evidence",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/dependency-map.md",
        (
            "Final integrated acceptance cannot be replaced by any single companion skill",
            "manual equivalent only when that equivalent",
            "records the same evidence",
        ),
    )


def main() -> None:
    if not getattr(flowguard, "SCHEMA_VERSION", ""):
        raise AssertionError("Real flowguard package is not importable")
    check_acceptance_model()
    check_skill_text()
    print(
        "OK: final integrated acceptance gate validated with FlowGuard schema "
        f"{flowguard.SCHEMA_VERSION}"
    )


if __name__ == "__main__":
    main()
