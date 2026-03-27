# Stale Pack Rotation Case 001

## Case Goal

Show whether a continuity pack remains safe when the source-of-truth packet rotates after the pack was already created.

The question is not only whether the pack speeds up resume.
The question is whether the next operator can detect that the pack is stale before acting on an outdated lane.

## Workflow Slice

- domain: agent product outreach
- task: resume an interrupted outreach workflow after the verifier may have changed the recommended lane or command
- interruption boundary: after a continuity pack exists, before a fresh operator performs the stale check
- handoff target: a fresh operator who must decide whether the existing pack is still executable

## Condition A: Raw Trace Only

Available material:

- current packet
- tracker
- today brief
- active goals

Observed failure modes:

- the operator may not know which file should win when pack and packet disagree
- packet rotation can be missed if the operator trusts a cached summary
- replay cost rises because freshness rules are scattered

## Condition B: Raw Trace Plus Freshness Contract

Available material:

- raw trace
- continuity pack
- evidence index
- validator

Expected gains:

- the operator checks freshness before action
- stale packs are detected explicitly instead of silently reused
- the winning source order is fixed
- the next safe action is "stop and refresh" instead of "guess and send"

## Repo-Local Artifacts For This Case

- [packs/operator-handoff-001/continuity-pack.md](../packs/operator-handoff-001/continuity-pack.md)
- [packs/operator-handoff-001/evidence-index.md](../packs/operator-handoff-001/evidence-index.md)
- [reports/operator-handoff-001-report-2026-03-26.md](../reports/operator-handoff-001-report-2026-03-26.md)
- [scripts/validate_continuity_artifacts.py](../scripts/validate_continuity_artifacts.py)

This case intentionally reuses the first pack so the next benchmark can test what happens when the same artifact ages past its last verification point.

## Evaluation Questions

1. Can a fresh operator identify the authoritative source order in under 2 minutes?
2. Can the operator tell whether the pack is stale before executing a send command?
3. Can the validator confirm the pack/report contract before the operator reads the prose?
4. If the packet changed, does the operator stop and refresh rather than acting on the stale pack?

## Success Threshold

This case counts as useful only if the freshness contract:

- makes stale detection explicit before any action
- reduces ambiguity about which source is authoritative
- avoids factual regression when the packet rotates

