# SESSION HANDOFF 245

**Turn type: data-only.** B130 data half (D342). No engine file and no gate logic was touched.

## Session open

Full `./baseline.sh --fetch --data-turn`: **37/37 pass**, 85 GW source files fetched from the
private repo and verified against `source_manifest.json`, nothing skipped.

All six S244-changed files verified against a fresh clone before any work started, and every hash
matched the S244 handoff table — `rules_assertions.py`, `pipeline_manifest.py`,
`pipeline_manifest.json`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`.
**`pipeline_manifest.json` was among what actually landed this time**; S243's omission did not
recur.

## What was found

**The B130 population is 28 units, not 6.** `B93_SCOPE.md` §12 said 5 Deathwing + 1 Ravenwing, and
`NEXT_SESSION_PROMPT.md` said the derivation "should not need a re-derivation from source." It was
re-derived anyway, per the standing rule. §12's figure is not wrong — it counts generic-pool
*Characters*, which is exactly what B93's bearer arc needs — but it is not a count of the data
defect, and building to it would have closed the ticket over a still-broken dataset.

Derived from `Datasheets_keywords.csv` / `Datasheets.csv` / `Source.csv` using
`wahapedia_transform.py`'s own `SUBFACTION_KEYWORD_ARMY`, `KNOWN_CHAPTERS` and
`source_is_excluded()`: **28 generic Adeptus Astartes units carry a stripped sub-faction keyword —
18 Deathwing, 10 Ravenwing.** All are all-models, non-faction keyword rows; all are present in the
shipped generic block. Beyond §12's six Characters the set adds Terminator Squad, Terminator
Assault Squad, Bladeguard Veteran Squad, Sternguard Veteran Squad, Vanguard Veteran Squad With Jump
Packs, Dreadnought, Ballistus/Brutalis/Redemptor Dreadnought, the three Land Raiders, Repulsor and
Repulsor Executioner; plus Outrider Squad, Invader ATV, the three Storm Speeders, Stormhawk
Interceptor, Stormraven Gunship and Stormtalon Gunship.

**Verified against the composition sources, not just the raw export.** `Dark_Angels_web.txt` carries
the keyword on the `KEYWORDS:` line of all 28. `Space_Marines_web.txt` carries zero
Deathwing/Ravenwing mentions of any kind, as do `Black_Templars_web.txt` and `Space_Wolves_web.txt`
— consistent with `SUBFACTION_KEYWORD_ARMY` naming one owning chapter for both keywords. So the
transform's strip is correct for the generic pool and wrong for the Dark Angels view, at 28 units.

**The fix does not fit one turn type.** Emitting the map is data; consuming it in `resolveUnits` is
engine. Split on the B56c/B56d precedent — B56c shipped `chapter_point_overrides` as inert data,
B56d taught the engine to read it. **B130 re-scoped to the data half (shipped here); B132 opened
for the engine half.**

## What shipped

`add_chapter_keyword_additions.py` (net new) derives the map fresh from the raw exports on every
build and stamps `chapter_keyword_additions` — `{"<Chapter Army Name>": ["<Keyword>", ...]}` — onto
the 28 qualifying generic units in `units.json`. It imports the transform's constants and exclusion
rule rather than re-implementing them, so the emitter cannot drift from the strip it inverts. It is
idempotent (clears the field everywhere before re-stamping) and exits non-zero if a model-scoped
sub-faction keyword row ever appears, since that is a different shape that must be designed rather
than flattened onto a whole unit. Placed last in the rebuild chain, after
`add_chapter_point_overrides.py`.

`units_repro_check.py` runs the new step in its rebuild chain and lists the script in `REQUIRED`,
so the derivation sits inside the byte-for-byte fixed point. **No new `rules_assertions.py` entry**:
the repro gate re-derives the map from source every run and fails on any drift, which satisfies
D107, matches how `chapter_point_overrides` is policed, and keeps this turn data-only.

`units.json` changed on exactly 28 records, each gaining exactly the one new key. Verified at the
key level, not just "the pipeline ran clean": a field-by-field comparison against the pre-run copy
found 28 records with key changes, zero out-of-scope diffs, and no changed value on any existing
key anywhere in the file.

**The field is inert.** Nothing reads it until B132 ships; no rendered behaviour changed this
session, and `index.html` was not touched (still the version S244 left).

## Files (SHA-256, first 12)

Verify these at S246 open.

| file | sha256:12 | note |
|------|-----------|------|
| `add_chapter_keyword_additions.py` | `9511ebe13f2b` | **net new** — derives and stamps the per-army keyword-restoration map |
| `units.json` | `1241ba9d498a` | `chapter_keyword_additions` on 28 generic units; nothing else changed |
| `units_repro_check.py` | `e8023696201b` | new step in the rebuild chain + `REQUIRED` entry |
| `pipeline_manifest.py` | `e33538c37d03` | `add_chapter_keyword_additions.py` and `SESSION_HANDOFF_245.md` registered |
| `40K_Decision_Log.md` | `ee2d04f4799e` | D342 appended |
| `DECISION_INDEX.md` | `70959fbe96d3` | D342 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `bf6e5e8e493d` | B130 shipped, re-scoped to the data half; B132 opened; 25 -> 25 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_245.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `add_chapter_keyword_additions.py`,
  `units.json`, `units_repro_check.py`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_245.md`,
  `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.** S244's push got this right; keep it right.

## Decisions resolved this session

D342 — population re-derivation (28, not 6), the per-army map shape, the B130/B132 turn split, and
the no-new-assertion call. All technical or scoping; nothing here required Ryan's input.

## Backlog

25 open at S244 close; **25 open at S245 close**. Resolved B130; added B132.
