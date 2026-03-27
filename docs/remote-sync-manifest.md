# Remote Sync Manifest

## Current State

- status: `remote_sync_ready_local`
- purpose: list the exact proof assets that should be pushed first when remote git auth is restored
- generated_at: `2026-03-27T12:05:49.183591+00:00`
- repo_root: `/ROOM/projects/memory-workbench`

## Rollup

| Signal | Value |
| --- | --- |
| Asset count | `20` |
| Group count | `6` |
| Groups | `cases, docs, evals, examples, reports, scripts` |
| Total bytes | `101647` |

## Sync Bundle

| Group | Asset | Path | Bytes | SHA256 |
| --- | --- | --- | --- | --- |
| `docs` | `proof_surface` | `docs/proof-surface.md` | `2762` | `7511773593cd` |
| `docs` | `architecture` | `docs/architecture.md` | `3091` | `7de6a0f6843e` |
| `docs` | `evaluate_memory_system` | `docs/evaluate-a-memory-system.md` | `5205` | `2533d9fa918b` |
| `docs` | `target_system_eval_packet` | `docs/target-system-eval-packet.md` | `2787` | `437b3a63049c` |
| `docs` | `product_spec` | `docs/product-spec.md` | `5387` | `0781eaf60716` |
| `examples` | `resume_demo` | `examples/resume-demo.md` | `1840` | `f20356660968` |
| `evals` | `continuity_benchmark` | `evals/continuity-benchmark.md` | `7481` | `2631bcdd146d` |
| `cases` | `operator_handoff_case` | `cases/operator-handoff-001.md` | `2161` | `5b5f45c18e20` |
| `cases` | `stale_pack_rotation_case` | `cases/stale-pack-rotation-001.md` | `2641` | `ecbf8547cc6d` |
| `reports` | `proof_surface_json` | `reports/proof-surface-2026-03-27.json` | `4404` | `f2e6ce202ef8` |
| `reports` | `operator_handoff_report` | `reports/operator-handoff-001-report-2026-03-26.md` | `4394` | `968bed9c961c` |
| `reports` | `stale_pack_rotation_report` | `reports/stale-pack-rotation-001-report-2026-03-26.md` | `4709` | `e9237cd40a25` |
| `reports` | `stale_pack_rotation_rerun` | `reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json` | `2152` | `5383dd420a47` |
| `reports` | `target_system_eval_packet` | `reports/target-system-eval-packet-2026-03-27.json` | `3082` | `a2238e0fa8ad` |
| `scripts` | `proof_surface_builder` | `scripts/build_proof_surface.py` | `9876` | `3c12f4f4c2c0` |
| `scripts` | `proof_refresh_bundle_builder` | `scripts/build_proof_refresh_bundle.py` | `9482` | `893dc2ff9ad5` |
| `scripts` | `remote_sync_manifest_builder` | `scripts/build_remote_sync_manifest.py` | `6721` | `be745df434a1` |
| `scripts` | `target_system_eval_packet_builder` | `scripts/build_target_system_eval_packet.py` | `8456` | `7b766f625c56` |
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

