# Operator Handoff Case 001

## Case Goal

Show a before-vs-after continuity comparison for an interrupted outreach workflow.

The question is not whether notes exist.
The question is whether a fresh operator can continue without rereading the full trace.

## Workflow Slice

- domain: agent product outreach
- task: prepare and send a source-backed outreach packet for a memory or harness maintainer
- interruption boundary: after research and packet drafting, before final send
- handoff target: a fresh operator with no access to the prior chat context except linked evidence

## Condition A: Raw Trace Only

Available material:

- long chat log
- scattered task files
- draft packet in progress

Observed failure modes:

- the next operator cannot quickly tell whether the packet was already sent
- verified facts and copied assumptions are mixed together
- the recommended send lane is hard to recover
- replay cost is dominated by rereading narrative logs

## Condition B: Raw Trace Plus Continuity Pack

Available material:

- raw trace
- one continuity pack
- one evidence index

Expected gains:

- send status is explicit
- latest verified facts are separated from open risks
- next action is singular and operational
- evidence for the recommended lane is linked directly

## Pack Skeleton For This Case

Repo-local first draft artifacts now exist:

- [packs/operator-handoff-001/continuity-pack.md](../packs/operator-handoff-001/continuity-pack.md)
- [packs/operator-handoff-001/evidence-index.md](../packs/operator-handoff-001/evidence-index.md)

They intentionally bind the case to one real workflow slice instead of a generic pack outline.

## Evaluation Questions

1. Can a fresh operator explain the send status in under 2 minutes?
2. Can they identify the active lane without searching the full workspace?
3. Can they distinguish verified facts from assumptions?
4. Can they act without re-opening unrelated logs?

## Success Threshold

This case counts as useful only if the continuity pack:

- reduces replay cost by at least 50 percent
- improves at least 3 rubric dimensions
- introduces no factual regression about send status or evidence
