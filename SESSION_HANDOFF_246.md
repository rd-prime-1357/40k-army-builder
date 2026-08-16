# SESSION HANDOFF 246

**Turn type: engine-only.** B132 (D343). No data file was regenerated; no parser was touched. The
one non-engine edits are the gate registration in `baseline.sh` and `pipeline_manifest.py`, which
are the new gate's own wiring rather than separate tooling work.

## Session open

`./baseline.sh --fetch`: **31/31 pass**, 5 tier-B gates correctly skipped (GW sources not loaded —
B132 needs none). Nothing was worked around.

All ten S245-changed files verified against a fresh clone before any work started, and every hash
matched the S245 handoff table — `add_chapter_keyword_additions.py`, `units.json`,
`units_repro_check.py`, `pipeline_manifest.py`, `pipeline_manifest.json`, `40K_Decision_Log.md`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_245.md`, `NEXT_SESSION_PROMPT.md`.
`pipeline_manifest.json` was among what landed; D337's concern did not recur.

## What was found

**S245's population headline is a typo; the data is correct.** The handoff says 18 Deathwing / 10
Ravenwing. `units.json` carries **19 Deathwing / 9 Ravenwing**, and S245's own narrative list in the
same paragraph enumerates 19 and 9. Total 28 unchanged, derivation unaffected, no data defect.
Corrected in D343 and in B130's backlog entry so it is not chased later.

**B131's `EXEMPT` removal is not a deletion — the follow-up was mis-scoped.** D342 and this
session's incoming prompt both framed it as a small tooling pass gated on B132. The zero-bearer gate
does not run the engine; it runs `rules_assertions.py`'s `Sources.resolved_pool()`, a Python mirror
of `resolveUnits()` that unions the generic and chapter blocks and applies **neither** per-chapter
map. B131's per-unit membership reads each unit's own built keyword fields (D341), so the 6
Deathwing-family records still resolve to zero admits under that mirror even with B132 shipped, and
removing the exemptions today fails the gate immediately. Opened as **B133**, scoped to teach the
mirror the map first, with the gate's count moving 36 → 30 as the proof.

Noted in the same place: the mirror has been missing `chapter_point_overrides` since B56d. No
assertion reads pool points today, so nothing is currently wrong because of it, but the docstring
claims a fidelity the function does not have. Folded into B133 rather than left to be rediscovered.

**One gate assertion was wrong on the first draft and the live data caught it.** The
generic-pool check was written as "no Deathwing anywhere in the generic pool" and failed — generic
Adeptus Astartes units that carry Deathwing *natively* exist. The rule being enforced is that
resolution changes nothing in that pool, so the check became a comparison against a pre-resolve
snapshot. Worth knowing because the same trap sits in any future "the keyword should not be here"
assertion.

## What shipped

`index.html` **v6.23 → v6.24**. New `applyChapterKeywordAdditions(units, armyName)` sits beside
`applyChapterPointOverrides()` and runs after it on the union path in `resolveUnits()`. The two maps
touch disjoint fields, so their order carries no meaning; they are adjacent so a reader finds all
per-chapter variation in one place. The `complete` early return still precedes both.

Non-mutation is deeper here than in B56d. Keywords live two levels down, so the function copies the
unit, its `model_groups` array, and each affected group object; an in-place `keyword_names` push
would have leaked Deathwing into every other chapter's resolved pool and into the generic Space
Marines pool, all of which hold the same object reference. Unaffected units are returned by their
original reference. It dedupes against natively-carried keywords, and places the addition
alphabetically when the existing list is already sorted while appending when it is not — the
Wahapedia-derived blocks sort `keyword_names`, the hand-built Chaos Daemons blocks keep source order
(75 of 508 model groups), and sorting unconditionally would silently reorder data this field does
not touch today but could reach later.

`b132_check.js` (**net new**), on the `b90_check.js` model. Eight synthetic checks: the keyword lands
for the owning chapter on every model group; it lands for no other chapter; the generic pool is
identical to a pre-resolve snapshot; the shared `units.json` objects are unmutated after every
resolve; reference identity holds on both the copied and uncopied paths, down to the
`keyword_names` array; dedupe; idempotence across two resolves; sorted and unsorted ordering; both
maps composing on one unit; and a call-counting tripwire proving the complete path never calls the
function. Then a live pass resolving all 11 built chapters against the shipped `units.json` and
`faction_taxonomy.json`, asserting the 28 real records land for Dark Angels, appear in no other
chapter's pool, and are absent from the generic pool.

Negative-tested against a deliberately in-place-mutating version of the function: it fails on
chapter leakage, generic-pool contamination, the mutation snapshot, the reference-identity checks,
the source-order check, and the live Dark-Angels-to-Deathwatch leak.

Registered in `baseline.sh` (after `b101_check`) and in `pipeline_manifest.py`'s GUARDED list.
Baseline is **32/32 tier-A** with the new gate included.

**The render still needs your eyeball.** The keyword pills in the unit modal are the visible effect
of this change; I cannot see the DOM. Open a Dark Angels list, inspect a Terminator Squad or an
Outrider Squad, and confirm Deathwing / Ravenwing appears in the Keywords block — then check the
same unit in an Ultramarines list and confirm it does not.

## Files (SHA-256, first 12)

Verify these at S247 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `8cdb20e29b5a` | v6.24 — `applyChapterKeywordAdditions()` + union-path consumption |
| `b132_check.js` | `3e3567097875` | **net new** — B132 gate, synthetic + live-data |
| `baseline.sh` | `7a629865cc1d` | `b132_check` registered after `b101_check` |
| `pipeline_manifest.py` | `0438dfb952ef` | `b132_check.js` and `SESSION_HANDOFF_246.md` registered |
| `40K_Decision_Log.md` | `daa4bd80425b` | D343 appended |
| `DECISION_INDEX.md` | `73943fc05bad` | D343 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `2a89db421010` | B132 → Closed/Shipped; B133 opened; B130's 18/10 corrected to 19/9; 25 → 25 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_246.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `index.html`, `b132_check.js`,
  `baseline.sh`, `pipeline_manifest.py`, `pipeline_manifest.json`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_246.md`, `NEXT_SESSION_PROMPT.md`.
- **`b132_check.js` is net new** — it must be added, not just updated.
- **`pipeline_manifest.json` must be included.** S244 and S245 both got this right; keep it right.

## Decisions resolved this session

D343 — the copy-depth rule for keyword restoration, the dedupe and ordering behaviours, the gate
shape, the 19/9 correction, and the B133 re-scope. All technical; nothing here required Ryan's
input. The one thing waiting on Ryan is the render check above, which is verification, not a
decision.

## Backlog

25 open at S245 close; **25 open at S246 close**. Resolved B132; added B133.
