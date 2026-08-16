# SESSION HANDOFF 252

**Turn type: data.** B137 — Chaos Space Marines' units-side migration to its v1.1 MFM, closing B89's
last piece of adoption debt and B94's last outstanding unit. No engine work, no tooling work mixed in.

## Session open

`./baseline.sh --fetch --data-turn`: **40/40 pass**, all guarded files verified against
`pipeline_manifest.json`. Nothing was worked around.

All S251 file hashes verified against `SESSION_HANDOFF_251.md`'s table before any work started:
`units.json`, `units_repro_check.py`, `rules_assertions.py`, `pipeline_manifest.py`,
`40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md` all matched.

A `^### ` grep inside the backlog's Open Items section returned **24** against a stated 24 — after
this session's own edits (see Backlog section below); it returned 25 at S251's stated count before
this session touched anything.

## What was found

**B137's own numbers, re-derived from source rather than trusted.** Parsed both
`MFM_Chaos_Space_Marines_v1_0.txt` and `_v1.1.txt` through the real `mfm_points_parser.py` and diffed
the output directly — not eyeballed off the MFM text. The result matched S251's count exactly: **17
units re-price**, three of them (Accursed Cultists, Dark Commune, Chosen) changing tier *shape* — the
2nd-copy price moves even where the printed number is unchanged, because v1.1 breaks the tier at
"1st-to-2nd / 3rd+" where v1_0 broke it at "1st / 2nd+". Chaos Rhino gains the esc4 shape (65/65/65,
4th+ 75) that B94 was waiting on.

