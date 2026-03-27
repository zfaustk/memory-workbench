# Proof Surface

## Current State

- status: `proof_ready_local`
- generated_at: `2026-03-27T15:05:30.913767+00:00`
- purpose: give one compact proof packet for `remote_synced + proof-ready + upstream-citable` work
- generated_from:
  - `/ROOM/projects/memory-workbench/reports/operator-handoff-001-report-2026-03-26.md`
  - `/ROOM/projects/memory-workbench/reports/stale-pack-rotation-001-report-2026-03-26.md`
  - `/ROOM/projects/memory-workbench/scripts/validate_continuity_artifacts.py`
  - `/ROOM/projects/memory-workbench/packs/stale-pack-rotation-001/continuity-pack-stale.md`

## Rollup

| Signal | Value |
| --- | --- |
| Benchmark cases | `2` |
| Scripted reruns | `1` |
| Average replay-cost reduction | `64.6%` |
| Average restart clarity | `0.94` |
| Stale verdict reproduced | `true` |

## Case Metrics

| Case | Status | Replay cost raw | Replay cost with continuity artifact | Reduction | Restart clarity | Traceability |
| --- | --- | --- | --- | --- | --- | --- |
| `operator-handoff-001` | `pass` | `4.0` min | `1.5` min | `62.5%` | `4.6/5 with continuity pack vs 2.4/5 raw average` | `4/5 with continuity pack vs 2/5 raw` |
| `stale-pack-rotation-001` | `pass` | `3.0` min | `1.0` min | `66.7%` | `4.8/5 with stale-pack validator vs 2.8/5 raw average` | `5/5 with validator vs 3/5 raw` |

## Why This Is Reusable

- `operator-handoff-001` shows a second operator can recover the live workflow state faster when the continuity pack compresses goal, state, next action, and evidence order.
- `stale-pack-rotation-001` shows continuity artifacts must include a freshness contract; otherwise an old pack can point at the wrong lane and command.
- `scripts/rerun_stale_pack_rotation.py` turns the stale fixture into a repeatable check instead of a one-off prose claim.

## Runnable Checks

- `python3 scripts/validate_continuity_artifacts.py --pack packs/operator-handoff-001/continuity-pack.md --report reports/operator-handoff-001-report-2026-03-26.md`
- `python3 scripts/rerun_stale_pack_rotation.py --json`
- `python3 scripts/build_proof_surface.py --json`

## Remaining Gap

- next_gap: `independent_second_operator_rerun`
- reason: the stale verdict is now repeatable through the validator and scripted replay harness, but not yet verified by a second operator outside the same execution path.

## Proof Hooks For Upstream Or Remote Sync

- operator handoff proof hook: replay cost `4.0 -> 1.5` minutes (`62.5%` reduction) with `restart_clarity_score = 4.6/5 with continuity pack vs 2.4/5 raw average`
- stale detection proof hook: replay cost `3.0 -> 1.0` minutes (`66.7%` reduction) with validator-backed stop-before-action freshness verdict
- scripted rerun proof hook: `stale_verdict_reproduced = true` with `validator_issue_count = 2`

