# Architecture

## Design Goal

Keep the system small enough to inspect, but structured enough to compare continuity approaches.

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
