# SESSION HANDOFF 228

**Turn type:** engine (B113 — enforce the detachment enhancement bearer restriction, Ryan's option
(A) call). Built, tested, and closed cleanly. Full write-up in the backlog's Closed / Shipped
section and D322. `index.html` (v6.20), `e4b_check.js`, `baseline.sh`, `rules_assertions.py` all
changed; `detachments.json`, `units.json`, `unit_loadouts.json`, `wargear_points.json` untouched —
confirmed by all three repro checks staying byte-identical throughout.

## What happened

1. **Open.** Ryan approved option (A) at turn start: enforce the bearer restriction only, leave the
   `LEADER:` attach-enablement unenforced. `./baseline.sh --fetch` clean (28/28, 5 tier-B skipped —
   no sources resident yet).

2. **Pulled the private sources repo directly** (token fetch, not through `--data-turn`, since this
   was reading source to verify a fact for an engine build, not regenerating any output — same
   precedent S227 used reading raw MFM). Needed for two of the eight rows the prose alone didn't
   cleanly resolve:
   - **Butcher Lord** ("World Eaters Infantry model only"): checked every World Eaters Character
     against `Datasheets_keywords.csv`. The two Daemon Princes and the Bloodthirster are Monster,
     Lord on Juggernaut is Mounted — none Infantry. Only **Master of Executions** and
     **Slaughterbound** carry the Infantry keyword. Curated bearer set is these two, not a guess.
   - **Wolf-touched** ("Space Wolves model only"): not a named unit at all — a faction-keyword
     restriction. `units.json`'s `faction_keyword_names` already distinguishes the three
     Space-Wolves-specific Characters (Iron Priest, Wolf Priest, Wolf Guard Battle Leader) from
     generic Adeptus Astartes Characters used in a Space Wolves list, which carry only
     `['Adeptus Astartes']`, statically, with no chapter tag. Enforced as a keyword check, not a
     hardcoded list, so a future Space Wolves Character build extends the restriction automatically.

3. **Re-derived the LEADER: census independently, before writing any code.** New
   `Sources.mfm_leader_lines()` walks the raw MFM DETACHMENTS blocks the same way
   `detachment_parser.py` does (reusing its `clean_chars`/`sniff_is_v1_1`/`normalize_detachments_v1_1`)
   but keeps the `LEADER:` lines the real parser treats as noise. Result: 8, exact row-for-row match
   to S227's D321 finding — not trusted from the prompt, actually re-run.

4. **Confirmed Pact of Cursed Pinions (Murdertalon Raiders) has no bearer text anywhere in the held
   sources.** Checked directly against the raw MFM, the Wahapedia web export
   (`Chaos_Space_Marines_web.txt`), and every raw CSV — genuinely absent, not unparsed. Left
   deliberately unenforced. Explicitly did not assume it shares its sibling Sorrowscent Vulture's
   bearer (Chaos Lord with Jump Pack) just because both enhancements' `LEADER:` line targets Warp
   Talons — different detachments, nothing in source ties the bearers together.

5. **Built the engine change.** `index.html`'s E4b block gains: a curated
   `ENHANCEMENT_BEARER_RESTRICTIONS` table (7 rows — 6 `unit_name`-kind, 1 `faction_keyword`-kind);
   `canAssignEnhancement` checks it right after the existing `unit_type` check (same tier — no
   rearrangement of the rest of the army fixes a bearer mismatch, only swapping the unit does);
   `enhancementRefusalText` gains matching prose for both restriction kinds; `enhancementArmyState`
   gains a `wrongBearer` array folded into `legal`, exactly mirroring the existing `wrongType`
   flag-don't-drop pattern — a stale bearer assignment (data regen, unit swap after assignment)
   surfaces as a warning and the row stays clickable/exitable, never silently dropped.

6. **Extended `e4b_check.js`** with a dedicated B113 section: named-bearer allow/refuse, the
   keyword-kind restriction allow/refuse, confirming Pact of Cursed Pinions stays freely assignable,
   and the stale-assignment flag-don't-drop path. Also threaded `units.json` into the harness (new
   3rd CLI arg) since the keyword check needs `rawUnits`; updated `baseline.sh`'s `e4b_check` gate
   call and `rules_assertions.py`'s `e4b_harness_gate` subprocess call to match. Ran it: pre-existing
   132-row sweep still passes, all new B113 checks pass.

7. **Two new pinned assertions.** E4b-6 re-derives the MFM census from raw source and pins it at 8.
   E4b-7 parses the curated table straight out of `index.html` and checks it against source, not
   just presence: every named-unit row resolves in its army's real resolved unit pool, the Space
   Wolves keyword row is confirmed non-vacuous, and Butcher Lord's set is required to equal the
   source-derived Infantry-keyword World Eaters Character set exactly. Negative-tested E4b-7 before
   trusting it — corrupted a bearer unit name in a scratch copy of `index.html`'s text and confirmed
   the assertion fails with a specific, correctly-attributed message.

