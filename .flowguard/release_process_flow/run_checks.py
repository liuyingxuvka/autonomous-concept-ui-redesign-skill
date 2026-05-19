"""Review release-readiness evidence freshness for this skill repository."""

from __future__ import annotations

from flowguard import (
    PROCESS_ARTIFACT_CODE,
    PROCESS_ARTIFACT_DOC,
    PROCESS_ARTIFACT_MODEL,
    PROCESS_ARTIFACT_RELEASE,
    PROCESS_ARTIFACT_REQUIREMENT,
    PROCESS_ARTIFACT_TEST,
    PROCESS_EVIDENCE_PASSED,
    PROCESS_SCOPE_RELEASE,
    DevelopmentProcessPlan,
    FreshnessRule,
    ProcessAction,
    ProcessArtifact,
    ProcessEvidence,
    ValidationRequirement,
    review_development_process_flow,
)


VERSION = "0.1.3"


def artifacts(version: str = VERSION) -> tuple[ProcessArtifact, ...]:
    return (
        ProcessArtifact(
            "openspec.final_acceptance",
            PROCESS_ARTIFACT_REQUIREMENT,
            version,
            path="openspec/changes/add-final-integrated-acceptance-gate",
            description="OpenSpec proposal, design, specs, and tasks.",
        ),
        ProcessArtifact(
            "skill.contract",
            PROCESS_ARTIFACT_DOC,
            version,
            path="autonomous-concept-ui-redesign",
            upstream_artifact_ids=("openspec.final_acceptance",),
            description="Skill instructions and references.",
        ),
        ProcessArtifact(
            "flowguard.regressions",
            PROCESS_ARTIFACT_MODEL,
            version,
            path=".flowguard",
            upstream_artifact_ids=("openspec.final_acceptance", "skill.contract"),
            description="FlowGuard model/check artifacts.",
        ),
        ProcessArtifact(
            "release.metadata",
            PROCESS_ARTIFACT_RELEASE,
            version,
            path="README.md, CHANGELOG.md, VERSION",
            upstream_artifact_ids=("skill.contract",),
            description="Public release version and notes.",
        ),
        ProcessArtifact(
            "sync.targets",
            PROCESS_ARTIFACT_RELEASE,
            version,
            path="$CODEX_HOME/skills and local shadow skill copies",
            upstream_artifact_ids=("skill.contract",),
            description="Installed and local shadow copies.",
        ),
    )


