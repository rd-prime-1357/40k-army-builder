# SESSION HANDOFF 201

**Turn type:** engine-only. `index.html` v6.16 → **v6.17**. One net-new harness. No data file, no
parser, no source, no `rules_assertions.py` change.

## What happened

1. **Baseline reconciled at open, 27/30.** All three failures trace to one cause:
   `SESSION_HANDOFF_199.md` is still absent from the public repo. Verified by direct clone rather than
   inferred — 165 files byte-identical, nothing else drifting. `rules_assertions` and
   `pipeline_manifest` both fail purely on that one absent guarded file; `repo_check` reports the same
   file as its only problem. Not a new failure and not fixable from inside a session. The other four
   `--fetch`-path failures seen on the first attempt were an artefact of the sandbox starting with 78
   guarded files absent from the working copy; overlaying them from the repo clone (the same thing
   `baseline.sh --fetch` does) cleared all but the one.

2. **B101's engine half shipped (D294).** New optional boolean `distinct` on `count` options carrying
   `replacement_choices`, expressing "you cannot select the same option more than once". The
   substance of the decision is that it is enforced at **three** places, not one, because whichever is
   omitted becomes the hole:
   - **Selection path** — `editLoadoutChoiceCount` takes a sixth argument `perMax` and refuses an
     increment past it. Every pre-existing caller omits it; absent means "no per-choice limit", never
     zero.
   - **Renderer** — the stepper's `+` disables once that choice is taken, so the duplicate is never
     offered rather than offered-and-rejected. Sub-note reads "pick up to N, no duplicates".
   - **Rollup** — `loDistinctPicks` re-derives the legal picks inside **both** `loRollup` branches,
     the fixed-1 model group and the multi-model body group. These are separate code paths and a fix
     to one has not historically implied the other. This is what stops a list saved before the flag
     existed, or edited in browser storage, from rolling up illegal weapons and their points; points
     derive from the rollup, so the clamp covers cost as well as display.

   Derived ceiling `loChoiceGroupCap`: a distinct option can never take more picks than it lists
   choices, so the effective group total is `min(loMaxCount(...), replacement_choices.length)`.
   Over-selection truncates in the option's own `replacement_choices` order rather than storage
   insertion order, so the outcome is deterministic.

3. **Non-distinct paths left byte-for-byte unchanged, on purpose.** `loDistinctPicks` is reached only
   when the flag is set. See item 6 for why.

4. **One rendering change reaches beyond distinct options.** The `+` on any `replacement_choices`
   stepper now greys out once the group total is reached; it was previously live and silently rejected
   by the handler. No legality outcome changes — it makes an existing hard rule visible, which is the
   same D0 principle the ticket is about. Flagging it because it is a visible change to shipped units
   that the ticket did not ask for.

5. **Two corrections to inherited framing, both from reading the data rather than the prior
   write-up.**
   - S200's table implied Legionaries `cc_5` was uncapped. It is not — `per_n_models: 5`,
     `max_per_n: 1`, so its cap is 2 at ten models and 1 at five. All three CSM options have a working
     *total* cap; only distinctness was missing.
   - The marker string is worse than a cosmetic fake menu entry. Selecting it pushes the rules
     sentence through `addRepl` and the unit gains a weapon literally named
     `Options (You Cannot Select The Same Option More Than Once):`. Points are unaffected —
     `wargearCostForRollup` looks names up in `wargear_points.json` and a rules sentence never matches
     — but the weapon list is visibly wrong. This raises the priority of the data half above cosmetic.

   Also verified rather than assumed: the marker appears in exactly three of the 39
   `replacement_choices` options across `unit_loadouts.json`, matching S200's list.

