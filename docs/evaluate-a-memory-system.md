# Evaluate A Memory System

## What This Guide Is For

Use this guide when you already have a memory system and want to evaluate whether it improves `continuity`, not just storage or retrieval.

Typical target systems:

- a new `honest` implementation
- a memory layer inside an agent runtime
- a continuity or handoff artifact generator
- a workflow state summarizer that claims to support resume

This guide is not for measuring broad retrieval accuracy, personalization, or knowledge coverage.

## The Right Question

Do not start with:

- "Does the system remember a lot?"
- "Can it retrieve many notes?"

Start with:

- "Can interrupted work resume correctly?"
- "Can a second operator safely take over?"
- "Can stale state be detected before action?"
- "Can the latest state be audited without replaying the full trace?"

## Evaluation Flow

### 1. Choose one real workflow slice

Pick a task that can actually break on interruption.

Good candidates:

- research that pauses after evidence collection but before synthesis
- coding that pauses after implementation but before verification
- outreach that pauses after packet drafting but before send
- decision work that pauses after recommendation but before execution

Bad candidates:

- tiny one-shot tasks with no real handoff risk
- tasks where all state already fits in one short note
- generic retrieval demos with no next action

### 2. Define the interruption boundary

The interruption boundary must be concrete.

Examples:

- research complete, report not yet written
- code changed, tests not yet rerun
- packet drafted, send not yet executed
- lane chosen, but source-of-truth may still rotate

If the interruption point is vague, the continuity benchmark will be vague too.

### 3. Export a continuity artifact from the target system

Your memory system should produce one artifact that tries to carry the minimum state required for safe resume.

Minimum contract:

- `problem`
- `current_state`
- `last_verified_facts`
- `decisions_and_why`
- `next_actions`
- `open_risks`
- `evidence_index`
- `operator_notes`
- `last_verified_at`
- `stale_check`

Reference:

- [schemas/continuity-pack.example.yaml](../schemas/continuity-pack.example.yaml)

### 4. Run the A/B comparison

Measure two conditions:

1. `raw trace only`
2. `raw trace + continuity artifact`

Use the same workflow slice for both.
Do not let the evaluator improvise a new procedure between conditions.

Reference:

- [evals/continuity-benchmark.md](../evals/continuity-benchmark.md)
- [evals/operator-handoff-001-runbook.md](../evals/operator-handoff-001-runbook.md)

### 5. Score the continuity outcome

Track these metrics:

- `restart_clarity_score`
- `second_operator_success_rate`
- `evidence_traceability_score`
- `replay_cost_minutes`

What good looks like:

- replay cost drops materially
- the second operator guesses less
- evidence is easier to reach
- stale state is caught before action

### 6. Add a stale-state check

A continuity artifact that speeds up resume but fails when the world changes is not safe enough.

At minimum, test one case where:

1. the pack is created
2. the source-of-truth changes
3. the next operator must detect the pack is stale before acting

Reference:

- [cases/stale-pack-rotation-001.md](../cases/stale-pack-rotation-001.md)

## What This Repo Will Tell You

If you use this workbench correctly, it can tell you:

- whether your memory system reduces restart cost
- whether it helps second-operator handoff
- whether its artifact is decision-relevant
- whether stale-state handling is explicit enough
- whether your proof is strong enough to publish

## What This Repo Will Not Tell You

This workbench does not directly tell you:

- overall retrieval recall
- long-term semantic memory quality
- personalization strength
- broad knowledge coverage
- full runtime quality

Those need separate benchmarks.

## Recommended Output Packet

For each evaluated system, keep one packet with:

- workflow slice description
- interruption point
- exported continuity artifact
- A/B report
- stale-state verdict
- one sentence on which field helped the most
- one sentence on what still failed

## Pass / Partial / Fail Heuristic

- `pass`: replay cost drops by at least 50%, clarity improves across at least 3 rubric dimensions, and no factual regression is introduced
- `partial`: the artifact helps, but either clarity or cost improvement is weak, or stale handling is still fragile
- `fail`: the artifact does not reduce restart cost meaningfully, or it introduces wrong state / unsafe next actions

## Decision Rule

If your system passes continuity but fails retrieval, keep improving the retrieval benchmark elsewhere.
If your system passes retrieval but fails continuity, it is still not good enough for long-running agent work.

That is the whole point of this repo.
