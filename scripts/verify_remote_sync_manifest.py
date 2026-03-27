#!/usr/bin/env python3
"""Verify whether the generated remote-sync manifest still matches local files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path("/ROOM/projects/memory-workbench")
MANIFEST_PATH = ROOT / "reports/remote-sync-manifest-2026-03-27.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compare_entry(entry: dict[str, object]) -> dict[str, object]:
    relative_path = Path(str(entry["path"]))
    target = ROOT / relative_path
    exists = target.exists()
    actual_bytes = None
    actual_sha256 = None
    matches = False

    if exists:
        stat = target.stat()
        actual_bytes = stat.st_size
        actual_sha256 = sha256(target)
        matches = (
            actual_bytes == int(entry["bytes"])
            and actual_sha256 == str(entry["sha256"])
        )

    return {
        "group": entry["group"],
        "asset_id": entry["asset_id"],
        "path": str(target),
        "exists": exists,
        "expected_bytes": entry["bytes"],
        "actual_bytes": actual_bytes,
        "expected_sha256": entry["sha256"],
        "actual_sha256": actual_sha256,
        "matches": matches,
    }


def build_report() -> dict[str, object]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    checks = [compare_entry(entry) for entry in manifest["sync_bundle"]]
    stale_items = [
        check["asset_id"]
        for check in checks
        if not check["exists"] or not check["matches"]
    ]
    status = "fresh" if not stale_items else "stale"
    return {
        "status": status,
        "manifest_path": str(MANIFEST_PATH),
        "repo_root": str(ROOT),
        "checked_item_count": len(checks),
        "stale_item_count": len(stale_items),
        "stale_items": stale_items,
        "checks": checks,
    }


def print_human(report: dict[str, object]) -> None:
    print(f"status: {report['status']}")
    print(f"checked_item_count: {report['checked_item_count']}")
    print(f"stale_item_count: {report['stale_item_count']}")
    for check in report["checks"]:
        if not check["exists"]:
            print(f"{check['asset_id']}: missing")
            continue
        verdict = "match" if check["matches"] else "stale"
        print(
            f"{check['asset_id']}: {verdict} "
            f"(bytes={check['actual_bytes']}, sha256={str(check['actual_sha256'])[:12]})"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_human(report)
    return 0 if report["status"] == "fresh" else 1


if __name__ == "__main__":
    raise SystemExit(main())