Cross-checked the four cult-troop cross-legion prices directly against each god-legion's own committed
`units.json` block (not the ticket's prose): **Plague Marines is 180 in Death Guard and 190 in Chaos
Space Marines; Khorne Berzerkers is 170/330 in World Eaters and 180/345 in Chaos Space Marines** —
both confirmed stale as claimed. **Rubric Marines agreed on base tiers but its CSM copy carried no 4th
tier** (Thousand Sons' committed block has 110/200). **Noise Marines needed no change** — Emperor's
Children and CSM agree at 145/145/160 in both MFM versions.

**A second-order staleness in Chaos Daemons, found by the gate rather than assumed.** After promoting
the CSM migration, `rules_assertions.py`'s `B114` (Shadow Legion Thralls census) failed on exactly 5 of
its 21 pinned units — the ones whose Chaos Space Marines native counterpart moved price this turn
(Chaos Lord with Jump Pack, Chaos Terminator Squad, Chosen, Dark Commune, Accursed Cultists). Chaos
Daemons is Gen-1 hand-authored data in Wahapedia-shaped CSVs at the project root, never routed through
`wahapedia_transform.py` — its `Unit_Points.csv` rows for these 5 units still carried the old v1_0-
shaped CSM prices, because nothing regenerates them automatically. Confirmed by grep across every
parser that nothing writes to the root `Unit_Points.csv` programmatically — it is hand-authored input,
the same class of file as an MFM text file for any other faction, so the fix belongs there, not in
`units.json`.

**A gap in the manifest's own coverage, found while fixing the above.** The Chaos Daemons root CSVs
(`Unit_Stats.csv`, `Unit_Points.csv`, and the rest of `CD_ROOT_CSVS`) are not in
`pipeline_manifest.py`'s `GUARDED` list at all — confirmed by reading the list directly. They are the
only hand-authored *army* data in the project; every other faction is Wahapedia-derived. A bad sync of
these files would go undetected by both `units_repro_check.py` (which would faithfully reproduce the
wrong committed input) and the manifest (which never checks them). Opened as **B138**, tooling-only,
not touched this session — adding files to `GUARDED` is a manifest/tooling change and this was a data
turn.

## Decisions made, not blocked on

**1. Both v1_0 CSM files dropped from `units_repro_check.py`'s `REQUIRED` list, not carried forward.**
Confirmed by grep that nothing else in the script reads `MFM_Chaos_Space_Marines_v1_0.txt` or the four
sibling `_v1_0` files once the CSM build and cult-troop appends both point at v1.1. (They remain
referenced elsewhere — `detachments_repro_check.py` and `mfm_points_parser.py`'s `FACTION_BY_MFM` — for
their own unrelated reasons, and were not touched.)

**2. The Chaos Daemons fix goes in the source CSV, not `units.json`.** Same principle as every other
faction: fix the input, regenerate, never hand-edit the output. `Unit_Points.csv` is CD's input, not a
pipeline output, so editing it directly is the correct move, not a violation of "never hand-edit
output files."

**3. B138 opened rather than folded in.** Adding nine filenames to `pipeline_manifest.py`'s `GUARDED`
list is a manifest/tooling change; this session is typed data-only. A ticket beats a widened scope.

## What shipped

**`units_repro_check.py`.** CSM's own build re-pointed from `MFM_Chaos_Space_Marines_v1_0.txt` to
`_v1.1.txt`; `--emit-fourth-plus` added to its `convert_to_json.py` call (previously missing — this is
exactly the class of gap `B94-2` exists to catch, and it did, live: the assertion failed the moment the
CSM prices moved before the flag was added, and passed after). All four `CSM_CULT_TROOP_POINTS`
entries re-pointed at their sibling legions' v1.1 files (each already `REQUIRED` for that legion's own
build, so no new source enters the pipeline). Both `MFM_Chaos_Space_Marines_v1_0.txt` and the four v1_0
sibling files dropped from `REQUIRED`.

**`units.json`.** Regenerated through the full chain twice, each diff-guarded against a byte-identical
control run of the unmodified pipeline first, so each diff is attributable to exactly one change.

*First regeneration (the CSM migration itself):* **exactly 20 units changed, zero others, zero unit
ids added or removed, `points` only** — the 17 CSM-native re-prices (Abaddon the Despoiler, Accursed
Cultists, Chaos Lord with Jump Pack, Chaos Predator Annihilator, Chaos Predator Destructor, Chaos Rhino,
Chaos Terminator Squad, Chosen, Dark Commune, Defiler, Huron Blackheart, Masters of the Maelstrom,
Mutilators, Nemesis Claw, Red Corsairs Reave-Captain, Vashtorr the Arkifane, Venomcrawler) plus the
three cult troops whose cross-legion price actually moved (Khorne Berzerkers, Plague Marines, Rubric
Marines — Noise Marines correctly untouched).

*Second regeneration (the Chaos Daemons fix, after `Unit_Points.csv` was corrected):* **exactly 5 units
changed, zero others** — the Shadow Legion Thralls copies of the 5 CSM units above whose price moved,
now matching CSM exactly.

**`Unit_Points.csv`.** Five rows corrected to match CSM's new v1.1 prices: Chaos Lord with Jump Pack
(90→80 flat), Chaos Terminator Squad (180/360 flat → 175/350 flat), Chosen (125/135/135/250/260/260 →
135/135/145/270/270/280), Dark Commune (90/100/100 → 90/90/100), Accursed Cultists
(90/110/110/195/215/215 → 90/90/110/195/195/215).

**`rules_assertions.py`.** No code changes — `B94-2` and `B114` both fired correctly against the
existing code once the data moved, which is exactly what those assertions were built to do. No new
assertion was needed; this was the design working, not a gap.

## Verified directly, not just through the gate

`./baseline.sh --fetch --data-turn`: **40/40** on first run before this session's edits; individual
gate checks re-run after each promotion (see below), full baseline deferred to close since
`pipeline_manifest`/`repo_check` are expected to report stale until `--write` runs.

`python3 rules_assertions.py --tier all`: **136/137** after both regenerations — the sole failure is
`P3` (manifest staleness), which is expected mid-session and resolves at close. `B94-2` and `B114` both
confirmed passing in that run.

Both regenerations were diff-guarded against a byte-identical control run of the *unmodified* pipeline
first, not just eyeballed against the prior committed file — so each diff is attributable to exactly
the one change made, per the project's diff-guard-everything discipline.

**Not verified this session:** nothing requiring a browser. This was a data turn and shipped no UI
change. The three-deep unseen-UI backlog from S248/S249/S250 is **unchanged and still outstanding** —
see below.

## Files (SHA-256, first 12)

Verify these at S253 open.

| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | `4319e2e5990c` | 20 CSM units re-price (S252 migration) + 5 CD Shadow Legion Thralls re-price (S252 downstream fix) |
| `units_repro_check.py` | `84c613d8ed1b` | CSM build + `CSM_CULT_TROOP_POINTS` repointed to v1.1; `--emit-fourth-plus` added to CSM convert call; v1_0 CSM files dropped from `REQUIRED` |
| `Unit_Points.csv` | `032a5b524735` | 5 Shadow Legion Thralls rows corrected to match new CSM prices — **not currently a `pipeline_manifest.py`-guarded file; see B138** |
| `40K_Decision_Log.md` | `877c58a71d31` | D349 appended |
| `DECISION_INDEX.md` | `cb6aa823df44` | D349 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `33ba1a0ab3b2` | B137 and B94 closed and moved to Closed/Shipped with closure notes; B138 opened; header 25 → 24; S252 ledger added |
| `pipeline_manifest.py` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_252.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `units.json`, `units_repro_check.py`,
  `Unit_Points.csv`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
  `pipeline_manifest.py`, `pipeline_manifest.json`, `SESSION_HANDOFF_252.md`,
  `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- **`Unit_Points.csv` is a GW-derived-adjacent file: it is hand-authored, not extracted GW text, and
  is not on the repo-exclusion list.** It has shipped to the repo before (it is one of the
  `CD_ROOT_CSVS`); this is a normal push, not a new category.
- **The render check from S248/S249/S250 is still outstanding.** This session shipped no UI, so the
  backlog is still three deep. S250's is still the one that matters most — it silently edits a saved
  list. Scripts are in each of those three handoffs.
- **Optional eyeball on this turn's data**, one list, no urgency: build a Chaos Space Marines list and
  confirm Chaos Rhino now costs **65** for the first three and **75** for a fourth (previously flat 75
  throughout). Same for the tier-shape units — Chosen's second copy is now **135**, not 145; Accursed
  Cultists' second copy is now **90**, not 110.

## Decisions resolved this session

D349 — B137's migration, the Chaos Daemons downstream fix, B94's closure, and B138's opening.

## Backlog

25 open at S251 close; **24 open at S252 close**. B137 closed. B94 closed. B138 opened.
