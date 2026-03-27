# Upstream Issue Packet

## Current State

- status: `upstream_issue_packet_ready_local`
- generated_at: `2026-03-27T12:05:49.225024+00:00`
- target_label: `NevaMind-AI / memU`
- repo_slug: `NevaMind-AI/memU`
- repo_url: `https://github.com/NevaMind-AI/memU/issues/new/choose`
- issue_title: `Add auditable workflow trace and resumable state alongside proactive memory`
- purpose: Compress local workflow-continuity proof into a submit-ready packet for an upstream issue without crossing the publish boundary.

## Proof Rollup

| Signal | Value |
| --- | --- |
| Benchmark cases | `2` |
| Scripted reruns | `1` |
| Average replay-cost reduction | `64.6%` |
| Average restart clarity ratio | `0.94` |
| Stale verdict reproduced | `true` |

## Positioning

- target_fit: NevaMind-AI / memU already has a public story around proactive memory, continuous intent capture, and lower token cost, so the adjacent wedge is workflow continuity with auditable trace and resumable state.
- why_now: Current local proof shows workflow continuity can be measured with restart clarity, replay-cost reduction, and stale-state detection instead of generic memory claims.

## Suggested Issue Title

Add auditable workflow trace and resumable state alongside proactive memory

## Compact Issue Hook

Current local proof shows workflow continuity is measurable: operator handoff cut replay cost from 4.0 to 1.5 minutes, stale-pack detection cut stale-check cost from 3.0 to 1.0 minute, and the stale verdict now reproduces through a scripted validator-backed rerun.

## Ready-to-Paste Body Blocks

### Opening

NevaMind-AI / memU already has a strong public story around proactive memory, continuous intent capture, and lower token cost.

The adjacent gap in long-running agent workflows is not only whether memory persists, but whether another operator can inspect what changed, understand the latest decision path, and safely continue work without replaying the entire trace.

### Problem

When a workflow drifts or pauses, teams often lose the operational layer between "memory exists" and "work can safely continue":

1. the last action path is hard to inspect,
2. the next executable step is mixed with raw trace,
3. stale cached state is easy to reuse by mistake,
4. replay and debugging cost stays high even if recall quality is decent.

### Proposed Improvement

Add an optional workflow-continuity layer next to proactive memory:

1. keep an auditable action and decision trace for important workflow transitions,
2. preserve resumable workflow state, not only memory items,
3. expose a compact resume path for second-operator handoff,
4. make stale-state detection explicit before action.

### Local Proof

- operator handoff reduced replay cost from 4.0 to 1.5 minutes (62.5% reduction)
- stale-pack rotation reduced stale-check replay cost from 3.0 to 1.0 minute (66.7% reduction)
- the stale verdict reproduces through a scripted validator-backed rerun
- average replay-cost reduction across the current proof set is 64.6%

### Minimal Eval Slice

One lightweight way to test this without broad product churn:

1. pick one continuity-critical workflow,
2. define the current raw-trace-only resume path,
3. add a compact continuity artifact with action trace + resumable state + stale-check,
4. measure replay cost, restart clarity, and stale-detection quality before vs after.

## Proof Points

- `operator_handoff`: Replay cost 4.0 -> 1.5 minutes (62.5% reduction); restart clarity 4.6/5 with continuity pack vs 2.4/5 raw average.
  - source: `/ROOM/projects/memory-workbench/reports/operator-handoff-001-report-2026-03-26.md`
- `stale_pack_rotation`: Replay cost 3.0 -> 1.0 minutes (66.7% reduction); validator stops stale lane reuse before action.
  - source: `/ROOM/projects/memory-workbench/reports/stale-pack-rotation-001-report-2026-03-26.md`
- `scripted_rerun`: Scripted replay reproduced the stale verdict with 2 expected validator issues.
  - source: `/ROOM/projects/memory-workbench/scripts/validate_continuity_artifacts.py`

## Source Paths

- `citation_pack_markdown`: `docs/public-citation-pack.md`
- `citation_pack_json`: `reports/public-citation-pack-2026-03-27.json`
- `proof_surface_json`: `reports/proof-surface-2026-03-27.json`
- `operator_handoff_report`: `reports/operator-handoff-001-report-2026-03-26.md`
- `stale_pack_rotation_report`: `reports/stale-pack-rotation-001-report-2026-03-26.md`
- `validator`: `scripts/validate_continuity_artifacts.py`

## Publish Boundary

- publish_boundary: `waiting_confirmation`
- next_step_if_confirmed: Open https://github.com/NevaMind-AI/memU/issues/new/choose and compress the packet into one upstream issue for NevaMind-AI/memU.

