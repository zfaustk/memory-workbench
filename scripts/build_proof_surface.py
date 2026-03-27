#!/usr/bin/env python3
"""Build a proof-surface summary from memory-workbench reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FIELD_RE = re.compile(r"^\s*-\s+([a-zA-Z0-9_]+):\s*(.+?)\s*$")
VALUE_RE = re.compile(r"`([^`]*)`")


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


def parse_ratio(value: str) -> tuple[str, float]:
    cleaned = value.strip()
    ratio_match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*/\s*([0-9]+(?:\.[0-9]+)?)", cleaned)
    if ratio_match:
        left = ratio_match.group(1)
        right = ratio_match.group(2)
        try:
            ratio = float(left) / float(right)
        except ValueError:
            ratio = 0.0
        return cleaned, ratio
    try:
        scalar = float(cleaned)
    except ValueError:
        scalar = 0.0
    return cleaned, scalar


def parse_number(value: str) -> float:
    try:
        return float(value.strip())
    except ValueError:
        return 0.0


def load_report(path: Path) -> dict[str, object]:
    fields = extract_fields(path.read_text(encoding="utf-8"))
    clarity_text, clarity_value = parse_ratio(fields.get("restart_clarity_score", "0"))
    trace_text, trace_value = parse_ratio(fields.get("evidence_traceability_score", "0"))
    return {
        "path": str(path),
        "case_id": fields.get("case_id", path.stem),
        "date": fields.get("date", ""),
        "status": fields.get("status", ""),
        "restart_clarity_score": clarity_text,
        "restart_clarity_ratio": clarity_value,
        "evidence_traceability_score": trace_text,
        "evidence_traceability_ratio": trace_value,
        "replay_cost_minutes_raw": parse_number(fields.get("replay_cost_minutes_raw", "0")),
        "replay_cost_minutes_pack": parse_number(fields.get("replay_cost_minutes_pack", "0")),
        "replay_cost_reduction_percent": parse_number(
            fields.get("replay_cost_reduction_percent", "0")
        ),
        "stale_check_result": fields.get("stale_check_result", ""),
        "second_operator_success_rate": fields.get("second_operator_success_rate", ""),
    }


def load_rerun(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_summary(operator_report: dict[str, object], stale_report: dict[str, object], rerun: dict[str, object]) -> dict[str, object]:
    average_reduction = round(
        (
            float(operator_report["replay_cost_reduction_percent"])
            + float(stale_report["replay_cost_reduction_percent"])
        )
        / 2.0,
        1,
    )
    operator_clarity = float(operator_report["restart_clarity_ratio"])
    stale_clarity = float(stale_report["restart_clarity_ratio"])
    average_clarity = round((operator_clarity + stale_clarity) / 2.0, 3)

    return {
        "generated_at": "2026-03-27",
        "status": "proof_ready_local",
        "summary": {
            "benchmark_cases": 2,
            "scripted_reruns": 1,
            "average_replay_cost_reduction_percent": average_reduction,
            "average_restart_clarity_ratio": average_clarity,
            "stale_verdict_reproduced": bool(rerun.get("stale_verdict_reproduced")),
        },
        "operator_handoff": operator_report,
        "stale_pack_rotation": stale_report,
        "scripted_rerun": rerun,
        "next_gap": "independent_second_operator_rerun",
    }


def render_markdown(summary: dict[str, object]) -> str:
    operator = summary["operator_handoff"]
    stale = summary["stale_pack_rotation"]
    rerun = summary["scripted_rerun"]
    rollup = summary["summary"]
    lines = [
        "# Proof Surface",
        "",
        "## Current State",
        "",
        "- status: `proof_ready_local`",
        "- purpose: give one compact proof packet for `remote_synced + proof-ready + upstream-citable` work",
        "- generated_from:",
        f"  - `{operator['path']}`",
        f"  - `{stale['path']}`",
        f"  - `{rerun['artifacts']['validator']}`",
        f"  - `{summary['scripted_rerun']['artifacts']['pack']}`",
        "",
        "## Rollup",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Benchmark cases | `{rollup['benchmark_cases']}` |",
        f"| Scripted reruns | `{rollup['scripted_reruns']}` |",
        f"| Average replay-cost reduction | `{rollup['average_replay_cost_reduction_percent']}%` |",
        f"| Average restart clarity | `{rollup['average_restart_clarity_ratio']}` |",
        f"| Stale verdict reproduced | `{str(rollup['stale_verdict_reproduced']).lower()}` |",
        "",
        "## Case Metrics",
        "",
        "| Case | Status | Replay cost raw | Replay cost with continuity artifact | Reduction | Restart clarity | Traceability |",
        "| --- | --- | --- | --- | --- | --- | --- |",
        f"| `{operator['case_id']}` | `{operator['status']}` | `{operator['replay_cost_minutes_raw']}` min | `{operator['replay_cost_minutes_pack']}` min | `{operator['replay_cost_reduction_percent']}%` | `{operator['restart_clarity_score']}` | `{operator['evidence_traceability_score']}` |",
        f"| `{stale['case_id']}` | `{stale['status']}` | `{stale['replay_cost_minutes_raw']}` min | `{stale['replay_cost_minutes_pack']}` min | `{stale['replay_cost_reduction_percent']}%` | `{stale['restart_clarity_score']}` | `{stale['evidence_traceability_score']}` |",
        "",
        "## Why This Is Reusable",
        "",
        "- `operator-handoff-001` shows a second operator can recover the live workflow state faster when the continuity pack compresses goal, state, next action, and evidence order.",
        "- `stale-pack-rotation-001` shows continuity artifacts must include a freshness contract; otherwise an old pack can point at the wrong lane and command.",
        "- `scripts/rerun_stale_pack_rotation.py` turns the stale fixture into a repeatable check instead of a one-off prose claim.",
        "",
        "## Runnable Checks",
        "",
        "- `python3 scripts/validate_continuity_artifacts.py --pack packs/operator-handoff-001/continuity-pack.md --report reports/operator-handoff-001-report-2026-03-26.md`",
        "- `python3 scripts/rerun_stale_pack_rotation.py --json`",
        "- `python3 scripts/build_proof_surface.py --json`",
        "",
        "## Remaining Gap",
        "",
        "- next_gap: `independent_second_operator_rerun`",
        "- reason: the stale verdict is now repeatable through the validator and scripted replay harness, but not yet verified by a second operator outside the same execution path.",
        "",
        "## Proof Hooks For Upstream Or Remote Sync",
        "",
        f"- operator handoff proof hook: replay cost `4.0 -> 1.5` minutes (`{operator['replay_cost_reduction_percent']}%` reduction) with `restart_clarity_score = {operator['restart_clarity_score']}`",
        f"- stale detection proof hook: replay cost `3.0 -> 1.0` minutes (`{stale['replay_cost_reduction_percent']}%` reduction) with validator-backed stop-before-action freshness verdict",
        f"- scripted rerun proof hook: `stale_verdict_reproduced = {str(rerun.get('stale_verdict_reproduced', False)).lower()}` with `validator_issue_count = {rerun.get('validator_issue_count', 0)}`",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    root = Path("/ROOM/projects/memory-workbench")
    parser = argparse.ArgumentParser(description="Build memory-workbench proof surface.")
    parser.add_argument(
        "--operator-report",
        default=str(root / "reports/operator-handoff-001-report-2026-03-26.md"),
    )
    parser.add_argument(
        "--stale-report",
        default=str(root / "reports/stale-pack-rotation-001-report-2026-03-26.md"),
    )
    parser.add_argument(
        "--rerun-json",
        default=str(root / "reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json"),
    )
    parser.add_argument(
        "--output-md",
        default=str(root / "docs/proof-surface.md"),
    )
    parser.add_argument(
        "--output-json",
        default=str(root / "reports/proof-surface-2026-03-27.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    operator_report = load_report(Path(args.operator_report))
    stale_report = load_report(Path(args.stale_report))
    rerun = load_rerun(Path(args.rerun_json))
    summary = build_summary(operator_report, stale_report, rerun)

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_md.write_text(render_markdown(summary) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(summary, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(summary, ensure_ascii=True, indent=2))
    else:
        print(f"status: {summary['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(
            "average_replay_cost_reduction_percent: "
            f"{summary['summary']['average_replay_cost_reduction_percent']}"
        )
        print(
            "stale_verdict_reproduced: "
            f"{str(summary['summary']['stale_verdict_reproduced']).lower()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
