# memory-workbench

`memory-workbench` is a repo for building and evaluating auditable memory and workflow continuity for long-running agents.

## Thesis

Most agent memory projects optimize retrieval or personalization. This repo starts from a different failure mode:

- the agent restarts and loses execution state
- a second operator cannot tell what happened
- traces exist, but they are not compact, replayable, or decision-relevant
- the workflow cannot be audited without rereading raw logs

The goal is to turn memory from "stored context" into a workbench for `resume`, `handoff`, `rollback`, and `audit`.

## What This Repo Will Build

- continuity packs that preserve the minimum state needed to resume work
- handoff artifacts that let a second operator continue without rereading everything
- evals for restart clarity, auditability, and replay cost
- small reproducible examples instead of vague memory claims

## Why This Matters

If long-running agents become normal, the bottleneck is not only generation quality. It is whether the work can survive interruption, supervision changes, and delayed review.

`memory-workbench` focuses on that operational layer.

## First Commit Scope

This first commit establishes the repo contract:

- [docs/product-spec.md](docs/product-spec.md): product definition and scope
- [docs/architecture.md](docs/architecture.md): system shape and design choices
- [examples/resume-demo.md](examples/resume-demo.md): a minimal continuity example
- [evals/continuity-benchmark.md](evals/continuity-benchmark.md): the first benchmark definition
- [ROADMAP.md](ROADMAP.md): staged build plan

## Initial Questions

- What is the smallest continuity artifact that still supports reliable resume?
- Which fields reduce restart cost the most?
- How should raw logs, operator summaries, and machine-readable state relate?
- What proof is strong enough to show continuity, not just storage?

## Principles

- proof before polish
- continuity before feature breadth
- auditable artifacts over hidden state
- small experiments over large architecture claims

## Near-Term Deliverables

1. Define a continuity pack schema.
2. Create one synthetic workflow with a restart and second-operator handoff.
3. Score the pack with a simple benchmark.
4. Turn the benchmark into a repeatable report format.

## Status

Local first commit only. No external publishing in this repo state yet.
