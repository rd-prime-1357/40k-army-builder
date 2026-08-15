# NEXT SESSION PROMPT — Session 242

## Recommended pick: B123, statline precedence build. Engine-only, mechanical.
## Flag before starting: mechanical — the rule is decided (D335), the fields are documented (S241).

Decided at D335 — show the best **unconditional** value; if a conditional value would be better,
show the unconditional one and mark the cell. 25 records / 11 names / 11 armies, re-derive at
build time rather than pinning these from this prompt. `enhModLegend` is already shared between
the weapon and stat tables and `statOverrideFromText` already writes the wargear side of these
cells; what is new is the precedence rule and the absolute-value path B119 deliberately left
unstubbed. Ship a `b123_check.js` pinning: an Enhancement absolute beating an unconditional
wargear value; an unconditional wargear value beating a conditional Enhancement one (unconditional
shown, cell marked); a Feel No Pain grant where no wargear speaks to the cell; and the legend
wording agreeing with B99's and B119's.

`40K_Data_Dictionary.md` now documents `detachments.json`'s enhancement `description` field and
flags it as rules-bearing — read that section before writing the census this build needs, rather
than re-deriving field coverage from scratch.

## Then: B125, chapter-keyword census across all twelve chapters. Scoping-only, analysis-grade — flag before starting.

Still the right next scoping turn regardless of S241's Deathwing finding (D338) — that finding was
about whether 6 specific enhancement records are zero-admit, not about whether chapter keywords are
correctly modelled generally. B125's own census should determine the actual scope independently;
do not assume D338 narrows or closes it.

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
distinction is exactly what this session's two methodologies diverged on.

## Also open, at your discretion — 26 tickets

B125, B126, B127, B128, B116, B120, B122, B123, B124, B97, B103, E28, B93, B90, B94, B85, B86,
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

- The last full `--fetch --data-turn` was **S240**, clean at 36/36. S241 was tooling-only and ran
  with only `Datasheets.csv`/`Datasheets_keywords.csv` loaded (sufficient for the B129 gate, not a
  full data-turn baseline). Run a full `--fetch --data-turn` at the next data or engine session.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check going forward (D337).** S240's handoff claimed
  `pipeline_manifest.py` was registered correctly and the pushed copy did not match. Before
  trusting a handoff's Files table at session open, verify the actual pushed file's hash against
  the table, not just that the file exists.
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules. Both
  are now documented in `40K_Data_Dictionary.md`'s S241 addendum.
- **An impossible result means widen the read, never explain the result.** No inference about what
  GW must have intended while any field is still unread (D334/D336).
- **Field-coverage convention is now written into `40K_Data_Dictionary.md`'s front matter (S241).**
  State every field on a record type and mark read/not-read, with a reason for each not-read,
  before censusing that file for a legality question.
- Turn typing stays strict. B125 is a scoping turn; do not fold a mechanism build into it even if
  the population turns out small.

## Ryan action required

- **Push S241's changed files** to the public repo: `40K_Data_Dictionary.md`, `rules_assertions.py`,
  `pipeline_manifest.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
  `SESSION_HANDOFF_241.md`, `NEXT_SESSION_PROMPT.md`. Given D337, please verify
  `pipeline_manifest.py` specifically lands as edited.

## Decisions waiting on Ryan

**Resolved at S241, listed so they are not re-asked:** D337 (manifest reconciliation, mechanical
fix, no product call); D338 (B129 gate built, exemption population re-derived to 30); D339 (B128
re-scoped smaller, not re-decided — still needs its own scoping turn).

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is now a production dependency** even
  though it is not in the priority order, and belongs on a release plan rather than being
  rediscovered later.

## Close

Produce the four documents, register `SESSION_HANDOFF_242.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
