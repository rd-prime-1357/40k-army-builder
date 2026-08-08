# SESSION HANDOFF 221

**Turn type:** data-only (B112 — Chaos Daemons LORDS OF THE WARP detachment disposition, verified
and shipped against `MFM_Chaos Daemons_v1.1.txt`). `detachment_parser.py` and `detachments.json`
shipped end to end. **Closes B112.** Chaos Daemons remains fully built (units) with detachments now
current to v1.1.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: public repo fetched and
   verified (101 overlay-needed files verified, 80 already local); private source repo fetched and
   verified fresh (85/85 files byte-match `source_manifest.json`). Full baseline: 34/34 gates clean,
   no surprises this time — `OUTPUT_FORMAT_SPEC_for_project_instructions.md` remains reconciled from
   S220 (still needs Ryan's push, see below).

2. **B112 forecast verified directly from source, not trusted.** `MFM_Chaos Daemons_v1.1.txt`'s
   LORDS OF THE WARP entry carries its own `FORCE DISPOSITION(S) CHANGED` banner, confirming Purge
   the Foe → Take and Hold exactly as forecast. Compared full DETACHMENTS blocks of both
   `MFM_Chaos_Daemons_v1_0.txt` and the v1.1 file by direct text read: same 9 detachments, same
   names, same DP costs (1–3), zero `UNIQUE:` tags in either file (confirmed by direct search of
   both).

3. **`detachment_parser.py` re-pointed, not re-registered.** `ARMY_TO_MFM["Chaos Daemons"]` and
   `MFM_SOURCE_NAME["MFM_Chaos Daemons_v1.1.txt"]` updated from `MFM_Chaos_Daemons_v1_0.txt`.
   `ARMY_TO_WAHA_FACTION` unchanged (Chaos Daemons was already fully registered in all three maps
   from its original units build). Confirmed no other hardcoded reference to the old filename
   remained in the parser.

4. **`detachments.json` regenerated and diff-guarded field-by-field**, not just re-run-clean: of
   202 total detachments in the file, exactly two carried real diffs, both Chaos Daemons — LORDS OF
   THE WARP's disposition, and three Scintillating Legion enhancement re-prices (Inescapable Eye
   10→15, Infernal Puppeteer 25→20, Neverblade 20→25), each matching the v1.1 text's own `▲`/`▼`
   price-change markers (final listed value only, per the standing points-note convention).
   Everything else in the 202-detachment file — all other factions, and Chaos Daemons' other 8
   detachments — byte-identical to the pre-change file.

5. **All detachment-dependent gates re-run clean** against the regenerated file:
   `detachments_repro_check`, `e1b_check`, `e1c_check`, `e4b_check`, `e4c_check`, `e21b_check`,
   `e21c_check`, `e25_check`.

6. **`detachment_effects.json` checked directly, not assumed** — same discipline as D313/D314. The
   one existing Chaos Daemons row (`Chaos Daemons|SHADOW LEGION`, D204 ruling 3) is unrelated to
   this session's change but was found to carry a stale `enforced: false` reason: it names Chaos
   Space Marines as "not built yet," which has been false since S212 (D307). **Opened as its own
   ticket, B114**, rather than folded into this data-only turn — resolving it may need the
   detachment's actual CSM unit list resolved from rule text, not just a flag flip.
   `rules_assertions.py`'s `e21a_coverage` assertion still passes clean; the gap was already
   correctly recorded as unenforced, just on a rationale that no longer holds.

7. **B113 gains zero new instances** — confirmed by direct text search of the Chaos Daemons
   `DETACHMENTS` block: no `LEADER:` lines present.

8. **`faction_taxonomy.json` needed no edit** — Chaos Daemons already carried `built: true` from its
   original units build.

9. **Full baseline re-run** after both file updates — every gate green except the expected
   pre-`--write` P3/`pipeline_manifest`/`repo_check` state (resolved by the `--write` at the end of
   this handoff).

## State at close

- `detachments.json`, `detachment_parser.py`: both updated, diff-guarded, byte-verified.
- `40K_Decision_Log.md`: D315 appended. `DECISION_INDEX.md`: D315 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S221, count **22 → 22** (B112 closed to
  Closed/Shipped with full body preserved; B114 opened — net zero change).
- `units.json`, `unit_loadouts.json`, `abilities.json`, `wargear_points.json`,
  `datasheet_wargear_abilities.json`, `detachment_effects.json`, `faction_taxonomy.json`,
  `e21b_check.js`: untouched this session.
- `index.html`: untouched.
- `pipeline_manifest.py`: `SESSION_HANDOFF_221.md` registered in GUARDED before `--write`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history), and push it to the private source repo.
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (still outstanding
   from S220 — the project-area edit was accepted as authoritative and the manifest re-pinned to it,
   but the repo itself still holds the old version).
3. Push this session's changed/new files to the public repo (listed below).

## Decisions waiting on Ryan

None. No new rules-legality call or lasting precedent this session — the disposition change and
enhancement re-prices both follow directly from the v1.1 source text, and B114's opening is a
routine finding, not a call requiring Ryan's input.

## Files (SHA-256, first 12)

Verify these at S222 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachments.json` | `fd21e0ff9a08` | Chaos Daemons: LORDS OF THE WARP disposition + 3 Scintillating Legion re-prices only |
| `detachment_parser.py` | `31cd9fc5d350` | Chaos Daemons re-pointed to `MFM_Chaos Daemons_v1.1.txt` |
| `40K_Decision_Log.md` | `e9fd54a6423d` | D315 appended |
| `DECISION_INDEX.md` | `07df19f19264` | D315 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `a6cf4e8b4d5d` | ledger header S221, 22 → 22 (B112 closed, B114 opened) |
| `pipeline_manifest.py` | (pre-`--write`; re-pinned by `--write`) | `SESSION_HANDOFF_221.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S222 |
| `SESSION_HANDOFF_221.md` | (this file) | |

## Net New Files

None. Every file touched this session is a versioned pipeline output or an existing script/doc
update — no new file role was introduced.

## Backlog

22 open at S220 close; **22 open at S221 close** (B112 closed — Chaos Daemons LORDS OF THE WARP
shipped, verified direct from v1.1 source; B114 opened — stale `enforced: false` reason on the
existing Shadow Legion HERETIC ASTARTES unlock row, found while checking `detachment_effects.json`
per standing discipline; net zero change to the open count).

Beginning: B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17, B112 (22). Resolved: B112 (1). Added: B114 (1). Ending: B114, B113, B108, B99,
B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (22).
