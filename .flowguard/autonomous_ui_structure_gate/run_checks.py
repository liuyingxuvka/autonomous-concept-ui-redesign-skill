"""Regression checks for the autonomous UI FlowGuard structure gate."""

from __future__ import annotations

from pathlib import Path

import flowguard
from flowguard import (
    UIControl,
    UIDisplayElement,
    UIInteractionModel,
    UIRegionRecommendation,
    UIStateNode,
    UIStructureDerivation,
    UITransition,
    review_ui_interaction_model,
    review_ui_structure_derivation,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _require_snippets(relative: str, snippets: tuple[str, ...]) -> None:
    text = _read(relative)
    missing = [snippet for snippet in snippets if snippet not in text]
    if missing:
        joined = "\n".join(f"- {snippet}" for snippet in missing)
        raise AssertionError(f"{relative} is missing required snippets:\n{joined}")


def _sample_model() -> UIInteractionModel:
    controls = (
        UIControl(
            "import",
            label="Import",
            level="global",
            persistent=True,
            placement_hint="top toolbar",
            function_key="import_file",
            rationale="Primary entry opens import flow.",
        ),
        UIControl(
            "cancel_import",
            label="Cancel",
            level="contextual",
            depends_on_states=("importing",),
            function_key="cancel_import",
            rationale="Recovery from long import.",
        ),
        UIControl(
            "retry_import",
            label="Retry",
            level="contextual",
            depends_on_states=("import_error",),
            function_key="retry_import",
            rationale="Recovery from failed import.",
        ),
    )
    displays = (
        UIDisplayElement(
            "status_summary",
            "import_status",
            label="Status",
            display_type="status",
            depends_on_states=("idle", "importing", "import_error", "ready"),
            region_hint="status",
            rationale="Shows one authoritative import state.",
        ),
        UIDisplayElement(
            "error_detail",
            "import_error_detail",
            label="Error detail",
            display_type="message",
            depends_on_states=("import_error",),
            region_hint="feedback",
            rationale="Explains failure and retry path.",
        ),
    )
    states = (
        UIStateNode(
            "idle",
            visible_controls=("import",),
            enabled_controls=("import",),
            visible_displays=("status_summary",),
            rationale="Initial ready state.",
        ),
        UIStateNode(
            "importing",
            visible_controls=("import", "cancel_import"),
            enabled_controls=("cancel_import",),
            disabled_controls=("import",),
            visible_displays=("status_summary",),
            rationale="Import in progress with cancel recovery.",
        ),
        UIStateNode(
            "import_error",
            failure=True,
            visible_controls=("import", "retry_import"),
            enabled_controls=("retry_import",),
            disabled_controls=("import",),
            recovery_controls=("retry_import",),
            visible_displays=("status_summary", "error_detail"),
            rationale="Failure state exposes recovery.",
        ),
        UIStateNode(
            "ready",
            visible_controls=("import",),
            enabled_controls=("import",),
            visible_displays=("status_summary",),
            terminal=True,
            rationale="Terminal success for modeled flow.",
        ),
    )
    transitions = (
        UITransition(
            "click_import",
            "import",
            "idle",
            "importing",
            function_block="import_file",
            output="import dialog/process starts",
            rationale="Primary import entry.",
        ),
        UITransition(
            "import_success",
            "import",
            "importing",
            "ready",
            function_block="import_file",
            output="data ready",
            rationale="Import completes.",
        ),
        UITransition(
            "import_failure",
            "import",
            "importing",
            "import_error",
            function_block="import_file",
            output="error detail",
            rationale="Import failure exposes retry.",
        ),
        UITransition(
            "click_cancel_import",
            "cancel_import",
            "importing",
            "idle",
            function_block="cancel_import",
            output="return to idle",
            rationale="User cancels import.",
        ),
        UITransition(
            "click_retry_import",
            "retry_import",
            "import_error",
            "importing",
            function_block="retry_import",
            output="retry import",
            rationale="Retry returns to running state.",
        ),
    )
    return UIInteractionModel(
        "autonomous-ui-flowguard-gate-sample",
        "idle",
        states=states,
        controls=controls,
        displays=displays,
        transitions=transitions,
        validation_boundaries=(
            "concept brief must preserve import flow states",
            "implementation brief must keep retry recovery",
        ),
        rationale="Sample gate contract for autonomous UI skill regression.",
    )


def _sample_derivation() -> UIStructureDerivation:
    regions = (
        UIRegionRecommendation(
            "surface",
            level="surface",
            placement="screen root",
            stable_across_states=True,
            validation_boundaries=("root owns high-level regions",),
            rationale="Parent surface for hierarchy.",
        ),
        UIRegionRecommendation(
            "global_toolbar",
            level="global",
            placement="top toolbar",
            parent_region_id="surface",
            owns_controls=("import",),
            owns_events=("click_import", "import_success", "import_failure"),
            stable_across_states=True,
            validation_boundaries=(
                "persistent import entry remains visible or disabled",
                "global controls do not own local retry",
            ),
            rationale="Stable global command area.",
        ),
        UIRegionRecommendation(
            "status_region",
            level="secondary",
            placement="top of work area",
            parent_region_id="surface",
            owns_states=("idle", "importing", "import_error", "ready"),
            owns_displays=("status_summary",),
            stable_across_states=True,
            validation_boundaries=("one status owner",),
            rationale="Single status source avoids duplicate semantic status.",
        ),
        UIRegionRecommendation(
            "feedback_region",
            level="secondary",
            placement="inline feedback below status",
            parent_region_id="status_region",
            owns_displays=("error_detail",),
            owns_controls=("cancel_import", "retry_import"),
            owns_events=("click_cancel_import", "click_retry_import"),
            validation_boundaries=("recovery controls remain contextual",),
            rationale="Recovery and error detail live near affected flow.",
        ),
    )
    return UIStructureDerivation(
        "autonomous-ui-flowguard-gate-structure",
        "autonomous-ui-flowguard-gate-sample",
        "autonomous-redesign-surface",
        target_regions=regions,
        interaction_model_reviewed=True,
        state_region_map=(
            ("idle", "status_region"),
            ("importing", "status_region"),
            ("import_error", "status_region"),
            ("ready", "status_region"),
        ),
        control_region_map=(
            ("import", "global_toolbar"),
            ("cancel_import", "feedback_region"),
            ("retry_import", "feedback_region"),
        ),
        event_region_map=(
            ("click_import", "global_toolbar"),
            ("import_success", "global_toolbar"),
            ("import_failure", "global_toolbar"),
            ("click_cancel_import", "feedback_region"),
            ("click_retry_import", "feedback_region"),
        ),
        display_region_map=(
            ("status_summary", "status_region"),
            ("error_detail", "feedback_region"),
        ),
        hierarchy_edges=(
            ("surface", "global_toolbar"),
            ("surface", "status_region"),
            ("status_region", "feedback_region"),
        ),
        persistent_control_ids=("import",),
        contextual_control_ids=("cancel_import", "retry_import"),
        stable_region_ids=("surface", "global_toolbar", "status_region"),
        validation_boundaries=("concept and implementation must preserve ownership maps",),
        rationale="Structure follows modeled import states and recovery.",
    )


def _duplicate_model() -> UIInteractionModel:
    base = _sample_model()
    extra_controls = base.controls + (
        UIControl(
            "upload",
            label="Upload",
            level="global",
            persistent=True,
            placement_hint="top toolbar",
            function_key="import_file",
            rationale="Duplicate import entry used to verify review catches it.",
        ),
    )
    extra_displays = base.displays + (
        UIDisplayElement(
            "status_copy",
            "import_status",
            label="Status copy",
            display_type="text",
            depends_on_states=("idle",),
            region_hint="status",
            rationale="Duplicate status used to verify review catches it.",
        ),
    )
    states = (
        UIStateNode(
            "idle",
            visible_controls=("import", "upload"),
            enabled_controls=("import", "upload"),
            visible_displays=("status_summary", "status_copy"),
            rationale="Initial state with intentional unexcused duplicates.",
        ),
    ) + base.states[1:]
    transitions = base.transitions + (
        UITransition(
            "click_upload",
            "upload",
            "idle",
            "importing",
            function_block="import_file",
            output="import dialog/process starts",
            rationale="Duplicate import transition used to verify review catches it.",
        ),
    )
    return UIInteractionModel(
        "autonomous-ui-flowguard-gate-duplicate-probe",
        "idle",
        states=states,
        controls=extra_controls,
        displays=extra_displays,
        transitions=transitions,
        validation_boundaries=base.validation_boundaries,
        rationale="Known-bad duplicate probe for regression.",
    )


def check_skill_text() -> None:
    _require_snippets(
        "autonomous-concept-ui-redesign/SKILL.md",
        (
            "### 2.5 FlowGuard UI Structure Gate",
            "flowguard-ui-flow-structure",
            "Skip the gate only when the task is visual-only",
            "duplicate information and duplicate same-level control review",
            "Carry the FlowGuard structure contract into:",
            "re-run the FlowGuard gate or",
            "record why the current model-derived structure contract remains valid",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/functional-framing.md",
        (
            "## FlowGuard UI Structure Inputs",
            "UI event x UI state -> Set(UI output x UI state)",
            "Duplicate/redundant information decisions:",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/dependency-map.md",
        (
            "flowguard-ui-flow-structure",
            "do not claim a FlowGuard pass",
        ),
    )
    _require_snippets(
        "autonomous-concept-ui-redesign/references/run-report-template.md",
        (
            "flowguard_gate: triggered | skipped | blocked",
            "duplicate_information_decisions:",
            "flowguard_contract_alignment:",
        ),
    )


def check_flowguard_model() -> None:
    if not getattr(flowguard, "SCHEMA_VERSION", ""):
        raise AssertionError("Real flowguard package is not importable")

    model = _sample_model()
    interaction_report = review_ui_interaction_model(model)
    if not interaction_report.ok:
        raise AssertionError(interaction_report.format_text())

    derivation = _sample_derivation()
    structure_report = review_ui_structure_derivation(derivation, interaction_model=model)
    if not structure_report.ok:
        raise AssertionError(structure_report.format_text())

    duplicate_report = review_ui_interaction_model(_duplicate_model())
    duplicate_codes = {finding.code for finding in duplicate_report.findings}
    required_codes = {
        "duplicate_information_same_state",
        "duplicate_control_function_same_state_level",
    }
    missing = required_codes - duplicate_codes
    if duplicate_report.ok or missing:
        raise AssertionError(
            "Duplicate probe did not produce expected FlowGuard findings: "
            + ", ".join(sorted(missing or duplicate_codes))
        )


def main() -> None:
    check_skill_text()
    check_flowguard_model()
    print(
        "OK: autonomous-concept-ui-redesign FlowGuard structure gate contract "
        f"validated with FlowGuard schema {flowguard.SCHEMA_VERSION}"
    )


if __name__ == "__main__":
    main()
