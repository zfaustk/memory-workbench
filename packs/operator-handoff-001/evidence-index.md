# Evidence Index: operator-handoff-001

## Decision-Critical Sources

| Claim | Source Path | What To Verify |
|------|-------------|----------------|
| Dynamic recommended lane is still unsent | `/ROOM/tasks/ai-memory-saas/outreach-tracker.md` | `P0` row and dynamic lane status remain `not_sent` |
| Current single-entry execution packet exists | `/ROOM/artifacts/deliverables/public-outreach-next-step.md` | `recommended_primary_review/open/recorder` commands are present |
| Recommended lane is `011 / memU` | `/ROOM/MEMORY/today_brief.md` | `今日注意力方向` still names `011 / memU` as the default main path |
| Backup ready-now lanes are `004 / 012 / 016` | `/ROOM/MEMORY/today_brief.md` | ready-now backup list still matches the pack |
| Sender-profile-blocked lanes are `013 / 014 / 015` | `/ROOM/MEMORY/today_brief.md` | blocked-lane list still matches the pack |
| External send still requires explicit confirmation | `/ROOM/MEMORY/active_goals.md` | G2 notes still keep real send behind confirmation |
| Auth lanes should not be re-probed now | `/ROOM/MEMORY/active_goals.md` | cooldown/freeze states still hold for Gmail, X, LinkedIn, and Vercel |

## Fast Open Order

1. `/ROOM/artifacts/deliverables/public-outreach-next-step.md`
2. `/ROOM/tasks/ai-memory-saas/outreach-tracker.md`
3. `/ROOM/MEMORY/today_brief.md`
4. `/ROOM/MEMORY/active_goals.md`

## Audit Rule

If any of the four files above disagrees with the pack, prefer the source file and mark the pack stale before acting.
