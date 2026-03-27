#!/usr/bin/env python3
"""Build a reusable eval packet for benchmarking an external memory system."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/ROOM/projects/memory-workbench")


def build_packet(args: argparse.Namespace) -> dict[str, object]:
    continuity_contract = [
        "problem",
        "current_state",
        "last_verified_facts",
        "decisions_and_why",
        "next_actions",
        "open_risks",
        "evidence_index",
        "operator_notes",
        "last_verified_at",
        "stale_check",
    ]
    commands = [
        "python3 scripts/validate_continuity_artifacts.py --pack <pack-path> --report <report-path>",
        "python3 scripts/build_proof_surface.py --json",
        "python3 scripts/build_target_system_eval_packet.py --json",
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "target_system_eval_packet_ready_local",
        "purpose": (
            "Give a future operator one fixed intake packet for benchmarking an external memory "
            "system against the continuity benchmark without inventing the eval structure from scratch."
        ),
        "target_system": {
            "system_id": args.system_id,
            "system_label": args.system_label,
            "system_type": args.system_type,
        },
        "evaluation_question": (
            "Does this target memory system reduce restart cost, preserve decision-relevant state, "
            "and detect stale state before action on a real interrupted workflow slice?"
        ),
        "workflow_contract": {
            "workflow_slice": args.workflow_slice,
            "interruption_boundary": args.interruption_boundary,
            "expected_next_action": args.expected_next_action,
            "continuity_artifact_path": args.continuity_artifact_path,
            "source_paths": args.source_path,
        },
        "continuity_contract": continuity_contract,
        "ab_conditions": [
            {
                "condition": "A",
                "label": "raw trace only",
                "operator_rule": "Use the bounded workflow slice and raw source paths without the target continuity artifact.",
            },
            {
                "condition": "B",
                "label": "raw trace + target continuity artifact",
                "operator_rule": "Start from the target continuity artifact, then open linked evidence only when needed.",
            },
        ],
        "scoring_focus": [
            "restart_clarity_score",
            "second_operator_success_rate",
            "evidence_traceability_score",
            "replay_cost_minutes",
            "stale_state_detected_before_action",
        ],
        "required_outputs": [
            "one filled continuity report under reports/",
            "one sentence on which field carried the most value",
            "one sentence on what remained unsafe or ambiguous",
            "one stale-state verdict if the source-of-truth can drift",
        ],
        "pass_partial_fail": {
            "pass": "Replay cost drops by at least 50 percent, clarity improves across at least 3 rubric dimensions, and no factual regression is introduced.",
            "partial": "The artifact helps, but the gain is weak or stale handling remains fragile.",
            "fail": "The artifact does not materially reduce restart cost, or it introduces wrong state or unsafe next actions.",
        },
        "runnable_commands": commands,
        "next_step": (
            "Replace the placeholder workflow and artifact paths with one real interrupted task slice, "
            "then run the A/B comparison and record the result as a new continuity report."
        ),
    }


def render_markdown(packet: dict[str, object]) -> str:
    target = packet["target_system"]
    contract = packet["workflow_contract"]
    lines = [
        "# Target System Eval Packet",
        "",
        "## Current State",
        "",
        f"- status: `{packet['status']}`",
        f"- generated_at: `{packet['generated_at']}`",
        f"- purpose: {packet['purpose']}",
        "",
        "## Target System",
        "",
        f"- system_id: `{target['system_id']}`",
        f"- system_label: `{target['system_label']}`",
        f"- system_type: `{target['system_type']}`",
        "",
        "## Evaluation Question",
        "",
        packet["evaluation_question"],
        "",
        "## Workflow Contract",
        "",
        f"- workflow_slice: `{contract['workflow_slice']}`",
        f"- interruption_boundary: `{contract['interruption_boundary']}`",
        f"- expected_next_action: `{contract['expected_next_action']}`",
        f"- continuity_artifact_path: `{contract['continuity_artifact_path']}`",
        "- source_paths:",
    ]
    for path in contract["source_paths"]:
        lines.append(f"  - `{path}`")

    lines.extend(["", "## Continuity Contract", ""])
    for field in packet["continuity_contract"]:
        lines.append(f"- `{field}`")

    lines.extend(["", "## A/B Conditions", ""])
    for condition in packet["ab_conditions"]:
        lines.append(
            f"- `{condition['condition']}` `{condition['label']}`: {condition['operator_rule']}"
        )

    lines.extend(["", "## Scoring Focus", ""])
    for metric in packet["scoring_focus"]:
        lines.append(f"- `{metric}`")

    lines.extend(["", "## Required Outputs", ""])
    for item in packet["required_outputs"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Pass / Partial / Fail",
            "",
            f"- `pass`: {packet['pass_partial_fail']['pass']}",
            f"- `partial`: {packet['pass_partial_fail']['partial']}",
            f"- `fail`: {packet['pass_partial_fail']['fail']}",
            "",
            "## Runnable Commands",
            "",
        ]
    )
    for command in packet["runnable_commands"]:
        lines.append(f"- `{command}`")

    lines.extend(
        [
            "",
            "## Next Step",
            "",
            f"- `{packet['next_step']}`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a target-system eval packet.")
    parser.add_argument("--system-id", default="new-honest")
    parser.add_argument("--system-label", default="new honest continuity candidate")
    parser.add_argument("--system-type", default="memory-system")
    parser.add_argument(
        "--workflow-slice",
        default="replace-with-one-real-interrupted-workflow-slice",
    )
    parser.add_argument(
        "--interruption-boundary",
        default="replace-with-one-concrete-boundary-before-the-next-safe-action",
    )
    parser.add_argument(
        "--expected-next-action",
        default="replace-with-the-one-safe-next-action-the-fresh-operator-should-take",
    )
    parser.add_argument(
        "--continuity-artifact-path",
        default="replace-with-target-system-artifact-path",
    )
    parser.add_argument(
        "--source-path",
        action="append",
        default=[
            "replace-with-raw-trace-or-task-slice-path-001",
            "replace-with-source-of-truth-path-002",
        ],
    )
    parser.add_argument(
        "--output-md",
        default=str(ROOT / "docs/target-system-eval-packet.md"),
    )
    parser.add_argument(
        "--output-json",
        default=str(ROOT / "reports/target-system-eval-packet-2026-03-27.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON packet.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_packet(args)

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_md.write_text(render_markdown(packet) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(packet, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(packet, ensure_ascii=True, indent=2))
    else:
        print(f"status: {packet['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(f"target_system: {packet['target_system']['system_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
