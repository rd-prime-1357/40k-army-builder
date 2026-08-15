# NEXT SESSION PROMPT — Session 241

## Recommended pick: B123, statline precedence build. Engine-only.
## Flag before starting: mechanical — the decision is made, the population is pinned, the render idiom already exists.

B123 was decision-blocked until S240 and is now the cheapest buildable item in the backlog. Ryan's
call (D335): **show the best unconditional value; if a conditional value would be better, show the
unconditional one and mark the cell.** 25 records / 11 names / 11 armies, re-derive from
`detachments.json` at build time rather than trusting that figure.

The render idiom exists — `enhModLegend` is already shared between the weapon table and the stat
table, and `statOverrideFromText` already writes the wargear side of these cells. What is new is
the precedence rule where both speak to the same cell, plus the absolute-value path B119
deliberately did not stub. Ship a `b123_check.js` pinning: an Enhancement absolute beating an
unconditional wargear value, an unconditional wargear value beating a conditional Enhancement one
(unconditional shown, cell marked), a Feel No Pain grant where no wargear speaks to the cell, and
the legend wording agreeing with B99's and B119's.

Do **not** fold B124 in. Do **not** fold in B93 work of any kind.

## Then: B125, chapter-keyword census across all twelve Adeptus Astartes chapters. Scoping-only, analysis-grade — flag before starting.

B93's census (D334, `B93_SCOPE.md`) found that chapter-specific keywords are stripped from the
generic `Adeptus Astartes` block and never re-added by the delta-shaped chapter blocks, so the union
roster serves stripped records. Dark Angels' `Deathwing model only` enhancements resolve to **zero**
eligible Characters as a result. Measured over the Dark Angels union pool: Deathwing 8 units held
against 27 the source would give (5 Characters lost); Ravenwing 7 against 16 (1 Character lost).

This is a prerequisite. **B93 cannot be built before it is at least scoped** — enforcing bearer
restrictions on today's roster data would refuse legal Dark Angels lists, which is worse than the
current over-admission.

**Do not carry the Dark Angels numbers forward as the population.** They are one chapter, found
incidentally. Census across all twelve chapters: for each, compare the keyword set the chapter's
union pool actually carries against what `Datasheets_keywords.csv` gives the same datasheet, and
report which keywords are lost and which units lose them. Then answer the design question, which is
the reason this is analysis-grade: the stripping is *correct* for the generic block, so the fix is
either (a) chapter blocks re-add their own keywords to the generic datasheets they inherit, or (b)
the union resolver applies a chapter-keyword overlay at selection time. Both interact with B90's
pending `union` to `complete` roster-mode flip, so B90's state has to be established first rather
than assumed. Produce `B125_SCOPE.md` with the population, the two mechanisms compared, and a
recommendation — **do not build this session.**

## Other open, at your discretion

26 open: B125, B126, B127, B128, B116, B120, B122, B123, B124, B97, B103, E28, B93, B90, B94, B85,
B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17. **Nothing is decision-blocked any more.**

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
- **Read `rule_text`, not just `restrictions`.** D334 was wrong for one session because the B93
  census read enhancement descriptions and the `restrictions` field (null for the detachment in
  question) and never read `rule_text`, where Headhunter Task Force states plainly that up to three
  Vehicles become Characters at muster. Any question about what a detachment permits must read
  `rule_text` — `restrictions` is a partial extraction of it, not a substitute.
- Turn typing stays strict. B125 is a scoping turn; do not fold a mechanism build into it even if
  the population turns out small.

## Ryan action required

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
