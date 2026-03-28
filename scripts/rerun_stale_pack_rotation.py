#!/usr/bin/env python3
"""Replay the stale-pack rotation case and assert the stale verdict is reproducible."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = ROOT / "packs/stale-pack-rotation-001/continuity-pack-stale.md"
DEFAULT_REPORT = ROOT / "reports/stale-pack-rotation-001-report-2026-03-26.md"
DEFAULT_SOURCE_PACKET = Path("/ROOM/artifacts/deliverables/public-outreach-next-step.md")
DEFAULT_SOURCE_TRACKER = Path("/ROOM/tasks/ai-memory-saas/outreach-tracker.md")
DEFAULT_VALIDATOR = ROOT / "scripts/validate_continuity_artifacts.py"
DEFAULT_OUTPUT = ROOT / "reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json"

EXPECTED_SUBSTRINGS = (
    "freshness: pack `recommended_lane` does not match packet `recommendation`",
    "freshness: pack command does not match packet `recommended_primary_open_command`",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replay stale-pack-rotation-001 with the canonical validator."
    )
    parser.add_argument("--pack", default=str(DEFAULT_PACK))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--source-packet", default=str(DEFAULT_SOURCE_PACKET))
    parser.add_argument("--source-tracker", default=str(DEFAULT_SOURCE_TRACKER))
    parser.add_argument("--validator", default=str(DEFAULT_VALIDATOR))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    return parser.parse_args()


def run_validator(args: argparse.Namespace) -> tuple[int, dict[str, object], str]:
    command = [
        sys.executable,
        args.validator,
        "--pack",
        args.pack,
        "--report",
        args.report,
        "--source-packet",
        args.source_packet,
        "--source-tracker",
        args.source_tracker,
        "--json",
    ]
    proc = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    stdout = proc.stdout.strip()
    if not stdout:
        raise RuntimeError(f"validator returned no JSON output; stderr={proc.stderr.strip()}")
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"validator returned invalid JSON: {exc}") from exc
    return proc.returncode, payload, proc.stderr.strip()


def main() -> int:
    args = parse_args()
    validator_exit_code, validator_payload, validator_stderr = run_validator(args)
    issues = validator_payload.get("issues") or []
    issue_text = "\n".join(str(item) for item in issues)
    missing_expected = [
        snippet for snippet in EXPECTED_SUBSTRINGS if snippet not in issue_text
    ]
    stale_detected = (
        validator_exit_code != 0
        and not bool(validator_payload.get("ok"))
        and not missing_expected
    )

    replay_payload = {
        "case_id": "stale-pack-rotation-001",
        "date": "2026-03-27",
        "operator": "Clio scripted replay harness",
        "status": "pass" if stale_detected else "fail",
        "stale_verdict_reproduced": stale_detected,
        "validator_exit_code": validator_exit_code,
        "validator_ok": validator_payload.get("ok"),
        "validator_issue_count": validator_payload.get("issue_count"),
        "expected_issue_snippets": list(EXPECTED_SUBSTRINGS),
        "missing_expected_issue_snippets": missing_expected,
        "validator_issues": issues,
        "freshness": validator_payload.get("freshness") or {},
        "artifacts": {
            "pack": args.pack,
            "report": args.report,
            "source_packet": args.source_packet,
            "source_tracker": args.source_tracker,
            "validator": args.validator,
        },
        "notes": [
            "The scripted replay passes only when the stale pack still fails validation for the expected freshness reasons.",
            "A validator failure is the desired outcome for this fixture, because the pack intentionally points at an outdated lane and command.",
        ],
    }
    if validator_stderr:
        replay_payload["validator_stderr"] = validator_stderr

    output_path = Path(args.output)
    output_path.write_text(json.dumps(replay_payload, ensure_ascii=True, indent=2) + "\n")

    if args.json:
        print(json.dumps(replay_payload, ensure_ascii=True, indent=2))
    else:
        print(f"status: {replay_payload['status']}")
        print(f"output: {output_path}")
        print(f"stale_verdict_reproduced: {str(stale_detected).lower()}")
        print(f"validator_issue_count: {replay_payload['validator_issue_count']}")
        if missing_expected:
            print("missing_expected_issue_snippets:")
            for snippet in missing_expected:
                print(f"- {snippet}")

    return 0 if stale_detected else 1


if __name__ == "__main__":
    raise SystemExit(main())
