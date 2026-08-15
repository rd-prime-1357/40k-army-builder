# NEXT SESSION PROMPT — Session 243

## Recommended pick: B125, chapter-keyword census across all twelve chapters. Scoping-only, analysis-grade — flag before starting.

Unchanged from S241's plan; B123 (built S242) did not touch this. Still the right next scoping
turn regardless of S241's Deathwing finding (D338) — that finding was about whether 6 specific
enhancement records are zero-admit, not about whether chapter keywords are correctly modelled
generally. B125's own census should determine the actual scope independently; do not assume D338
narrows or closes it.

**Read D338 first.** S241 found the 6 Deathwing enhancement records are NOT zero-admit under a
direct `Datasheets_keywords.csv` read (`S.all_keywords()`), contradicting `B93_SCOPE.md` §4.2.
Two live possibilities, and B125's scoping turn should settle which:
- The engine's actual bearer-assignment logic reads a different, pipeline-derived per-unit
  keyword field (candidate: `model_groups[*].faction_keyword_names`, referenced in
  `b113_bearer_table_matches_source`) that IS stripped for chapter-specific keywords, in which
  case the original B93 census was right about the *live* behaviour and D338's gate is checking
  the wrong representation — B129's gate would need a follow-up fix to read the same field the
  engine does.
- Or the original gap was narrower than `B93_SCOPE.md` stated and B125's scope is smaller than
  the "8 units vs 27 the source would give" table implied.

Either way, census which representation `resolveUnits()`/the enhancement-assignment path in
`index.html` actually consults, not just what `Datasheets_keywords.csv` says in isolation — that
distinction is exactly what S241's two methodologies diverged on.

## Also open, at your discretion — 25 tickets

B125, B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86,
B69, B70, B75, P2, P4, E23, B67b, E12, B17. **Nothing is decision-blocked.**

- **B128** (muster-time detachment keyword conferral) — **re-scoped smaller by D339.**
  `detachment_effects.json` already models 7 `battleline` effects (`enforced: true`, live) and
  Headhunter Task Force's `tank_ace` (scoped since D273/S182). Read that file's `_meta` before
  re-censusing `rule_text` — most of the scoping work for the automatic conferrals is very likely
  already done; the genuine remaining gap is Headhunter's player-choice-with-a-cap mechanism.
- **B126** (Marks of Chaos) is a feature, not a fix — mark selection, list persistence, plus two
  unenforced D0 rules of its own (attachment and Transport must share a mark). Same shape as B128:
  a muster-time selection that changes a unit's keywords. Worth reading B128's re-scoped entry
  before writing B126's, so the two do not invent different mechanisms for the same problem.
- **B127** (74 records with no rule text in any held source) needs nothing from Claude until
  source exists — a Ryan-side acquisition item.
- **B120** still needs its own scoping turn before build; per S238's note, widen its census from
  Set D *weapons* to Set D effects generally so **B124** lands inside it.
- **B122** needs a scoping turn answering a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all, or only shorthand summaries (distinct from
  B127's 74 records, which have none at all)?

## Standing reminders

- The last full `--fetch --data-turn` was **S240**, clean at 36/36. S241 and S242 were tooling/
  engine turns and ran with only what each needed loaded — neither is a full data-turn baseline.
  Run a full `--fetch --data-turn` at the next data session.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check going forward (D337).** Before trusting a handoff's
  Files table at session open, verify the actual pushed file's hash against the table, not just
  that the file exists. S242 verified clean at open — the discipline is working, keep it up.
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules. Both
  are documented in `40K_Data_Dictionary.md`'s S241 addendum.
- **An impossible result means widen the read, never explain the result.** No inference about what
  GW must have intended while any field is still unread (D334/D336).
- **Field-coverage convention is written into `40K_Data_Dictionary.md`'s front matter (S241).**
  State every field on a record type and mark read/not-read, with a reason for each not-read,
  before censusing that file for a legality question.
- Turn typing stays strict. B125 is a scoping turn; do not fold a mechanism build into it even if
  the population turns out small.
- **B123's precedence mechanism (D335) has no known live collision case yet.** If a future census
  (B120, B122, or a new faction build) turns up a record where wargear and an Enhancement really
  do compete for the same SV/FNP/W cell, `enh.condAbs` and the comparator (`B123_BETTER`) are
  already built and tested — extend the curated table, don't re-derive the mechanism.

## Ryan action required

- **Push S242's changed files** to the public repo: `index.html`, `b123_check.js`,
  `b119_check.js`, `baseline.sh`, `pipeline_manifest.py`, `40K_Decision_Log.md`,
  `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_242.md`, `NEXT_SESSION_PROMPT.md`. Given D337, please
  verify `pipeline_manifest.py` specifically lands as edited.

## Decisions waiting on Ryan

**Resolved at S242, listed so they are not re-asked:** none new — B123 was decided at D335 (S240)
and built exactly as scoped this session.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is now a production dependency** even
  though it is not in the priority order, and belongs on a release plan rather than being
  rediscovered later.

## Close

Produce the four documents, register `SESSION_HANDOFF_243.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
