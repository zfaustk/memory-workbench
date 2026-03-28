#!/usr/bin/env python3
"""Build an independent rerun kit for a future second operator."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_kit(
    proof_surface: dict[str, object],
    remote_manifest: dict[str, object],
    citation_pack: dict[str, object],
) -> dict[str, object]:
    summary = proof_surface["summary"]
    operator = proof_surface["operator_handoff"]
    stale = proof_surface["stale_pack_rotation"]
    rerun = proof_surface["scripted_rerun"]

    artifact_sequence = [
        {
            "step": 1,
            "label": "README and benchmark contract",
            "path": "README.md",
            "why": "Anchor the repo thesis and the current proof boundary before opening case-specific files.",
        },
        {
            "step": 2,
            "label": "benchmark rubric",
            "path": "evals/continuity-benchmark.md",
            "why": "Review the scoring dimensions and pass criteria for continuity claims.",
        },
        {
            "step": 3,
            "label": "operator handoff runbook",
            "path": "evals/operator-handoff-001-runbook.md",
            "why": "Use the existing evaluator protocol instead of inventing a new procedure.",
        },
        {
            "step": 4,
            "label": "operator handoff continuity pack",
            "path": "packs/operator-handoff-001/continuity-pack.md",
            "why": "Start from the compact continuity artifact before drilling into raw case evidence.",
        },
        {
            "step": 5,
            "label": "operator handoff report",
            "path": "reports/operator-handoff-001-report-2026-03-26.md",
            "why": "Compare the expected replay-cost and restart-clarity deltas against the current rerun.",
        },
        {
            "step": 6,
            "label": "stale-pack fixture and validator",
            "path": "packs/stale-pack-rotation-001/continuity-pack-stale.md",
            "why": "Reproduce the stale-state failure mode before claiming continuity artifacts are safe to reuse.",
        },
    ]

    report_path = ROOT / f"reports/independent-rerun-check-{datetime.now(timezone.utc):%Y-%m-%d}.json"
    runnable_checks = [
        "python3 scripts/run_independent_rerun_check.py --json",
        "python3 scripts/build_proof_surface.py --json",
        "python3 scripts/build_remote_sync_manifest.py --json",
        "python3 scripts/build_public_citation_pack.py --json",
        "python3 scripts/build_independent_rerun_kit.py --json",
        "python3 scripts/rerun_stale_pack_rotation.py --json",
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "independent_rerun_kit_ready_local",
        "purpose": (
            "Package the smallest verified artifact set and command sequence that a future "
            "second operator can use to rerun the current continuity proof without reconstructing "
            "the repo from scratch."
        ),
        "proof_rollup": {
            "benchmark_cases": summary["benchmark_cases"],
            "scripted_reruns": summary["scripted_reruns"],
            "average_replay_cost_reduction_percent": summary["average_replay_cost_reduction_percent"],
            "average_restart_clarity_ratio": summary["average_restart_clarity_ratio"],
            "stale_verdict_reproduced": summary["stale_verdict_reproduced"],
            "remote_sync_asset_count": remote_manifest["summary"]["asset_count"],
            "public_asset_count": len(citation_pack["public_asset_shortlist"]),
        },
        "independent_operator_goal": (
            "A fresh operator should be able to restate the current continuity thesis, rerun the stale-pack "
            "fixture, and identify the next publish-ready artifact path without opening unrelated workspace files."
        ),
        "single_command_check": "python3 scripts/run_independent_rerun_check.py --json",
        "latest_runner_report": str(report_path),
        "artifact_sequence": artifact_sequence,
        "runnable_checks": runnable_checks,
        "expected_outcomes": [
            (
                f"Confirm operator handoff proof still shows replay cost "
                f"{operator['replay_cost_minutes_raw']} -> {operator['replay_cost_minutes_pack']} minutes "
                f"({operator['replay_cost_reduction_percent']}% reduction)."
            ),
            (
                f"Confirm stale-pack proof still shows replay cost "
                f"{stale['replay_cost_minutes_raw']} -> {stale['replay_cost_minutes_pack']} minutes "
                f"({stale['replay_cost_reduction_percent']}% reduction)."
            ),
            (
                f"Confirm scripted stale rerun still reproduces the expected verdict with "
                f"{rerun['validator_issue_count']} validator issues."
            ),
            "Confirm the next publish boundary remains confirmation-gated rather than auth- or copy-blocked.",
        ],
        "blocking_gap": (
            "The kit is ready locally, but a real independent rerun still needs a second operator or a later session "
            "to execute it and record a fresh report."
        ),
        "next_step": (
            "Hand this kit to the next operator or later session, run the listed checks in order, "
            "and record a new rerun note or report delta."
        ),
    }


def render_markdown(kit: dict[str, object]) -> str:
    rollup = kit["proof_rollup"]
    lines = [
        "# Independent Rerun Kit",
        "",
        "## Current State",
        "",
        f"- status: `{kit['status']}`",
        f"- generated_at: `{kit['generated_at']}`",
        f"- purpose: {kit['purpose']}",
        "",
        "## Proof Rollup",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Benchmark cases | `{rollup['benchmark_cases']}` |",
        f"| Scripted reruns | `{rollup['scripted_reruns']}` |",
        f"| Average replay-cost reduction | `{rollup['average_replay_cost_reduction_percent']}%` |",
        f"| Average restart clarity ratio | `{rollup['average_restart_clarity_ratio']}` |",
        f"| Stale verdict reproduced | `{str(rollup['stale_verdict_reproduced']).lower()}` |",
        f"| Remote-sync assets | `{rollup['remote_sync_asset_count']}` |",
        f"| Public proof assets | `{rollup['public_asset_count']}` |",
        "",
        "## Independent Operator Goal",
        "",
        kit["independent_operator_goal"],
        "",
        "## Artifact Sequence",
        "",
        "| Step | Artifact | Path | Why |",
        "| --- | --- | --- | --- |",
    ]
    for item in kit["artifact_sequence"]:
        lines.append(
            f"| `{item['step']}` | `{item['label']}` | `{item['path']}` | {item['why']} |"
        )

    lines.extend(
        [
            "",
            "## Single-Command Check",
            "",
            f"- `{kit['single_command_check']}`",
            f"- latest_runner_report: `{kit['latest_runner_report']}`",
            "",
            "## Runnable Checks",
            "",
        ]
    )
    for command in kit["runnable_checks"]:
        lines.append(f"- `{command}`")

    lines.extend(["", "## Expected Outcomes", ""])
    for outcome in kit["expected_outcomes"]:
        lines.append(f"- {outcome}")

    lines.extend(
        [
            "",
            "## Remaining Gap",
            "",
            f"- blocking_gap: `{kit['blocking_gap']}`",
            f"- next_step: `{kit['next_step']}`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an independent rerun kit.")
    parser.add_argument(
        "--proof-surface-json",
        default=str(ROOT / "reports/proof-surface-2026-03-27.json"),
    )
    parser.add_argument(
        "--remote-sync-json",
        default=str(ROOT / "reports/remote-sync-manifest-2026-03-27.json"),
    )
    parser.add_argument(
        "--citation-json",
        default=str(ROOT / "reports/public-citation-pack-2026-03-27.json"),
    )
    parser.add_argument(
        "--output-md",
        default=str(ROOT / "docs/independent-rerun-kit.md"),
    )
    parser.add_argument(
        "--output-json",
        default=str(ROOT / "reports/independent-rerun-kit-2026-03-27.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    proof_surface = load_json(Path(args.proof_surface_json))
    remote_manifest = load_json(Path(args.remote_sync_json))
    citation_pack = load_json(Path(args.citation_json))
    kit = build_kit(proof_surface, remote_manifest, citation_pack)

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_md.write_text(render_markdown(kit) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(kit, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(kit, ensure_ascii=True, indent=2))
    else:
        print(f"status: {kit['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(
            "average_replay_cost_reduction_percent: "
            f"{kit['proof_rollup']['average_replay_cost_reduction_percent']}"
        )
        print(f"artifact_sequence_count: {len(kit['artifact_sequence'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
