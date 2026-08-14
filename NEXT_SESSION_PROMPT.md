# NEXT SESSION PROMPT — Session 239

## Recommended pick: B119's tooling half. Tooling-only.

B119's engine half shipped at S238 (D332); the ticket does not close until the census assertion
lands. Same shape as `B99-CENSUS` (D331) and for the same reason: without a source → table check,
the curated `ENHANCEMENT_BEARER_STATS` rots silently the moment a later faction lands an
enhancement with an unhandled shape. `b119_check.js` already covers table → source.

**Do not re-derive the method from scratch.** `b99_source_census_matches_curated_table` in
`rules_assertions.py` already has the clause splitter, the conditional-marker vocabulary and the
bearer-possessive regex, all tested against real source text at S237. What B119's version needs
on top of it:

- A **statline** characteristic vocabulary (Toughness / Wounds / Objective Control / Save /
  Leadership / Movement) instead of the weapon one, paired with an add/improve verb.
- The bearer-self regex must exclude the possessive form: `\bthe bearer\b(?!'?s\s+unit)` —
  a bare `\bthe bearer\b` wrongly matches "models in **the bearer**'s unit" and pulls Set D
  records in as false positives. Found at S238 by testing against the real 10, exactly the way
  S237 found its two.
- Pin **10 records / 6 names / 8 armies** and fail on any candidate with no
  `ENHANCEMENT_BEARER_STATS` row.
- Negative-test it: remove one row from the curated table and confirm the assertion fails naming
  exactly that record. A census that passes by construction is worth nothing.

**Worth folding in, and cheap:** the same assertion can also pin **B123's** 25-record absolute /
Feel No Pain population as a *known and deliberately unhandled* set, rather than letting those
records read as ordinary non-matches. That is the same treatment `B99-CENSUS` gives Chaos
Daemons' 29 shorthand records, and it keeps the gap visible instead of silent.

## Ryan action required

- **Push S238's changed files** to the public repo. `repo_check` is red at S238 close for
  `index.html`, `baseline.sh`, `pipeline_manifest.py`, `b119_check.js`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md` and `SESSION_HANDOFF_238.md` — expected for
  unpushed work, not a regression. Reconcile at open.
- **Eyeball the B119 render.** I cannot see the DOM. One bearer of *Rites of War* (OC highlighted,
  "Modified by Rites of War" beneath the table) and one *Ravenwing Command Squad* (OC asterisked,
  printed value kept, "* bearer only — Rites of War").

## Open, at your discretion

23 open: B116 (decision-blocked), B119 (tooling half), B120, B122, B123 (decision-blocked), B124,
B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.

- **B93 deserves a look ahead of more display work.** S238 read all ten Set C descriptions in full
  and every one of the six names carries a bearer restriction in its own text ("World Eaters
  Monster model only", "Haemonculus model only", "Chaos Lord model only", "Adeptus Astartes
  Terminator model only"). None is enforced — B113's table was scoped to enhancements carrying a
  `LEADER:` line. So the "model only" form is the norm rather than the exception, and B119 will
  now render a modified statline on a bearer the rules do not allow. That is a live D0 gap and the
  display work keeps making it more visible. It needs an analysis turn across all 739 records
  before a mechanism is chosen; that turn is the sensible next big item after B119 closes.
- **B120** still needs its own scoping turn before build, and that turn should now widen its
  census from Set D *weapons* to Set D effects generally, so **B124** (*Master Artisan*'s
  unit-wide Toughness half) lands inside it rather than staying orphaned.
- **B122** needs a scoping turn that answers a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all? If yes it is a `detachment_parser.py` bug;
  if no it is a source-acquisition item.
- **B123** is blocked on Ryan's display-precedence call and should not be started before it.

## Standing reminders

- Keep running a data-turn baseline periodically even on non-data sessions. S238 was `--fetch`
  only; the last full `--fetch --data-turn` was S237.
- `40K_Decision_Log.md` has now been absent from the project-area mount for **six** sessions
  running and is recovered from the repo each time. Not a signal of anything wrong on its own.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- The project-area file mount silently strips apostrophes from filenames on upload. Before
  trusting a project-area filename as the real repo filename, especially for anything going into
  GUARDED, check a fresh clone.
- Turn typing stays strict. B119's two halves were split for exactly this reason; do not fold the
  census assertion into an engine session.

## Decisions waiting on Ryan

- **B123 display precedence — new, and it blocks 25 records.** When an Enhancement and equipped
  wargear both set the same statline cell (Save, Feel No Pain), does the app show the better
  value, the Enhancement's value, or an asterisk? Recommendation: the better of the two, cell
  marked.
- **B99 display, four decisions** — unchanged since S236, all still reversible. B119 followed the
  same idiom, so a change of mind now moves both.
- **B116** — unchanged. `DRUKHARI_BUILD_SCOPE.md` §6. Blocks nothing.
- **Next faction after Drukhari** — the documented priority order is fully built; none is queued.
  Recommendation stands: clear the engine backlog first.

## Close

Produce the four documents, register `SESSION_HANDOFF_239.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
