# NEXT SESSION PROMPT — Session 241

## Recommended pick: B129, documentation and census-coverage tooling. Tooling-only.
## Flag before starting: mechanical throughout — describing fields that exist and writing one gate.

This is the fix for D334, and D336 explains why it is a documentation problem rather than a
carefulness problem. `40K_Data_Dictionary.md` stops at Session 19 addenda and **has no entry for
`detachments.json` at all** — 211 records, nine fields each, undocumented. The B93 census read
`description` and `restrictions` and never read `rule_text`, where Headhunter Task Force states
that up to three Vehicles gain CHARACTER at muster. Wrong legality decision, survived a session.

Three parts, one turn:

1. **Document the undocumented outputs, field by field.** `detachments.json` first — every field on
   a detachment record and on an enhancement record. Then `detachment_effects.json`,
   `datasheet_wargear_abilities.json`, `wargear_points.json`, and anything else that has grown
   without an entry. Check the actual JSON for fields rather than working from the parser, since
   the parser is what would have carried the omission forward. For each field: what it carries, and
   a flag for **free text that can contain rules**. That flag is the whole point — `rule_text` and
   `restrictions` both carry rules, and a census reading one but not the other is then visibly
   wrong instead of invisibly wrong.
2. **Field-coverage convention.** Write it into the data dictionary's front matter: a census states
   every field on the record type and marks each read or not-read, with a reason for each
   not-read. Ten mechanical lines at the head of the work, no judgment involved.
3. **The gate.** A `rules_assertions.py` assertion failing when any enhancement resolves to no
   eligible bearer without a named, commented exemption. Today's exemption list is the 24 Vehicle
   (B128), 6 Deathwing (B125) and 4 Marks (B126) records — re-derive that set rather than pinning
   these numbers from this prompt. Negative-test it: remove one exemption and confirm the assertion
   names that record.

Do not fold B123 in. Do not touch `index.html`.

## Then: B123, statline precedence build. Engine-only, mechanical.

Decided at D335 — show the best **unconditional** value; if a conditional value would be better,
show the unconditional one and mark the cell. 25 records / 11 names / 11 armies, re-derived at build
time. `enhModLegend` is already shared between the weapon and stat tables and
`statOverrideFromText` already writes the wargear side of these cells; what is new is the
precedence rule and the absolute-value path B119 deliberately left unstubbed. Ship a
`b123_check.js` pinning: an Enhancement absolute beating an unconditional wargear value; an
unconditional wargear value beating a conditional Enhancement one (unconditional shown, cell
marked); a Feel No Pain grant where no wargear speaks to the cell; and the legend wording agreeing
with B99's and B119's.

## Then: B125, chapter-keyword census across all twelve chapters. Scoping-only, analysis-grade — flag before starting.

## Other open, at your discretion

27 open: B125, B126, B127, B128, B129, B116, B120, B122, B123, B124, B97, B103, E28, B93, B90,
B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17. **Nothing is decision-blocked any
more.**

- **B128** (muster-time detachment keyword conferral) is new and is the prerequisite for B93's 24
  Vehicle records specifically. 28 detachments confer keywords, 35 conferrals; only Headhunter Task
  Force's is a capped player choice (up to three Tank Ace units gain CHARACTER, one may be
  Warlord), and that one is legality-critical. Its scoping turn should also check whether any rule
  *removes* a keyword — the census only looked for grants.

- **B126** (Marks of Chaos) is a feature, not a fix — mark selection, list persistence, plus two
  unenforced D0 rules of its own (attachment and Transport must share a mark). It needs its own
  scoping turn and does not block B125. Note it is the same *shape* as B128: a muster-time
  selection that changes a unit's keywords. Worth scoping them close together, or at least reading
  B128's scope before writing B126's, so the two do not invent different mechanisms for the same
  problem.
- **B127** (74 records with no rule text in any held source) needs nothing from Claude until source
  exists. It is a Ryan-side acquisition item, listed here so it is not forgotten.
- **B120** still needs its own scoping turn before build, and per S238's note that turn should widen
  its census from Set D *weapons* to Set D effects generally so **B124** lands inside it.
- **B122** needs a scoping turn that answers a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all? Note this is now clearly distinct from B127 —
  B122's 24 records have text of a kind (shorthand summaries), B127's 74 have none.

## Standing reminders

- The last full `--fetch --data-turn` was **this session (S240)** and it was clean at 36/36. Keep
  running one periodically even on non-data sessions.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push access
  — verify with a real write attempt.
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Census hygiene, learned twice now.** Split description sentences on `[.?!]`, not `.` — the first
  pass of S240's census lost *Unravelled Fates* and reported 640 instead of 641. And when a count
  comes out wrong, re-derive it; do not patch the number.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules.
- **An impossible result means widen the read, never explain the result.** No inference about what
  GW must have intended while any field is still unread. This is the D334 lesson and it generalises
  past detachments (D336).
- Turn typing stays strict. B125 is a scoping turn; do not fold a mechanism build into it even if
  the population turns out small.

## Ryan action required

- **Add two lines to the project instructions**, so they are read at the top of every session
  rather than living only in the decision log:
  - "An impossible result — an enhancement no model can take, a unit no rule permits — means a
    source field has not been read. Widen the read. Never explain an impossible result by inference
    about what GW must have intended."
  - "Before censusing a data file, state every field on the record type and mark each one read or
    not-read, with a reason for each not-read."
- **Push S240's changed files** to the public repo: `B93_SCOPE.md`, `pipeline_manifest.py`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_240.md`,
  `NEXT_SESSION_PROMPT.md`. `repo_check` is red at S240 close for these — expected, not a
  regression. S238's and S239's sets are now both landed.

## Decisions waiting on Ryan

**Resolved at S240, listed so they are not re-asked:** D334 reversed by D335 (the clause narrows);
B123 decided (best unconditional value, mark the cell when a conditional one is better); B99's four
display decisions found to have shipped at D330/D332 and closed — they had been carried forward as
open in error since S236; B116 reclassified as required before production.

- **Next faction after Drukhari** — the documented priority order is fully built and none is queued.
  Recommendation stands: clear the engine backlog first. But B116's reclassification means
  **Aeldari is now a production dependency** even though it is not in the priority order, and that
  belongs on a release plan rather than being rediscovered later.

## Close

Produce the four documents, register `SESSION_HANDOFF_241.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
