#!/usr/bin/env python3
"""Validate memory-workbench continuity pack/report contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PACK_REQUIRED_FIELDS = (
    "case_id",
    "created_at",
    "last_verified_at",
    "source_workflow",
    "send_status",
    "recommended_lane",
    "current_next_action",
)

REPORT_REQUIRED_FIELDS = (
    "case_id",
    "date",
    "operator",
    "condition",
    "pack_last_verified_at",
    "restart_clarity_score",
    "replay_cost_minutes_raw",
    "replay_cost_minutes_pack",
    "replay_cost_reduction_percent",
    "factual_regression_present",
    "stale_check_performed",
    "stale_check_result",
    "status",
)

FIELD_RE = re.compile(r"^\s*-\s+([a-zA-Z0-9_]+):\s*(.+?)\s*$")
VALUE_RE = re.compile(r"`([^`]*)`")
TRACKER_ROW_RE = re.compile(r"^\|\s*(\d{3})\s*\|.*?\|\s*`([^`]+)`\s*\|", re.MULTILINE)


def extract_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = FIELD_RE.match(line)
        if not match:
            continue
        key = match.group(1)
        raw_value = match.group(2).strip()
        code_match = VALUE_RE.search(raw_value)
        fields[key] = code_match.group(1).strip() if code_match else raw_value
    return fields


def extract_lane_id(value: str) -> str:
    match = re.search(r"(\d{3})", value or "")
    return match.group(1) if match else ""


def extract_pack_command(text: str) -> str:
    for line in text.splitlines():
        if "recommended_primary_open_command =" not in line:
            continue
        _, _, command = line.partition("=")
        return command.strip().strip(" `.").strip()
    return ""


def extract_tracker_status(text: str, target_id: str) -> str:
    for match in TRACKER_ROW_RE.finditer(text):
        if match.group(1) == target_id:
            return match.group(2).strip()
    return ""


def validate_required(
    fields: dict[str, str], required: tuple[str, ...], label: str
) -> list[str]:
    issues: list[str] = []
    for key in required:
        value = fields.get(key, "").strip()
        if not value:
            issues.append(f"{label}: missing required field `{key}`")
    return issues


def validate_pack(text: str, path: Path) -> tuple[dict[str, str], list[str]]:
    fields = extract_fields(text)
    issues = validate_required(fields, PACK_REQUIRED_FIELDS, "pack")

    if "## Stale-Check Rule" not in text:
        issues.append("pack: missing `## Stale-Check Rule` section")
    if "/ROOM/artifacts/deliverables/public-outreach-next-step.md" not in text:
        issues.append("pack: missing canonical next-step packet reference")
    if "/ROOM/tasks/ai-memory-saas/outreach-tracker.md" not in text:
        issues.append("pack: missing tracker SSOT reference")

    if fields.get("case_id") and path.stem not in {"continuity-pack"}:
        pass

    return fields, issues


def validate_report(
    text: str, path: Path, pack_fields: dict[str, str] | None
) -> tuple[dict[str, str], list[str]]:
    fields = extract_fields(text)
    issues = validate_required(fields, REPORT_REQUIRED_FIELDS, "report")

    status = fields.get("status", "")
    if status and status not in {"pass", "partial", "fail"}:
        issues.append("report: `status` must be one of `pass`, `partial`, `fail`")

    stale_check_performed = fields.get("stale_check_performed", "")
    if stale_check_performed and stale_check_performed not in {"yes", "no"}:
        issues.append("report: `stale_check_performed` must be `yes` or `no`")

    if pack_fields:
        pack_last_verified_at = pack_fields.get("last_verified_at", "")
        report_pack_last_verified_at = fields.get("pack_last_verified_at", "")
        if (
            pack_last_verified_at
            and report_pack_last_verified_at
            and pack_last_verified_at != report_pack_last_verified_at
        ):
            issues.append(
                "report: `pack_last_verified_at` does not match pack "
                f"`last_verified_at` ({report_pack_last_verified_at} != "
                f"{pack_last_verified_at})"
            )
        pack_case_id = pack_fields.get("case_id", "")
        report_case_id = fields.get("case_id", "")
        if pack_case_id and report_case_id and pack_case_id != report_case_id:
            issues.append(
                f"report: `case_id` does not match pack ({report_case_id} != {pack_case_id})"
            )

    if "Condition B" not in text:
        issues.append("report: missing `Condition B` section")
    if str(path).endswith(".md") and "stale_check_result" not in text:
        issues.append("report: missing stale-check result entry")

    return fields, issues


def validate_freshness_against_sources(
    *,
    pack_text: str,
    pack_fields: dict[str, str],
    source_packet_path: Path | None,
    source_tracker_path: Path | None,
) -> tuple[dict[str, str], list[str]]:
    details = {
        "packet_recommendation": "",
        "packet_recommended_open_command": "",
        "tracker_send_status": "",
        "pack_recommended_lane": pack_fields.get("recommended_lane", ""),
        "pack_open_command": extract_pack_command(pack_text),
        "target_id": extract_lane_id(pack_fields.get("recommended_lane", "")),
    }
    issues: list[str] = []

    if source_packet_path:
        packet_text = source_packet_path.read_text(encoding="utf-8")
        packet_fields = extract_fields(packet_text)
        details["packet_recommendation"] = packet_fields.get("recommendation", "")
        details["packet_recommended_open_command"] = packet_fields.get(
            "recommended_primary_open_command", ""
        )

        pack_lane_id = extract_lane_id(pack_fields.get("recommended_lane", ""))
        packet_lane_id = extract_lane_id(packet_fields.get("recommendation", ""))
        if pack_lane_id and packet_lane_id and pack_lane_id != packet_lane_id:
            issues.append(
                "freshness: pack `recommended_lane` does not match packet "
                f"`recommendation` ({pack_fields.get('recommended_lane', '')} != "
                f"{packet_fields.get('recommendation', '')})"
            )

        pack_command = details["pack_open_command"]
        packet_command = details["packet_recommended_open_command"]
        if pack_command and packet_command and pack_command != packet_command:
            issues.append(
                "freshness: pack command does not match packet "
                f"`recommended_primary_open_command` ({pack_command} != {packet_command})"
            )

    if source_tracker_path:
        tracker_text = source_tracker_path.read_text(encoding="utf-8")
        target_id = details["target_id"]
        tracker_status = extract_tracker_status(tracker_text, target_id)
        details["tracker_send_status"] = tracker_status
        if target_id and not tracker_status:
            issues.append(
                f"freshness: tracker row for target `{target_id}` was not found"
            )
        elif tracker_status and tracker_status != pack_fields.get("send_status", ""):
            issues.append(
                "freshness: pack `send_status` does not match tracker "
                f"row ({pack_fields.get('send_status', '')} != {tracker_status})"
            )

    return details, issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate continuity pack/report freshness fields."
    )
    parser.add_argument("--pack", required=True, help="Path to continuity pack markdown")
    parser.add_argument(
        "--report", required=True, help="Path to continuity report markdown"
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    parser.add_argument(
        "--source-packet",
        help="Optional canonical packet path used for freshness checks",
    )
    parser.add_argument(
        "--source-tracker",
        help="Optional tracker path used for freshness checks",
    )
    args = parser.parse_args()

    pack_path = Path(args.pack)
    report_path = Path(args.report)
    pack_text = pack_path.read_text(encoding="utf-8")
    report_text = report_path.read_text(encoding="utf-8")
    source_packet_path = Path(args.source_packet) if args.source_packet else None
    source_tracker_path = Path(args.source_tracker) if args.source_tracker else None

    pack_fields, pack_issues = validate_pack(pack_text, pack_path)
    report_fields, report_issues = validate_report(report_text, report_path, pack_fields)
    freshness_details, freshness_issues = validate_freshness_against_sources(
        pack_text=pack_text,
        pack_fields=pack_fields,
        source_packet_path=source_packet_path,
        source_tracker_path=source_tracker_path,
    )
    issues = pack_issues + report_issues + freshness_issues

    payload = {
        "ok": not issues,
        "pack": str(pack_path),
        "report": str(report_path),
        "source_packet": str(source_packet_path) if source_packet_path else "",
        "source_tracker": str(source_tracker_path) if source_tracker_path else "",
        "pack_fields_checked": sorted(PACK_REQUIRED_FIELDS),
        "report_fields_checked": sorted(REPORT_REQUIRED_FIELDS),
        "issue_count": len(issues),
        "issues": issues,
        "pack_last_verified_at": pack_fields.get("last_verified_at", ""),
        "report_pack_last_verified_at": report_fields.get("pack_last_verified_at", ""),
        "freshness": freshness_details,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=True, indent=2))
    else:
        status = "OK" if payload["ok"] else "FAIL"
        print(
            f"{status}: validated pack={pack_path} report={report_path} "
            f"issues={payload['issue_count']}"
        )
        for issue in issues:
            print(f"- {issue}")

    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
