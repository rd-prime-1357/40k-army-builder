# SESSION HANDOFF 192

**Turn type:** data + coupled tooling/assertion (same shape as the B87/S190 exception — the data
fix and the assertion that prevents its recurrence shipped together, not shimmed apart). B95
closed. B94 decided by Ryan, engine turn queued for S193. No engine change — `index.html`
untouched, still v6.15.

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`, 32/32. S191's ten changed/net-new
   files hash-verified against the handoff table — all matched exactly. Repo confirmed current, no
   mid-push false alarm this session.
2. **Found `40K_Decision_Log.md` missing from the `/mnt/project` mount** (not stale — genuinely
   absent; 90 files in the mount vs. the guarded set). Not treated as evidence of anything —
   cloned the public repo, confirmed the file present there with a matching hash, read D284 from
   the clone. Worth Ryan checking whether it dropped out of the project area for real, since it's a
   file the next-session prompt depends on being readable at open.
3. **B94 answered by Ryan:** add the real 4th copy-tier to the points schema. Matches the D283
   recommendation. Queued as S193's engine-only turn (schema + `resolveUnits`/points lookup in
   `index.html` + the `resolved_pool`/points mirror in `rules_assertions.py`); data and assertion
   turns follow, sequenced with B89's adoption arc.
4. **B95 investigated, and the real question was bigger than the flag.** Checked source before
   answering: Chaos Space Marines (58/58 units with loadouts, 17 detachments, CSM-1/2/3 passing) and
   Thousand Sons (34/34 units with loadouts, 9 detachments, TS-1/2/3 passing) are both fully built —
   the `built: false` flag was stale for both. Also found that `Thousand_Sons_web.txt` now exists in
   the project area (37 KB), resolving `THOUSAND_SONS_BUILD_SCOPE.md` §5's old loadout-defaults
   blocker — a prior handoff's framing had carried the faction as "mid-build," which was itself
   stale; **the Thousand Sons build is complete.**
5. **Before flipping the flag, read `index.html`'s consumers of it.** `resolveUnits()` (~2291) falls
   back to `unitsByArmy['Adeptus Astartes']` when a non-subfaction faction's `data_army` is missing;
   `resolveDetachments()` (~2881) has no fallback at all. Neither CSM's nor Thousand Sons' taxonomy
   entry carried a `data_army` key. Flipping `built` to `true` alone would have made both factions
   selectable while silently serving the wrong unit pool and zero detachments — a live D0 violation
   introduced by the fix itself. Both gaps closed together: `built: true` and
   `data_army: "Chaos Space Marines"` / `"Thousand Sons"` added, verified against the exact keys
   `units.json`/`detachments.json` already use.
6. **New assertion B95-1** (`rules_assertions.py`), mirroring B90-1's shape: every `built: true`,
   non-subfaction faction must carry a `data_army` naming a real `units.json` army block. Prevents
   this exact silent-fallback class from recurring on a future faction flip. 117/117 assertions
   (was 116).
7. **Manifest regenerated twice** — once after the `faction_taxonomy.json` edit, once after the
   `rules_assertions.py` edit — each time re-verified green before proceeding.

## State
- Baseline: green at close (pending this handoff's own hash, verified last via
  `pipeline_manifest.py --freshness-check`).
- `index.html` unchanged, still **v6.15**.
- `rules_assertions.py`: 117/117 (B95-1 added). No engine change.
- `faction_taxonomy.json`: Chaos Space Marines and Thousand Sons now `built: true` with correct
  `data_army`. Both factions should now appear selectable in the UI and resolve their real rosters —
  **not yet eyeballed in a running browser this session; worth a quick look before relying on it.**
- Live behaviour: CSM and Thousand Sons go from "coming soon" (disabled) to selectable with their
  real 58- and 34-unit rosters and 17/9 detachments respectively.
- `repo_check` will show drift until pushed: `faction_taxonomy.json`, `rules_assertions.py`,
  `pipeline_manifest.json`, `OPEN_ITEMS_BACKLOG.md`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `SESSION_HANDOFF_192.md` (net-new).

## Ryan action required
1. Push this session's changes.
2. Confirm `40K_Decision_Log.md`'s absence from the `/mnt/project` mount — screenshot of the file
   list if it looks like it should be there.
3. Optional but recommended: load the app and spot-check that Chaos Space Marines and Thousand Sons
   now appear as selectable factions with their real rosters, before the next session builds on top
   of this.

## Decisions still waiting on Ryan
None outstanding — B94 and B95 both resolved this session.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `faction_taxonomy.json` | 96a72946aa63 | CSM/Thousand Sons `built: true` + `data_army` added |
| `rules_assertions.py` | bc9cfab09a4c | B95-1 added; 117/117 |
| `pipeline_manifest.py` | c943edd628e0 | `SESSION_HANDOFF_192.md` registered in GUARDED |
| `pipeline_manifest.json` | regenerated after this edit | regenerated, `--write`, 151 guarded files |
| `OPEN_ITEMS_BACKLOG.md` | 91573bbbb3c3 | B95 closed; B94 decision recorded; 16 open |
| `40K_Decision_Log.md` | c3a96c54b1ae | D285 appended |
| `DECISION_INDEX.md` | c146f86a045a | D285 index entry |
| `NEXT_SESSION_PROMPT.md` | (see next file) | S193 (unguarded by design) |
| `SESSION_HANDOFF_192.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
16 open, down from 17 at S191. Beginning: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B89,
B90, E28, B93, B94, B95. Resolved: B95 (closed, D285). Added: none. Ending: B69, B70, B75, B85, B86,
P2, P4, E23, B67b, E12, B17, B89, B90, E28, B93, B94.
