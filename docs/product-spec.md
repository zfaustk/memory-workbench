# Product Spec

## One-Line Product Definition

`memory-workbench` is an experiment repo for making long-running agent work resumable, auditable, and transferable across restarts and operators.

## Problem

Current agent systems often fail in one of these ways:

1. A run is interrupted and the next session lacks the execution state needed to continue.
2. Another operator inherits the task but must reread raw logs or reconstruct intent manually.
3. The system can store notes, but cannot prove that the notes are sufficient for audit or replay.
4. Memory is discussed at a feature level, while the real operational question is restart cost.

## Target Users

- agent builders working on long-running tasks
- researchers comparing memory or harness strategies
- operators who need reliable handoff between sessions or collaborators

## Non-Users for the First Phase

- teams looking for a production knowledge base
- consumer chatbot personalization use cases
- broad RAG benchmarks with no workflow continuity angle

## Product Promise

If a workflow is captured in a `continuity pack`, a fresh operator should be able to:

- understand current goal and state quickly
- see what evidence supports the latest decisions
- resume the next action with low ambiguity
- audit what happened without reading the full raw trace

## Scope for v0

### In Scope

- continuity pack design
- synthetic workflow examples
- operator handoff examples
- continuity benchmark definition
- markdown and machine-readable artifact patterns

### Out of Scope

- production runtime
- hosted service
- model orchestration framework
- generic memory retrieval system

## Success Metrics

The first benchmark tracks these repo-level outcomes:

- `restart_clarity_score`
- `second_operator_success_rate`
- `evidence_traceability_score`
- `replay_cost_minutes`

## Core Artifact

The central object in this repo is the `continuity pack`.

Minimum fields:

- problem
- current_state
- last_verified_facts
- decisions_and_why
- next_actions
- open_risks
- evidence_index
- operator_notes

## Product Risks

- overbuilding schema before enough examples exist
- confusing "summary quality" with "continuity quality"
- drifting into a general memory repo with no clear proof surface

## First Validation Loop

1. Create one realistic interrupted workflow.
2. Capture its continuity pack.
3. Ask a fresh operator to continue from the pack.
4. Measure ambiguity, missing facts, and restart cost.

## Exit Criteria for v0

The repo should graduate from concept to externally publish-ready when:

- there is at least one convincing before-vs-after continuity demo
- the benchmark has a stable scoring rubric
- the continuity pack schema has survived at least two examples
- the README can point to proof, not only thesis