6. **B103 opened for a looser pre-existing defect, deliberately not fixed here.** In `loRollup`'s body
   branch a `replacement_choices` option pushes every tallied pick into `emit` and only then clamps
   the total for the source charge. So more weapons can be emitted than the cap allows, and because
   the source charge is the clamped figure the per-source check never sees the overrun and
   `overAllocated` does not fire — the list looks clean while being wrong. The fixed-1 branch clamps
   differently again, so the two branches disagree on the same shape. Not folded into B101 because the
   emitted weapons feed `wargearCostForRollup`, so tightening it changes the **points** of
   already-saved lists across shipped factions. It needs its own turn, its own census, and a product
   call from Ryan on whether an over-cap saved list should be corrected silently or corrected *and*
   flagged.

7. **Net-new `b101_check.js`**, registered in `baseline.sh` and `pipeline_manifest.py`. Loads the real
   `loRollup` and the real `editLoadoutChoiceCount` out of `index.html` and covers all three
   enforcement points plus a non-distinct control on each. Fixtures are synthetic by design: no
   shipped unit carries the flag, so a harness written against real data would pin nothing today and
   would only start meaning something at the moment the data landed, which is backwards. Each
   enforcement point was mutation-tested individually — neutering `loDistinctCap`, the `perMax` guard,
   or `loChoiceGroupCap` each fails the harness on named assertions rather than crashing it.

8. `rules_assertions.py` untouched. The natural assertion — any option whose `replacement_choices`
   contains a no-duplicate marker must carry `distinct: true` — would fail on all three CSM options
   today and belongs with the data turn that makes it true, not with the engine turn.

9. Decision log (D294) and its index entry, data dictionary (the `distinct` field), and backlog
   updated. `SESSION_HANDOFF_201.md` and `b101_check.js` registered in `pipeline_manifest.py`'s
   GUARDED list.

10. **The manifest could NOT be regenerated, and this is the session's real blocker.**
    `pipeline_manifest.py --write` refuses while any guarded file is absent, and
    `SESSION_HANDOFF_199.md` is absent from every location reachable from a session: not in the
    public repo (direct clone), not on the `/mnt/project` mount. It is not merely unpushed — it may
    be gone. The manifest banked a hash for it at S199 close
    (`4feb6caeb93e1433b86d9e60f41209aad1dca0c6275af82d2ad434f57034f32d`), so the file did exist then;
    it was never pushed, and routine project-area housekeeping deletes handoffs. Consequently
    `--write` did not run and `--freshness-check` was not run either — both are carried to S202. The
    Files table below therefore carries hashes computed directly this session rather than read back
    from a regenerated manifest, which is the redundancy the protocol asks for and works without it.

    **The mount is not authoritative for presence**, so this is not yet a conclusion. A file-list
    screenshot is needed before anyone treats `SESSION_HANDOFF_199.md` as lost, and nothing should be
    removed from GUARDED on the strength of the mount alone.

## The caveat that matters most

**The engine can now express the rule and nothing uses it.** No shipped option carries
`distinct: true`. Authoring it on the three Chaos Space Marines options needs the parser to emit the
flag (tooling turn) and then a regeneration (data turn), and neither could ride here under turn
typing. For a player, those three units are exactly as wrong at v6.17 as they were at v6.16. Tracked
as **B101-data**, and it is what B100 now waits on — not B101.

## What's explicitly not done

- No data or parser change of any kind. The marker strings are still in `unit_loadouts.json`.
- B103 opened, not fixed.
- B102 (`detachment_parser.py --report` `KeyError`) untouched — it is a tooling item and this was an
  engine turn.
- The renderer change is unverified by eye. The harnesses load engine functions, not the DOM, so the
  disabled `+` and the "no duplicates" sub-note need Ryan's eyeball on a real unit once a `distinct`
  option actually ships. Until B101-data lands there is nothing on screen to look at.

## State

- Baseline: 27/30 at open and at close, the three failures being `rules_assertions`,
  `pipeline_manifest` and `repo_check`, all on the unpushed `SESSION_HANDOFF_199.md` plus (at close)
  this session's own not-yet-pushed changes. `b101_check` runs green inside `baseline.sh`.
- `index.html`: **v6.17**.
- `units.json`, `unit_loadouts.json`, `detachments.json`, all parsers, `rules_assertions.py`:
  untouched.
