# NEXT SESSION PROMPT — Session 205

## Turn type: tooling-only. No data, no engine changes. No exceptions.

Read `SESSION_HANDOFF_204.md` first, then this prompt. S204 shipped B100's units half (Grey Knights
added to `units.json`, 25 units, diff-guarded clean) but found a real, pre-existing bug while
attempting the loadouts half: `equipped_parser.py`'s `scoped_name2id` silently corrupts 8 unrelated,
already-shipped units the moment Grey Knights (or any future faction reusing a generic vehicle name)
is added to `units.json`. `unit_loadouts.json` is untouched, byte-identical to S203. This session's
job is **B104 only** — fix the bug, do not touch data.

## The bug, precisely

`scoped_name2id` (in `equipped_parser.py`) resolves a composition-pass title to a `unit_id` by exact
army-scope match first, and falls back to `cands[-1][1]` — the **last-declared candidate** in
`units.json`'s block iteration order — whenever the current pass's own army name matches none of the
name's real candidates. For names referenced only by passes whose scope matches *none* of the
candidates (confirmed case: "Land Raider Crusader" has candidates `(Adeptus Astartes, 000000066)`
and `(Black Templars, 000004139)`, but its actual composition text lives only in
`Space_Marines_web.txt`, `Dark_Angels_web.txt` and `Space_Wolves_web.txt` — none of those scopes
match either candidate), the fallback is not a considered default, it's whichever block happened to
be declared last. Appending a new faction that shares the name makes IT the new last-declared
candidate, silently stealing the match.

Affected today (confirmed by diff-guard, S204): Land Raider (`000000065`), Land Raider Crusader
(`000004139`), Land Raider Redeemer (`000002173`), Rhino (`000002723`), Razorback (`000000129`),
Stormhawk Interceptor (`000000084`), Stormtalon Gunship (`000001190`), Stormraven Gunship
(`000001191`) — all lose their real per-model `default_weapon_counts` and revert to
`loadout_parser.py`'s flat placeholder the moment Grey Knights' block exists in `units.json`.

## What to check before choosing a fix — don't assume the shape

Read `equipped_parser.py`'s `load_roster` and `scoped_name2id` directly (docstrings included) before
writing anything. Candidate fix directions, not a prescription — evaluate against real data:

1. **Only fall back when genuinely unambiguous** — e.g. only use `cands[-1]` when there is exactly
   one candidate whose army isn't the current pass's own scope; when there are two or more
   non-matching candidates, this is real ambiguity and should be flagged (a new `_parser_flags`
   entry, or a `--report` line), not guessed.
2. **Prefer the generic/base-army block explicitly** — several of the passes that hit this
   (`Space_Marines_web.txt`) really do mean the generic "Adeptus Astartes" block; teaching
   `scoped_name2id` that `'Space Marines'` (the filename-derived scope) means `'Adeptus Astartes'`
   (the real block name) might resolve several of these correctly by real scope match instead of
   fallback, shrinking how often the ambiguous case even fires. Check whether this alone covers all
   8 known cases or only some.
3. Whatever the fix, it must not regress the *existing* correct behaviour for genuinely unambiguous
   single-candidate names (the overwhelming majority) — `scoped_name2id`'s own docstring's claim of
   "byte-identical to the old flat name2id for every non-colliding title" must still hold.

## Verification — this is the load-bearing part of the session

1. Fix `scoped_name2id` (or wherever the real fix belongs).
2. Run the full `repro_check.py` regeneration **twice**: once with `GK` still excluded from
   `FACTIONS` (confirm the 8 previously-corrupted units now resolve correctly even without Grey
   Knights' own loadouts being touched — this is the regression test), and once with `GK` added back
   to `FACTIONS` (confirm Grey Knights' own 25 units parse correctly *and* the 8 vehicles still
   resolve correctly with Grey Knights actually present).
3. Diff-guard both runs at the key level against the currently-committed `unit_loadouts.json` before
   concluding anything — do not trust a clean exit code alone; check the actual field values byte by
   byte for at least the 8 named units plus a handful of unrelated ones, the same discipline every
   data turn already uses.
4. This is a real, executable check, not just a passing gate: add or extend a `rules_assertions.py`
   assertion (or a new `bXX_check.js`) that pins this specific failure mode — a same-named generic
   unit across two-plus faction blocks, none matching a given pass's scope, must resolve
   deterministically and correctly, not merely "whatever `cands[-1]` happens to be." Decide the
   right shape once you've seen how the real fix works; a synthetic fixture is fine and probably
   necessary (mirrors B101's own synthetic-fixture precedent, since pinning this against Grey
   Knights' real data would make the assertion mean nothing once GK's own build eventually changes).

## Explicitly out of scope this session

- Do **not** add `GK` back to `repro_check.py`'s `FACTIONS` permanently — that's the loadouts data
  turn, not this one. Test with it added, but leave it reverted at session close unless the loadouts
  turn is deliberately folded in (it shouldn't be — turn typing).
- Do **not** touch B105 (narthecium sentence classifier) or B106 (Dreadknight distinct-addition
  engine gap) — separate tickets, separate turns.
- Do **not** regenerate `unit_loadouts.json` for real / commit any data changes this session.

## After this session

Once B104 ships and is reverified: B105 (parser-only, XS) can ship on its own data+tooling turn, or
ride along with the eventual Grey Knights loadouts turn. B106 needs its own engine-scoped session
(read `loRollup`'s `add`/`pool_id` mechanism and B101's `distinct` mechanism together before choosing
a shape). Then, finally: B100's loadouts half — add `GK` to `repro_check.py`'s `FACTIONS` for real,
author the four flagged units (Brotherhood Terminator Squad / Paladin Squad's narthecium line via
B105's new classifier; both Dreadknights' ranged-weapon option via B106's new engine support),
regenerate and diff-guard `unit_loadouts.json` for the whole roster, not just Grey Knights.

## Standing reminders
- `./baseline.sh --fetch --data-turn` to get GW sources loaded before starting (tooling turns still
  need sources loaded, since `repro_check.py` exercises the real pipeline for verification).
- Expect `repro_check` red at open, tracing to exactly B104 — confirmed, not a surprise. Every other
  gate should be clean.
- **Check sources directly, don't trust prior-session prose** — including this prompt's own
  characterization of the bug. Re-derive from `equipped_parser.py` and real `units.json`/web-pass
  data before building on it.

## Close
Produce the four documents, register `SESSION_HANDOFF_205.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command — after every other edit, including edits to the handoff itself (leave the handoff's own row
in its Files table as "(this file)").
