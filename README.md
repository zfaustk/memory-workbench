# memory-workbench

`memory-workbench` is a continuity benchmark workbench for long-running agents.

It does not ask "can the system remember more?" first.
It asks the narrower operational question that actually breaks work:

> Can interrupted work resume correctly, transfer safely, and stay auditable without replaying the full trace?

## At A Glance

| Signal | Current value |
| --- | --- |
| Focus | Continuity artifacts for `resume`, `handoff`, `stale-check`, and `audit` |
| Benchmark cases | `2` |
| Scripted reruns | `1` |
| Average replay-cost reduction | `64.6%` |
| Remote status | published to `origin/main` |
| Main remaining gap | `independent_second_operator_rerun` |

## Why This Repo Exists

Most agent-memory work emphasizes retrieval breadth, personalization, or token savings.
This repo starts from a different failure mode:

- the agent restarts and loses execution state
- a second operator cannot tell what happened
- the trace exists, but it is not compact, replayable, or decision-relevant
- stale state is easy to reuse by mistake
- audit still requires rereading raw logs

The goal is to turn memory from "stored context" into an artifact system that makes continuity measurable.

## What Success Looks Like

A fresh operator should be able to:

- understand the current goal and workflow state quickly
- distinguish verified facts from assumptions
- find the evidence behind the important decisions
- detect stale state before acting
- continue the next action without reopening the whole trace

If a new idea mainly improves retrieval breadth, long-term semantic coverage, or generic memory APIs, it probably belongs in another repo.
If it lowers restart cost, clarifies handoff, or catches stale state before action, it belongs here.

## Proof Surface

Current proof assets:

- [docs/proof-surface.md](docs/proof-surface.md)
- [docs/proof-refresh-bundle.md](docs/proof-refresh-bundle.md)
- [docs/public-citation-pack.md](docs/public-citation-pack.md)
- [docs/independent-rerun-kit.md](docs/independent-rerun-kit.md)
- [docs/remote-sync-manifest.md](docs/remote-sync-manifest.md)
- [docs/upstream-issue-packet-memu.md](docs/upstream-issue-packet-memu.md)
- [reports/operator-handoff-001-report-2026-03-26.md](reports/operator-handoff-001-report-2026-03-26.md)
- [reports/stale-pack-rotation-001-report-2026-03-26.md](reports/stale-pack-rotation-001-report-2026-03-26.md)
- [reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json](reports/stale-pack-rotation-001-scripted-rerun-2026-03-27.json)
- [reports/remote-sync-manifest-verify-2026-03-27.json](reports/remote-sync-manifest-verify-2026-03-27.json)

Current measured outcomes:

| Case | Result |
| --- | --- |
| `operator-handoff-001` | replay cost `4.0 -> 1.5` minutes, `62.5%` reduction |
| `stale-pack-rotation-001` | replay cost `3.0 -> 1.0` minute, `66.7%` reduction |
| Rollup | `64.6%` average replay-cost reduction across the current proof set |

## Use It In Two Ways

### 1. Benchmark an existing memory system

Use this repo when you already have a memory system and want to test whether it preserves workflow continuity.

1. Choose a real interrupted workflow slice.
2. Export a continuity artifact from that system.
3. Compare `raw trace only` versus `raw trace + continuity artifact`.
4. Score replay cost, restart clarity, evidence traceability, and stale detection.

Start here:

- [docs/evaluate-a-memory-system.md](docs/evaluate-a-memory-system.md)
- [docs/target-system-eval-packet.md](docs/target-system-eval-packet.md)

### 2. Design better continuity artifacts

Use the cases, schema, validator, and generated proof packets here to iterate on what an actually reusable continuity artifact needs to contain.

## Fast Start

If you only want the shortest path to the current proof:

1. Read [docs/proof-surface.md](docs/proof-surface.md).
2. Run `python3 scripts/run_independent_rerun_check.py --json`.
3. Inspect [docs/independent-rerun-kit.md](docs/independent-rerun-kit.md) for the next operator handoff path.

If you want the full benchmark contract first:

1. Read [evals/continuity-benchmark.md](evals/continuity-benchmark.md).
2. Read [evals/operator-handoff-001-runbook.md](evals/operator-handoff-001-runbook.md).
3. Validate the existing pack with `python3 scripts/validate_continuity_artifacts.py --pack packs/operator-handoff-001/continuity-pack.md --report reports/operator-handoff-001-report-2026-03-26.md`.

## Repo Map

| Path | Why it matters |
| --- | --- |
| [docs/product-spec.md](docs/product-spec.md) | Product definition, boundary, and exit criteria |
| [docs/architecture.md](docs/architecture.md) | Artifact model and evaluation loop |
| [docs/evaluate-a-memory-system.md](docs/evaluate-a-memory-system.md) | Practical entrypoint for benchmarking another memory system |
| [docs/target-system-eval-packet.md](docs/target-system-eval-packet.md) | Fixed intake packet for external-system evaluation |
| [evals/continuity-benchmark.md](evals/continuity-benchmark.md) | Scoring contract and benchmark dimensions |
| [evals/operator-handoff-001-runbook.md](evals/operator-handoff-001-runbook.md) | Runnable evaluator procedure |
| [cases/operator-handoff-001.md](cases/operator-handoff-001.md) | Handoff failure-mode case |
| [cases/stale-pack-rotation-001.md](cases/stale-pack-rotation-001.md) | Stale-state failure-mode case |
| [schemas/continuity-pack.example.yaml](schemas/continuity-pack.example.yaml) | Minimal continuity-pack schema |
| [scripts/](scripts) | Builders, validators, rerun harnesses, and packet generators |

## Runnable Commands

- `python3 scripts/run_independent_rerun_check.py --json`
- `python3 scripts/build_proof_surface.py --json`
- `python3 scripts/build_proof_refresh_bundle.py --json`
- `python3 scripts/build_remote_sync_manifest.py --json`
- `python3 scripts/verify_remote_sync_manifest.py --json`
- `python3 scripts/build_public_citation_pack.py --json`
- `python3 scripts/build_independent_rerun_kit.py --json`
- `python3 scripts/build_upstream_issue_packet.py --json`
- `python3 scripts/build_target_system_eval_packet.py --json`
- `python3 scripts/rerun_stale_pack_rotation.py --json`

## Principles

- proof before polish
- continuity before feature breadth
- auditable artifacts over hidden state
- stale-check before action
- small reproducible cases over broad claims

## Current Status

The repo is now published to `origin/main` and the generated proof packets describe a runnable local baseline instead of a blocked pre-publish state.

The largest remaining product gap is still `independent_second_operator_rerun`: the proof is reproducible locally, but still needs a genuinely separate operator or later-session rerun to strengthen the claim.
