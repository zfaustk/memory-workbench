#!/usr/bin/env python3
"""Build a compact upstream issue packet from local proof assets."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TARGET_PRESETS = {
    "memu": {
        "target_label": "NevaMind-AI / memU",
        "repo_slug": "NevaMind-AI/memU",
        "repo_url": "https://github.com/NevaMind-AI/memU/issues/new/choose",
        "issue_title": "Add auditable workflow trace and resumable state alongside proactive memory",
        "story": "proactive memory, continuous intent capture, and lower token cost",
        "adjacent_wedge": "workflow continuity with auditable trace and resumable state",
    },
    "openmemory": {
        "target_label": "CaviraOSS / OpenMemory",
        "repo_slug": "CaviraOSS/OpenMemory",
        "repo_url": "https://github.com/CaviraOSS/OpenMemory/issues/new/choose",
        "issue_title": "Add auditable workflow trace and resumable state alongside explainable recall",
        "story": "real long-term memory, explainable traces, and shared memory infrastructure",
        "adjacent_wedge": "workflow continuity that turns explainable recall into safer handoff and resume",
    },
    "memos": {
        "target_label": "MemTensor / MemOS",
        "repo_slug": "MemTensor/MemOS",
        "repo_url": "https://github.com/MemTensor/MemOS/issues/new/choose",
        "issue_title": "Add auditable workflow trace and resumable checkpoints on top of the memory OS",
        "story": "multi-agent memory, lower token usage, and a unified memory API",
        "adjacent_wedge": "workflow continuity with auditable trace and cheaper cross-operator resume",
    },
}


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_packet(
    citation_pack: dict[str, object],
    target_label: str,
    repo_slug: str,
    repo_url: str,
    issue_title: str,
    story: str,
    adjacent_wedge: str,
) -> dict[str, object]:
    summary = citation_pack["proof_summary"]
    proof_points = citation_pack["proof_points"]
    copy_blocks = citation_pack["copy_blocks"]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "upstream_issue_packet_ready_local",
        "target_label": target_label,
        "repo_slug": repo_slug,
        "repo_url": repo_url,
        "issue_title": issue_title,
        "purpose": (
            "Compress local workflow-continuity proof into a submit-ready packet "
            "for an upstream issue without crossing the publish boundary."
        ),
        "proof_rollup": {
            "benchmark_cases": summary["benchmark_cases"],
            "scripted_reruns": summary["scripted_reruns"],
            "average_replay_cost_reduction_percent": summary["average_replay_cost_reduction_percent"],
            "average_restart_clarity_ratio": summary["average_restart_clarity_ratio"],
            "stale_verdict_reproduced": summary["stale_verdict_reproduced"],
        },
        "positioning": {
            "target_fit": (
                f"{target_label} already has a public story around {story}, "
                f"so the adjacent wedge is {adjacent_wedge}."
            ),
            "why_now": (
                "Current local proof shows workflow continuity can be measured with "
                "restart clarity, replay-cost reduction, and stale-state detection "
                "instead of generic memory claims."
            ),
        },
        "proof_points": proof_points,
        "copy_blocks": {
            "short_issue_hook": copy_blocks["upstream_issue_short"],
            "opening": (
                f"{target_label} already has a strong public story around {story}.\n\n"
                "The adjacent gap in long-running agent workflows is not only whether memory persists, "
                "but whether another operator can inspect what changed, understand the latest decision "
                "path, and safely continue work without replaying the entire trace."
            ),
            "problem": (
                "When a workflow drifts or pauses, teams often lose the operational layer between "
                "\"memory exists\" and \"work can safely continue\":\n\n"
                "1. the last action path is hard to inspect,\n"
                "2. the next executable step is mixed with raw trace,\n"
                "3. stale cached state is easy to reuse by mistake,\n"
                "4. replay and debugging cost stays high even if recall quality is decent."
            ),
            "proposed_improvement": (
                "Add an optional workflow-continuity layer next to proactive memory:\n\n"
                "1. keep an auditable action and decision trace for important workflow transitions,\n"
                "2. preserve resumable workflow state, not only memory items,\n"
                "3. expose a compact resume path for second-operator handoff,\n"
                "4. make stale-state detection explicit before action."
            ),
            "proof_block": (
                f"- operator handoff reduced replay cost from 4.0 to 1.5 minutes (62.5% reduction)\n"
                f"- stale-pack rotation reduced stale-check replay cost from 3.0 to 1.0 minute (66.7% reduction)\n"
                f"- the stale verdict reproduces through a scripted validator-backed rerun\n"
                f"- average replay-cost reduction across the current proof set is "
                f"{summary['average_replay_cost_reduction_percent']}%"
            ),
            "minimal_eval_slice": (
                "One lightweight way to test this without broad product churn:\n\n"
                "1. pick one continuity-critical workflow,\n"
                "2. define the current raw-trace-only resume path,\n"
                "3. add a compact continuity artifact with action trace + resumable state + stale-check,\n"
                "4. measure replay cost, restart clarity, and stale-detection quality before vs after."
            ),
        },
        "source_paths": {
            "citation_pack_markdown": "docs/public-citation-pack.md",
            "citation_pack_json": "reports/public-citation-pack-2026-03-27.json",
            "proof_surface_json": "reports/proof-surface-2026-03-27.json",
            "operator_handoff_report": "reports/operator-handoff-001-report-2026-03-26.md",
            "stale_pack_rotation_report": "reports/stale-pack-rotation-001-report-2026-03-26.md",
            "validator": "scripts/validate_continuity_artifacts.py",
        },
        "next_step_if_confirmed": (
            f"Open {repo_url} and compress the packet into one upstream issue for {repo_slug}."
        ),
        "publish_boundary": "waiting_confirmation",
    }


def render_markdown(packet: dict[str, object]) -> str:
    proof_rollup = packet["proof_rollup"]
    lines = [
        "# Upstream Issue Packet",
        "",
        "## Current State",
        "",
        f"- status: `{packet['status']}`",
        f"- generated_at: `{packet['generated_at']}`",
        f"- target_label: `{packet['target_label']}`",
        f"- repo_slug: `{packet['repo_slug']}`",
        f"- repo_url: `{packet['repo_url']}`",
        f"- issue_title: `{packet['issue_title']}`",
        f"- purpose: {packet['purpose']}",
        "",
        "## Proof Rollup",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Benchmark cases | `{proof_rollup['benchmark_cases']}` |",
        f"| Scripted reruns | `{proof_rollup['scripted_reruns']}` |",
        f"| Average replay-cost reduction | `{proof_rollup['average_replay_cost_reduction_percent']}%` |",
        f"| Average restart clarity ratio | `{proof_rollup['average_restart_clarity_ratio']}` |",
        f"| Stale verdict reproduced | `{str(proof_rollup['stale_verdict_reproduced']).lower()}` |",
        "",
        "## Positioning",
        "",
        f"- target_fit: {packet['positioning']['target_fit']}",
        f"- why_now: {packet['positioning']['why_now']}",
        "",
        "## Suggested Issue Title",
        "",
        packet["issue_title"],
        "",
        "## Compact Issue Hook",
        "",
        packet["copy_blocks"]["short_issue_hook"],
        "",
        "## Ready-to-Paste Body Blocks",
        "",
        "### Opening",
        "",
        packet["copy_blocks"]["opening"],
        "",
        "### Problem",
        "",
        packet["copy_blocks"]["problem"],
        "",
        "### Proposed Improvement",
        "",
        packet["copy_blocks"]["proposed_improvement"],
        "",
        "### Local Proof",
        "",
        packet["copy_blocks"]["proof_block"],
        "",
        "### Minimal Eval Slice",
        "",
        packet["copy_blocks"]["minimal_eval_slice"],
        "",
        "## Proof Points",
        "",
    ]
    for point in packet["proof_points"]:
        lines.append(f"- `{point['label']}`: {point['result']}")
        lines.append(f"  - source: `{point['source']}`")

    lines.extend(
        [
            "",
            "## Source Paths",
            "",
        ]
    )
    for key, value in packet["source_paths"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(
        [
            "",
            "## Publish Boundary",
            "",
            f"- publish_boundary: `{packet['publish_boundary']}`",
            f"- next_step_if_confirmed: {packet['next_step_if_confirmed']}",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an upstream issue packet.")
    parser.add_argument(
        "--preset",
        choices=sorted(TARGET_PRESETS),
        default="memu",
        help="Target preset used to seed labels, URLs, titles, and output paths.",
    )
    parser.add_argument(
        "--citation-json",
        default=str(ROOT / "reports/public-citation-pack-2026-03-27.json"),
    )
    parser.add_argument(
        "--target-label",
        default=None,
    )
    parser.add_argument(
        "--repo-slug",
        default=None,
    )
    parser.add_argument(
        "--repo-url",
        default=None,
    )
    parser.add_argument(
        "--issue-title",
        default=None,
    )
    parser.add_argument(
        "--output-md",
        default=None,
    )
    parser.add_argument(
        "--output-json",
        default=None,
    )
    parser.add_argument("--json", action="store_true", help="Print JSON packet.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    preset = TARGET_PRESETS[args.preset]
    citation_pack = load_json(Path(args.citation_json))
    target_label = args.target_label or preset["target_label"]
    repo_slug = args.repo_slug or preset["repo_slug"]
    repo_url = args.repo_url or preset["repo_url"]
    issue_title = args.issue_title or preset["issue_title"]
    output_md = Path(
        args.output_md or ROOT / "docs" / f"upstream-issue-packet-{args.preset}.md"
    )
    output_json = Path(
        args.output_json
        or ROOT / "reports" / f"upstream-issue-packet-{args.preset}-2026-03-27.json"
    )
    packet = build_packet(
        citation_pack=citation_pack,
        target_label=target_label,
        repo_slug=repo_slug,
        repo_url=repo_url,
        issue_title=issue_title,
        story=preset["story"],
        adjacent_wedge=preset["adjacent_wedge"],
    )

    output_md.write_text(render_markdown(packet) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(packet, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(packet, ensure_ascii=True, indent=2))
    else:
        print(f"status: {packet['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(
            "average_replay_cost_reduction_percent: "
            f"{packet['proof_rollup']['average_replay_cost_reduction_percent']}"
        )
        print(f"target: {packet['target_label']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
