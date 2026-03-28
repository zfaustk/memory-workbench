#!/usr/bin/env python3
"""Run the current independent rerun checks and write one consolidated report."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("proof_surface", ["python3", "scripts/build_proof_surface.py", "--json"]),
    ("remote_sync_manifest", ["python3", "scripts/build_remote_sync_manifest.py", "--json"]),
    ("public_citation_pack", ["python3", "scripts/build_public_citation_pack.py", "--json"]),
    ("independent_rerun_kit", ["python3", "scripts/build_independent_rerun_kit.py", "--json"]),
    ("stale_pack_scripted_rerun", ["python3", "scripts/rerun_stale_pack_rotation.py", "--json"]),
]


def run_json(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    stdout = completed.stdout.strip()
    if not stdout:
        raise RuntimeError(f"Command produced no JSON output: {' '.join(command)}")
    return json.loads(stdout)


def build_report(step_outputs: dict[str, dict[str, object]]) -> dict[str, object]:
    proof_surface = step_outputs["proof_surface"]
    remote_manifest = step_outputs["remote_sync_manifest"]
    citation_pack = step_outputs["public_citation_pack"]
    rerun_kit = step_outputs["independent_rerun_kit"]
    stale_rerun = step_outputs["stale_pack_scripted_rerun"]
    proof_summary = proof_surface["summary"]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "independent_rerun_check_ready_local",
        "purpose": (
            "Give a future second operator one command that reruns the current continuity proof "
            "checks and records the latest local evidence bundle."
        ),
        "refresh_command": "python3 scripts/run_independent_rerun_check.py --json",
        "steps": [
            {
                "step_id": step_id,
                "status": step_outputs[step_id].get("status", "unknown"),
            }
            for step_id, _ in STEPS
        ],
        "summary": {
            "benchmark_cases": proof_summary["benchmark_cases"],
            "scripted_reruns": proof_summary["scripted_reruns"],
            "average_replay_cost_reduction_percent": proof_summary["average_replay_cost_reduction_percent"],
            "average_restart_clarity_ratio": proof_summary["average_restart_clarity_ratio"],
            "remote_sync_asset_count": remote_manifest["summary"]["asset_count"],
            "public_asset_count": len(citation_pack["public_asset_shortlist"]),
            "independent_rerun_artifact_count": len(rerun_kit["artifact_sequence"]),
            "stale_verdict_reproduced": stale_rerun["stale_verdict_reproduced"],
            "validator_issue_count": stale_rerun["validator_issue_count"],
        },
        "artifacts": {
            "proof_surface_json": str(ROOT / "reports/proof-surface-2026-03-27.json"),
            "remote_sync_manifest_json": str(ROOT / "reports/remote-sync-manifest-2026-03-27.json"),
            "public_citation_pack_json": str(ROOT / "reports/public-citation-pack-2026-03-27.json"),
            "independent_rerun_kit_json": str(ROOT / "reports/independent-rerun-kit-2026-03-27.json"),
            "stale_pack_scripted_rerun_json": str(
                ROOT / "reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json"
            ),
        },
        "expected_outcome": (
            "A later operator can run one command, confirm the stale verdict still reproduces, "
            "and inspect the latest continuity-proof rollup without reconstructing the refresh order."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the current independent rerun checks.")
    parser.add_argument(
        "--output-json",
        default=str(ROOT / f"reports/independent-rerun-check-{datetime.now(timezone.utc):%Y-%m-%d}.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    step_outputs: dict[str, dict[str, object]] = {}
    for step_id, command in STEPS:
        step_outputs[step_id] = run_json(command)

    report = build_report(step_outputs)
    output_path = Path(args.output_json)
    output_path.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        print(f"status: {report['status']}")
        print(f"output_json: {output_path}")
        print(f"validator_issue_count: {report['summary']['validator_issue_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
