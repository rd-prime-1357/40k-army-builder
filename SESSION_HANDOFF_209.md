# SESSION HANDOFF 209

**Turn type:** scoping-only (Emperor's Children, D303). No `units.json`, `unit_loadouts.json`,
`detachments.json`, `index.html`, or parser file changed. `EMPEROR'S_CHILDREN_BUILD_SCOPE.md`
net-new.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch` first (32/33 gated, 39 tier-B assertions
   skipped — sources not yet loaded, expected for a fresh fetch-only open), then
   `./baseline.sh --fetch --data-turn` to pull the GW sources for the scoping checks below. 33 gates,
   sources loaded, 121/121 assertions, both repro checks byte-identical. `repo_check` red on exactly
   the pre-existing B108 finding (`Thousand_Sons_web.txt` in the public repo) — confirmed unchanged
   from S208 close, not a new reconciliation problem.

2. **Emperor's Children scoped (D303).** Full write-up in `EMPEROR'S_CHILDREN_BUILD_SCOPE.md`.
   Headline findings:
   - 23 datasheets, exact match between `Datasheets.csv` and the MFM — **zero LEGENDS exclusions**,
     first faction in the project where that's true.
   - Full dry-run pipeline (transform → points → convert) clean: 23/23 priced, 0 collisions, 0
     dropped attach entries, 4 Leader-eligibility overrides.
   - Loadout parser scoped to EC alone flagged exactly **2 units** (Tormentors, Infractors — both
     the same free equip-only "icon of excess" item, the exact shape already solved by Grey Knights'
     Ancient's banner). **Zero engine gaps found** — the first faction where scoping surfaces no
     engine ticket at all (Grey Knights needed B106 before its Dreadknights could be authored).
   - One cross-faction wrinkle checked and resolved, not a conflict: CSM's own cult-troop Noise
     Marines (`000004099`) is priced from `MFM_Emperors_Children_v1_0.txt`, a *different* datasheet
     ID from EC's own Noise Marines (`000004088`) — confirmed both MFM versions price it identically,
     so no version mismatch with CSM's already-shipped cross-reference.
   - Confirmed EC needs no `add_chapter_point_overrides.py` or `add_co_leader.py` registration, same
     conclusion as Grey Knights and for the same reason (Heretic Astartes, not Space Marine-descended).
   - Detachments: 10, zero unique tags, 4 force-disposition changes v1_0→v1.1 (Carnival of Excess,
     Coterie of the Conceited, Frenzied Host, Spectacle of Slaughter). One genuine points change: two
     Defiler wargear options moved 10→15 pts between versions (marked with the source's own up-arrow
     annotation, not a data problem). Build from v1.1 per D293.

3. **Found and logged B110** (unrelated to Emperor's Children): `faction_taxonomy.json` still shows
   Grey Knights as `built: false` under the Imperium group, stale since B100 closed at S208. XS data
   fix, not yet made — this turn is scoping-only.

4. **Located B109's render site, did not touch it.** `index.html`'s `renderMyLists()`:
   `const tgt = r.points_target ? ('target ' + r.points_target) : '';` — one-line change to
   `(r.points_target + ' Points')`. Not made this session; an `index.html` edit would mix engine work
   into a scoping-typed turn. Confirmed genuinely XS and single-line for whenever it's picked up.

## State at close

- `EMPEROR'S_CHILDREN_BUILD_SCOPE.md`: net-new, full findings and suggested sequencing.
- `40K_Decision_Log.md`, `DECISION_INDEX.md`: D303 appended.
- `OPEN_ITEMS_BACKLOG.md`: B110 opened; B109 updated with render-site location; header count 22→23.
- `units.json`, `unit_loadouts.json`, `wargear_points.json`, `detachments.json`,
  `detachment_effects.json`, `index.html`, every parser, `rules_assertions.py`,
  `faction_taxonomy.json`: **untouched.**
- `pipeline_manifest.py`: `SESSION_HANDOFF_209.md` appended to `GUARDED`.
- Emperor's Children is fully scoped, no open design decisions, no engine tickets. Ready for its
  units data turn next.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged from
   S208; ideally scrub git history).
2. Push this session's changed files to the public repo (listed below).

## Decisions waiting on Ryan

None. Nothing found this session was rules-legality-ambiguous or a lasting-precedent question.

## Files (SHA-256, first 12)

Verify these at S210 open.

| file | note |
|------|------|
| `EMPEROR'S_CHILDREN_BUILD_SCOPE.md` | net-new |
| `40K_Decision_Log.md` | D303 appended |
| `DECISION_INDEX.md` | D303 entry |
| `OPEN_ITEMS_BACKLOG.md` | B110 opened; B109 updated; header count updated |
| `pipeline_manifest.py` | `SESSION_HANDOFF_209.md` appended to GUARDED |
| `pipeline_manifest.json` | regenerated via `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) S210 |
| `SESSION_HANDOFF_209.md` | this file |

`index.html`, `units.json`, `unit_loadouts.json`, `wargear_points.json`, `detachments.json`,
`detachment_effects.json`, `faction_taxonomy.json`, every parser, `rules_assertions.py`,
`source_manifest.json`, `baseline.sh`: **untouched**, no entry needed.

## Backlog

22 open at S208 close; 23 open here (B110 opened, nothing closed). Beginning: B108, B99, B98, B97,
B103, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17, B109 (22).
Resolved: none. Added: B110. Ending: B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89,
B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (23).