- `OPEN_ITEMS_BACKLOG.md`: **23 open** (up from 22 — B101's engine half closed, B101-data and B103
  opened).
- `pipeline_manifest.json`: **not** regenerated — `--write` refused on the absent
  `SESSION_HANDOFF_199.md`. `b101_check.js` and `SESSION_HANDOFF_201.md` are registered in
  `pipeline_manifest.py`'s GUARDED list and will be banked by the first successful `--write`.
- `repo_check` will show drift until pushed: S199's seven files, S200's eight, and this session's
  seven.

## Ryan action required

1. **Push the Calgar missing-comma fix** to the private repo's `MFM_Space_Marines_v1.1.txt` —
   outstanding since S198. Not re-checked this session (no sources loaded; engine turn).
2. Push S199's, S200's and this session's public-repo changes — three sessions' worth now pending.
   `SESSION_HANDOFF_199.md` in particular is the single cause of all three failing gates, so pushing
   it clears the baseline.
3. **A file-list screenshot of the project area is needed**, specifically to answer whether
   `SESSION_HANDOFF_199.md` is present. The mount shows it absent, but the mount is not authoritative
   for presence — it deduplicates by filename and goes stale. Nothing should be removed from GUARDED,
   and no one should treat the file as lost, until that is settled.

## Decisions waiting on Ryan

**One that blocks S202's close: what to do about `SESSION_HANDOFF_199.md`.** If it is genuinely gone,
the manifest can never be regenerated while it stays in GUARDED, and every session from here closes
with a stale manifest. Removing it from GUARDED would unblock the pipeline at the cost of a permanent
hole in the record — the guarded-handoff design exists precisely to make that hole visible, so
patching over it is a call about the integrity of the record, not a development decision, and I am not
making it. I have not recommended removing anything; the first step is the screenshot. If the file
does still exist in the project area, it just needs re-uploading and everything clears.

And one that is not blocking: **B103's product question** — when a saved list exceeds a wargear cap,
should the app correct it silently or correct it and show a warning? My recommendation is silently:
under D0 the state was never legal, so there is nothing to warn about, and `overAllocated` stays
reserved for genuine same-source contention. Recorded in the ticket; the B103 turn can proceed on that
reading unless overruled.

## Files (SHA-256, first 12)

Computed directly this session with `sha256sum`, **not** read back from a regenerated manifest —
`--write` was blocked (see item 10). Verify these at S202 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | 3e741fc6296d | **v6.17** — `distinct` flag, three enforcement points |
| `b101_check.js` | 7dcc24bfa39d | **net-new** — pins all three enforcement points |
| `baseline.sh` | 6bfe72149ad4 | `b101_check` gate registered |
| `pipeline_manifest.py` | a8fd35671770 | `b101_check.js` + handoff 201 registered in GUARDED |
| `40K_Data_Dictionary.md` | 455953e90852 | `distinct` field documented |
| `40K_Decision_Log.md` | b9ef489be3af | D294 appended |
| `DECISION_INDEX.md` | cc8c81589508 | D294 index entry |
| `OPEN_ITEMS_BACKLOG.md` | 677195229e1b | B101 engine half closed; B101-data, B103 opened; 23 open |
| `NEXT_SESSION_PROMPT.md` | c9b9d480dc70 | (unguarded by design) S202 |
| `SESSION_HANDOFF_201.md` | (this file) | net-new; **not** banked — `--write` blocked |
| `pipeline_manifest.json` | unchanged | `--write` refused; regeneration carried to S202 |

## Backlog

23 open, up from 22 at S200. Beginning: B99, B98, B97, B101, E28, B93, B90, B94, B89, B100, B102,
B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (22). Resolved: B101 (engine half). Added:
B101-data (parser must emit the flag, then regenerate), B103 (non-distinct rollup emits past its cap
and hides the over-allocation). Ending: B99, B98, B97, B101-data, B103, E28, B93, B90, B94, B89,
B100, B102, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (23). B100 stays blocked, now on
B101-data.
