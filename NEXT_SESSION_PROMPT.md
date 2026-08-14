# NEXT SESSION PROMPT — Session 240

## Recommended pick: B93, full census across all 739 enhancement records. Scoping-only.
## Flag before starting: this is an analysis turn (rules-legality census), not mechanical — switch models before work begins.

B119's closing session confirmed what S238 already found: all six B119 names carry an unenforced
"X model only" bearer restriction in their own text, and B119 will now render a modified statline
on a bearer the rules don't allow. That's a live D0 gap, and every display session since (B99,
B119) has made it more visible without touching it. S238's own recommendation stands: this needs
an analysis turn across all 739 enhancement records before any mechanism is chosen — B113's table
was scoped to enhancements carrying a `LEADER:` line, and the "model only" restriction form looks
like the norm rather than the exception, so the real population is probably much larger than the
six names found so far as a side effect of other work.

**Do not carry forward a number from this session or S238 — census it properly.** The six known
instances are a floor, found incidentally, not a real count. Read every enhancement description in
`detachments.json` for a bearer-restriction clause (the "ADEPTUS ASTARTES TERMINATOR model only"
pattern sits at the *start* of the description, before any effect text, which is a different shape
from the mid-clause conditional markers B99-CENSUS and B119-CENSUS already parse — this is a new
regex, not a reuse). Cross-reference against `ENHANCEMENT_BEARER_RESTRICTIONS` to find the real
gap size. Produce a scope document (`B93_SCOPE.md`) with the population, the restriction-text
vocabulary found, and a recommended mechanism — do not build this session.

## Other open, at your discretion

22 open: B116 (decision-blocked), B120, B122, B123 (decision-blocked), B124, B97, B103, E28, B93,
B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.

- **B120** still needs its own scoping turn before build, and per S238's note that turn should
  widen its census from Set D *weapons* to Set D effects generally, so **B124** (*Master
  Artisan*'s unit-wide Toughness half) lands inside it rather than staying orphaned. If B93's
  census runs long, this is the fallback pick — also scoping-only, also analysis-grade.
- **B122** needs a scoping turn that answers a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all? If yes it's a `detachment_parser.py` bug; if
  no it's a source-acquisition item.
- **B123** is blocked on Ryan's display-precedence call (see below) and should not be started
  before it.

## Standing reminders

- Keep running a data-turn baseline periodically even on non-data sessions. The last full
  `--fetch --data-turn` was S237; this session was `--fetch` only, same as S238.
- `40K_Decision_Log.md` was absent from the project-area mount again this session (seventh
  session running) and recovered from the repo. Not a signal of anything wrong on its own.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- The project-area file mount silently strips apostrophes from filenames on upload. Before
  trusting a project-area filename as the real repo filename, especially for anything going into
  GUARDED, check a fresh clone.
- Turn typing stays strict. B93's census is a scoping turn; do not fold a mechanism build into it
  even if the population turns out small.

## Ryan action required

- **Push S238 and S239's changed files** to the public repo. `repo_check` is red at S239 close for
  `rules_assertions.py`, `pipeline_manifest.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_239.md`, plus S238's still-unpushed set
  (`index.html`, `baseline.sh`, `pipeline_manifest.py`, `b119_check.js`, and the same four rolling
  docs) — expected for unpushed work across two sessions now, not a regression. Reconcile both at
  once at open.

## Decisions waiting on Ryan

- **B123 display precedence — unchanged, still blocks a build.** When an Enhancement and equipped
  wargear both set the same statline cell (Save, Feel No Pain), does the app show the better
  value, the Enhancement's value, or an asterisk? Recommendation: the better of the two, cell
  marked. 25 records wait on it.
- **B99 display, four decisions** — unchanged since S236, all still reversible.
- **B116** — unchanged. `DRUKHARI_BUILD_SCOPE.md` §6. Blocks nothing.
- **Next faction after Drukhari** — the documented priority order is fully built; none is queued.
  Recommendation stands: clear the engine backlog first.

## Close

Produce the four documents, register `SESSION_HANDOFF_240.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
