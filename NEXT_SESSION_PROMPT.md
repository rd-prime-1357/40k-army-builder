# NEXT SESSION PROMPT — Session 248

## Recommended pick: B128, Headhunter Task Force's capped Tank Ace selection. Data + engine turn — needs a full `--fetch --data-turn` baseline (this touches `detachment_effects.json` and its consumer).

B133 (S247) closed the B125/B130/B131/B132 arc. The next open D0 gap is B128: Headhunter Task Force
lets the player select **up to three** Character-eligible Tank Ace units, one of which may be
Warlord — a hard cap that must be a real, capped, persisted list-building step, not a derived flag,
or a list with four Character Tank Aces is reachable and illegal.

**Do not re-census from zero.** D339 (S241) already found most of this scoped: `detachment_effects.json`
carries 7 `battleline` effects (`enforced: true`, live in the engine) and Headhunter's own `tank_ace`
effect, pool/cap/source-cited back at D273 (S182). Start from that file's `_meta` and the existing
`tank_ace` effect record, confirm what `enforced: false` currently means for it in the engine, and
scope the selection UI/persistence from there — the pool and cap are not the open question, the
selection mechanism is.

**Sequencing reason this comes before B126.** B126 (Marks of Chaos) is the third feature in the
project needing "a unit's keywords/eligibility depend on context" (after B128's detachment
conferral and B132's per-chapter restoration). Read B128's shipped shape before scoping B126's, so
the project doesn't end up with three different mechanisms for the same kind of problem.

Also worth checking during B128's build, per the ticket's own note: whether any detachment
conferral runs the other way — removing a keyword rather than granting one — since the original
census only looked for grants.

## Also open, at your discretion — 24 tickets

B126, B127, B120, B116, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17. **Nothing is decision-blocked.**

- **B127** (74 records with no rule text in any held source) needs nothing from Claude until source
  exists — a Ryan-side acquisition item.
- **B120** still needs its own scoping turn before build; per S238's note, widen its census from
  Set D *weapons* to Set D effects generally so **B124** lands inside it.
- **B122** needs a scoping turn answering a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all, or only shorthand summaries (distinct from
  B127's 74 records, which have none at all)?

## Standing reminders

- The last full `--fetch --data-turn` was **S247**, clean at 38/38 with 85 source files verified.
  **B128 is data + engine — run the full `--fetch --data-turn` again**, don't assume S247's fetch
  is still fresh.
- **A Python "mirror" of an engine function is a second implementation, and it drifts.** B133
  closed the arc where `resolved_pool()` fell behind `resolveUnits()` twice (B56d, B132) with
  nobody noticing either time, because no assertion depended on the missing behaviour. If B128
  adds another engine-side concept that a Python assertion needs to reason about, consider whether
  it needs its own mirror or can read `detachment_effects.json` directly instead of duplicating
  engine logic.
- **Do not trust a scope document's or a handoff's population figure — re-derive it.** Three cases
  in five sessions now: S245's headline said 18/10, the data is 19/9; S245 itself found 28 where
  the scope doc said 6; B93's original census undercounted before the vocabulary-derivation fix.
  Re-derive every time, and check against a second source.
- **An assertion phrased as "X should be absent" is usually wrong.** B132's first draft asserted no
  Deathwing anywhere in the generic pool and failed on live data — generic units carry it natively.
  The real rule was "resolution changes nothing here", i.e. a snapshot comparison. Keep this in
  mind if B128 needs a similar "nothing else changed" gate for the Tank Ace selection.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check (D337).** Verify the actual pushed file's hash against
  the handoff table at session open, and confirm `pipeline_manifest.json` itself is among what
  landed. S244 through S247 all got this right; S243 did not.
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
- **Non-mutation on shared cached/JS objects is not optional.** B132 and B133 both required copying
  nested structures, not just the top-level dict/object, because the same object reference is
  handed to every pool/view built from a shared cache. Any future per-chapter or per-detachment
  transform touching nested fields needs the same discipline — check reference identity directly,
  don't assume a shallow copy is enough.

## Ryan action required

- **Push S247's changed files** to the public repo: `rules_assertions.py`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `SESSION_HANDOFF_247.md`, `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- No render check needed — S247 was tooling-only.

## Decisions waiting on Ryan

**Resolved at S247, listed so they are not re-asked:** none new needing Ryan. D344 (mirror
copy-depth, population gating, docstring rewrites) was technical throughout.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is a production dependency** even though
  it is not in the priority order, and belongs on a release plan rather than being rediscovered
  later.
- **Grey Knights detachments** were never built despite its units being complete — still
  outstanding.

## Close

Produce the four documents, register `SESSION_HANDOFF_248.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
