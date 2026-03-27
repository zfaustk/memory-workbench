# Continuity Benchmark v0

## Purpose

Measure whether a continuity artifact actually reduces restart cost and ambiguity.

## Benchmark Object

A benchmark case contains:

- task slice
- interruption point
- continuity artifact
- expected resume action
- scoring rubric

## Core Metrics

### restart_clarity_score

Can a fresh operator explain:

- what the goal is
- what has already been done
- what remains
- what is verified versus assumed

### second_operator_success_rate

Can a fresh operator complete the expected next action correctly using only the continuity artifact plus linked evidence?

### evidence_traceability_score

Can the operator quickly find the evidence behind major decisions?

### replay_cost_minutes

How much time is needed before the operator is confident enough to act?

## Baseline Comparison

Compare two conditions:

1. raw trace only
2. raw trace plus continuity pack

The repo thesis only holds if condition 2 materially improves restart quality.

## Suggested Rubric

Score each case from 1 to 5:

- goal clarity
- state clarity
- next action clarity
- evidence access
- ambiguity remaining

## First Experimental Standard

For the repo to claim useful progress, the continuity pack should:

- reduce replay cost by at least 50 percent in the synthetic case
- raise clarity on at least 3 of 5 rubric dimensions
- produce no major factual regression

## Current Local Proof Assets

- case: [cases/operator-handoff-001.md](../cases/operator-handoff-001.md)
- next case: [cases/stale-pack-rotation-001.md](../cases/stale-pack-rotation-001.md)
- report template: [reports/continuity-report-template.md](../reports/continuity-report-template.md)
- eval runbook: [evals/operator-handoff-001-runbook.md](./operator-handoff-001-runbook.md)
- first filled report: [reports/operator-handoff-001-report-2026-03-26.md](../reports/operator-handoff-001-report-2026-03-26.md)
- stale-rotation report: [reports/stale-pack-rotation-001-report-2026-03-26.md](../reports/stale-pack-rotation-001-report-2026-03-26.md)
- scripted rerun evidence: [reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json](../reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json)
- stale fixture pack: [packs/stale-pack-rotation-001/continuity-pack-stale.md](../packs/stale-pack-rotation-001/continuity-pack-stale.md)
- validator: [scripts/validate_continuity_artifacts.py](../scripts/validate_continuity_artifacts.py)
- replay harness: [scripts/rerun_stale_pack_rotation.py](../scripts/rerun_stale_pack_rotation.py)

## First Runnable Procedure

Use [evals/operator-handoff-001-runbook.md](./operator-handoff-001-runbook.md) as the default procedure for the first manual benchmark run.

The runbook adds:

- a fixed artifact set for Condition A and Condition B
- the five operator questions that must be answered
- explicit timer start/stop points
- a concrete pass / partial / fail rule

Before a rerun, validate the current pack/report pair:

- `python3 scripts/validate_continuity_artifacts.py --pack packs/operator-handoff-001/continuity-pack.md --report reports/operator-handoff-001-report-2026-03-26.md`

Current result from the first manual run:

- `operator-handoff-001` reduced replay cost from `4.0` minutes to `1.5` minutes
- replay cost reduction: `62.5%`
- benchmark status: `pass`
- first schema correction after the run: continuity packs now need a pack-local `last_verified_at` and an explicit stale-check before action

Current result from the stale-pack rotation run:

- `stale-pack-rotation-001` reduced stale-detection replay cost from `3.0` minutes to `1.0` minute
- replay cost reduction: `66.7%`
- benchmark status: `pass`
- validator now checks the pack against the canonical packet recommendation, the canonical open command, and the tracker send status instead of only validating pack/report field presence

Current result from the scripted replay harness:

- `scripts/rerun_stale_pack_rotation.py` replays the same stale fixture against the live canonical packet and tracker
- the scripted rerun passes only when the validator still reports the expected stale lane mismatch and stale command mismatch
- current rerun evidence is stored at `reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json`

Next repeatability target:

- rerun [cases/stale-pack-rotation-001.md](../cases/stale-pack-rotation-001.md) with an independent second operator so the same stale verdict repeats outside both the same-session evaluator and the scripted replay harness

## Future Expansion

- multi-operator handoff
- delayed resume after several days
- stale pack after packet rotation
- partial evidence corruption
- conflicting summaries

