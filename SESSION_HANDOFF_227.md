# SESSION HANDOFF 227

**Turn type:** typed engine-only (B113 — enforce detachment enhancement `LEADER:` restrictions).
Diagnosed before building and **stopped the build cleanly at open**: the scoped mechanic is wrong.
No engine, data, or assertion change shipped. Output is scoping — `B113_LEADER_RESTRICTION_SCOPE.md`
(net-new), a re-scoped B113, and a decision handed to Ryan. Only committed-file changes are the
four rolling close documents plus one open-time manifest reconciliation. `index.html`,
`detachments.json`, `detachment_parser.py`, `rules_assertions.py` untouched. See D321.

## What happened

1. **Open-time baseline, and a manifest reconciliation before any work.** `./baseline.sh --fetch
   --data-turn` (data-turn used, not the prompt's `--fetch`-only: zero source files were resident in
   the workspace, and the MFM sources are needed both to re-derive the census from source per the
   prompt's item 3 and to run tier-all — the flag runs *more* gate, not less; turn type unaffected).
   Reported 32/34; the two reds were both `SESSION_HANDOFF_226.md` not matching the manifest.
   Reconciled before starting, not carried forward: the committed handoff (`eb4ac9ac4851`) and the
   project-area copy are byte-identical, but the committed manifest banked `ad9575270ad0` — one edit
   behind. This is the D239/D251/B81 "handoff edited after `--write`" slip that S226's
   `--freshness-check` should have caught last and evidently didn't. Re-banked via `--write`;
   diff-guarded that exactly one entry changed (`SESSION_HANDOFF_226.md` `ad9575270ad0` →
   `eb4ac9ac4851`), nothing else added/removed/changed. Both gates then green; full baseline 34/34.

2. **Re-derived the census from source — it is 8, not 6.** Every prior statement (S227 prompt, the
   B113 entry, D311) says 6. Parsing every `ARMY_TO_MFM` v1.1 file with the parser's own line
   handling and v1.1 normalisation finds **8** `LEADER:` lines. The two missed are both **Space
   Wolves** (Saga of the Beastslayer → Wolf-touched → Wulfen / Wulfen w/ Storm Shields; Saga of the
   Great Wolf → Grimnar's Mark → Wolf Guard Terminators), a faction that shipped after B113 opened at
   S217. v1_0 files and unbuilt factions also carry `LEADER:` lines but are not referenced by
   `ARMY_TO_MFM` and are correctly out of scope.

3. **Corrected the binding.** The `LEADER:` line binds to the enhancement **immediately above** it,
   not the last enhancement and not the detachment. It is mid-list in most cases. The B113 entry's
   "Khorne Daemonkin's Icon of War" was wrong — that case is **Disciple of Khorne**; Icon of War
   sits below the line and is unrestricted. Confirmed against the 10e rules text already in
   `detachments.json`, which names the same target unit under the same enhancement and leaves the
   others (incl. the one printed directly above) untouched.

4. **The decisive finding: `LEADER:` is an attach-ENABLER, not an assignment restriction.** The
   named units are bodyguard units the bearer normally cannot lead. Checked against the app's own
   `leaderEligible` / `canAttachLeader` model: for six of eight targets (Warp Talons, Wulfen ×2,
   Jakhals, Goremongers, Bloodcrushers, Flesh Hounds) **no leader in the faction can attach at
   all**, and in every case the intended bearer attaches elsewhere (Chaos Lord w/ Jump Pack →
   Raptors, not Warp Talons; Lord on Juggernaut → Eightbound/Berzerkers, not Bloodcrushers/Flesh
   Hounds). The S227 prompt's "refuse the enhancement unless the leader is already attached to the
   named unit" would therefore make these enhancements assignable to **nobody**, because the app
   won't permit the prerequisite attachment — strictly worse than the over-permissive present state
   and the opposite of D0. The reachable illegal state is the "X model only" **bearer restriction**
   in the description prose (any Character can currently take Disciple of Khorne, when only a Lord on
   Juggernaut should), which is not on the `LEADER:` line.

5. **Stopped, wrote it up, handed Ryan the decision.** Full write-up in
   `B113_LEADER_RESTRICTION_SCOPE.md`. B113 stays open, re-scoped, decision-ready — not closed.
   Recommended mechanic is (A) enforce the bearer restriction only; do not build the prompt's
   attach-target assignment gate under any option. The corrected census and binding are the settled
   inputs and should land as a `rules_assertions.py` census check at the top of the eventual build.

## Not investigated this session

B114, GK §6/§7 — untouched, different turn types. No engine/data/assertion change was made because
none is correct until Ryan settles the B113 mechanic.

## State at close

- `B113_LEADER_RESTRICTION_SCOPE.md`: net-new; the corrected census, binding, attach-enabler
  finding, and the (A)/(B)/(C) options.
- `40K_Decision_Log.md`: D321 appended. `DECISION_INDEX.md`: D321 line appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header → S227; B113 entry rewritten (re-scoped, corrected census,
  decision-pending). Count unchanged at 23.
- `pipeline_manifest.py`: `SESSION_HANDOFF_227.md` appended to GUARDED. `pipeline_manifest.json`:
  re-banked at open (one entry) and again by `--write` at close.
- `index.html`, `detachments.json`, `detachment_parser.py`, `rules_assertions.py`,
  `unit_loadouts.json`, `units.json`, `wargear_points.json`: untouched.

## Ryan action required

1. **B113 mechanic decision** — pick (A)/(B)/(C) per `B113_LEADER_RESTRICTION_SCOPE.md` §4.
   Recommended: (A). Blocks the B113 build only; nothing shipped depends on it.
2. **B108** — remove `Thousand_Sons_web.txt` from the public repo (still outstanding, unchanged).
3. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md`** (outstanding from S220).
4. **Push `pipeline_manifest.json`** (outstanding from S223's open-time reconciliation).
5. Push this session's changed/new files: `B113_LEADER_RESTRICTION_SCOPE.md`, `40K_Decision_Log.md`,
   `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`/`.json`, this handoff,
   `NEXT_SESSION_PROMPT.md`. Adds to the same pending push queue as S223–S226; `repo_check.py` will
   keep showing `DIFFERS` until pushed — expected, not new.

## Decisions waiting on Ryan

- **B113 mechanic** — (A)/(B)/(C) above; recommended (A).
- **B116** — unchanged (Drukhari Harlequins/Anhrathe cross-book allied inclusion; see
  `DRUKHARI_BUILD_SCOPE.md` §6). Own follow-on ticket once Ryan decides; blocks nothing shipped.
- **Next faction after Drukhari** — priority order fully built; none queued. Recommend clearing the
  engine/scoping backlog (B113, B114, GK §6/§7) before revisiting.

## Files (SHA-256, first 12)

Verify these at S228 open.

| file | sha256:12 | note |
|------|-----------|------|
| `B113_LEADER_RESTRICTION_SCOPE.md` | `1c976fa1febd` | net-new; B113 diagnosis + options |
| `40K_Decision_Log.md` | `41907ca55161` | D321 appended |
| `DECISION_INDEX.md` | `1ebdd03f42ad` | D321 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `9b4f2a6a4af8` | header → S227; B113 entry re-scoped; count 23 |
| `pipeline_manifest.py` | `5bc07c28d07f` | `SESSION_HANDOFF_227.md` appended to GUARDED |
| `NEXT_SESSION_PROMPT.md` | `e395adb9f708` | informational only, never guarded — S228 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate, not this row |
| `SESSION_HANDOFF_227.md` | (this file) | hash not self-referential; banked by `--write`, checked by `--freshness-check` |

## Net New Files

`B113_LEADER_RESTRICTION_SCOPE.md` — the project has held no B113 scope/diagnosis document before.
Everything else this turn is an update to an existing rolling document or the manifest.

## Backlog

23 open at S226 close; **23 open at S227 close** (unchanged — B113 was worked but stayed open,
re-scoped, not closed; nothing else closed, nothing opened).

Beginning: B116, B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23). Resolved: none (0). Added: none (0). Ending: B116, B114,
B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17 (23).
