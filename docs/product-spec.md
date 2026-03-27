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

## Primary Use Modes

### 1. Evaluate an existing memory system

The repo can benchmark whether an existing system improves continuity quality for a real interrupted workflow.

The question is not whether the target system has many memory features.
The question is whether it produces an artifact that reduces restart cost without hiding risk.

The default intake surface for this mode is:

- `docs/evaluate-a-memory-system.md`
- `docs/target-system-eval-packet.md`

### 2. Design a better continuity artifact

The repo can also serve as a design lab for continuity packs, freshness contracts, and proof packets before a broader memory runtime exists.

## Core Question

The core question for `memory-workbench` is not "can the system remember more?"

It is:

- can interrupted work resume correctly
- can a second operator take over safely
- can the latest state be audited without replaying the entire trace
- can stale memory be detected before action

## Capability Boundary

What this repo is meant to be good at:

- designing continuity artifacts for resume and handoff
- benchmarking restart clarity and replay cost
- validating whether a memory artifact is decision-relevant and evidence-linked
- exposing stale-state failure before execution

What this repo is not meant to be, at least in `v0`:

- a complete memory operating system
- a generic retrieval benchmark
- a production-grade knowledge base
- a hosted agent runtime or orchestration platform

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
- general long-term semantic memory evaluation
- personalization or profile memory

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
- stale_check
- last_verified_at

## Definition Of Done For One Case

A case is not done when a pack merely exists.

A case is done when:

- the interruption boundary is explicit
- `raw trace only` and `raw trace + continuity artifact` can be compared
- replay cost and clarity are scored
- factual regression is checked
- stale-state handling is tested if the workflow can drift
- the result is written into a reusable report

## Product Risks

- overbuilding schema before enough examples exist
- confusing "summary quality" with "continuity quality"
- drifting into a general memory repo with no clear proof surface

## Simple Boundary Test

If a new idea mainly answers one of these questions, it likely belongs here:

- "Will this reduce restart cost?"
- "Will this make handoff safer?"
- "Will this improve evidence traceability?"
- "Will this catch stale state before action?"

If it mainly answers one of these questions, it probably belongs in a different repo:

- "Will this improve generic retrieval quality?"
- "Will this improve long-term semantic memory coverage?"
- "Will this personalize responses better?"
- "Will this provide a full agent runtime?"

## First Validation Loop

1. Create one realistic interrupted workflow.
2. Capture its continuity pack.
3. Ask a fresh operator to continue from the pack.
4. Measure ambiguity, missing facts, and restart cost.
5. Verify stale-state handling before action if the source-of-truth can rotate.

## Exit Criteria for v0

The repo should graduate from concept to externally publish-ready when:

- there is at least one convincing before-vs-after continuity demo
- the benchmark has a stable scoring rubric
- the continuity pack schema has survived at least two examples
- the README can point to proof, not only thesis
