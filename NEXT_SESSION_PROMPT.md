# NEXT SESSION PROMPT — Session 253

## Read first

`SESSION_HANDOFF_252.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S252 close: `index.html` **v6.26** (unchanged — S252 was a data turn), decision log through
**D349**, `SCHEMA_VERSION` **5**, baseline **40/40**, rules assertions **137/137**, **24 open**
backlog items.

## Open

Run `./baseline.sh --fetch --data-turn`. It covers every gate in one command. **40/40 must pass.**
If a gate fails, reconcile before starting — do not work around it.

Then verify the S252 file hashes in `SESSION_HANDOFF_252.md`'s Files table against the fetched repo.
This is deliberately redundant with `repo_check`, so a bad sync is still caught when the repo is
unreachable or stale.

## Assigned work: B138 — tooling turn

**Type this turn tooling-only.** No engine or data work mixed in.

Found while closing B137 (S252): the nine Chaos Daemons hand-authored root CSVs (`Unit_Stats.csv`,
`Unit_Points.csv`, `Unit_Wargear_Options.csv`, `Unit_Other_Options.csv`, `Unit_Weapons.csv`,
`Unit_Abilities.csv`, `Keywords.csv`, `Rules.csv`, `Weapon_Abilities.csv` — `CD_ROOT_CSVS` in
`units_repro_check.py`) are not in `pipeline_manifest.py`'s `GUARDED` list. Read B138's full entry in
`OPEN_ITEMS_BACKLOG.md`, confirm the list yourself before touching anything — do not trust this
prompt's filename list as final; re-derive it from `CD_ROOT_CSVS` directly.

**Build shape.** Add the nine filenames to `GUARDED`, run `pipeline_manifest.py --write`, confirm
`--freshness-check` passes. That should be the entire turn. Sanity-check afterward that a deliberately
tampered copy of one of the nine files (e.g. `Unit_Points.csv`) actually fails `pipeline_manifest`
before restoring it — an untested guard is not a known-working guard, per the project's own precedent
on negative-testing new gates (see S251/`B94-2`).

**Flag the model before any analysis turn.** This one should be entirely mechanical — adding filenames
to a Python list and running a write/verify command — but if anything about `CD_ROOT_CSVS`'s scope
turns out ambiguous (e.g. a file used by CD that isn't actually hand-authored, or vice versa), stop and
flag before guessing.

## Once B138 closes: two live-risk items are next, pick one

Both are large (`L`, spans sessions) and neither is reachable in a single sitting — the choice of which
to open first is a sequencing call for whoever runs S254, not decided here. Read both scope sections
before choosing.

**B90 — SM-family chapter rosters union bug, engine+data, blocks further faction work.**
`resolveUnits()` unions the full generic Adeptus Astartes pool into every `is_subfaction` chapter, with
no distinction between the six vanilla chapters (correct to union) and the five dedicated-MFM chapters
— Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves — whose MFM is a complete,
self-contained roster that should never be unioned with generic. This is shipping wrong rosters today
for five already-built factions, not a blocker for unbuilt work.

**B93 — Enhancement/Upgrade eligibility, engine+data, live D0 gap, Ryan-flagged.** The engine checks
Character-vs-not instead of the Enhancement's own qualification requirement. Censused at 641 records /
363 names / 173 detachments / 13 armies bearer-restricted, with 369 records over-admitting today (mean
9.2 illegal bearers per record). This is a live D0 violation — an enhancement can currently be assigned
to a bearer the rules do not permit — which outranks B90's mispriced-roster defect on the D0 principle
alone, but B90 affects rosters players see immediately on list-build and B93's fix is larger. Sequencing
call for S254.

## Precedents from S252 that will matter again

**A ticket's population figure is a snapshot — the second session running this has been re-derived and
confirmed, not just re-derived and corrected.** B137's own 17-unit/3-shape-change/cult-troop figures,
written at S251, matched exactly when re-parsed from source at S252. Re-deriving does not always find
an error; it is still the right discipline every time, because the one time it does not match is the
one that matters.

**A migration inside a pipeline faction can strand a hand-authored faction that copies its prices.**
Chaos Daemons' Shadow Legion Thralls census (`B114`) exists specifically because CD borrows CSM
datasheets by name; it caught the staleness this session created before it shipped. Any future
migration of a faction whose units are named-copied elsewhere (check for other `allied_group` census
assertions before starting a migration turn) should budget for this class of downstream check.

**Fix hand-authored input at its own file, never at `units.json`, even when that input isn't guarded.**
`Unit_Points.csv`'s five stale rows were corrected directly, the same as any MFM-sourced fix would be,
despite not yet being manifest-guarded (that gap is B138 itself). The manifest's absence does not
change which file is the source of truth.

**`B94-2`'s election mechanism worked exactly as designed, with zero code change.** It failed the
moment CSM's prices moved and the flag hadn't been added yet, and passed cleanly once both landed
together — this is the second session running an assertion built this way needed no maintenance to
track a migration it was never told about by name.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_253.md`), this file rewritten for S254, then:

1. add `SESSION_HANDOFF_253.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan action carried forward from S248, S249 and S250

**A render check covering three sessions' UI.** S248's Tank Ace checkbox, S249's Mark of Chaos
selector, S250's silent truncation of an over-cap tally on size reduction. S252 shipped no UI, so the
backlog is still three deep. S250's is the one that matters most — it is the only one that edits a
saved list without telling the player. All three handoffs carry step-by-step scripts.
