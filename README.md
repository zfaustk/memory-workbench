# memory-workbench

`memory-workbench` is a continuity benchmark workbench for long-running agents.

It does not try to answer "can the system remember more?" first.
It tries to answer a narrower and more operational question:

`Can interrupted work resume correctly, transfer safely, and stay auditable without replaying the full trace?`

## Thesis

Most agent memory work emphasizes retrieval, personalization, or token savings.
This repo starts from a different failure mode:

- the agent restarts and loses execution state
- a second operator cannot tell what happened
- traces exist, but they are not compact, replayable, or decision-relevant
- stale state is easy to reuse by mistake
- audit requires rereading raw logs

The goal is to turn memory from "stored context" into an artifact system for `resume`, `handoff`, `stale-check`, and `audit`.

## Core Question

`memory-workbench` exists to measure whether a memory artifact lowers restart cost while preserving correctness.

The repo is successful when a fresh operator can:

- understand the current goal and state quickly
- identify what is verified versus assumed
- find the evidence behind important decisions
- detect stale state before acting
- continue the next action without reopening the whole trace

## Capability Boundary

This repo is meant to be good at:

- continuity-pack design
- restart and handoff evaluation
- stale-state detection before action
- evidence-linked workflow artifacts
- compact proof packets for public comparison

This repo is not meant to be, at least in `v0`:

- a full memory operating system
- a generic retrieval benchmark
- a broad personalization framework
- a hosted runtime or orchestration platform

If a new idea mainly improves retrieval breadth, long-term semantic coverage, or generic memory APIs, it probably belongs in another repo.
If it mainly reduces restart cost, clarifies handoff, or catches stale state before action, it belongs here.

## Primary Use Modes

### 1. Benchmark an existing memory system

If you already have a memory system such as a new `honest` implementation, use this repo to test its continuity quality:

1. choose a real interrupted workflow slice
2. export a continuity artifact from that system
3. compare `raw trace only` vs `raw trace + continuity artifact`
4. score replay cost, restart clarity, evidence traceability, and stale detection

Entry point: [docs/evaluate-a-memory-system.md](docs/evaluate-a-memory-system.md)

If you want a fixed intake packet before filling real paths, start from:

- [docs/target-system-eval-packet.md](docs/target-system-eval-packet.md)

### 2. Design better continuity artifacts

If you do not have a stable artifact yet, use the cases, schema, validator, and reports here to design one and iterate on what fields actually matter.

## Repo Map

- [docs/product-spec.md](docs/product-spec.md): product definition, promise, boundary, and exit criteria
- [docs/architecture.md](docs/architecture.md): artifact model and evaluation loop
- [docs/evaluate-a-memory-system.md](docs/evaluate-a-memory-system.md): practical entrypoint for evaluating an existing memory system
- [docs/target-system-eval-packet.md](docs/target-system-eval-packet.md): generated intake packet for benchmarking an external memory system
- [evals/continuity-benchmark.md](evals/continuity-benchmark.md): benchmark contract and scoring dimensions
- [evals/operator-handoff-001-runbook.md](evals/operator-handoff-001-runbook.md): first runnable manual eval procedure
- [cases/operator-handoff-001.md](cases/operator-handoff-001.md): first handoff case
- [cases/stale-pack-rotation-001.md](cases/stale-pack-rotation-001.md): freshness and stale-state case
- [schemas/continuity-pack.example.yaml](schemas/continuity-pack.example.yaml): minimal continuity-pack contract
- [docs/proof-surface.md](docs/proof-surface.md): current proof rollup

## Principles

- proof before polish
- continuity before feature breadth
- auditable artifacts over hidden state
- stale-check before action
- small reproducible cases over broad claims

## Current Proof Surface

Current local proof assets:

- [docs/proof-surface.md](docs/proof-surface.md)
- [docs/proof-refresh-bundle.md](docs/proof-refresh-bundle.md)
- [docs/public-citation-pack.md](docs/public-citation-pack.md)
- [docs/independent-rerun-kit.md](docs/independent-rerun-kit.md)
- [docs/upstream-issue-packet-memu.md](docs/upstream-issue-packet-memu.md)
- [docs/remote-sync-manifest.md](docs/remote-sync-manifest.md)
- [reports/remote-sync-manifest-verify-2026-03-27.json](reports/remote-sync-manifest-verify-2026-03-27.json)
- [reports/operator-handoff-001-report-2026-03-26.md](reports/operator-handoff-001-report-2026-03-26.md)
- [reports/stale-pack-rotation-001-report-2026-03-26.md](reports/stale-pack-rotation-001-report-2026-03-26.md)
- [reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json](reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json)

Current local results:

- `operator-handoff-001`: replay cost `4.0 -> 1.5` minutes, `62.5%` reduction
- `stale-pack-rotation-001`: replay cost `3.0 -> 1.0` minute, `66.7%` reduction
- proof-surface rollup: `64.6%` average replay-cost reduction across the current proof set

## Runnable Commands

- `python3 scripts/validate_continuity_artifacts.py --pack packs/operator-handoff-001/continuity-pack.md --report reports/operator-handoff-001-report-2026-03-26.md`
- `python3 scripts/rerun_stale_pack_rotation.py --json`
- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/build_proof_refresh_bundle.py --json`
- `python3 scripts/build_remote_sync_manifest.py --json`
- `python3 scripts/verify_remote_sync_manifest.py --json`
- `python3 scripts/build_public_citation_pack.py --json`
- `python3 scripts/build_independent_rerun_kit.py --json`
- `python3 scripts/build_upstream_issue_packet.py --json`
- `python3 scripts/build_target_system_eval_packet.py --json`

## Current Status

Remote repo exists, but local git history is not fully synced yet.

The repo is already `proof_ready_local`, not yet fully publish-complete.
The largest remaining gap is still `independent_second_operator_rerun`.
