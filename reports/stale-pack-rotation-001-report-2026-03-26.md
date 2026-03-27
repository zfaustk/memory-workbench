# Continuity Report

## Report Metadata

- case_id: `stale-pack-rotation-001`
- date: `2026-03-26`
- operator: `Clio manual same-session evaluator`
- condition: `Condition A vs Condition B`
- pack_last_verified_at: `2026-03-26T18:20:00Z`
- source_paths:
  - `Condition A`: `/ROOM/artifacts/deliverables/public-outreach-next-step.md`, `/ROOM/tasks/ai-memory-saas/outreach-tracker.md`, `/ROOM/MEMORY/today_brief.md`, `/ROOM/MEMORY/active_goals.md`
  - `Condition B`: `/ROOM/projects/memory-workbench/packs/stale-pack-rotation-001/continuity-pack-stale.md`, `/ROOM/projects/memory-workbench/scripts/validate_continuity_artifacts.py`

## Task Slice

- task: detect whether a cached continuity pack is stale after the canonical outreach packet rotated away from `004 / SpecMem` to `011 / memU`
- interruption_boundary: after a cached pack exists, before any fresh operator revalidates it against the current packet
- expected_next_action: stop using the stale pack, then refresh from `/ROOM/artifacts/deliverables/public-outreach-next-step.md` before any execution step

## Evaluation Conditions

### Condition A

- artifact set: raw operational packet + tracker + today brief + active goals
- replay_start_point: open `/ROOM/artifacts/deliverables/public-outreach-next-step.md` and determine which source should win if an older summary disagrees

### Condition B

- artifact set: stale continuity pack + validator + canonical packet/tracker
- replay_start_point: run the validator against `/ROOM/projects/memory-workbench/packs/stale-pack-rotation-001/continuity-pack-stale.md`

## Scored Dimensions

| Dimension | Raw Trace Only | With Continuity Pack | Delta | Notes |
|-----------|----------------|----------------------|-------|-------|
| Goal clarity | 3 | 5 | +2 | Raw sources reveal the live lane, but they do not frame the decision as a stale-pack check. The stale fixture plus validator turns the goal into a single freshness question. |
| State clarity | 3 | 5 | +2 | Raw sources show the current lane, but the operator must infer that a cached summary is outdated. The validator names the mismatch directly. |
| Next action clarity | 3 | 5 | +2 | Raw trace implies "use the packet," while the validator makes the safe action explicit: stop and refresh. |
| Evidence access | 3 | 4 | +1 | Raw sources are already short, but the validator points directly at the packet and tracker fields that disagree. |
| Ambiguity remaining | 2 | 5 | +3 | Without the freshness contract, the operator still has to decide how much to trust the cached pack. The validator reduces ambiguity to zero by marking the pack stale. |

## Outcome Metrics

- restart_clarity_score: `4.8/5 with stale-pack validator vs 2.8/5 raw average`
- second_operator_success_rate: `1/1 manual trial; Condition B reached the correct stop-and-refresh decision without relying on prose interpretation`
- evidence_traceability_score: `5/5 with validator vs 3/5 raw`
- replay_cost_minutes_raw: `3.0`
- replay_cost_minutes_pack: `1.0`
- replay_cost_reduction_percent: `66.7`

## Regression Check

- factual_regression_present: `no`
- regression_notes: `The stale pack intentionally pointed at 004 / SpecMem, but the validator caught both the rotated lane and the rotated open command before any action was taken.`
- stale_check_performed: `yes`
- stale_check_result: `pass - validator reported packet disagreement (`004 / SpecMem` != `011 NevaMind-AI / memU`) and command disagreement, so the operator stopped and treated the packet as authoritative`

## Key Observations

- what became easier: `The freshness contract turned "compare several files and reason about trust" into one explicit stale verdict with source-backed mismatches.`
- what was still ambiguous: `The validator checks lane, command, and tracker send status, but it still relies on the packet and tracker remaining parseable with the current markdown shapes.`
- which field in the continuity pack carried the most value: `last_verified_at` because it makes it legitimate to challenge the cached pack instead of treating it as timeless truth.`
- which missing field caused the most friction: `none in the stale fixture itself; the main remaining gap is missing a second independent operator rerun rather than another schema field.`

## Decision

- status: `pass`
- why: `The stale case now has real executable evidence: the validator catches lane rotation before action, replay cost drops, and no factual regression is introduced because the operator stops instead of sending.`
- next schema or workflow change: `Run this stale-pack case with an independent second operator or a scripted replay harness so the repeatability claim no longer depends on the same-session evaluator.`