8. **Close.** Copied the full GW source set into the workspace to run `rules_assertions.py --tier
   all` and all three repro checks with real data before regenerating the manifest — confirms no
   output JSON was touched (all three repro checks byte-identical) and that 124/124 assertions pass
   (was 121/124 pre-`--write`, the three reds all expected manifest/source-drift from files this
   session legitimately changed). Registered `SESSION_HANDOFF_228.md` in `pipeline_manifest.py`'s
   GUARDED list before running `--write`.

## Not investigated this session

B114, GK §6/§7 — untouched, different turn types (B113 was a full engine turn on its own). Also
untouched: any faction-priority decision (priority order remains fully built, none queued).

## Shipped / changed

- `index.html`: v6.19 → **v6.20**. `ENHANCEMENT_BEARER_RESTRICTIONS` table, `bearer_restriction`
  refusal reason, `wrongBearer` roll-up, matching refusal prose. E4b block only.
- `e4b_check.js`: extended with the B113 test section; now takes `units.json` as an optional 3rd arg.
- `baseline.sh`: `e4b_check` gate now passes `units.json`.
- `rules_assertions.py`: new `Sources.mfm_leader_lines()`, `Sources.all_keywords()`;
  `b113_leader_line_census`/`b113_bearer_table_matches_source` registered as E4b-6/E4b-7;
  `e4b_engine_functions_defined_once`'s guarded-name list extended;
  `e4b_harness_gate`'s subprocess call now passes `units.json`.
- `40K_Decision_Log.md`: D322 appended. `DECISION_INDEX.md`: D322 paragraph appended.
- `OPEN_ITEMS_BACKLOG.md`: header → S228, count 23 → 22 open. B113 entry moved from Open Items to
  Closed / Shipped with the full close write-up.
- `pipeline_manifest.py`: `SESSION_HANDOFF_228.md` appended to GUARDED (before `--write`, per
  protocol). `pipeline_manifest.json`: regenerated by `--write` at close.
- `detachments.json`, `units.json`, `unit_loadouts.json`, `wargear_points.json`,
  `detachment_parser.py`: untouched — confirmed by repro checks.

### Net New Files

None. `e4b_check.js`, `rules_assertions.py`, `index.html`, `baseline.sh` are all updates to
existing files. No new harness, parser, or reference document was created this session.

## Ryan action required

1. **B108** — remove `Thousand_Sons_web.txt` from the public repo (still outstanding, unchanged).
2. **Push the pending queue** — S220 onward, now also carrying this session's changed/new files:
   `index.html`, `e4b_check.js`, `baseline.sh`, `rules_assertions.py`, `40K_Decision_Log.md`,
   `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`/`.json`, this handoff,
   `NEXT_SESSION_PROMPT.md`. `repo_check.py` will keep showing `DIFFERS` until pushed — expected,
   not new.

## Decisions waiting on Ryan

- **B116** — unchanged (Drukhari Harlequins/Anhrathe cross-book allied inclusion; see
  `DRUKHARI_BUILD_SCOPE.md` §6). Own follow-on ticket once Ryan decides; blocks nothing shipped.
- **Next faction after Drukhari** — priority order fully built; none queued. Recommend clearing the
  remaining engine/scoping backlog (B114, GK §6/§7) before revisiting.
- **B113 option (B)** (full attach-enablement) — not raised for a decision; noted only as a possible
  later follow-on per the scope doc, not blocking anything shipped.

## Files (SHA-256, first 12)

Verify these at S229 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `1f506b77f20d` | v6.20; ENHANCEMENT_BEARER_RESTRICTIONS + bearer gate + wrongBearer |
| `e4b_check.js` | `3a066dba4dff` | B113 test section added; takes units.json as 3rd arg |
| `baseline.sh` | `9b1788793b19` | e4b_check gate call passes units.json |
| `rules_assertions.py` | `797aac8ede20` | E4b-6/E4b-7 added; mfm_leader_lines/all_keywords added |
| `40K_Decision_Log.md` | `36039bc8bda8` | D322 appended |
| `DECISION_INDEX.md` | `c20b67b2ef51` | D322 paragraph appended |
| `OPEN_ITEMS_BACKLOG.md` | `a6dfaa9b96d1` | header → S228; B113 moved to Closed/Shipped; count 22 |
| `pipeline_manifest.py` | `2860a8e6f9d6` | SESSION_HANDOFF_228.md appended to GUARDED |
| `NEXT_SESSION_PROMPT.md` | not guarded | informational only, never guarded — S229 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `SESSION_HANDOFF_228.md` | `368e284f8534` | hash not self-referential; checked by `--freshness-check` |

## Backlog

23 open at S227 close; **22 open at S228 close** (B113 closed; nothing else closed; nothing opened).

Beginning: B116, B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23).
Resolved: B113 (1).
Added: none (0).
Ending: B116, B114, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17 (22).
