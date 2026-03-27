# Proof Refresh Bundle

## Current State

- status: `proof_refresh_bundle_ready_local`
- generated_at: `2026-03-27T11:38:22.400746+00:00`
- purpose: Rebuild the current proof surface, remote-sync packet, public citation pack, upstream issue packet, and independent rerun kit in one local command so later operators do not need to remember the refresh order.

## Proof Rollup

| Signal | Value |
| --- | --- |
| Benchmark cases | `2` |
| Scripted reruns | `1` |
| Average replay-cost reduction | `64.6%` |
| Average restart clarity ratio | `0.94` |
| Remote-sync assets | `17` |
| Public proof assets | `10` |
| Independent rerun artifacts | `6` |
| Upstream target | `NevaMind-AI / memU` |
| Upstream publish boundary | `waiting_confirmation` |
| Stale verdict reproduced | `true` |

## Refresh Steps

| Step | Command | Markdown | JSON |
| --- | --- | --- | --- |
| `proof surface` | `python3 scripts/build_proof_surface.py` | `docs/proof-surface.md` | `reports/proof-surface-2026-03-27.json` |
| `remote sync manifest` | `python3 scripts/build_remote_sync_manifest.py` | `docs/remote-sync-manifest.md` | `reports/remote-sync-manifest-2026-03-27.json` |
| `public citation pack` | `python3 scripts/build_public_citation_pack.py` | `docs/public-citation-pack.md` | `reports/public-citation-pack-2026-03-27.json` |
| `upstream issue packet` | `python3 scripts/build_upstream_issue_packet.py --preset memu` | `docs/upstream-issue-packet-memu.md` | `reports/upstream-issue-packet-memu-2026-03-27.json` |
| `independent rerun kit` | `python3 scripts/build_independent_rerun_kit.py` | `docs/independent-rerun-kit.md` | `reports/independent-rerun-kit-2026-03-27.json` |

## Generated Assets

- `proof_surface` `markdown`: `docs/proof-surface.md`
- `proof_surface` `json`: `reports/proof-surface-2026-03-27.json`
- `remote_sync_manifest` `markdown`: `docs/remote-sync-manifest.md`
- `remote_sync_manifest` `json`: `reports/remote-sync-manifest-2026-03-27.json`
- `public_citation_pack` `markdown`: `docs/public-citation-pack.md`
- `public_citation_pack` `json`: `reports/public-citation-pack-2026-03-27.json`
- `upstream_issue_packet_memu` `markdown`: `docs/upstream-issue-packet-memu.md`
- `upstream_issue_packet_memu` `json`: `reports/upstream-issue-packet-memu-2026-03-27.json`
- `independent_rerun_kit` `markdown`: `docs/independent-rerun-kit.md`
- `independent_rerun_kit` `json`: `reports/independent-rerun-kit-2026-03-27.json`

## Single Refresh Command

- `python3 scripts/build_proof_refresh_bundle.py --json`

## Remaining Gap

- next_step: `Use the single refresh command after any benchmark or proof change, then hand the independent rerun kit to a later operator or push the refreshed bundle once auth returns.`

