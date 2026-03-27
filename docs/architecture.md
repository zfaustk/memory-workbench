# Architecture

## Design Goal

Keep the system small enough to inspect, but structured enough to compare continuity approaches.

The architecture is intentionally artifact-first.
It assumes that continuity should be inspectable before any storage backend, runtime, or UI decision becomes central.

## Repo Architecture

### 1. Workflow Slice

A workflow slice is a bounded task fragment used for experiment and evaluation.

It includes:

- the initial task statement
- relevant evidence
- an interruption point
- the continuity pack produced at interruption time
- the expected next action

### 2. Continuity Pack

The continuity pack is the smallest durable state bundle that should enable resume and audit.

It has two surfaces:

- human-facing markdown for fast review
- machine-readable structure for later tooling and evals

### 3. Evidence Layer

Evidence is not copied into every summary. It is indexed.

The design assumption is:

- raw traces remain the source of truth
- the continuity pack stores only the decision-relevant subset
- each important claim should point back to evidence

### 4. Eval Layer

The eval layer scores the continuity artifact, not the raw model output.

Early questions:

- can a fresh operator resume the task?
- can they explain why the current state exists?
- can they find supporting evidence quickly?
- can they detect stale state before action?

## Evaluation Loop

The default loop is:

1. choose one workflow slice
2. define one interruption boundary
3. produce one continuity artifact
4. compare `raw trace only` against `raw trace + continuity artifact`
5. score replay cost, clarity, traceability, and stale handling
6. revise the artifact contract, not just the prose summary

This keeps the repo anchored in operational evidence instead of feature vocabulary.

## Initial Artifact Topology

```text
README.md
docs/
  product-spec.md
  architecture.md
examples/
  resume-demo.md
cases/
  operator-handoff-001.md
evals/
  continuity-benchmark.md
reports/
  continuity-report-template.md
schemas/
  continuity-pack.example.yaml
```

## Default Flow

1. Start with a workflow slice.
2. Produce a continuity pack at an interruption boundary.
3. Hand the pack to a fresh operator.
4. Measure resume clarity, evidence access, and replay cost.
5. Revise schema or pack-writing rules based on failure.

## Deliberate Omissions

This repo does not yet decide:

- storage backend
- vector database
- runtime framework
- UI shape

Those choices come later, after the continuity artifact proves itself.

## Boundary Reminder

This repo does not try to answer whether a memory system is broadly intelligent, retrieval-complete, or personalized.
It only tries to answer whether the system can carry interrupted work forward safely and cheaply.
