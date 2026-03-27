# Remote Sync Manifest

## Current State

- status: `remote_sync_ready_local`
- purpose: list the exact proof assets that should be pushed first when remote git auth is restored
- generated_at: `2026-03-27T02:42:35.988978+00:00`
- repo_root: `/ROOM/projects/memory-workbench`

## Rollup

| Signal | Value |
| --- | --- |
| Asset count | `15` |
| Group count | `6` |
| Groups | `cases, docs, evals, examples, reports, scripts` |
| Total bytes | `66289` |

## Sync Bundle

| Group | Asset | Path | Bytes | SHA256 |
| --- | --- | --- | --- | --- |
| `docs` | `proof_surface` | `docs/proof-surface.md` | `2711` | `f1f1184485c9` |
| `docs` | `architecture` | `docs/architecture.md` | `1903` | `2d1f3876298f` |
| `docs` | `product_spec` | `docs/product-spec.md` | `2786` | `13369a27ba50` |
| `examples` | `resume_demo` | `examples/resume-demo.md` | `1840` | `f20356660968` |
| `evals` | `continuity_benchmark` | `evals/continuity-benchmark.md` | `5736` | `92411ad7586b` |
| `cases` | `operator_handoff_case` | `cases/operator-handoff-001.md` | `2161` | `5b5f45c18e20` |
| `cases` | `stale_pack_rotation_case` | `cases/stale-pack-rotation-001.md` | `2641` | `ecbf8547cc6d` |
| `reports` | `proof_surface_json` | `reports/proof-surface-2026-03-27.json` | `4246` | `0a1fc1097fbe` |
| `reports` | `operator_handoff_report` | `reports/operator-handoff-001-report-2026-03-26.md` | `4394` | `968bed9c961c` |
| `reports` | `stale_pack_rotation_report` | `reports/stale-pack-rotation-001-report-2026-03-26.md` | `4709` | `e9237cd40a25` |
| `reports` | `stale_pack_rotation_rerun` | `reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json` | `2152` | `5383dd420a47` |
| `scripts` | `proof_surface_builder` | `scripts/build_proof_surface.py` | `9749` | `e61ab4b88f2b` |
| `scripts` | `remote_sync_manifest_builder` | `scripts/build_remote_sync_manifest.py` | `6245` | `38dc65cb9eb5` |
| `scripts` | `stale_rerun_harness` | `scripts/rerun_stale_pack_rotation.py` | `5043` | `a6ba866a4716` |
| `scripts` | `continuity_validator` | `scripts/validate_continuity_artifacts.py` | `9973` | `b7652d85d746` |

## Push Order

1. docs + examples + evals + cases
2. reports
3. scripts

## Runnable Checks

- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/rerun_stale_pack_rotation.py --json`
- `python3 scripts/build_remote_sync_manifest.py --json`

## Remaining Gap

- next_step: `Push this asset set once gh auth and git push are available again.`
- blocking_gap: `remote git auth still unavailable in the current lane`

