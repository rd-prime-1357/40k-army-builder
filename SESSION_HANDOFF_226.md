# SESSION HANDOFF 226

**Turn type:** data-only (Drukhari detachments — build `detachments.json` for the 9 detachments,
plus the deferred `detachment_parser.py` three-map registration). `detachment_parser.py`,
`detachments.json`, `rules_assertions.py` changed. `units.json`, `unit_loadouts.json`,
`wargear_points.json`, `index.html` untouched. Closes no numbered backlog ticket — Drukhari's
build is part of the standing faction-priority-order sequence, not its own item. See D320.

## What happened

1. **Open-time baseline clean.** `./baseline.sh --fetch --data-turn`: 34/34 gates, 85 source
   files verified, 106 overlay-needed files (including `detachments.json`, not resident locally
   in the project area) fetched and verified against the public repo.

2. **Registered Drukhari in `detachment_parser.py`'s three maps** — `ARMY_TO_MFM` →
   `MFM_Drukhari_v1.1.txt`, `MFM_SOURCE_NAME` → "Drukhari", `ARMY_TO_WAHA_FACTION` → "DRU". Safe
   now that `detachments.json` content is about to exist (deferred at S224 specifically because
   doing it early broke `detachments_repro_check`).

3. **§5's numbers re-derived from a real parser run, not trusted unchecked — matched exactly.**
   9 detachments, DP range 1–3: Covenite Coterie (2), Exhibition of Slaughter (1), Kabalite
   Agonysts (1), Kabalite Cartel (2), Realspace Raiders (2), Reaper's Wager (3), Skysplinter
   Assault (2), Spectacle of Spite (2), Tools of Torment (1). Three shared Unique tags confirmed
   (COVENS, WYCH CULT, KABAL, each shared by two detachments) — already-precedented mechanism
   (Blood Angels, Death Guard, CSM, Thousand Sons), no new code. 30 enhancements total, confirmed
   by direct count. Three `FORCE DISPOSITION(S) CHANGED` tags confirmed by direct grep of
   `MFM_Drukhari_v1.1.txt` (3 instances, not assumed).

4. **Three detachments confirmed `text_source: "none"`** (Exhibition of Slaughter, Kabalite
   Agonysts, Tools of Torment) — no Wahapedia rule text exists for these in either
   `Detachment_abilities.csv` or `Detachments.csv`, checked directly. Matches the precedented gap
   shape (25 → 28 instances). Tools of Torment's "Elixir of the Corpse Courts (Upgrade)" confirmed
   correctly stripped by the existing `is_upgrade` handling.

5. **B113 re-confirmed at 0 new instances for Drukhari** — checked directly against the real
   9-detachment build: zero `LEADER:` lines inside Drukhari's `DETACHMENTS` block in
   `MFM_Drukhari_v1.1.txt`.

6. **Diff-guarded against a clean repo fetch, not just "ran clean."** Pulled the pre-session
   committed `detachments.json` fresh from the public repo tarball (not the local copy) and
   compared field-by-field against the regenerated file: +9 Drukhari detachment records, +1 army
   entry, 0 removed, 0 existing detachment records changed. `_meta` counts move cleanly: armies
   19→20, detachment_records 202→211, enhancements 709→739 (+30), upgrade_enhancements 47→48
   (+1), gap manifest 25→28 (+3).

7. **Real finding: Drukhari adds 2 same-army enhancement-name collisions, both differently
   priced.** Towering Arrogance (Kabalite Agonysts 15pts vs Kabalite Cartel 20pts) and Periapt of
   Torments (Exhibition of Slaughter 20pts vs Spectacle of Spite 25pts) — both flagged in
   `DRUKHARI_BUILD_SCOPE.md` §5 as non-issues mechanically, since enhancements key off
   detachment+name, not name alone. Confirmed against the live build: `rules_assertions.py`'s
   `e4b_name_collision_census` (D199 pinned assertion) moved from 30 pairs / 6 names / 1
   differently-priced to 32 pairs / 8 names / 3 differently-priced. Updated the literal, same
   pattern as S225's E14 update, with a dated comment recording the new figures. No engine
   change needed — the existing detachment-keyed storage already handles this correctly.

