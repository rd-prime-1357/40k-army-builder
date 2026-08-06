# NEXT SESSION PROMPT — Session 202

## Turn type: tooling-only. No engine, no data regeneration. No exceptions.

Read `SESSION_HANDOFF_201.md` first, then this prompt. S201 landed B101's engine half; the rule is now
expressible and **nothing authors it**, which is what this session starts fixing.

## This session's job: B101-data turn 1 (the parser), plus B102 riding along

Both are tooling. They are unrelated to each other, which is fine — S194 set the precedent for two
tooling items in one tooling turn.

### 1. B101-data, turn 1 — `loadout_parser.py` emits `distinct`

Three shipped Chaos Space Marines options carry a no-duplicate restriction as a literal string inside
`replacement_choices`, where it renders as a fake selectable entry and, if selected, adds a weapon
named after the rules sentence to the unit:

| unit | option | shape | marker |
|------|--------|-------|--------|
| Raptors `000000958` | `cc_6` | `max_total_all`, `up_to` 2, 3 real choices | `Options (You Cannot Select The Same Option More Than Once):` |
| Legionaries `000002570` | `cc_5` | `per_n_models` 5 / `max_per_n` 1, 9 real choices | `(Duplicates Are Not Allowed):` |
| Traitor Guardsmen Squad `000002590` | `cc_1` | `max_total_all`, `up_to` 3, 5 real choices | `(Duplicates Are Not Allowed):` |

Verified in S201 as the only three occurrences among all 39 `replacement_choices` options. Note
Legionaries is **not** an uncapped option — S200's table was wrong about that.

The parser should recognise the marker wording and emit `distinct: true` on the option instead of
letting it through as a choice. Likely site: `_choices_from_list` strips a parenthesised note only at
the **end** of the list text, which is why a mid-sentence marker survives — but derive the real cause
from the source text, don't take that as given. Raptors also carries a related `UNMATCHED`
`_parser_flags` entry on the same sentence; check whether one fix covers both rather than assuming it.

**Do not regenerate `unit_loadouts.json` this session.** Prove the parser change against the sources
in a temp dir and stop there. The regeneration is turn 2 and is a data turn.

### 2. B102 — `detachment_parser.py --report` `KeyError`

One line. Gap records carry `source_faction`; the report writer reads `g["army"]`. Latent because no
gate passes `--report`. Eleven gaps already exist across built factions.

## One thing to verify at open

S201 could not regenerate the manifest until late: `SESSION_HANDOFF_199.md` had never been pushed at
S199's close, so it was absent from the repo *and* from the project area, and `--write` refuses while
any guarded file is missing. Ryan recovered it from the S199 conversation and it is now banked — but
**the recovered copy does not hash-match what S199 originally banked** (`17e21c73b96c…`, was
`4feb6caeb93e…`). The file is complete and sound; the difference is almost certainly a Drive
round-trip. The banked hash is now the recovered copy's. If `repo_check` or the manifest flags that
file at open, check that the copy in the repo is the same one S201 banked before treating it as new
drift.

Also correct a habit that bit S200 and S201: both carried forward a prose claim about which files were
unpushed, and both were wrong. Checking the repo against its own manifest takes one command and
settles it. Do that instead of restating the prior handoff.

## Standing reminders
- `./baseline.sh --fetch --data-turn` to get GW sources loaded — a parser change cannot be proved
  tier-A-only. `--data-turn` here means "fetch the sources", not "this is a data turn"; the turn type
  is still tooling and no output file gets committed.
- **Check sources directly, don't trust prior-session prose.** Every session since S196 has found
  something a report, a hardcoded assumption or a session prompt got wrong — including S201, which
  corrected S200's own table. Treat it as the norm.
- One Ryan action is outstanding and it is not this session's to resolve: the Calgar missing-comma fix
  in the private repo, unpushed since S198. S201's own files and `SESSION_HANDOFF_199.md` were handed
  over for pushing at S201's close; confirm by clone rather than assuming either way.

## After this session
B101-data turn 2 (data): regenerate `unit_loadouts.json`, diff-guard at key level against the
committed file, and add the `rules_assertions.py` assertion that any option whose
`replacement_choices` contains a no-duplicate marker carries `distinct: true`. That assertion would
fail today, which is exactly why it belongs with the turn that makes it true.

Then B100's two data turns — Grey Knights units, then Grey Knights detachments, separate per the B89
arc's convention. The units turn's first check is the open `Grey_Knights_web.txt` question in
`GREY_KNIGHTS_BUILD_SCOPE.md` §5; resolve it from the pipeline, don't assume it either way. The two
Nemesis Dreadknights are authored against `distinct: true` directly and need no marker handling.

B103 (non-distinct rollup emits past its cap and hides the over-allocation) is an engine turn and
carries one product question for Ryan — recorded in the ticket with a recommendation, not blocking.

## Close
Produce the four documents, register `SESSION_HANDOFF_202.md` in `pipeline_manifest.py`'s GUARDED list
**before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last** command
— after every other edit, including edits to the handoff itself (leave the handoff's own row in its
Files table as "(this file)").
