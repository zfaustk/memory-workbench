#!/usr/bin/env python3
"""Build a compact remote-sync manifest for memory-workbench proof assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/ROOM/projects/memory-workbench")
DEFAULT_FILES: tuple[tuple[str, str, str], ...] = (
    ("docs", "proof_surface", "docs/proof-surface.md"),
    ("docs", "architecture", "docs/architecture.md"),
    ("docs", "product_spec", "docs/product-spec.md"),
    ("examples", "resume_demo", "examples/resume-demo.md"),
    ("evals", "continuity_benchmark", "evals/continuity-benchmark.md"),
    ("cases", "operator_handoff_case", "cases/operator-handoff-001.md"),
    ("cases", "stale_pack_rotation_case", "cases/stale-pack-rotation-001.md"),
    ("reports", "proof_surface_json", "reports/proof-surface-2026-03-27.json"),
    (
        "reports",
        "operator_handoff_report",
        "reports/operator-handoff-001-report-2026-03-26.md",
    ),
    (
        "reports",
        "stale_pack_rotation_report",
        "reports/stale-pack-rotation-001-report-2026-03-26.md",
    ),
    (
        "reports",
        "stale_pack_rotation_rerun",
        "reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json",
    ),
    ("scripts", "proof_surface_builder", "scripts/build_proof_surface.py"),
    ("scripts", "remote_sync_manifest_builder", "scripts/build_remote_sync_manifest.py"),
    ("scripts", "stale_rerun_harness", "scripts/rerun_stale_pack_rotation.py"),
    ("scripts", "continuity_validator", "scripts/validate_continuity_artifacts.py"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for group, asset_id, relative_path in DEFAULT_FILES:
        path = ROOT / relative_path
        stat = path.stat()
        entries.append(
            {
                "group": group,
                "asset_id": asset_id,
                "path": relative_path,
                "bytes": stat.st_size,
                "sha256": sha256(path),
            }
        )
    return entries


def build_manifest(entries: list[dict[str, object]]) -> dict[str, object]:
    total_bytes = sum(int(entry["bytes"]) for entry in entries)
    groups = sorted({str(entry["group"]) for entry in entries})
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "remote_sync_ready_local",
        "repo_root": str(ROOT),
        "summary": {
            "asset_count": len(entries),
            "group_count": len(groups),
            "groups": groups,
            "total_bytes": total_bytes,
        },
        "sync_bundle": entries,
        "next_step": "Push this asset set once gh auth and git push are available again.",
        "blocking_gap": "remote git auth still unavailable in the current lane",
    }


def render_markdown(manifest: dict[str, object]) -> str:
    summary = manifest["summary"]
    entries = manifest["sync_bundle"]
    lines = [
        "# Remote Sync Manifest",
        "",
        "## Current State",
        "",
        f"- status: `{manifest['status']}`",
        "- purpose: list the exact proof assets that should be pushed first when remote git auth is restored",
        f"- generated_at: `{manifest['generated_at']}`",
        f"- repo_root: `{manifest['repo_root']}`",
        "",
        "## Rollup",
        "",
        "| Signal | Value |",
        "| --- | --- |",
        f"| Asset count | `{summary['asset_count']}` |",
        f"| Group count | `{summary['group_count']}` |",
        f"| Groups | `{', '.join(summary['groups'])}` |",
        f"| Total bytes | `{summary['total_bytes']}` |",
        "",
        "## Sync Bundle",
        "",
        "| Group | Asset | Path | Bytes | SHA256 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            f"| `{entry['group']}` | `{entry['asset_id']}` | "
            f"`{entry['path']}` | `{entry['bytes']}` | `{entry['sha256'][:12]}` |"
        )
    lines.extend(
        [
            "",
            "## Push Order",
            "",
            "1. docs + examples + evals + cases",
            "2. reports",
            "3. scripts",
            "",
            "## Runnable Checks",
            "",
            "- `python3 scripts/build_proof_surface.py --json`",
            "- `python3 scripts/rerun_stale_pack_rotation.py --json`",
            "- `python3 scripts/build_remote_sync_manifest.py --json`",
            "",
            "## Remaining Gap",
            "",
            f"- next_step: `{manifest['next_step']}`",
            f"- blocking_gap: `{manifest['blocking_gap']}`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a remote-sync manifest.")
    parser.add_argument(
        "--output-md",
        default=str(ROOT / "docs/remote-sync-manifest.md"),
    )
    parser.add_argument(
        "--output-json",
        default=str(ROOT / "reports/remote-sync-manifest-2026-03-27.json"),
    )
    parser.add_argument("--json", action="store_true", help="Print JSON manifest.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    entries = build_entries()
    manifest = build_manifest(entries)

    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    output_md.write_text(render_markdown(manifest) + "\n", encoding="utf-8")
    output_json.write_text(json.dumps(manifest, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, ensure_ascii=True, indent=2))
    else:
        print(f"status: {manifest['status']}")
        print(f"output_md: {output_md}")
        print(f"output_json: {output_json}")
        print(f"asset_count: {manifest['summary']['asset_count']}")
        print(f"group_count: {manifest['summary']['group_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
