# Public Citation Pack

## Current State

- status: `citation_pack_ready_local`
- generated_at: `2026-03-27T12:05:49.202257+00:00`
- purpose: Give one compact proof packet that can be pasted into a profile README, upstream issue, or publish page.

## Rollup

| Signal | Value |
| --- | --- |
| Benchmark cases | `2` |
| Scripted reruns | `1` |
| Average replay-cost reduction | `64.6%` |
| Average restart clarity ratio | `0.94` |
| Stale verdict reproduced | `true` |
| Remote-sync-ready assets | `20` |

## Headline Hooks

- Built two continuity benchmark cases plus one scripted stale-state rerun for long-running agent workflows.
- Average replay cost dropped 64.6% across the current proof set.
- The repo now includes a generated target-system eval packet so external memory systems can be benchmarked with a fixed intake contract.
- Current proof bundle is already packaged for first remote sync once git auth returns.

## Proof Points

- `operator_handoff`: Replay cost 4.0 -> 1.5 minutes (62.5% reduction); restart clarity 4.6/5 with continuity pack vs 2.4/5 raw average.
  - source: `/ROOM/projects/memory-workbench/reports/operator-handoff-001-report-2026-03-26.md`
- `stale_pack_rotation`: Replay cost 3.0 -> 1.0 minutes (66.7% reduction); validator stops stale lane reuse before action.
  - source: `/ROOM/projects/memory-workbench/reports/stale-pack-rotation-001-report-2026-03-26.md`
- `scripted_rerun`: Scripted replay reproduced the stale verdict with 2 expected validator issues.
  - source: `/ROOM/projects/memory-workbench/scripts/validate_continuity_artifacts.py`

## Copy Blocks

### Profile README

Built a memory-workbench for long-running agents: 2 continuity benchmark cases + 1 scripted stale-state rerun, with 64.6% average replay-cost reduction and a first remote-sync proof bundle ready for publish.

### Upstream Issue

Current local proof shows workflow continuity is measurable: operator handoff cut replay cost from 4.0 to 1.5 minutes, stale-pack detection cut stale-check cost from 3.0 to 1.0 minute, and the stale verdict now reproduces through a scripted validator-backed rerun.

### Publish Page

memory-workbench packages auditable workflow continuity for agents: compact proof surface, stale-state replay checks, a generated external-eval intake packet, and a remote-sync-ready artifact bundle for public release.

## Public Asset Shortlist

| Group | Asset | Path | SHA256 |
| --- | --- | --- | --- |
| `docs` | `proof_surface` | `docs/proof-surface.md` | `7511773593cd` |
| `docs` | `architecture` | `docs/architecture.md` | `7de6a0f6843e` |
| `docs` | `evaluate_memory_system` | `docs/evaluate-a-memory-system.md` | `2533d9fa918b` |
| `docs` | `target_system_eval_packet` | `docs/target-system-eval-packet.md` | `437b3a63049c` |
| `docs` | `product_spec` | `docs/product-spec.md` | `0781eaf60716` |
| `examples` | `resume_demo` | `examples/resume-demo.md` | `f20356660968` |
| `evals` | `continuity_benchmark` | `evals/continuity-benchmark.md` | `2631bcdd146d` |
| `reports` | `proof_surface_json` | `reports/proof-surface-2026-03-27.json` | `f2e6ce202ef8` |
| `reports` | `operator_handoff_report` | `reports/operator-handoff-001-report-2026-03-26.md` | `968bed9c961c` |
| `reports` | `stale_pack_rotation_report` | `reports/stale-pack-rotation-001-report-2026-03-26.md` | `e9237cd40a25` |
| `reports` | `stale_pack_rotation_rerun` | `reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json` | `5383dd420a47` |
| `reports` | `target_system_eval_packet` | `reports/target-system-eval-packet-2026-03-27.json` | `a2238e0fa8ad` |

## Runnable Commands

- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/build_remote_sync_manifest.py --json`
- `python3 scripts/build_public_citation_pack.py --json`

## Remaining Gap

- next_gap: `independent_second_operator_rerun_or_remote_sync`