def release_plan() -> DevelopmentProcessPlan:
    return DevelopmentProcessPlan(
        "autonomous-concept-ui-redesign-0.1.3-release",
        artifacts=artifacts(),
        actions=(
            ProcessAction(
                "write-openspec",
                writes_artifacts=("openspec.final_acceptance",),
            ),
            ProcessAction(
                "edit-skill-contract",
                reads_artifacts=("openspec.final_acceptance",),
                writes_artifacts=("skill.contract",),
                order_after=("write-openspec",),
            ),
            ProcessAction(
                "edit-flowguard-regressions",
                reads_artifacts=("openspec.final_acceptance", "skill.contract"),
                writes_artifacts=("flowguard.regressions",),
                order_after=("edit-skill-contract",),
            ),
            ProcessAction(
                "update-release-metadata",
                reads_artifacts=("skill.contract",),
                writes_artifacts=("release.metadata",),
                order_after=("edit-skill-contract",),
            ),
            ProcessAction(
                "run-release-validation",
                reads_artifacts=(
                    "openspec.final_acceptance",
                    "skill.contract",
                    "flowguard.regressions",
                    "release.metadata",
                ),
                produced_evidence_ids=(
                    "openspec-all-strict",
                    "flowguard-structure-gate",
                    "flowguard-final-acceptance",
                    "python-pycompile",
                    "git-diff-check",
                    "privacy-scan",
                ),
                order_after=("edit-flowguard-regressions", "update-release-metadata"),
            ),
            ProcessAction(
                "sync-installed-copies",
                reads_artifacts=("skill.contract",),
                writes_artifacts=("sync.targets",),
                order_after=("run-release-validation",),
            ),
            ProcessAction(
                "validate-sync",
                reads_artifacts=("skill.contract", "sync.targets"),
                produced_evidence_ids=("sync-hash-check",),
                order_after=("sync-installed-copies",),
            ),
            ProcessAction(
                "claim-release",
                action_type="claim_release",
                required_validation_ids=(
                    "openspec-current",
                    "flowguard-current",
                    "compile-current",
                    "git-diff-current",
                    "privacy-current",
                    "sync-current",
                ),
                decision_scope=PROCESS_SCOPE_RELEASE,
                order_after=("validate-sync",),
            ),
        ),
        evidence=(
            ProcessEvidence(
                "openspec-all-strict",
                evidence_kind="openspec",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=("openspec.final_acceptance",),
                covered_versions={"openspec.final_acceptance": VERSION},
                validation_requirement_ids=("openspec-current",),
                produced_by_action_id="run-release-validation",
                command="openspec validate --changes --strict --no-interactive",
                release_required=True,
            ),
            ProcessEvidence(
                "flowguard-structure-gate",
                evidence_kind="flowguard",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=("skill.contract", "flowguard.regressions"),
                covered_versions={
                    "skill.contract": VERSION,
                    "flowguard.regressions": VERSION,
                },
                validation_requirement_ids=("flowguard-current",),
                produced_by_action_id="run-release-validation",
                command="python .flowguard/autonomous_ui_structure_gate/run_checks.py",
                release_required=True,
            ),
            ProcessEvidence(
                "flowguard-final-acceptance",
                evidence_kind="flowguard",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=("skill.contract", "flowguard.regressions"),
                covered_versions={
                    "skill.contract": VERSION,
                    "flowguard.regressions": VERSION,
                },
                validation_requirement_ids=("flowguard-current",),
                produced_by_action_id="run-release-validation",
                command="python .flowguard/final_integrated_acceptance_gate/run_checks.py",
                release_required=True,
            ),
            ProcessEvidence(
                "python-pycompile",
                evidence_kind="compile",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=("flowguard.regressions", "skill.contract"),
                covered_versions={
                    "flowguard.regressions": VERSION,
                    "skill.contract": VERSION,
                },
                validation_requirement_ids=("compile-current",),
                produced_by_action_id="run-release-validation",
                command="python -m py_compile <flowguard checks and app_icon_asset_check.py>",
                release_required=True,
            ),
            ProcessEvidence(
                "git-diff-check",
                evidence_kind="git",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=(
                    "openspec.final_acceptance",
                    "skill.contract",
                    "flowguard.regressions",
                    "release.metadata",
                ),
                covered_versions={
                    "openspec.final_acceptance": VERSION,
                    "skill.contract": VERSION,
                    "flowguard.regressions": VERSION,
                    "release.metadata": VERSION,
                },
                validation_requirement_ids=("git-diff-current",),
                produced_by_action_id="run-release-validation",
                command="git diff --check",
                release_required=True,
            ),
            ProcessEvidence(
                "privacy-scan",
                evidence_kind="privacy",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=(
                    "openspec.final_acceptance",
                    "skill.contract",
                    "flowguard.regressions",
                    "release.metadata",
                ),
                covered_versions={
                    "openspec.final_acceptance": VERSION,
                    "skill.contract": VERSION,
                    "flowguard.regressions": VERSION,
                    "release.metadata": VERSION,
                },
                validation_requirement_ids=("privacy-current",),
                produced_by_action_id="run-release-validation",
                command="rg privacy/secret scan",
                release_required=True,
            ),
            ProcessEvidence(
                "sync-hash-check",
                evidence_kind="sync",
                status=PROCESS_EVIDENCE_PASSED,
                covers_artifacts=("skill.contract", "sync.targets"),
                covered_versions={
                    "skill.contract": VERSION,
                    "sync.targets": VERSION,
                },
                validation_requirement_ids=("sync-current",),
                produced_by_action_id="validate-sync",
                command="hash compare source and installed/shadow copies",
                release_required=True,
            ),
        ),
        validation_requirements=(
            ValidationRequirement(
                "openspec-current",
                required_artifact_ids=("openspec.final_acceptance",),
                required_evidence_kinds=("openspec",),
                evidence_ids=("openspec-all-strict",),
                scope=PROCESS_SCOPE_RELEASE,
                release_required=True,
                v_model_pair=True,
            ),
            ValidationRequirement(
                "flowguard-current",
                required_artifact_ids=("skill.contract", "flowguard.regressions"),
                required_evidence_kinds=("flowguard",),
                evidence_ids=("flowguard-structure-gate", "flowguard-final-acceptance"),
                scope=PROCESS_SCOPE_RELEASE,
                release_required=True,
                v_model_pair=True,
            ),
            ValidationRequirement(
                "compile-current",
                required_artifact_ids=("flowguard.regressions",),
                required_evidence_kinds=("compile",),
                evidence_ids=("python-pycompile",),
                scope=PROCESS_SCOPE_RELEASE,
                release_required=True,
            ),
            ValidationRequirement(
                "git-diff-current",
                required_artifact_ids=(
                    "openspec.final_acceptance",
                    "skill.contract",
                    "flowguard.regressions",
                    "release.metadata",
                ),
                required_evidence_kinds=("git",),
                evidence_ids=("git-diff-check",),
                scope=PROCESS_SCOPE_RELEASE,
                release_required=True,
            ),
            ValidationRequirement(
                "privacy-current",
                required_artifact_ids=(
                    "openspec.final_acceptance",
                    "skill.contract",
                    "flowguard.regressions",
                    "release.metadata",
                ),
                required_evidence_kinds=("privacy",),
                evidence_ids=("privacy-scan",),
                scope=PROCESS_SCOPE_RELEASE,
                release_required=True,
            ),
            ValidationRequirement(
                "sync-current",
                required_artifact_ids=("skill.contract", "sync.targets"),
                required_evidence_kinds=("sync",),
                evidence_ids=("sync-hash-check",),
                scope=PROCESS_SCOPE_RELEASE,
                release_required=True,
            ),
        ),
        freshness_rules=(
            FreshnessRule(
                "openspec-invalidates-skill-and-models",
                upstream_artifact_id="openspec.final_acceptance",
                invalidates_artifact_ids=("skill.contract", "flowguard.regressions"),
                invalidates_evidence_kinds=("flowguard", "compile", "git", "privacy"),
            ),
            FreshnessRule(
                "skill-invalidates-validation-and-sync",
                upstream_artifact_id="skill.contract",
                invalidates_artifact_ids=("flowguard.regressions", "sync.targets"),
                invalidates_evidence_kinds=("flowguard", "compile", "sync", "git", "privacy"),
            ),
            FreshnessRule(
                "release-metadata-invalidates-release-checks",
                upstream_artifact_id="release.metadata",
                invalidates_evidence_kinds=("git", "privacy"),
            ),
        ),
        decision_scope=PROCESS_SCOPE_RELEASE,
        release_deferred_allowed=False,
    )


