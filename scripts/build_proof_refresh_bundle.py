#!/usr/bin/env python3
"""Refresh the current memory-workbench proof artifacts in one command."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    {
        "step_id": "proof_surface",
        "label": "proof surface",
        "command": ["python3", "scripts/build_proof_surface.py"],
        "output_md": "docs/proof-surface.md",
        "output_json": "reports/proof-surface-2026-03-27.json",
    },
    {
        "step_id": "remote_sync_manifest",
        "label": "remote sync manifest",
        "command": ["python3", "scripts/build_remote_sync_manifest.py"],
        "output_md": "docs/remote-sync-manifest.md",
        "output_json": "reports/remote-sync-manifest-2026-03-27.json",
    },
    {
        "step_id": "public_citation_pack",
        "label": "public citation pack",
        "command": ["python3", "scripts/build_public_citation_pack.py"],
        "output_md": "docs/public-citation-pack.md",
        "output_json": "reports/public-citation-pack-2026-03-27.json",
    },
    {
        "step_id": "upstream_issue_packet_memu",
        "label": "upstream issue packet",
        "command": ["python3", "scripts/build_upstream_issue_packet.py", "--preset", "memu"],
        "output_md": "docs/upstream-issue-packet-memu.md",
        "output_json": "reports/upstream-issue-packet-memu-2026-03-27.json",
    },
    {
        "step_id": "independent_rerun_kit",
        "label": "independent rerun kit",
        "command": ["python3", "scripts/build_independent_rerun_kit.py"],
        "output_md": "docs/independent-rerun-kit.md",
        "output_json": "reports/independent-rerun-kit-2026-03-27.json",
    },
    {
        "step_id": "target_system_eval_packet",
        "label": "target-system eval packet",
        "command": ["python3", "scripts/build_target_system_eval_packet.py"],
        "output_md": "docs/target-system-eval-packet.md",
        "output_json": "reports/target-system-eval-packet-2026-03-27.json",
    },
]


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_step(step: dict[str, object]) -> dict[str, object]:
    completed = subprocess.run(
        step["command"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    stdout_lines = [line for line in completed.stdout.strip().splitlines() if line]
    output_md = ROOT / step["output_md"]
    output_json = ROOT / step["output_json"]
    return {
        "step_id": step["step_id"],
        "label": step["label"],
        "command": " ".join(step["command"]),
        "stdout_lines": stdout_lines,
        "output_md": step["output_md"],
        "output_json": step["output_json"],
        "output_md_exists": output_md.exists(),
        "output_json_exists": output_json.exists(),
    }


def build_bundle(step_results: list[dict[str, object]]) -> dict[str, object]:
    proof_surface = load_json(ROOT / "reports/proof-surface-2026-03-27.json")
    remote_manifest = load_json(ROOT / "reports/remote-sync-manifest-2026-03-27.json")
    citation_pack = load_json(ROOT / "reports/public-citation-pack-2026-03-27.json")
    upstream_packet = load_json(ROOT / "reports/upstream-issue-packet-memu-2026-03-27.json")
    rerun_kit = load_json(ROOT / "reports/independent-rerun-kit-2026-03-27.json")
    target_eval_packet = load_json(ROOT / "reports/target-system-eval-packet-2026-03-27.json")

    proof_summary = proof_surface["summary"]
    remote_summary = remote_manifest["summary"]
    citation_summary = citation_pack["proof_summary"]
    rerun_summary = rerun_kit["proof_rollup"]

    generated_assets: list[dict[str, str]] = []
    for result in step_results:
        generated_assets.append(
            {
                "step_id": result["step_id"],
                "path": result["output_md"],
                "kind": "markdown",
            }
        )
        generated_assets.append(
            {
                "step_id": result["step_id"],
                "path": result["output_json"],
                "kind": "json",
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "proof_refresh_bundle_ready_local",
        "purpose": (
            "Rebuild the current proof surface, remote-sync packet, public citation pack, "
            "upstream issue packet, and independent rerun kit in one local command so later "
            "operators do not need to remember the refresh order."
        ),
        "refresh_steps": step_results,
        "proof_rollup": {
            "benchmark_cases": proof_summary["benchmark_cases"],
            "scripted_reruns": proof_summary["scripted_reruns"],
            "average_replay_cost_reduction_percent": proof_summary["average_replay_cost_reduction_percent"],
            "average_restart_clarity_ratio": proof_summary["average_restart_clarity_ratio"],
            "remote_sync_asset_count": remote_summary["asset_count"],
            "public_asset_count": len(citation_pack["public_asset_shortlist"]),
            "independent_rerun_artifact_count": len(rerun_kit["artifact_sequence"]),
            "target_eval_packet_system": target_eval_packet["target_system"]["system_id"],
            "upstream_target": upstream_packet["target_label"],
            "upstream_publish_boundary": upstream_packet["publish_boundary"],
            "stale_verdict_reproduced": citation_summary["stale_verdict_reproduced"],
        },
        "generated_assets": generated_assets,
        "refresh_command": "python3 scripts/build_proof_refresh_bundle.py --json",
        "next_step": (
            "Use the single refresh command after any benchmark or proof change, then hand the "
            "independent rerun kit to a later operator or republish the refreshed bundle after any proof change."
        ),
    }


def render_markdown(bundle: dict[str, object]) -> str:
    rollup = bundle["proof_rollup"]
    lines = [
        "# Proof Refresh Bundle",
        "",
        "## Current State",
        "",
        f"- status: `{bundle['status']}`",
        f"- generated_at: `{bundle['generated_at']}`",
        f"- purpose: {bundle['purpose']}",
        "",
        "## Proof Rollup",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Benchmark cases | `{rollup['benchmark_cases']}` |",
        f"| Scripted reruns | `{rollup['scripted_reruns']}` |",
        f"| Average replay-cost reduction | `{rollup['average_replay_cost_reduction_percent']}%` |",
        f"| Average restart clarity ratio | `{rollup['average_restart_clarity_ratio']}` |",
        f"| Remote-sync assets | `{rollup['remote_sync_asset_count']}` |",
        f"| Public proof assets | `{rollup['public_asset_count']}` |",
        f"| Independent rerun artifacts | `{rollup['independent_rerun_artifact_count']}` |",
        f"| Target eval packet system | `{rollup['target_eval_packet_system']}` |",
        f"| Upstream target | `{rollup['upstream_target']}` |",
        f"| Upstream publish boundary | `{rollup['upstream_publish_boundary']}` |",
        f"| Stale verdict reproduced | `{str(rollup['stale_verdict_reproduced']).lower()}` |",
        "",
        "## Refresh Steps",
        "",
        "| Step | Command | Markdown | JSON |",
        "| --- | --- | --- | --- |",
    ]
    for result in bundle["refresh_steps"]:
        lines.append(
            f"| `{result['label']}` | `{result['command']}` | "
            f"`{result['output_md']}` | `{result['output_json']}` |"
        )

    lines.extend(["", "## Generated Assets", ""])
    for asset in bundle["generated_assets"]:
        lines.append(f"- `{asset['step_id']}` `{asset['kind']}`: `{asset['path']}`")

    lines.extend(
        [
            "",
            "## Single Refresh Command",
            "",
            f"- `{bundle['refresh_command']}`",
            "",
            "## Remaining Gap",
            "",
            f"- next_step: `{bundle['next_step']}`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh all local proof builders in one command.")
    parser.add_argument(
        "--output-md",
        default=str(ROOT / "docs/proof-refresh-bundle.md"),
    )
    parser.add_argument(
        "--output-json",
        default=str(ROOT / "reports/proof-refresh-bundle-2026-03-27.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    step_results = [run_step(step) for step in STEPS]
    bundle = build_bundle(step_results)

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_md.write_text(render_markdown(bundle) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(bundle, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(bundle, ensure_ascii=True, indent=2))
    else:
        print(f"status: {bundle['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(f"refreshed_steps: {len(bundle['refresh_steps'])}")
        print(f"generated_asset_count: {len(bundle['generated_assets'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
