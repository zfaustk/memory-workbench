#!/usr/bin/env python3
"""Build a compact public citation pack from existing memory-workbench proof assets."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/ROOM/projects/memory-workbench")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_pack(proof_surface: dict[str, object], remote_manifest: dict[str, object]) -> dict[str, object]:
    operator = proof_surface["operator_handoff"]
    stale = proof_surface["stale_pack_rotation"]
    rerun = proof_surface["scripted_rerun"]
    proof_summary = proof_surface["summary"]
    manifest_summary = remote_manifest["summary"]

    public_assets = []
    for entry in remote_manifest["sync_bundle"]:
        if entry["group"] not in {"docs", "examples", "evals", "reports"}:
            continue
        public_assets.append(
            {
                "group": entry["group"],
                "asset_id": entry["asset_id"],
                "path": entry["path"],
                "sha256_short": entry["sha256"][:12],
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "citation_pack_ready_local",
        "purpose": "Give one compact proof packet that can be pasted into a profile README, upstream issue, or publish page.",
        "proof_summary": {
            "benchmark_cases": proof_summary["benchmark_cases"],
            "scripted_reruns": proof_summary["scripted_reruns"],
            "average_replay_cost_reduction_percent": proof_summary["average_replay_cost_reduction_percent"],
            "average_restart_clarity_ratio": round(
                float(proof_summary["average_restart_clarity_ratio"]), 2
            ),
            "stale_verdict_reproduced": proof_summary["stale_verdict_reproduced"],
            "asset_count_ready_for_remote_sync": manifest_summary["asset_count"],
        },
        "headline_hooks": [
            "Built two continuity benchmark cases plus one scripted stale-state rerun for long-running agent workflows.",
            f"Average replay cost dropped {proof_summary['average_replay_cost_reduction_percent']}% across the current proof set.",
            "The repo now includes a generated target-system eval packet so external memory systems can be benchmarked with a fixed intake contract.",
            "Current proof bundle is already packaged for first remote sync once git auth returns.",
        ],
        "proof_points": [
            {
                "label": "operator_handoff",
                "result": (
                    f"Replay cost {operator['replay_cost_minutes_raw']} -> "
                    f"{operator['replay_cost_minutes_pack']} minutes "
                    f"({operator['replay_cost_reduction_percent']}% reduction); "
                    f"restart clarity {operator['restart_clarity_score']}."
                ),
                "source": operator["path"],
            },
            {
                "label": "stale_pack_rotation",
                "result": (
                    f"Replay cost {stale['replay_cost_minutes_raw']} -> "
                    f"{stale['replay_cost_minutes_pack']} minutes "
                    f"({stale['replay_cost_reduction_percent']}% reduction); "
                    "validator stops stale lane reuse before action."
                ),
                "source": stale["path"],
            },
            {
                "label": "scripted_rerun",
                "result": (
                    f"Scripted replay reproduced the stale verdict with "
                    f"{rerun['validator_issue_count']} expected validator issues."
                ),
                "source": rerun["artifacts"]["validator"],
            },
        ],
        "copy_blocks": {
            "profile_readme_short": (
                "Built a memory-workbench for long-running agents: 2 continuity benchmark "
                "cases + 1 scripted stale-state rerun, with 64.6% average replay-cost reduction "
                "and a first remote-sync proof bundle ready for publish."
            ),
            "upstream_issue_short": (
                "Current local proof shows workflow continuity is measurable: "
                "operator handoff cut replay cost from 4.0 to 1.5 minutes, stale-pack detection "
                "cut stale-check cost from 3.0 to 1.0 minute, and the stale verdict now reproduces "
                "through a scripted validator-backed rerun."
            ),
            "publish_page_short": (
                "memory-workbench packages auditable workflow continuity for agents: "
                "compact proof surface, stale-state replay checks, a generated external-eval intake packet, "
                "and a remote-sync-ready artifact bundle for public release."
            ),
        },
        "public_asset_shortlist": public_assets,
        "next_gap": "independent_second_operator_rerun_or_remote_sync",
    }


def render_markdown(pack: dict[str, object]) -> str:
    summary = pack["proof_summary"]
    lines = [
        "# Public Citation Pack",
        "",
        "## Current State",
        "",
        f"- status: `{pack['status']}`",
        f"- generated_at: `{pack['generated_at']}`",
        f"- purpose: {pack['purpose']}",
        "",
        "## Rollup",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Benchmark cases | `{summary['benchmark_cases']}` |",
        f"| Scripted reruns | `{summary['scripted_reruns']}` |",
        f"| Average replay-cost reduction | `{summary['average_replay_cost_reduction_percent']}%` |",
        f"| Average restart clarity ratio | `{summary['average_restart_clarity_ratio']}` |",
        f"| Stale verdict reproduced | `{str(summary['stale_verdict_reproduced']).lower()}` |",
        f"| Remote-sync-ready assets | `{summary['asset_count_ready_for_remote_sync']}` |",
        "",
        "## Headline Hooks",
        "",
    ]
    for item in pack["headline_hooks"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Proof Points", ""])
    for point in pack["proof_points"]:
        lines.append(f"- `{point['label']}`: {point['result']}")
        lines.append(f"  - source: `{point['source']}`")

    lines.extend(
        [
            "",
            "## Copy Blocks",
            "",
            "### Profile README",
            "",
            pack["copy_blocks"]["profile_readme_short"],
            "",
            "### Upstream Issue",
            "",
            pack["copy_blocks"]["upstream_issue_short"],
            "",
            "### Publish Page",
            "",
            pack["copy_blocks"]["publish_page_short"],
            "",
            "## Public Asset Shortlist",
            "",
            "| Group | Asset | Path | SHA256 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for asset in pack["public_asset_shortlist"]:
        lines.append(
            f"| `{asset['group']}` | `{asset['asset_id']}` | "
            f"`{asset['path']}` | `{asset['sha256_short']}` |"
        )

    lines.extend(
        [
            "",
            "## Runnable Commands",
            "",
            "- `python3 scripts/build_proof_surface.py --json`",
            "- `python3 scripts/build_remote_sync_manifest.py --json`",
            "- `python3 scripts/build_public_citation_pack.py --json`",
            "",
            "## Remaining Gap",
            "",
            f"- next_gap: `{pack['next_gap']}`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a public citation pack.")
    parser.add_argument(
        "--proof-surface-json",
        default=str(ROOT / "reports/proof-surface-2026-03-27.json"),
    )
    parser.add_argument(
        "--remote-sync-json",
        default=str(ROOT / "reports/remote-sync-manifest-2026-03-27.json"),
    )
    parser.add_argument(
        "--output-md",
        default=str(ROOT / "docs/public-citation-pack.md"),
    )
    parser.add_argument(
        "--output-json",
        default=str(ROOT / "reports/public-citation-pack-2026-03-27.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON pack.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    proof_surface = load_json(Path(args.proof_surface_json))
    remote_manifest = load_json(Path(args.remote_sync_json))
    pack = build_pack(proof_surface, remote_manifest)

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_md.write_text(render_markdown(pack) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(pack, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(pack, ensure_ascii=True, indent=2))
    else:
        print(f"status: {pack['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(
            "average_replay_cost_reduction_percent: "
            f"{pack['proof_summary']['average_replay_cost_reduction_percent']}"
        )
        print(
            f"asset_count_ready_for_remote_sync: {pack['proof_summary']['asset_count_ready_for_remote_sync']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
