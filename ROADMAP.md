# Roadmap

## Phase 0: Repo Contract

- [x] define thesis
- [x] define continuity pack concept
- [x] define first synthetic example
- [x] define first benchmark rubric
- [x] fix the public repo identity around `continuity benchmark workbench`, not `general memory repo`
- [x] add a direct evaluator entrypoint for benchmarking an existing memory system

## Phase 1: Minimal Proof

- [x] add one before-vs-after restart experiment
- [x] add one second-operator handoff case
- [x] add one scored report template
- [x] connect the case and report template to the benchmark rubric
- [x] produce the first filled report: `reports/operator-handoff-001-report-2026-03-26.md`

## Phase 2: Repeatability

- add more cases with different interruption types
  - current next case: `cases/stale-pack-rotation-001.md`
- stabilize the continuity pack fields
- [x] add simple tooling to validate required fields
- [x] run one stale-pack rotation case with executable freshness evidence
- [x] add a scripted replay harness for `stale-pack-rotation-001`

## Phase 3: External Proof Surface

- publish repo with convincing artifacts
- link benchmark results from the homepage
- [x] add one generated proof-surface summary for remote sync and upstream citations
- [x] add one generated public citation pack for profile README, publish page, and upstream issue reuse
- [x] add one generated remote-sync manifest so the first push bundle is explicit before auth returns
- [x] add one generated independent rerun kit so a later second operator has a fixed proof replay entrypoint
- [x] add one single-command proof refresh bundle so later proof updates do not depend on remembering builder order
- contribute continuity ideas back to upstream memory or harness projects

## Phase 4: Stronger External Validity

- run one independent second-operator rerun
- add one case from a memory system outside this repo
- compare one existing memory system against the current continuity benchmark
- publish a public narrative that stays inside the continuity boundary

## Notable Decisions

- No runtime framework before continuity evidence exists.
- No generalized "memory" claims before benchmark evidence exists.
- No public launch before there is at least one proof packet worth showing.
