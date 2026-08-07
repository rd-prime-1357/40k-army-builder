# SESSION HANDOFF 207

**Turn type:** engine-only (B106). `index.html`, `pipeline_manifest.py`, `baseline.sh` edited;
`b106_check.js` net-new. No parser, data or assertion file changed.

## What happened

1. **Baseline reconciled at open — one critical finding, one prompt-caveat cleared.**
   - `repo_check.py` flagged `Thousand_Sons_web.txt` CRITICAL: present in the public repo. Verified
     by fetching the public tarball directly. Content is verbatim GW datasheet material — profiles,
     weapons, abilities — matching every other `*_web.txt` faction composition file the standing
     constraint excludes. Cross-checked the private repo via the read-only token: file still not
     there, `source_manifest.json` still doesn't list it. S206's Ryan action (push to the private
     repo) was not completed; the file appears to have gone to the public repo instead. Cannot fix
     from this session — opened as **B108** (see backlog) and continued with B106.
   - The S207 prompt's second caveat (data-turn source fetch would fail on the same
     `Thousand_Sons_web.txt` gap) did not apply — this session is engine-only, so `--data-turn`
     wasn't run.

2. **B106 shipped (D301).** `loRollup`'s fixed-1 branch now accepts a distinct-addition count option
   (`type: 'count'`, `distinct: true`, `replacement_choices: [...]`, `max_total: N`, no `replaces`).
   Chose the mechanism after reading both existing paths against source: the fixed-1 branch was the
   actual gap; the body-group branch already accepts the shape via `loSrcOnGroup` returning true for
   empty `replaces` (verified, not assumed); `add`+`pool_id` can't express the rule because its
   pool cap is `max` of member caps, not a sum; a new top-level type would multiply surface area.
   Fix reuses B101's `loDistinctCap` / `loChoiceGroupCap` / `loDistinctPicks` verbatim. Two-line
   guard split on the fixed-1 branch, plus a one-line skip inside `chargeF` so source-consumption
   doesn't fire for an add-only option.

3. **Net-new `b106_check.js` (32 assertions).** Covers: helpers are shape-agnostic re: `replaces`;
   fixed-1 rollup emits picks without consuming the default weapon; stale duplicates clamp to one
   with the freed slot not spent elsewhere; `max_total` binds even when the menu is larger than the
   cap (the Grand Master's 4-choice sublimator variant); selection path refuses duplicates and
   third picks; body-group branch pinned as a regression check; plain replacement shape (with
   `replaces`, no `distinct`) is byte-for-byte unchanged. Registered in `pipeline_manifest.py`'s
   `GUARDED` and gated in `baseline.sh` immediately after `b101_check`.

4. **`index.html` bumped v6.17 → v6.18.**

5. **Full harness suite green.** All 24 engine/data harnesses pass, including b101 (no regression)
   and the new b106. `rules_assertions --tier a`: 81/82 mid-session — the only failing assertion is
   P3, tripped on this session's own `index.html` and `baseline.sh` edits before the manifest was
   regenerated. Resolved by `pipeline_manifest.py --write` at close, then `--freshness-check`.

## State at close

- `index.html`: v6.18. `loRollup` fixed-1 branch accepts the distinct-addition shape; body-group
  branch untouched (verified to already accept it).
- `pipeline_manifest.py`: `b106_check.js` appended to `GUARDED` after `b101_check.js`;
  `SESSION_HANDOFF_207.md` appended.
- `baseline.sh`: `b106_check` gate added after `b101_check`.
- `b106_check.js`: net-new, 32 assertions covering both rollup branches, selection path, and the
  plain-replacement regression.
- `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`: D301 recorded; B106 moved to
  Closed / Shipped pointers; B108 opened as CRITICAL Ryan action.
- `loadout_parser.py`, `equipped_parser.py`, `detachment_parser.py`, `unit_loadouts.json`,
  `units.json`, `wargear_points.json`, `detachments.json`, `detachment_effects.json`,
  `rules_assertions.py`: **untouched.**
- Grey Knights fully unblocked for the parser + data turn. B100 (Grey Knights) will close once the
  two Dreadknights' ranged-weapon options land.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (at minimum from HEAD; ideally
   scrub git history via `git filter-repo` since the content shouldn't have been public). Standing
   constraint: GW-derived source material never in the public repo.
2. **B108 — push `Thousand_Sons_web.txt` to the private `rd-prime-1357-data-sources` repo and
   regenerate `source_manifest.json`.** This is the still-unfixed S206 action. Until it lands, any
   data-turn `--fetch --data-turn` open will fall back on the same project-mount-only stopgap S206
   and S207 both used.
3. Push this session's changed files to the public repo (listed below).

## Decisions waiting on Ryan

None on the tool's product/rules-legality surface. B108 is a compliance action, not a decision.

## Files (SHA-256, first 12)

Verify these at S208 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `696c18d3e188` | v6.17 → v6.18; `loRollup` fixed-1 branch B106 fix |
| `b106_check.js` | `15b04736aff0` | **net-new**; 32 assertions, all pass |
| `baseline.sh` | `c0bf6d9f90af` | `b106_check` gate added after `b101_check` |
| `pipeline_manifest.py` | `277ee3f889d3` | `b106_check.js` + `SESSION_HANDOFF_207.md` appended to GUARDED |
| `pipeline_manifest.json` | `dc8d001aef14` | regenerated via `--write` at session close |
| `40K_Decision_Log.md` | `c48b06ebcc7e` | D301 appended |
| `DECISION_INDEX.md` | `bd4cefeab265` | D301 entry |
| `OPEN_ITEMS_BACKLOG.md` | `8a819ffbf133` | B106 → Closed/Shipped; B108 opened; header updated |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S208 |
| `SESSION_HANDOFF_207.md` | (hash is pre-computation; verify against banked copy) | this file |

`loadout_parser.py`, `equipped_parser.py`, `detachment_parser.py`, `units.json`,
`unit_loadouts.json`, `wargear_points.json`, `abilities.json`, `weapon_abilities.json`,
`datasheet_wargear_abilities.json`, `detachments.json`, `detachment_effects.json`,
`faction_taxonomy.json`, `source_manifest.json`, `rules_assertions.py`: **untouched**, no entry
needed.

## Backlog

22 open at S206 close; 22 open here (B106 closed, B108 opened). Beginning: B106, B99, B98, B97,
B103, E28, B93, B90, B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (22 —
matches S206 ending). Resolved: B106. Added: B108. Ending: B108, B99, B98, B97, B103, E28, B93, B90,
B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (22).
