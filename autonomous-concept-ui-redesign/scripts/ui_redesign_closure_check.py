#!/usr/bin/env python
"""Check an autonomous UI redesign final acceptance ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_STATUSES = {
    "pass",
    "accepted_deviation",
    "skipped_with_reason",
    "partial",
    "blocked",
}

PASSING_STATUSES = {"pass", "accepted_deviation", "skipped_with_reason"}
BAD_FRESHNESS = {
    "",
    "missing",
    "not_run",
    "not-run",
    "stale",
    "untrusted",
    "wrong_surface",
    "failed",
    "blocked",
}


def _as_bool(value: Any, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() not in {"no", "false", "0", "not_applicable"}


def _load_rows(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {}, [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        raise SystemExit(f"{path} must contain a JSON object or list")
    rows = payload.get("ledger_rows", payload.get("rows", []))
    if not isinstance(rows, list):
        raise SystemExit("ledger_rows/rows must be a list")
    return payload, [row for row in rows if isinstance(row, dict)]


def check_ledger(path: Path) -> dict[str, Any]:
    payload, rows = _load_rows(path)
    findings: list[dict[str, Any]] = []
    missing_inputs: list[dict[str, str]] = []
    stale_evidence: list[dict[str, str]] = []
    skipped_checks: list[dict[str, str]] = []
    next_actions: list[dict[str, str]] = []

    if not rows:
        missing_inputs.append({
            "field": "ledger_rows",
            "message": "Final integrated acceptance ledger has no rows.",
        })

    seen_gates = {str(row.get("gate", "")).strip() for row in rows if row.get("gate")}
    for gate in payload.get("required_gates", []) if isinstance(payload.get("required_gates"), list) else []:
        if str(gate) not in seen_gates:
            missing_inputs.append({
                "field": "required_gates",
                "message": f"Required gate is missing from ledger: {gate}",
            })

    for index, row in enumerate(rows):
        gate = str(row.get("gate") or f"row_{index}").strip()
        status = str(row.get("status", "")).strip().lower()
        triggered = _as_bool(row.get("triggered"), default=True)
        freshness = str(row.get("evidence_freshness", "")).strip().lower()
        evidence = row.get("evidence")
        reason = str(row.get("skip_or_deviation_reason", "")).strip()

        if status not in VALID_STATUSES:
            findings.append({
                "severity": "error",
                "type": "invalid_status",
                "gate": gate,
                "message": f"Invalid ledger status: {status or '<missing>'}",
            })
            continue

        if status == "blocked":
            findings.append({
                "severity": "error",
                "type": "blocked_gate",
                "gate": gate,
                "message": "A final acceptance gate is blocked.",
            })
        elif status == "partial":
            findings.append({
                "severity": "warning",
                "type": "partial_gate",
                "gate": gate,
                "message": "A final acceptance gate is partial.",
            })

        if status == "skipped_with_reason":
            skipped_checks.append({"check": gate, "message": reason or "Skip reason is missing."})
            if not reason:
                findings.append({
                    "severity": "warning",
                    "type": "skip_reason_missing",
                    "gate": gate,
                    "message": "A skipped gate must state why the skip is safe.",
                })
            continue

        if status == "accepted_deviation" and not reason:
            findings.append({
                "severity": "warning",
                "type": "accepted_deviation_reason_missing",
                "gate": gate,
                "message": "Accepted deviations need a product, accessibility, content-density, or design-system reason.",
            })

        if triggered and status in {"pass", "accepted_deviation"}:
            if not evidence:
                missing_inputs.append({
                    "field": f"{gate}.evidence",
                    "message": "Passing triggered gate is missing evidence.",
                })
            if freshness in BAD_FRESHNESS:
                stale_evidence.append({
                    "field": f"{gate}.evidence_freshness",
                    "message": f"Passing triggered gate has non-current evidence freshness: {freshness or '<missing>'}",
                })

    if missing_inputs:
        findings.append({
            "severity": "warning",
            "type": "missing_ledger_inputs",
            "count": len(missing_inputs),
        })
    if stale_evidence:
        findings.append({
            "severity": "warning",
            "type": "stale_or_missing_ui_evidence",
            "count": len(stale_evidence),
        })

    has_error = any(str(item.get("severity", "")).lower() in {"error", "blocker"} for item in findings)
    if has_error:
        closure_status = "blocked"
    elif findings or missing_inputs or stale_evidence:
        closure_status = "partial"
    else:
        closure_status = "pass"

    if closure_status != "pass":
        next_actions.append({
            "owner": "autonomous-concept-ui-redesign",
            "action": "repair_or_downgrade_final_acceptance_ledger",
            "reason": "The final acceptance ledger has blocked, partial, stale, missing, or unsupported rows.",
        })

    return {
        "owner_guard": "autonomous-concept-ui-redesign",
        "artifact_kind": "ui_redesign_final_acceptance_closure",
        "closure_status": closure_status,
        "checked_inputs": [{"check": "final_acceptance_ledger", "path": str(path)}],
        "findings": findings,
        "missing_inputs": missing_inputs,
        "stale_evidence": stale_evidence,
        "skipped_checks": skipped_checks,
        "next_actions": next_actions,
        "safe_claim": payload.get("safe_claim", "UI redesign completion is limited by the current final acceptance ledger."),
        "unsafe_claim_boundary": payload.get(
            "unsafe_claim_boundary",
            "Do not claim full completion while final acceptance rows are blocked, partial, stale, missing, or unsupported.",
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a UI redesign final acceptance ledger.")
    parser.add_argument("--ledger", type=Path, required=True, help="JSON final acceptance ledger.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = check_ledger(args.ledger)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['closure_status'].upper()}: UI redesign final acceptance")
        for finding in result["findings"]:
            print(f"- {finding.get('severity', 'warning')}: {finding.get('type', '')}".rstrip())
    return 0 if result["closure_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
