# SESSION HANDOFF 194

**Turn type:** tooling-only. B94's pipeline-emit turn shipped; B96 folded in and closed. `index.html`
untouched (correctly — no engine work this turn), stays v6.16. No `units.json` regeneration.

## What happened
1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn` initially failed two gates
   (`rules_assertions`, `pipeline_manifest`) on `OPEN_ITEMS_BACKLOG.md` not matching the manifest.
   Traced before touching anything: cloned the public repo, found a single additive commit (`b9ad46b`,
   Ryan, +53/-1, only that file) between S193 close and S194 open that had added B97/B98/B99 to the
   backlog out of band. Confirmed mount and repo agreed with each other and disagreed only with the
   manifest's stale pinned hash. Regenerated the manifest (`--write`) to reconcile; both gates went
   green. Also confirmed `40K_Decision_Log.md`'s two-session absence from the `/mnt/project` mount is
   mount staleness, not a real gap — present, current, hash-matching in the repo; the fetch step pulls
   it in as an overlay file regardless.
2. **Parser reality checked before designing**, per the prompt. Read `to_points_row`'s fixed-width
   positional row shape and `convert_to_json.py`'s `csv.DictReader` (name-keyed, order-independent)
   reader directly. Confirmed `merge_factions.py` never touches the points schema — it concatenates
   already-built per-army JSON, so no change needed there.
3. **B94 pipeline-emit shipped.** `mfm_points_parser.py`: three new CSV columns (`Points_1-4`,
   `Points_2-4`, `Points_3-4`), unconditional, populated from `info["_esc4_fourth_plus"]` on esc4 units
   and blank elsewhere — same bracket-tier and trailing-blank conventions as every other column.
   `convert_to_json.py`: carries the value into `points.sizes[*].fourth_plus`, but only when a new
   opt-in `--emit-fourth-plus` CLI flag is passed (default off).
4. **Design correction found by testing, not by inspection.** First implementation made the JSON
   carry-through unconditional. `units_repro_check` then failed — Rubric Marines diverged from committed
   `units.json`, because the real GW sources genuinely carry a 4th tier now that the parser captures it,
   so the full from-source pipeline stopped reproducing the currently-committed 3-tier data. This
   directly violated the prompt's "provably inert until the data turn runs it" requirement. Fixed by
   gating the JSON-emission step behind the opt-in flag; `units_repro_check` green again on the second
   pass. This is a mechanism choice (dev-manager decision), not a product/legality call — made and
   recorded here rather than surfaced.
5. **Verified three ways, without regenerating committed `units.json`:** an isolated synthetic
   CSV→JSON round trip; the real parser against `MFM_Thousand_Sons_v1.1.txt` (Rubric Marines'
   `to_points_row` output carries 110/200 in the new columns, Castellan's v1_0 non-esc4 row stays
   blank); a full-CLI Thousand Sons build (transform → points → convert) run twice, flag off vs on,
   diffed — exactly two unit_ids change (Rubric Marines, Chaos Rhino), each gaining a correctly-valued
   `fourth_plus` and nothing else.
6. **`b87_check.js` extended** with a fourth fact pinning the row-level carry-through (esc4 rows carry
   the captured tier; non-esc4 rows carry three blank cells, not a repeated `third_plus`).
7. **B96 folded in and closed.** Moved `b87_check`/`b88_check` from `baseline.sh`'s always-run block
   into the `SOURCES_OK` conditional, matching the three repro checks — they `SKIP` cleanly now on a
   sources-absent open instead of crashing in a way that read identically to a real failure.

## State
- Baseline: green at close under `--fetch --data-turn` (31 gates: 29 pass, repo_check pending push,
  manifest regenerated last).
- `index.html`: untouched, **v6.16**.
- `rules_assertions.py`: untouched this session, 118/118 (no new assertion needed — this turn's
  guarantees are pinned by `b87_check.js`, not the Python assertion suite).
- `mfm_points_parser.py`: emits `Points_1-4/2-4/3-4` unconditionally (blank on non-esc4 units).
- `convert_to_json.py`: `build_units(data, emit_fourth_plus=False)` / `--emit-fourth-plus` CLI flag,
  default off. Every existing call site is unaffected; `units_repro_check` confirmed byte-identical.
- `units.json`: **untouched** — still 3-tier, no row carries `fourth_plus`. The 34 esc4 units' data
  migration remains B94's data turn (folds into B89 per D283), which will invoke the pipeline with
  `--emit-fourth-plus` on purpose.
- `b87_check.js`: 4 facts now (was 3); all pass.
- `baseline.sh`: `b87_check`/`b88_check` moved into the sources-loaded conditional (B96).
- `OPEN_ITEMS_BACKLOG.md`: B96 closed; B94 updated to reflect the shipped pipeline-emit turn with one
  remaining turn (data). 19 open, down from 20 at S194 open (B97/B98/B99 were Ryan's out-of-band
  additions counted at open; B96 closes this session).
- `repo_check` will show drift until pushed: `mfm_points_parser.py`, `convert_to_json.py`,
  `b87_check.js`, `baseline.sh`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `OPEN_ITEMS_BACKLOG.md`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `NEXT_SESSION_PROMPT.md`,
  `SESSION_HANDOFF_194.md` (net-new).

## Ryan action required
1. Push this session's changes.
2. No file-list screenshot needed — this session's mount/manifest question resolved from repo evidence
   without one.

## Decisions still waiting on Ryan
None outstanding. The convert_to_json opt-in-flag mechanism was a dev-manager call, made and recorded
in D287 rather than surfaced. B94's remaining data + assertion turns are sequencing calls I own.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `mfm_points_parser.py` | eb879fa81825 | 3 new `Points_b-4` columns; unconditional emission |
| `convert_to_json.py` | 92273fc5e751 | opt-in `--emit-fourth-plus` / `emit_fourth_plus` param |
| `b87_check.js` | 8630fc6c860e | fact 4 added: row-level 4th-tier carry-through |
| `baseline.sh` | 87b14e715044 | B96: `b87`/`b88` moved into sources-loaded conditional |
| `pipeline_manifest.py` | 6aa0cbd953ae | `SESSION_HANDOFF_194.md` registered in GUARDED |
| `pipeline_manifest.json` | regenerated at close | `--write`, 153 guarded files |
| `OPEN_ITEMS_BACKLOG.md` | 29bd36e187eb | B96 closed; B94 pipeline-emit turn noted; 19 open |
| `40K_Decision_Log.md` | 2956cd1e0e97 | D287 appended |
| `DECISION_INDEX.md` | a199180c9f2f | D287 index entry |
| `NEXT_SESSION_PROMPT.md` | (unguarded by design) | S195 (B94 data turn, folds into B89's first migration) |
| `SESSION_HANDOFF_194.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
19 open, down from 20 at S194 open (B96 closed; B97/B98/B99 were already open, added by Ryan between
S193 and S194). Beginning: B99, B98, B97, E28, B93, B90, B94, B96, B89, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17 (20). Resolved: B96. Added: none. Ending: B99, B98, B97, E28, B93, B90, B94, B89,
B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (19).
