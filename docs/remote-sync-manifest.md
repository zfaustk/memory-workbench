# Remote Sync Manifest

## Current State

- status: `remote_sync_ready_local`
- purpose: list the exact published proof assets that define the current remote-sync baseline
- generated_at: `2026-03-28T01:32:39.000109+00:00`
- repo_root: `/ROOM/projects/memory-workbench`

## Rollup

| Signal | Value |
| --- | --- |
| Asset count | `21` |
| Group count | `6` |
| Groups | `cases, docs, evals, examples, reports, scripts` |
| Total bytes | `104906` |

## Sync Bundle

| Group | Asset | Path | Bytes | SHA256 |
| --- | --- | --- | --- | --- |
| `docs` | `proof_surface` | `docs/proof-surface.md` | `2762` | `14b2252c60cb` |
| `docs` | `architecture` | `docs/architecture.md` | `3091` | `7de6a0f6843e` |
| `docs` | `evaluate_memory_system` | `docs/evaluate-a-memory-system.md` | `5205` | `2533d9fa918b` |
| `docs` | `target_system_eval_packet` | `docs/target-system-eval-packet.md` | `2787` | `db75f9f26c3b` |
| `docs` | `product_spec` | `docs/product-spec.md` | `5387` | `0781eaf60716` |
| `examples` | `resume_demo` | `examples/resume-demo.md` | `1840` | `f20356660968` |
| `evals` | `continuity_benchmark` | `evals/continuity-benchmark.md` | `7481` | `2631bcdd146d` |
| `cases` | `operator_handoff_case` | `cases/operator-handoff-001.md` | `2161` | `5b5f45c18e20` |
| `cases` | `stale_pack_rotation_case` | `cases/stale-pack-rotation-001.md` | `2641` | `ecbf8547cc6d` |
| `reports` | `proof_surface_json` | `reports/proof-surface-2026-03-27.json` | `4404` | `0d97f5b0bcd4` |
| `reports` | `operator_handoff_report` | `reports/operator-handoff-001-report-2026-03-26.md` | `4394` | `968bed9c961c` |
| `reports` | `stale_pack_rotation_report` | `reports/stale-pack-rotation-001-report-2026-03-26.md` | `4709` | `e9237cd40a25` |
| `reports` | `stale_pack_rotation_rerun` | `reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json` | `2152` | `5383dd420a47` |
| `reports` | `target_system_eval_packet` | `reports/target-system-eval-packet-2026-03-27.json` | `3082` | `83195597b9d9` |
| `scripts` | `proof_surface_builder` | `scripts/build_proof_surface.py` | `9870` | `cef93fde7e78` |
| `scripts` | `proof_refresh_bundle_builder` | `scripts/build_proof_refresh_bundle.py` | `9488` | `0f9f9df47481` |
| `scripts` | `remote_sync_manifest_builder` | `scripts/build_remote_sync_manifest.py` | `6939` | `47e2ff024265` |
| `scripts` | `remote_sync_manifest_verifier` | `scripts/verify_remote_sync_manifest.py` | `3049` | `a81d7d3c0a6f` |
| `scripts` | `target_system_eval_packet_builder` | `scripts/build_target_system_eval_packet.py` | `8452` | `dd2752f4a3ec` |
| `scripts` | `stale_rerun_harness` | `scripts/rerun_stale_pack_rotation.py` | `5039` | `764d09ee7ee9` |
| `scripts` | `continuity_validator` | `scripts/validate_continuity_artifacts.py` | `9973` | `b7652d85d746` |

## Push Order

1. docs + examples + evals + cases
2. reports
3. scripts

## Runnable Checks

- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/rerun_stale_pack_rotation.py --json`
- `python3 scripts/build_remote_sync_manifest.py --json`
- `python3 scripts/verify_remote_sync_manifest.py --json`

## Remaining Gap

- next_step: `Use this manifest as the auditable published asset bundle and rerun it after any proof refresh.`
- blocking_gap: `no remote auth blocker; next gap is keeping regenerated assets in sync with origin/main`

