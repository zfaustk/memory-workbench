# Target System Eval Packet

## Current State

- status: `target_system_eval_packet_ready_local`
- generated_at: `2026-03-28T01:32:00.914217+00:00`
- purpose: Give a future operator one fixed intake packet for benchmarking an external memory system against the continuity benchmark without inventing the eval structure from scratch.

## Target System

- system_id: `new-honest`
- system_label: `new honest continuity candidate`
- system_type: `memory-system`

## Evaluation Question

Does this target memory system reduce restart cost, preserve decision-relevant state, and detect stale state before action on a real interrupted workflow slice?

## Workflow Contract

- workflow_slice: `replace-with-one-real-interrupted-workflow-slice`
- interruption_boundary: `replace-with-one-concrete-boundary-before-the-next-safe-action`
- expected_next_action: `replace-with-the-one-safe-next-action-the-fresh-operator-should-take`
- continuity_artifact_path: `replace-with-target-system-artifact-path`
- source_paths:
  - `replace-with-raw-trace-or-task-slice-path-001`
  - `replace-with-source-of-truth-path-002`

## Continuity Contract

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

## A/B Conditions

- `A` `raw trace only`: Use the bounded workflow slice and raw source paths without the target continuity artifact.
- `B` `raw trace + target continuity artifact`: Start from the target continuity artifact, then open linked evidence only when needed.

## Scoring Focus

- `restart_clarity_score`
- `second_operator_success_rate`
- `evidence_traceability_score`
- `replay_cost_minutes`
- `stale_state_detected_before_action`

## Required Outputs

- one filled continuity report under reports/
- one sentence on which field carried the most value
- one sentence on what remained unsafe or ambiguous
- one stale-state verdict if the source-of-truth can drift

## Pass / Partial / Fail

- `pass`: Replay cost drops by at least 50 percent, clarity improves across at least 3 rubric dimensions, and no factual regression is introduced.
- `partial`: The artifact helps, but the gain is weak or stale handling remains fragile.
- `fail`: The artifact does not materially reduce restart cost, or it introduces wrong state or unsafe next actions.

## Runnable Commands

- `python3 scripts/validate_continuity_artifacts.py --pack <pack-path> --report <report-path>`
- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/build_target_system_eval_packet.py --json`

## Next Step

- `Replace the placeholder workflow and artifact paths with one real interrupted task slice, then run the A/B comparison and record the result as a new continuity report.`

