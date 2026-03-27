# Operator Handoff 001 Eval Runbook

## Purpose

Turn `operator-handoff-001` from a thesis-only case into a repeatable evaluation that another operator can run without inventing the procedure.

This runbook does not claim measured results yet.
It defines exactly how to produce the first scored report.

## Scope

- case: [cases/operator-handoff-001.md](../cases/operator-handoff-001.md)
- schema: [schemas/continuity-pack.example.yaml](../schemas/continuity-pack.example.yaml)
- report template: [reports/continuity-report-template.md](../reports/continuity-report-template.md)
- benchmark contract: [evals/continuity-benchmark.md](./continuity-benchmark.md)

## Preconditions

- The evaluator is a fresh operator for this case.
- The evaluator may read only the artifact set listed for each condition.
- The evaluator must time the run with a simple stopwatch.
- The evaluator must record answers before opening any extra workspace files.

## Test Question

Can a fresh operator recover the correct send status, active lane, and next action for an interrupted outreach workflow faster and with less ambiguity when a continuity pack is present?

## Condition Setup

### Condition A: Raw Trace Only

Artifact set:

- raw case description
- underlying outreach packet files
- linked raw task materials

Evaluator rules:

- do not use any continuity pack summary
- do not read the report template before answering the task questions

### Condition B: Raw Trace Plus Continuity Pack

Artifact set:

- everything from Condition A
- [packs/operator-handoff-001/continuity-pack.md](../packs/operator-handoff-001/continuity-pack.md)
- [packs/operator-handoff-001/evidence-index.md](../packs/operator-handoff-001/evidence-index.md)

Evaluator rules:

- start from the continuity pack first
- only open linked evidence when the pack says it is needed

## Tasks To Complete

The evaluator must answer all five prompts for both conditions:

1. What is the current send status?
2. What is the currently recommended lane?
3. What evidence supports that lane choice?
4. What is the exact next action?
5. What remains uncertain or blocked?

## Measurement Procedure

### Step 1: Start Timer

Start timing when the evaluator opens the first artifact for the condition.

### Step 2: Record First Actionable Answer

Stop the first timer when the evaluator can state all of the following in one note:

- send status
- recommended lane
- next action

Record this as `replay_cost_minutes`.

### Step 2.5: Run Stale Check

Before acting on Condition B, compare the continuity pack against the current source packet and tracker.

Record:

- `pack_last_verified_at`
- whether `recommended_lane`, `send_status`, and the open command still match
- whether the pack should be marked stale

### Step 3: Score The Five Dimensions

Use a 1-5 scale for:

- goal clarity
- state clarity
- next action clarity
- evidence access
- ambiguity remaining

Scoring anchor:

- `1`: evaluator is mostly guessing
- `3`: evaluator can proceed, but needs extra search or inference
- `5`: evaluator can proceed confidently with minimal extra search

### Step 4: Regression Check

Before ending the condition, compare the evaluator's answer with the case contract.

Mark `factual_regression_present = yes` if any of these are wrong:

- send status
- active lane
- next action
- major blocker state

### Step 5: Fill The Report

Copy [reports/continuity-report-template.md](../reports/continuity-report-template.md) and populate:

- `condition`
- `pack_last_verified_at`
- `source_paths`
- all five scored dimensions
- replay cost for both conditions
- regression notes
- stale-check result
- the single field that carried the most value

## Pass / Partial / Fail Rule

- `pass`: continuity pack reduces replay cost by at least 50 percent, improves at least 3 scored dimensions, and introduces no factual regression
- `partial`: continuity pack helps, but one of the benchmark thresholds is missed
- `fail`: replay cost does not improve materially, or the pack introduces a factual regression

## Expected Output

The first real run should produce:

- one filled report under `reports/`
- one short note on which continuity-pack field mattered most
- one schema or process change if the evaluator still got stuck

## First Follow-Up

After the first filled report exists, update:

- [README.md](../README.md) status section with the proof artifact path
- [ROADMAP.md](../ROADMAP.md) by marking the first scored report as complete
- [evals/continuity-benchmark.md](./continuity-benchmark.md) with any rubric adjustment discovered in the run