def stale_plan() -> DevelopmentProcessPlan:
    plan = release_plan()
    stale_evidence = tuple(
        evidence
        if evidence.evidence_id != "flowguard-final-acceptance"
        else ProcessEvidence(
            evidence.evidence_id,
            evidence.evidence_kind,
            evidence.producer_route,
            evidence.status,
            evidence.covers_artifacts,
            {"skill.contract": "0.1.2", "flowguard.regressions": "0.1.2"},
            evidence.verifier_artifacts,
            evidence.validation_requirement_ids,
            evidence.produced_by_action_id,
            evidence.command,
            evidence.result_path,
            evidence.background,
            evidence.has_exit_artifact,
            evidence.has_result_artifact,
            evidence.progress_only,
            evidence.skipped_count,
            evidence.skipped_visible,
            evidence.release_required,
            ("known-bad stale evidence probe",),
        )
        for evidence in plan.evidence
    )
    return DevelopmentProcessPlan(
        "autonomous-concept-ui-redesign-0.1.3-stale-release-probe",
        artifacts=plan.artifacts,
        actions=plan.actions,
        evidence=stale_evidence,
        validation_requirements=plan.validation_requirements,
        freshness_rules=plan.freshness_rules,
        decision_scope=PROCESS_SCOPE_RELEASE,
        release_deferred_allowed=False,
    )


def main() -> int:
    release_report = review_development_process_flow(release_plan())
    stale_report = review_development_process_flow(stale_plan())
    print(release_report.format_text(max_findings=8))
    print()
    print(stale_report.format_text(max_findings=8))
    if not release_report.ok:
        return 1
    if stale_report.ok:
        print("Expected stale release probe to fail, but it passed.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
