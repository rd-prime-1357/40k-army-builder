# NEXT SESSION PROMPT — Session 246

## Recommended pick: B132, consume `chapter_keyword_additions` in `resolveUnits`. Engine turn — a plain `--fetch` baseline is enough (no sources needed).

B130 (S245) shipped the data half: 28 generic Adeptus Astartes units in `units.json` now carry
`chapter_keyword_additions`, a per-army map of the form `{"Dark Angels": ["Deathwing"]}`. **Nothing
reads it yet.** B132 is the engine half and finishes the fix.

This is the direct analogue of **B56d**. Read `applyChapterPointOverrides()` in `index.html` before
writing anything — same problem, same solution shape, and the comment above it already states the
one thing that must not go wrong: **never mutate the shared generic unit object.** It is the same
object reference across every chapter's resolved set, so an in-place keyword push would leak
Deathwing into Ultramarines. Return a fresh object only where an addition actually applies.

The keywords are all-models on every one of the 28 records (verified at D342), so they go onto every
model group's `keyword_names` and no per-model-group carve-out is needed. Ordering against the
point-override step does not matter — the two touch disjoint fields — but keep the new step beside
it rather than scattering a second per-army transform elsewhere in the file.

Needs its own gate, on the `b90_check.js` model: a synthetic fixture proving (a) the keywords land
for the owning chapter, (b) they do **not** land in any other chapter's resolved pool, and (c) the
generic Space Marines pool is unchanged. (b) is the one that matters.

**After B132 ships, B131's `EXEMPT` block in the zero-bearer gate goes stale** — the 6
Deathwing-family enhancement records gain real eligible bearers — and must be removed in a separate
tooling pass. That follow-up is gated on B132, **not** on B130; S244's note said B130 and is now
superseded.

## Also open, at your discretion — 25 tickets

B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75,
P2, P4, E23, B67b, E12, B17, B132. **Nothing is decision-blocked.**

- **B126** (Marks of Chaos) is a feature, not a fix — mark selection, list persistence, plus two
  unenforced D0 rules of its own (attachment and Transport must share a mark). Same shape as B128:
  a muster-time selection that changes a unit's keywords. Worth reading B128's re-scoped entry
  before writing B126's, so the two do not invent different mechanisms for the same problem. Note
  that B132 will have just built a third variant of "a unit's keywords depend on context" — read it
  too before designing either.
- **B127** (74 records with no rule text in any held source) needs nothing from Claude until source
  exists — a Ryan-side acquisition item.
- **B120** still needs its own scoping turn before build; per S238's note, widen its census from
  Set D *weapons* to Set D effects generally so **B124** lands inside it.
- **B122** needs a scoping turn answering a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all, or only shorthand summaries (distinct from
  B127's 74 records, which have none at all)?
- **B128** (muster-time detachment keyword conferral) — re-scoped smaller by D339 (S241).
  `detachment_effects.json` already models 7 `battleline` effects (`enforced: true`, live) and
  Headhunter Task Force's `tank_ace`. Read that file's `_meta` before re-censusing `rule_text`; the
  genuine remaining gap is Headhunter's player-choice-with-a-cap mechanism.

## Standing reminders

- The last full `--fetch --data-turn` was **S245**, clean at 37/37 with 85 source files verified.
  B132 is engine-only and does not need sources.
- **Do not trust a scope document's population figure — re-derive it.** S245 is the second case in
  three sessions where a prior session's count was correct only for what it was counting.
  `B93_SCOPE.md` §12 said 6; the real defect was 28, because §12 counted only the Characters B93
  needed. The prompt explicitly said this "should not need a re-derivation from source." It did.
  Re-derive anyway, every time, and check the derivation against a second source before building on
  it — the raw Wahapedia export alone would have been enough to get 28, but only the composition
  files confirm 28 is *right*.
- **A ticket sized as one turn can turn out to need two turn types.** B130 needed a data emitter and
  an engine consumer. Split it rather than mixing; the project already had the precedent in
  B56c/B56d. Check for a per-army mechanism precedent before inventing one.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check (D337).** Verify the actual pushed file's hash against the
  handoff table at session open, and confirm `pipeline_manifest.json` itself is among what landed.
  S244 and S245 both got this right; S243 did not.
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules.
- **An impossible result means widen the read, never explain the result** (D334/D336/D341).
- **Field-coverage convention is in `40K_Data_Dictionary.md`'s front matter (S241).** State every
  field on a record type and mark read/not-read, with a reason for each not-read, before censusing.
- **B123's precedence mechanism (D335) has no known live collision case yet.** If a future census
  turns one up, `enh.condAbs` and `B123_BETTER` are already built — extend the curated table.

## Ryan action required

- **Push S245's changed files** to the public repo: `add_chapter_keyword_additions.py`,
  `units.json`, `units_repro_check.py`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_245.md`,
  `NEXT_SESSION_PROMPT.md`.
- `add_chapter_keyword_additions.py` is **net new** — it must be added, not just updated.

## Decisions waiting on Ryan

**Resolved at S245, listed so they are not re-asked:** none new needing Ryan. D342 (population
28-not-6, the per-army map shape, the B130/B132 split, no new assertion) was technical and scoping,
not product.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is a production dependency** even though it
  is not in the priority order, and belongs on a release plan rather than being rediscovered later.
- **Grey Knights detachments** were never built despite its units being complete — still outstanding.

## Close

Produce the four documents, register `SESSION_HANDOFF_246.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
