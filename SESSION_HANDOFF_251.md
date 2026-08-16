# SESSION HANDOFF 251

**Turn type: data.** B94 (D348) — the Space Marines 4th+ tier, and the assertion covering the class
of defect that hid it. No engine work, no tooling work mixed in.

## Session open

`./baseline.sh --fetch --data-turn`: **41/41 pass**, 85 source files verified against
`source_manifest.json`. Nothing was worked around.

All eight S250 changed files verified against the fetched repo before any work started; every hash
matched the S250 handoff table — `index.html`, `b103_check.js`, `rules_assertions.py`, `baseline.sh`,
`pipeline_manifest.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`.

A `^### ` grep inside the backlog's Open Items section returned **24** against a stated 24.

## What was found

**B94's remaining-population figure was stale by a factor of six, and re-deriving it was the whole
point of the prompt's warning.** The ticket says 31 units remain. That is an S196 snapshot. Parsed
fresh from the raw MFM files with the real parser: the `YOUR 1ST TO 3RD UNITS COST` / `YOUR 4TH +
UNIT COSTS` shape appears on **34 rows across the 15 v1.1 files**, matching B94's own original scope
figure — and **nine units already carried `fourth_plus`** in committed `units.json`, not the three
the backlog names. Grey Knights, Emperor's Children, World Eaters and Drukhari each picked it up in
their own build turn, having been built after S194 added the flag. Only two factions were still
missing it.

(Three esc4 rows also sit in non-priority v1_0 files — Adepta Sororitas' Immolator, two Adeptus
Custodes units. Correctly out of scope; those factions are unbuilt.)

**The Space Marines gap had been shipping for roughly fifty sessions with every gate green.**
`--emit-fourth-plus` was added to `convert_to_json.py` at S194. Space Marines migrated to its v1.1
source at S198 (D291). The flag was never added to the SM `convert_to_json.py` call in
`units_repro_check.py`. Rhino, Razorback, Drop Pod and Impulsor have priced a 4th copy at the
1st-to-3rd rate ever since.

**Why no gate could see it, which matters more than the five units.** `units_repro_check.py` proves
`units.json` is what the pipeline emits — a convert call that was never given the flag reproduces
byte-for-byte just as faithfully as one that was. `B94-1` pins the engine ladder and the
well-formedness of any `fourth_plus` row that exists; it says nothing about rows that ought to exist
and do not, so it passed vacuously the entire time. The project had no check at all of the class
"the pipeline was invoked correctly but incompletely". That is what `B94-2` now covers.

**Found, not fixed: Chaos Space Marines is shipping wrong points today.** Its `units.json` block
still builds from `MFM_Chaos_Space_Marines_v1_0.txt`. B89 closed at S213 having migrated every
faction's *detachments*; CSM's *units* half was recorded blocked at S199 because World Eaters and
Emperor's Children did not exist yet, and was never revisited once both were built (S209, S218).
Quantified by direct parse-and-diff this session rather than inferred:

- **17 units re-price** from CSM's own file.
- **Three change tier *shape***, not just value — Accursed Cultists, Dark Commune and Chosen move
  from `1st unit`/`2nd +` to `1st to 2nd`/`3rd +`, so the **second copy** prices differently even
  where the printed numbers did not move.
- **The D240 cult-troop appends now disagree with their parent legions**, because those factions
  migrated and CSM did not: **Plague Marines at 10 models is 180 in Death Guard and 190 in Chaos
  Space Marines; Khorne Berzerkers is 170/330 in World Eaters and 180/345 in Chaos Space Marines.**
  Same datasheet, two prices, both shipped.
- CSM's Chaos Rhino should be 65 for copies 1–3 with a 4th+ of 75; it ships as a flat 75. That is
  B94's last outstanding unit.

Opened as **B137**. Deliberately not folded in — a ~20-unit migration with tier-shape changes and a
cult-troop reconciliation is its own diff-guarded turn, and a ticket beats a widened scope.

## Decisions made, not blocked on

**1. B94 stays open rather than closing on the Space Marines half.** Its data half is complete for
every faction except CSM, and CSM's one unit is unreachable without B137's whole-faction migration.
Closing it today would mean either shipping a knowingly-wrong Chaos Rhino or claiming a completeness
the data does not have.

**2. B137 is the next data turn, ahead of B90.** B90 blocks factions that do not exist yet. B137
moves points players are charged today, and two shipped units currently disagree with their own
parent legion. Sequencing call, mine; recorded so it is not re-litigated.

**3. `B94-2` elects its source file rather than being told it.** The obvious implementation is a
table mapping each army to the MFM file it builds from. That is precisely the artefact that just went
stale for fifty sessions, so it is not what was built — see below.

## What shipped

**`units_repro_check.py`.** `--emit-fourth-plus` added to the Space Marines `convert_to_json.py`
call, matching the seven faction blocks that already carried it. One line.

**`units.json`.** Regenerated through the full chain — transform, points, five chapter appends,
convert, merge, `add_loadout_groups`, `add_co_leader`, `add_bodyguard_stat_flags`,
`add_chapter_point_overrides`, `add_chapter_keyword_additions`. Diff-guarded against a
**byte-identical control run of the unmodified pipeline first**, so the diff is attributable to the
flag and nothing else. **Exactly 5 units changed, zero others, zero unit ids added or removed, and
only the `points` field on each:** Adeptus Astartes Drop Pod (4th+ 70), Razorback (95), Impulsor
(80), Rhino (75), Black Templars Impulsor (85). Every value checked against its MFM source line.

