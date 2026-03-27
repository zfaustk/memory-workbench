# Continuity Benchmark v0

## Purpose

Measure whether a continuity artifact actually reduces restart cost and ambiguity.

This benchmark is intentionally narrower than a general memory benchmark.
It focuses on continuity quality, not broad recall quality.

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

## What This Benchmark Does Not Measure

This benchmark does not directly measure:

- generic retrieval recall
- long-term semantic coverage
- personalization quality
- memory API ergonomics
- full agent runtime quality

## Baseline Comparison

Compare two conditions:

1. raw trace only
2. raw trace plus continuity pack

The repo thesis only holds if condition 2 materially improves restart quality.

## Recommended Inputs

For a fair comparison, each case should include:

- one bounded workflow slice
- one explicit interruption point
- one continuity artifact
- one expected next action
- one report with before-vs-after scoring
- one stale-state check when the source-of-truth can drift

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
- detect stale-state mismatch before action when the source-of-truth changes

## Entry Point For Existing Systems

If you already have a memory system and want to evaluate it with this benchmark, start here:

- [docs/evaluate-a-memory-system.md](../docs/evaluate-a-memory-system.md)

## Current Local Proof Assets

- generated proof surface: [docs/proof-surface.md](../docs/proof-surface.md)
- generated remote-sync manifest: [docs/remote-sync-manifest.md](../docs/remote-sync-manifest.md)
- case: [cases/operator-handoff-001.md](../cases/operator-handoff-001.md)
- next case: [cases/stale-pack-rotation-001.md](../cases/stale-pack-rotation-001.md)
- report template: [reports/continuity-report-template.md](../reports/continuity-report-template.md)
- eval runbook: [evals/operator-handoff-001-runbook.md](./operator-handoff-001-runbook.md)
- first filled report: [reports/operator-handoff-001-report-2026-03-26.md](../reports/operator-handoff-001-report-2026-03-26.md)
- stale-rotation report: [reports/stale-pack-rotation-001-report-2026-03-26.md](../reports/stale-pack-rotation-001-report-2026-03-26.md)
- scripted rerun evidence: [reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json](../reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json)
- remote-sync manifest JSON: [reports/remote-sync-manifest-2026-03-27.json](../reports/remote-sync-manifest-2026-03-27.json)
- stale fixture pack: [packs/stale-pack-rotation-001/continuity-pack-stale.md](../packs/stale-pack-rotation-001/continuity-pack-stale.md)
- validator: [scripts/validate_continuity_artifacts.py](../scripts/validate_continuity_artifacts.py)
- replay harness: [scripts/rerun_stale_pack_rotation.py](../scripts/rerun_stale_pack_rotation.py)
- proof-surface builder: [scripts/build_proof_surface.py](../scripts/build_proof_surface.py)
- remote-sync manifest builder: [scripts/build_remote_sync_manifest.py](../scripts/build_remote_sync_manifest.py)

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

Current proof-surface rollup:

- `scripts/build_proof_surface.py` now compacts both continuity reports plus the scripted rerun JSON into one reusable summary
- current proof-surface outputs are `docs/proof-surface.md` and `reports/proof-surface-2026-03-27.json`

Current public citation-pack rollup:

- `scripts/build_public_citation_pack.py` now turns the proof surface plus remote-sync manifest into one compact packet for profile README copy, upstream issue snippets, and publish-page reuse
- current citation-pack outputs are `docs/public-citation-pack.md` and `reports/public-citation-pack-2026-03-27.json`

Current remote-sync packaging rollup:

- `scripts/build_remote_sync_manifest.py` now compacts the first remote push bundle into a readable checklist plus a machine-readable manifest
- current remote-sync outputs are `docs/remote-sync-manifest.md` and `reports/remote-sync-manifest-2026-03-27.json`

Current independent rerun-kit rollup:

- `scripts/build_independent_rerun_kit.py` now compacts the minimum second-operator replay entrypoint into one markdown guide plus one machine-readable kit summary
- current rerun-kit outputs are `docs/independent-rerun-kit.md` and `reports/independent-rerun-kit-2026-03-27.json`
- the generated kit fixes the replay order, runnable checks, expected outcomes, and remaining publish boundary for a future independent operator

Next repeatability target:

- rerun [cases/stale-pack-rotation-001.md](../cases/stale-pack-rotation-001.md) with an independent second operator so the same stale verdict repeats outside both the same-session evaluator and the scripted replay harness

## Future Expansion

- multi-operator handoff
- delayed resume after several days
- stale pack after packet rotation
- partial evidence corruption
- conflicting summaries
