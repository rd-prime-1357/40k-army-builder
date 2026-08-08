# SESSION HANDOFF 220

**Turn type:** data-only (Grey Knights detachments — per `GREY_KNIGHTS_BUILD_SCOPE.md` §10 step 4).
`detachment_parser.py`, `detachments.json`, `faction_taxonomy.json` shipped end to end. Grey
Knights is now fully built (units + detachments both complete) and selectable. **This closes the
entire Adeptus Astartes group — all twelve armies are now built.**

## What happened

1. **Baseline reconciled at open**, with one genuine surprise beyond the expected B108 finding.
   `./baseline.sh --fetch --data-turn`: private source repo fetched and verified fresh (85/85 files
   byte-match `source_manifest.json`). `OUTPUT_FORMAT_SPEC_for_project_instructions.md` failed both
   `pipeline_manifest.py` and `repo_check.py` — the project-area copy carries a new instruction
   (grouping delivered files into "Repo-only" vs "Project area" labels) not yet pushed to the repo.
   `repo_check.py` confirmed this was the *only* file differing between area and repo (185
   byte-identical, 1 differs, 13 repo-only informational — no data/pipeline file affected).
   Reconciled by re-pinning the manifest to the area's copy (the standing "area copy wins"
   convention for docs); verified via before/after diff that only this one entry changed. Left
   `repo_check.py` correctly red on this file going forward — Ryan's push action, same shape as
   B108. Full baseline then ran clean (31/31 gates, tier-A+B).

2. **`GK` registered in `detachment_parser.py`'s three maps** (`ARMY_TO_MFM`, `MFM_SOURCE_NAME`,
   `ARMY_TO_WAHA_FACTION`), mirroring the World Eaters pattern (D313) exactly. `GK` confirmed as the
   correct Wahapedia faction code from `mfm_points_parser.py`/`repro_check.py`/`units_repro_check.py`
   before use.

3. **`detachments.json` built** from `MFM_Grey_Knights_v1.1.txt` per D293 (always the newest MFM).
   Diff-guarded: **9 Grey Knights detachments added, 0 changed, 0 removed elsewhere.** Verified
   directly against `GREY_KNIGHTS_BUILD_SCOPE.md` §8's forecast, re-derived from source rather than
   trusted: DP 1–3; zero `UNIQUE:` tags anywhere in the faction (confirmed by direct text search of
   both MFM files); exactly the three forecast force-disposition changes, each with its own `FORCE
   DISPOSITION(S) CHANGED` banner — Argent Assault Purge the Foe → Priority Assets, Immaterial
   Interdiction Priority Assets → Reconnaissance, Warpbane Task Force Purge the Foe → Take and Hold.
   No DP changes, no enhancement re-prices between v1_0 and v1.1.

   **Correction to the scope doc:** §8 forecast 28 enhancements total; the real count from source is
   **30** (2+4+4+4+2+4+2+4+4 across the nine). The "4 Upgrade" part was correct. Caught by
   re-deriving from source per the standing discipline rather than trusting a four-session-old scope
   doc's own analysis.

4. **`detachment_effects.json` needed no new row — checked directly, not assumed.** Manual read of
   all nine detachments' `rule_text`/`restrictions` found no allied-unlock or BATTLELINE-grant
   pattern, consistent with Grey Knights being fully self-contained (§3: no allied-codex problem, no
   cross-file points sourcing). `rules_assertions.py`'s `e21a_coverage` assertion — the same
   automated scan that caught World Eaters' unflagged Cult of Blood gap at D313 — passed clean on
   the full baseline re-run, confirming the manual scan wasn't missing anything.

5. **`e21b_check.js`'s battleline-sweep literal unchanged at 9** — Grey Knights grants no BATTLELINE
   keyword, confirmed by the harness's own live sweep still passing with no update needed.

6. **`faction_taxonomy.json`: Grey Knights' `built` flag flipped to `true`, `data_army: "Grey
   Knights"` added** — same sequencing as D298 (original attempt, corrected S210 when detachments
   turned out to be zero), D305 (Emperor's Children), D313 (World Eaters). **This closes B110**
   (`faction_taxonomy.json` stale `built: false`), which was correctly left open at S210 pending
   exactly this build rather than flipped prematurely into a broken empty-detachment-picker state.

7. **B113 gains zero new instances** — confirmed by direct text search of the Grey Knights
   `DETACHMENTS` block: no `LEADER:` lines present.

8. **Full baseline re-run** after all three file updates (`detachment_parser.py`, `detachments.json`,
   `faction_taxonomy.json`): every gate green except the expected pre-`--write` P3/`pipeline_manifest`/
   `repo_check` state (resolved by the `--write` at the end of this handoff).

## State at close

- `detachments.json`, `detachment_parser.py`, `faction_taxonomy.json`: all updated, diff-guarded,
  byte-verified.
- `40K_Decision_Log.md`: D314 appended. `DECISION_INDEX.md`: D314 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S220, count **23 → 22** (B110 closed, moved to
  Closed / Shipped with full body preserved). B113 unchanged (0 new instances this session).
- `OUTPUT_FORMAT_SPEC_for_project_instructions.md`: unchanged content, manifest re-pinned to match
  (area copy). Still needs pushing to the repo — see Ryan action below.
- `units.json`, `unit_loadouts.json`, `abilities.json`, `wargear_points.json`,
  `datasheet_wargear_abilities.json`, `detachment_effects.json`, `e21b_check.js`: untouched this
  session.
- `index.html`: untouched.
- `pipeline_manifest.py`: `SESSION_HANDOFF_220.md` registered in GUARDED before `--write`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history), and push it to the private source repo.
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (or confirm the
   project-area edit is final first) — this session accepted the area's copy as authoritative and
   re-pinned the manifest to it, but the repo itself still holds the old version.
3. Push this session's changed/new files to the public repo (listed below).

## Decisions waiting on Ryan

None. No new rules-legality call or lasting precedent — the `detachment_effects.json` no-row
finding and the B110 closure both follow directly from already-established patterns (D204/D248's
construction-effect shapes; D298/D305/D313's `built`-flag sequencing).

## Files (SHA-256, first 12)

Verify these at S221 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachments.json` | `2ae62e030015` | +9 Grey Knights detachments |
| `detachment_parser.py` | `e0385ff53a12` | `GK` registered in all three maps |
| `faction_taxonomy.json` | `9ee4e83fe660` | Grey Knights `built` → `true`, `data_army` added |
| `40K_Decision_Log.md` | `9473613188b5` | D314 appended |
| `DECISION_INDEX.md` | `7ff7e225c4ab` | D314 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `36ebdb7e8b6a` | ledger header S220, 23 → 22 (B110 closed) |
| `OUTPUT_FORMAT_SPEC_for_project_instructions.md` | `b7a22f6e9398` | unchanged content; manifest re-pinned to area copy — still needs pushing to repo |
| `pipeline_manifest.py` | (pre-`--write`; re-pinned by `--write`) | `SESSION_HANDOFF_220.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S221 |
| `SESSION_HANDOFF_220.md` | (this file) | |

## Net New Files

None. Every file touched this session is a versioned pipeline output or an existing script/doc
update — no new file role was introduced.

## Backlog

23 open at S219 close; **22 open at S220 close** (B110 closed — Grey Knights detachments shipped,
closing the ticket that was blocked on exactly this build; nothing new opened).
Beginning: B113, B110, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2,
P4, E23, B67b, E12, B17, B112 (23). Resolved: B110 (1). Added: none (0). Ending: B113, B108, B99,
B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17, B112 (22).
