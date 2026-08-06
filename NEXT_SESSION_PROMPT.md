# NEXT SESSION PROMPT — Session 203

## Turn type: data-only. No engine, no tooling parser changes. No exceptions.

Read `SESSION_HANDOFF_202.md` first, then this prompt. S202 landed B101-data turn 1 (the parser now
recognises the no-duplicate marker and emits `distinct: true`); the fix is proven against sources in a
temp dir but **`unit_loadouts.json` has not been regenerated**. That's this session's job.

## This session's job: B101-data turn 2

### 1. Regenerate `unit_loadouts.json`

Run the real pipeline (`loadout_parser.py` + the seven-pass `equipped_parser.py` chain — the same
shape `repro_check.py` uses) and commit the result. S202's temp-dir proof already showed the expected
diff: exactly three units change —

| unit | option | what changes |
|------|--------|---------------|
| Raptors `000000958` | `cc_6` | fake marker choice removed, `distinct: true` added |
| Legionaries `000002570` | `cc_5` | fake marker choice removed, `distinct: true` added |
| Traitor Guardsmen Squad `000002590` | `cc_1` | fake marker choice removed, `distinct: true` added |

Diff-guard at key level against the currently-committed file before banking — confirm it's still only
those three, nothing else moved. If it isn't, stop and find out why before proceeding; don't assume
S202's proof still holds byte-for-byte without re-checking (source files could in principle have
changed since).

### 2. Add the `rules_assertions.py` assertion

The natural assertion — any option whose `replacement_choices` contains a no-duplicate marker string
must carry `distinct: true` — can't be written the same way anymore, because the marker string is
gone from the parsed output by design (that's the fix). Two reasonable shapes:
- Pin the three known units/options directly (`distinct: true` present on `000000958`'s `cc_6`,
  `000002570`'s `cc_5`, `000002590`'s `cc_1`) — simple, but only guards regression on these three, not
  the general rule.
- A structural check against the *source* CSV (`Datasheets_options.csv`) — scan for the known marker
  phrases and confirm every option built from a marked source line carries `distinct: true` in the
  output. Closer to the actual rule, more coupled to source format.

This is a "how it gets built" call, not a "how it works" one — pick one, note the reasoning in the
decision log, and proceed; it doesn't need to come back to Ryan.

### 3. B103's residual `UNMATCHED` flags — leave alone, don't fold in

Three flags remain after regeneration (Raptors' 10-model-bonus sentence, Legionaries' two spelled-out
"One Legionary's..." lines) — confirmed in S202 as separate, pre-existing parser gaps unrelated to the
marker fix. They are not part of B101-data. If they're worth a ticket, open one, but don't spend this
session's data-turn budget fixing them — that would be a tooling change riding inside a data turn,
which the turn-typing rule doesn't allow.

## After turn 2 lands

B100's two data turns — Grey Knights units, then Grey Knights detachments, separate per the B89 arc's
convention. The units turn's first check is the open `Grey_Knights_web.txt` question in
`GREY_KNIGHTS_BUILD_SCOPE.md` §5; resolve it from the pipeline, don't assume it either way. The two
Nemesis Dreadknights are authored against `distinct: true` directly and need no marker handling — the
whole point of clearing this ticket first.

B103 (non-distinct rollup emits past its cap and hides the over-allocation) is an engine turn, not a
data turn, and carries one product question for Ryan — already recorded in the ticket with a
recommendation, not blocking. Take it whenever an engine turn comes up next in the sequence.

## Standing reminders
- `./baseline.sh --fetch --data-turn` to get GW sources loaded before starting.
- Expect `repro_check` to currently show FAIL at open (parser diverges from still-unregenerated data)
  — that's S202's known, documented state, not new drift. It should go PASS once this session's
  regeneration is committed and the manifest re-hashed.
- **Check sources directly, don't trust prior-session prose.** S202 found the fix needed a second,
  separate propagation site (`build_loadout`'s entry rebuild) that the classifier-level fix alone
  didn't cover — caught only by checking actual proof output field-by-field. Treat "ran clean" as
  necessary, not sufficient; check the actual values.

## Close
Produce the four documents, register `SESSION_HANDOFF_203.md` in `pipeline_manifest.py`'s GUARDED list
**before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command — after every other edit, including edits to the handoff itself (leave the handoff's own row
in its Files table as "(this file)").
