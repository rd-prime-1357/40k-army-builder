# NEXT SESSION PROMPT — Session 208

## Recommended turn type: data-turn (Grey Knights Dreadknights authoring + parser change), unless
## B108 is still open — see below.

Read `SESSION_HANDOFF_207.md` first, then this prompt. S207 shipped B106 — `loRollup`'s fixed-1
branch now accepts a distinct-addition count option (`type: 'count'`, `distinct: true`,
`replacement_choices: [...]`, `max_total: N`, no `replaces`). `index.html` is at v6.18. Grey Knights
is fully unblocked for the parser + data turn.

## Before starting: B108 status check

S207 open surfaced a critical publication problem: `Thousand_Sons_web.txt` is in the public repo
(GW-derived content, standing-constraint violation) AND still absent from the private repo. Both are
Ryan actions and neither could be fixed from S207.

- If Ryan has removed it from the public repo AND pushed it to the private repo, `repo_check` and
  the `--fetch --data-turn` source-fetch gate will both clear at open. Proceed with the main task.
- If either is still outstanding, `repo_check` will keep flagging CRITICAL (public-repo copy still
  present) and/or the source-fetch gate will fail the same way S206/S207 did. This is a data turn,
  so a source-fetch failure DOES gate work. If B108's second half (private-repo push) is not done,
  fall back to the same project-mount stopgap S206 and S207 used: pull `Thousand_Sons_web.txt` from
  `/mnt/project/` and re-flag B108. Do NOT treat this as new — it's still B108.

## Primary task: author both Dreadknights' ranged-weapon options + regeneration

Both Grey Knights Dreadknights (`000000389` Nemesis Dreadknight, `000001360` Grand Master in Nemesis
Dreadknight) carry the sentence:

> "This model can be equipped with up to two of the following, but cannot take duplicates:
> 1 gatling psilencer / 1 heavy incinerator / 1 heavy psycannon[/1 sublimator]"

The sublimator is only on the Grand Master, not the vanilla Nemesis Dreadknight — verify against
source before authoring, don't assume.

### Parser change

`loadout_parser.py` needs a new classifier for this sentence shape:

- Trigger phrase: "up to N of the following, but cannot take duplicates" (or the equivalent —
  read source, don't assume; there may be prior-art phrasings this session should catch too).
- Emitted option shape: `type: 'count'`, `distinct: true`, `replacement_choices: [...listed weapons]`,
  `max_total: N`, no `replaces` field. `scope` = the model-group name. `group` = a sensible label
  authored from the sentence (e.g. "Ranged Weapons").
- Regression-check the new classifier against the full options corpus before touching the pipeline:
  scan `Datasheets_options.csv` for every match, then confirm each hit is currently unclassified by
  every other function in `CLASSIFIERS` and belongs to a currently-built unit — same methodology
  B105 (S206) used. Any hits outside Grey Knights need explicit review; do not silently regenerate.

### Data regeneration

Run the seven-pass `equipped_parser.py` chain in a scratch directory, seeded with the four
`HAND_AUTHORED` entries only (same methodology `repro_check.py` uses, NOT a `--existing`
carry-forward — that would silently preserve the pre-fix `UNMATCHED` residuals on both Dreadknights).
Diff-guard at key level: expected diff is exactly the two Dreadknight units updated (both losing
their `_parser_flags` line, both gaining the new ranged-weapon option), zero change elsewhere. Field-
check the actual emitted option on both units against source before promoting.

### Cost sanity check

`wargear_points.json` may need regeneration if the MFM prices the ranged weapons — check
`MFM_Grey_Knights_v1.1.txt`'s WARGEAR OPTIONS block for the two Dreadknights and confirm whether
prices already exist in `wargear_points.json` (they may — S206 already added 4 GK units to it).
If prices exist and are already correct, no regeneration; if any are missing, run the canonical
`FACTION_BY_MFM` insertion-order path (NOT alphabetical — S206 documented the trap), diff-guard,
and update `E14-2`'s pinned census if the counts change.

### Assertion

Add a structural assertion in `rules_assertions.py` covering the new sentence shape — scan
`Datasheets_options.csv` for the trigger phrase and confirm every match in a currently-built
faction has a corresponding option in `unit_loadouts.json` with the correct shape (`type: 'count'`,
`distinct: true`, `replacement_choices` populated, `max_total` set, no `replaces`). Same shape as
B101-DATA. Don't pin by unit ID — a future faction may hit this sentence too.

## After the Dreadknight turn ships

Grey Knights will be **fully complete**. Move to the next Adeptus Astartes faction per the standing
priority order — check `40K_Decision_Log.md`'s most recent faction-priority note for which is next
(the standing order is Black Templars, Dark Angels, Blood Angels, Deathwatch, Grey Knights, Imperial
Fists, Iron Hands, Raven Guard, Salamanders, Space Wolves, Ultramarines, White Scars, but the log is
the authority on which are already built).

## Standing reminders

- `./baseline.sh --fetch --data-turn` at open (see B108 caveat above).
- All 30+ gates should be green at S207 close (once the manifest is regenerated) — confirm they
  still are before starting new work.
- Re-derive from source, don't trust prior-session prose.
- Do NOT hand-edit `unit_loadouts.json`. Fix parsers, regenerate.
- Turn typing: this is a data turn (with parser + assertion pieces). Do not mix in unrelated engine
  or tooling changes.

## Close

Produce the four documents, register `SESSION_HANDOFF_208.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
