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
- [cases/operator-handoff-001.md](cases/operator-handoff-001.md): a concrete interruption and second-operator handoff case
- [evals/continuity-benchmark.md](evals/continuity-benchmark.md): the first benchmark definition
- [reports/continuity-report-template.md](reports/continuity-report-template.md): a scored report template for before-vs-after comparison
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
5. Add one before-vs-after case that shows what the pack changed operationally.

## Status

Remote repo exists, but local git history is not fully synced yet.

Current proof assets available locally:

- [examples/resume-demo.md](examples/resume-demo.md)
- [docs/proof-surface.md](docs/proof-surface.md)
- [docs/remote-sync-manifest.md](docs/remote-sync-manifest.md)
- [cases/operator-handoff-001.md](cases/operator-handoff-001.md)
- [cases/stale-pack-rotation-001.md](cases/stale-pack-rotation-001.md)
- [reports/continuity-report-template.md](reports/continuity-report-template.md)
- [reports/operator-handoff-001-report-2026-03-26.md](reports/operator-handoff-001-report-2026-03-26.md)
- [reports/stale-pack-rotation-001-report-2026-03-26.md](reports/stale-pack-rotation-001-report-2026-03-26.md)
- [reports/remote-sync-manifest-2026-03-27.json](reports/remote-sync-manifest-2026-03-27.json)
- [evals/operator-handoff-001-runbook.md](evals/operator-handoff-001-runbook.md)
- [packs/operator-handoff-001/continuity-pack.md](packs/operator-handoff-001/continuity-pack.md)
- [packs/operator-handoff-001/evidence-index.md](packs/operator-handoff-001/evidence-index.md)
- [packs/stale-pack-rotation-001/continuity-pack-stale.md](packs/stale-pack-rotation-001/continuity-pack-stale.md)
- [scripts/validate_continuity_artifacts.py](scripts/validate_continuity_artifacts.py)
- [scripts/rerun_stale_pack_rotation.py](scripts/rerun_stale_pack_rotation.py)
- [scripts/build_proof_surface.py](scripts/build_proof_surface.py)
- [scripts/build_remote_sync_manifest.py](scripts/build_remote_sync_manifest.py)
- [reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json](reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json)

Next proof step:

- regenerate `docs/proof-surface.md` whenever benchmark evidence changes, rebuild `docs/remote-sync-manifest.md`, then rerun `stale-pack-rotation-001` with an independent second operator so the stale-check proof no longer depends on one evaluator path

Current scripted rerun command:

- `python3 scripts/rerun_stale_pack_rotation.py --json`

Current proof-surface build command:

- `python3 scripts/build_proof_surface.py --json`

Current remote-sync manifest command:

- `python3 scripts/build_remote_sync_manifest.py --json`
