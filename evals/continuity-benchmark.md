# Continuity Benchmark v0

## Purpose

Measure whether a continuity artifact actually reduces restart cost and ambiguity.

## Benchmark Object

A benchmark case contains:

- task slice
- interruption point
- continuity artifact
- expected resume action
- scoring rubric

## Core Metrics

### restart_clarity_score

Can a fresh operator explain:

- what the goal is
- what has already been done
- what remains
- what is verified versus assumed

### second_operator_success_rate

Can a fresh operator complete the expected next action correctly using only the continuity artifact plus linked evidence?

### evidence_traceability_score

Can the operator quickly find the evidence behind major decisions?

### replay_cost_minutes

How much time is needed before the operator is confident enough to act?

## Baseline Comparison

Compare two conditions:

1. raw trace only
2. raw trace plus continuity pack

The repo thesis only holds if condition 2 materially improves restart quality.

## Suggested Rubric

Score each case from 1 to 5:

- goal clarity
- state clarity
- next action clarity
- evidence access
- ambiguity remaining

## First Experimental Standard

For the repo to claim useful progress, the continuity pack should:

- reduce replay cost by at least 50 percent in the synthetic case
- raise clarity on at least 3 of 5 rubric dimensions
- produce no major factual regression

## Future Expansion

- multi-operator handoff
- delayed resume after several days
- partial evidence corruption
- conflicting summaries
