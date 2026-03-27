# Continuity Pack: stale-pack-rotation-001

## Pack Metadata

- case_id: `stale-pack-rotation-001`
- created_at: `2026-03-26`
- last_verified_at: `2026-03-26T18:20:00Z`
- source_workflow: `G2 public outreach execution`
- pack_intent: simulate a cached continuity pack that was verified before the canonical outreach packet rotated to a new recommended lane

## Problem

Decide whether a fresh operator should trust this cached pack after the canonical packet changed.

## Current State

- send_status: `not_sent`
- recommended_lane: `004 / SpecMem`
- preferred_delivery_path: `no_auth_fallback`
- commercial_primary_mode: `priced_pilot`
- current_next_action: wait for explicit external-send confirmation, then run `python3 /ROOM/tasks/ai-memory-saas/public-outreach-launcher.py --target 004 --preferred-open --priced`

## Last Verified Facts

- `/ROOM/artifacts/deliverables/public-outreach-next-step.md` previously exposed `recommended_primary_open_command = python3 /ROOM/tasks/ai-memory-saas/public-outreach-launcher.py --target 004 --preferred-open --priced`.
- `/ROOM/artifacts/deliverables/public-outreach-next-step.md` previously recommended `004 / SpecMem` for the next public lane.
- `/ROOM/tasks/ai-memory-saas/outreach-tracker.md` showed target `004` as `not_sent`.
- `/ROOM/MEMORY/today_brief.md` already listed `011 / memU`, `012 / OpenMemory`, and `016 / MemOS` as live ready-now lanes, but this pack cached `004 / SpecMem` as the active lane anyway.
- `/ROOM/MEMORY/active_goals.md` kept real external send behind explicit confirmation and blocked repeated auth lane reprobes.

## Decisions And Why

- decision: keep `004 / SpecMem` as the active lane
  why: this stale fixture represents a pack that was not refreshed after the recommendation rotated
- decision: treat `/ROOM/artifacts/deliverables/public-outreach-next-step.md` as the source that should overrule this pack if disagreement appears
  why: this case exists to prove that the operator must stop and refresh instead of trusting the cached summary

## Exact Next Actions

1. Open `/ROOM/artifacts/deliverables/public-outreach-next-step.md`.
2. Compare `recommended_lane`, `send_status`, and the preferred open command against this pack.
3. If the packet disagrees with this pack, mark this pack stale and stop using it as the execution source.
4. Refresh the continuity pack from the current packet before any send action.

## Open Risks

- this pack intentionally contains an outdated recommended lane and open command
- a fresh operator could act on the wrong lane if freshness checks are skipped
- explicit external-send confirmation may still be absent even after the stale check

## Evidence Index Summary

- canonical next-step packet: `/ROOM/artifacts/deliverables/public-outreach-next-step.md`
- tracker SSOT: `/ROOM/tasks/ai-memory-saas/outreach-tracker.md`
- active goal rationale: `/ROOM/MEMORY/active_goals.md`
- current operator briefing: `/ROOM/MEMORY/today_brief.md`

## Stale-Check Rule

- before acting, compare this pack against `/ROOM/artifacts/deliverables/public-outreach-next-step.md` and `/ROOM/tasks/ai-memory-saas/outreach-tracker.md`
- if `recommended_lane`, `send_status`, or the preferred open command differ, treat the source file as authoritative and mark this pack stale
- `last_verified_at` shows that this pack predates the current packet recommendation and must be revalidated before use

## Handoff Note

This fixture is intentionally wrong on the active lane so the stale-check procedure has something concrete to catch.

