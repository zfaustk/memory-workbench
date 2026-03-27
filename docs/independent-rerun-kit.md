# Independent Rerun Kit

## Current State

- status: `independent_rerun_kit_ready_local`
- generated_at: `2026-03-27T12:05:49.247786+00:00`
- purpose: Package the smallest verified artifact set and command sequence that a future second operator can use to rerun the current continuity proof without reconstructing the repo from scratch.

## Proof Rollup

| Signal | Value |
| --- | --- |
| Benchmark cases | `2` |
| Scripted reruns | `1` |
| Average replay-cost reduction | `64.6%` |
| Average restart clarity ratio | `0.94` |
| Stale verdict reproduced | `true` |
| Remote-sync assets | `20` |
| Public proof assets | `12` |

## Independent Operator Goal

A fresh operator should be able to restate the current continuity thesis, rerun the stale-pack fixture, and identify the next publish-ready artifact path without opening unrelated workspace files.

## Artifact Sequence

| Step | Artifact | Path | Why |
| --- | --- | --- | --- |
| `1` | `README and benchmark contract` | `README.md` | Anchor the repo thesis and the current proof boundary before opening case-specific files. |
| `2` | `benchmark rubric` | `evals/continuity-benchmark.md` | Review the scoring dimensions and pass criteria for continuity claims. |
| `3` | `operator handoff runbook` | `evals/operator-handoff-001-runbook.md` | Use the existing evaluator protocol instead of inventing a new procedure. |
| `4` | `operator handoff continuity pack` | `packs/operator-handoff-001/continuity-pack.md` | Start from the compact continuity artifact before drilling into raw case evidence. |
| `5` | `operator handoff report` | `reports/operator-handoff-001-report-2026-03-26.md` | Compare the expected replay-cost and restart-clarity deltas against the current rerun. |
| `6` | `stale-pack fixture and validator` | `packs/stale-pack-rotation-001/continuity-pack-stale.md` | Reproduce the stale-state failure mode before claiming continuity artifacts are safe to reuse. |

## Runnable Checks

- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/build_remote_sync_manifest.py --json`
- `python3 scripts/build_public_citation_pack.py --json`
- `python3 scripts/build_independent_rerun_kit.py --json`
- `python3 scripts/rerun_stale_pack_rotation.py --json`

## Expected Outcomes

- Confirm operator handoff proof still shows replay cost 4.0 -> 1.5 minutes (62.5% reduction).
- Confirm stale-pack proof still shows replay cost 3.0 -> 1.0 minutes (66.7% reduction).
- Confirm scripted stale rerun still reproduces the expected verdict with 2 validator issues.
- Confirm the next publish boundary remains confirmation-gated rather than auth- or copy-blocked.

## Remaining Gap

- blocking_gap: `The kit is ready locally, but a real independent rerun still needs a second operator or a later session to execute it and record a fresh report.`
- next_step: `Hand this kit to the next operator or later session, run the listed checks in order, and record a new rerun note or report delta.`