No chapter-override churn, and the reason is worth keeping rather than re-deriving: all six SM-family
v1.1 files price Drop Pod, Razorback and Rhino identically, so `add_chapter_point_overrides.py` finds
nothing to override; and the one that differs — Black Templars' Impulsor at 75/85 against a base
70/80 — is a Black-Templars-owned datasheet with its own `units.json` entry, so it never enters the
override comparison at all.

*One latent gap noticed while confirming that, recorded here rather than opened as a ticket because
nothing can reach it today:* `add_chapter_point_overrides.py`'s `_row_to_sizes` reads only the nine
1st/2nd/3rd points cells, so it would silently drop a 4th tier — but its equality test compares the
**full** row including the 4th-tier cells, so a chapter differing from base *only* in its 4th+ value
would create an override identical to base with the 4th tier lost. No shipped file has that shape.
Worth a look if a future MFM introduces one.

**`rules_assertions.py` — new `B94-2`.** For each `units.json` army block, every MFM file mapped to
that army's faction code in `FACTION_BY_MFM` is scored by how many of the block's units it prices at
exactly the committed 1st/2nd/3rd tiers, and the top scorer is **elected**. Only the army *name* is
hardcoded; which file it is built from is inferred from the data every run. A tie is permitted —
v1_0 and v1.1 genuinely agree on every unit of several small chapter blocks — but the tied files must
then agree on the 4th+ tier for the unit under test, or that unit fails as **ambiguous** rather than
passing on whichever filename sorted first. That is what disambiguates Grey Knights' Brotherhood
Terminator Squad, `esc4` in v1_0 and not in v1.1: the election picks v1.1 25-to-21 and the right
answer follows from the data, not from a remembered note.

A unit whose committed prices match nothing in the elected file is **skipped**, not failed — priced
by another mechanism (the four CSM cult troops per D240, the chapter override map, Chaos Daemons'
hand-authored CSVs). Seven today; the count is reported so a jump is visible. An army elected onto a
v1_0 file while a v1.1 exists is **reported, not failed** — that is B89 debt with its own ticket now,
and an assertion that fails on known-open work stops every session.

`parse_mfm` added to `TIER_B_NAMES`. `B94-2` resolves its filenames from `FACTION_BY_MFM` rather than
naming one literally, so the string-constant path that correctly tiers `E14-1` would have missed it
and a `--tier a` run would have **crashed on absent sources instead of skipping**. Confirmed no
existing assertion reclassifies.

## Verified directly, not just through the gate

`./baseline.sh`: **41/41**. `python3 rules_assertions.py --tier all`: **137/137** (136 before, plus
`B94-2`). All three repro gates reproduce byte-for-byte after the promotion.

**The new assertion was negative-tested three ways**, per S250's precedent that an untested gate is
not known to be a gate. Against the pre-change `units.json` it fails on exactly the five units and
names each expected value. A tampered `fourth_plus` value fails. A `fourth_plus` planted on a unit
whose MFM prints no 4th tier fails. It also passes the tier check: classified **B**, and a `--tier a`
run skips it cleanly rather than erroring.

**Not verified this session:** nothing requiring a browser. This was a data turn and shipped no UI
change. The three-deep unseen-UI backlog from S248/S249/S250 is **unchanged and still outstanding** —
see below.

## Files (SHA-256, first 12)

Verify these at S252 open.

| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | `3e965bbccf69` | 5 units gain `fourth_plus`: AA Drop Pod 70, Razorback 95, Impulsor 80, Rhino 75; BT Impulsor 85 |
| `units_repro_check.py` | `b99b72e630d3` | `--emit-fourth-plus` on the Space Marines convert call |
| `rules_assertions.py` | `1da8109777a2` | `B94-2` added; `parse_mfm` added to `TIER_B_NAMES` |
| `pipeline_manifest.py` | `16429fcb3b88` | `SESSION_HANDOFF_251.md` registered |
| `40K_Decision_Log.md` | `a9a389bddba7` | D348 appended |
| `DECISION_INDEX.md` | `a7c83da64333` | D348 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `323f71c09538` | B137 opened; B94 entry updated and its scope narrowed; header 24 → 25; S251 ledger added |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_251.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `units.json`, `units_repro_check.py`,
  `rules_assertions.py`, `pipeline_manifest.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.json`, `SESSION_HANDOFF_251.md`,
  `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- **The render check from S248/S249/S250 is still outstanding.** This session added no UI, so the
  backlog is three deep, not four. S250's is still the one that matters most — it silently edits a
  saved list. Scripts are in each of those three handoffs.
- **Optional eyeball on this turn's data**, one list, no urgency: build any Space Marines list, add
  **four** Rhinos, and confirm the fourth costs **75** where the first three cost 65. Same shape for
  Razorback (85 → 95), Drop Pod (60 → 70), Impulsor (70 → 80). Before this session the fourth
  charged the same as the first three.

## Decisions resolved this session

D348 — B94's Space Marines data half, the `B94-2` assertion and its election mechanism, the three
calls above, the re-derived population, and B137's split.

## Backlog

24 open at S250 close; **25 open at S251 close**. Nothing resolved; B137 opened. B94 advanced — its
remaining scope narrowed from "31 units" to one unit sitting behind B137 — but it does not close, for
the reason under decision 1.
