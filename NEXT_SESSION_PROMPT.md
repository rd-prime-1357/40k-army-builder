# NEXT SESSION PROMPT — Session 247

## Recommended pick: B133, teach `resolved_pool()` the per-chapter maps and retire B131's `EXEMPT` block. Tooling turn — needs a full `--fetch --data-turn` baseline (the zero-bearer gate is tier B).

B132 (S246) shipped the engine consumer, so the Dark Angels union pool now really does carry
Deathwing and Ravenwing. The zero-bearer gate still does not see it, because it does not run the
engine: it runs `rules_assertions.py`'s `Sources.resolved_pool()`, a Python mirror of
`resolveUnits()` that unions the generic and chapter blocks and applies **neither** per-chapter map.
B131's per-unit membership test reads each unit's own built keyword fields (D341), so the 6
Deathwing-family records still resolve to zero admits. **Deleting the exemptions without fixing the
mirror first fails the gate immediately** — this is the whole reason B133 exists rather than a
one-line follow-up.

Read `applyChapterKeywordAdditions()` in `index.html` before writing the Python side; the mirror has
to reproduce it, including the non-mutation rule. The mirror hands out the same dict objects across
pools exactly as the engine hands out the same JS objects, so building the pool for one chapter must
not alter the record another chapter's pool will read. Verify that directly rather than assuming a
shallow `dict()` copy is enough — `model_groups` is a list of dicts and the keyword list is inside
them.

The proof is the gate's own count moving **36 -> 30** with no other exemption disturbed: the 24
Vehicle (B128), 4 Marks of Chaos (B126), 1 Spawn and 1 Harlequins entries must all still resolve
exactly as they do now. B131's docstring paragraph describing the 6 records as exempt has to be
rewritten in the same pass, not left describing a state that no longer exists.

**Also in scope:** the same mirror has been missing `chapter_point_overrides` since B56d. Nothing
asserts on pool points today so no assertion is currently wrong, but the docstring claims a fidelity
the function does not have. Close it here rather than let a third session rediscover it.

## Also open, at your discretion — 25 tickets

B133, B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17. **Nothing is decision-blocked.**

- **B126** (Marks of Chaos) is a feature, not a fix — mark selection, list persistence, plus two
  unenforced D0 rules of its own (attachment and Transport must share a mark). The project now has
  **three** variants of "a unit's keywords depend on context": B128's detachment conferral, B132's
  per-chapter restoration, and whatever B126 invents. Read B128's re-scoped entry and B132's shipped
  mechanism before writing B126's, so the three do not end up with three different shapes.
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
  S246 was engine-only and ran tier A at 32/32 (the new `b132_check` included). **B133 is tier B —
  run the full `--fetch --data-turn`.**
- **A Python "mirror" of an engine function is a second implementation, and it drifts.** B133 exists
  because `resolved_pool()` fell behind `resolveUnits()` twice — B56d and B132 — and nobody noticed
  either time, because no assertion depended on the missing behaviour. When B133 lands, consider
  whether anything pins the two together, the way B94-1 pins `copy_tier_pts`.
- **Do not trust a scope document's or a handoff's population figure — re-derive it.** S246 makes
  the third case in four sessions: S245's headline said 18/10, the data is 19/9 (total 28 unaffected);
  S245 itself found 28 where the scope doc said 6. Re-derive every time, and check against a second
  source.
- **An assertion phrased as "X should be absent" is usually wrong.** B132's first draft asserted no
  Deathwing anywhere in the generic pool and failed on live data — generic units carry it natively.
  The real rule was "resolution changes nothing here", i.e. a snapshot comparison.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check (D337).** Verify the actual pushed file's hash against the
  handoff table at session open, and confirm `pipeline_manifest.json` itself is among what landed.
  S244, S245 and S246 all got this right; S243 did not.
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

- **Push S246's changed files** to the public repo: `index.html`, `b132_check.js`, `baseline.sh`,
  `pipeline_manifest.py`, `pipeline_manifest.json`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_246.md`, `NEXT_SESSION_PROMPT.md`.
- `b132_check.js` is **net new** — it must be added, not just updated.
- **Eyeball the render.** Open a Dark Angels list, inspect Terminator Squad and Outrider Squad, and
  confirm Deathwing / Ravenwing appear in the Keywords block; then confirm the same units in an
  Ultramarines list do not show them. This is the visible half of B132 and Claude cannot see the DOM.

## Decisions waiting on Ryan

**Resolved at S246, listed so they are not re-asked:** none new needing Ryan. D343 (copy depth,
dedupe and ordering, gate shape, the 19/9 correction, the B133 re-scope) was technical throughout.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is a production dependency** even though it
  is not in the priority order, and belongs on a release plan rather than being rediscovered later.
- **Grey Knights detachments** were never built despite its units being complete — still outstanding.

## Close

Produce the four documents, register `SESSION_HANDOFF_247.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