8. **Full baseline re-run with all changes in place.** `repro_check`, `units_repro_check`,
   `detachments_repro_check` all byte-identical to committed; `rules_assertions` 121/122 (the one
   red is the expected P3 manifest-drift for the three edited files, cleared by `--write` below);
   every harness clean — zero regression to any already-built faction.

## Not investigated this session

B114, GK §6/§7 untouched — different turn types, not mixed per the standing rule. B113 was
re-confirmed (not newly investigated) as part of this build's own item 5, per the next-session
prompt's instruction — no separate engine turn opened for it.

## State at close

- `detachment_parser.py`: Drukhari registered in all three maps (`ARMY_TO_MFM`,
  `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`).
- `detachments.json`: +9 Drukhari detachment records, +1 army entry. 0 removed, 0 existing
  records changed.
- `rules_assertions.py`: `e4b_name_collision_census` literal 30/6/1 → 32/8/3, with a dated
  comment recording Drukhari's two new colliding names.
- `units.json`, `unit_loadouts.json`, `wargear_points.json`, `index.html`: untouched.
- `40K_Decision_Log.md`: D320 appended. `DECISION_INDEX.md`: D320 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S226, count unchanged at 23 (no ticket
  closes or opens — Drukhari's detachments build isn't a numbered backlog item).

Drukhari's units (D318), loadouts (D319), and detachments (D320) are now all shipped. Only B116
(Harlequins/Anhrathe allied-inclusion mechanic) remains open on the Drukhari build, still
awaiting Ryan's call, still not blocking anything already shipped.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged).
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (still outstanding
   from S220).
3. **Push `pipeline_manifest.json`** — still outstanding from S223's open-time reconciliation.
4. Push this session's new/changed files to the public repo: `detachment_parser.py`,
   `detachments.json`, `rules_assertions.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
   `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`/`.json`, this handoff,
   `NEXT_SESSION_PROMPT.md`. This adds to the same pending push queue as S223–S225's files —
   `repo_check.py` will keep showing `DIFFERS` findings until pushed; expected, not a new
   problem.

## Decisions waiting on Ryan

**B116** — unchanged (Drukhari's Harlequins/Anhrathe allied-inclusion mechanic; see
`DRUKHARI_BUILD_SCOPE.md` §6). Not touched this session. Recommendation remains to build it as
its own follow-on ticket once Ryan decides whether/how to admit a cross-book allied-inclusion
mechanic — does not block anything already shipped.

## Files (SHA-256, first 12)

Verify these at S227 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachment_parser.py` | `7fc60458b51a` | Drukhari registered in 3 maps |
| `detachments.json` | `04d17e35f2bb` | +9 Drukhari detachments, additive |
| `rules_assertions.py` | `cfd776236c49` | name-collision census literal 30/6/1 → 32/8/3 |
| `40K_Decision_Log.md` | `8b5da9f31513` | D320 appended |
| `DECISION_INDEX.md` | `295a442171bb` | D320 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `d6dc3aa6e722` | ledger header S226, count unchanged (23) |
| `pipeline_manifest.py` | `55d1a63ae30e` | `SESSION_HANDOFF_226.md` appended to GUARDED |
| `pipeline_manifest.json` | `af3ebea44df9` | regenerated by `--write` at close |
| `NEXT_SESSION_PROMPT.md` | `21c442ab22cf` | informational only, never guarded — S227 |
| `SESSION_HANDOFF_226.md` | `ad9575270ad0` | this file, hash not self-referential |

## Net New Files

None this session. `detachments.json` is an update to an existing, versioned file (new army data
inside it, not a new file). `detachment_parser.py` and `rules_assertions.py` are updates to
existing pipeline/harness files.

## Backlog

23 open at S225 close; **23 open at S226 close** (unchanged — Drukhari's detachments build
advances the standing faction-priority-order sequence but isn't its own backlog ticket; nothing
closed, nothing opened).

Beginning: B116, B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23). Resolved: none (0). Added: none (0). Ending: B116, B114,
B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17 (23).
