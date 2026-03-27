# Resume Demo

## Scenario

An agent is preparing a public outreach packet for a memory product.

The run is interrupted after source verification and draft preparation, but before sending.

## Before Interruption

- goal: prepare a credible outreach packet for a target maintainer
- verified facts:
  - the target project accepts public GitHub issues
  - the pitch is focused on workflow continuity and audit trail
  - no external send has happened yet
- current state:
  - draft copy exists
  - evidence links are collected
  - send path is known
- risk:
  - a future operator may resend stale copy or miss the latest proof

## Continuity Pack Example

See the machine-readable companion:
[schemas/continuity-pack.example.yaml](../schemas/continuity-pack.example.yaml)

Human-readable summary:

- problem: send a high-signal outreach message without losing source-backed context
- current_state: packet drafted, not sent
- last_verified_facts:
  - public issue path exists
  - buyer-language version is preferred
  - no reply state needs checking before send
- decisions_and_why:
  - use public issue path first because it has lower auth friction
  - keep audit-trail framing because it matches target thesis
- next_actions:
  - review final copy
  - confirm send boundary
  - submit through the verified public path
- open_risks:
  - proof language may be too broad
  - sender profile fields may still need confirmation

## What A Fresh Operator Should Be Able To Do

- explain the exact send status in under 2 minutes
- identify why the current channel was chosen
- continue with the next action without rereading the whole raw history

## What Would Count As Failure

- cannot tell whether the message was already sent
- cannot locate the evidence behind the current recommendation
- cannot distinguish verified facts from assumptions

