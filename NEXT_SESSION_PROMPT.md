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

## Before anything else: the manifest is stale and cannot be regenerated

`pipeline_manifest.py --write` refused at S201's close because `SESSION_HANDOFF_199.md` is absent from
the public repo **and** from the `/mnt/project` mount. It is not merely unpushed. The manifest banked
a hash for it at S199 close, so it existed then. Until it comes back — or Ryan decides it will not —
`--write` cannot run and `pipeline_manifest.json` stays at its S200 contents, so `pipeline_manifest`,
`rules_assertions` and `repo_check` will all be red at open for that reason on top of the ordinary
unpushed drift.

Do not remove anything from GUARDED to make the red go away. That is Ryan's call and it is about the
integrity of the record, not the pipeline. Ask for a file-list screenshot first; the mount is not
authoritative for presence. Verify S201's file hashes from its handoff table by hand at open, since
the manifest cannot do it for you this time.

## Standing reminders
- `./baseline.sh --fetch --data-turn` to get GW sources loaded — a parser change cannot be proved
  tier-A-only. `--data-turn` here means "fetch the sources", not "this is a data turn"; the turn type
  is still tooling and no output file gets committed.
- **Check sources directly, don't trust prior-session prose.** Every session since S196 has found
  something a report, a hardcoded assumption or a session prompt got wrong — including S201, which
  corrected S200's own table. Treat it as the norm.
- Three Ryan actions are outstanding and none is this session's to resolve: the Calgar missing-comma
  fix in the private repo (unpushed since S198), and three sessions' worth of public-repo changes
  (S199, S200, S201). `repo_check`, `pipeline_manifest` and `rules_assertions` all stay red on
  `SESSION_HANDOFF_199.md` alone until that lands — expected, not a new failure. Confirm by clone
  rather than assuming.

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
