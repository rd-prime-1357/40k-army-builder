# SESSION HANDOFF 223

**Turn type:** tooling-only (B115 — fix `wahapedia_transform.py`'s Drukhari faction-selection bug).
`wahapedia_transform.py` changed; `pipeline_manifest.json` regenerated to match. No `units.json`,
`unit_loadouts.json`, `detachments.json`, or `detachment_effects.json` touched. Closes **B115**.

## What happened

1. **Open-time gate failure, reconciled before starting assigned work.** `./baseline.sh --fetch
   --data-turn` failed `pipeline_manifest.py`'s plain check: `SESSION_HANDOFF_222.md` and
   `wargear_points.json` did not match the hashes `--write` banked at S222 close. Verified rather
   than assumed: a fresh clone of the public repo agreed byte-for-byte with the local project-area
   copy of both files (no CRLF/BOM artifact either — checked directly), so neither file is stale or
   corrupted relative to what's actually live; `wargear_points.json` also independently reproduces
   byte-for-byte from the current pipeline (`units_repro_check` passed against it). Every other one
   of the 183 guarded entries matched clean — this was isolated to exactly the two files S222's own
   close protocol structurally cannot self-verify (a handoff can't list its own hash; S222 never
   touched `wargear_points.json`, so nothing in that session's own checks would have caught a stale
   entry for it). Reconciled by re-running `pipeline_manifest.py --write` against the verified-
   correct live state — confirmed by diff that only those two entries changed, guarded-file count
   unchanged (183) — then full baseline passed clean (31/31, 34/34 with `repo_check`). Root cause is
   unconfirmed; there's no surviving evidence to chase it further, and the plain manifest check
   already did its job by catching the drift at the very next session's open. See D317.

2. **B115 re-derived from source, not trusted from S222.** Confirmed directly:
   `wahapedia_transform.py --faction DRU` selects 37 datasheets against a real 23-unit roster; the
   14 extras are genuinely Aeldari-book content (Harlequins/Aeldari-Corsairs), zero MFM points
   entries anywhere in `MFM_Drukhari_v1.1.txt`.

3. **Both fix shapes from the prompt tested before any code changed, not just the recommended one.**
   The "preferred" generalized version — exclude a datasheet if its source is itself a different,
   real Factions.csv faction's own Faction Pack — was run against every faction_id (built and
   unbuilt) as a dry simulation first. It fixes Drukhari cleanly and correctly leaves Space Marines
   untouched (chapter packs like Black Templars/Blood Angels have no standalone Factions.csv entry
   of their own, so the rule never fires on them). But it would have broken the already-shipped
   **Chaos Space Marines** roster: `CSM_BUILD_SCOPE.md` §4 (D240, S157) documents that CSM's four
   cult-troop units (Khorne Berzerkers, Rubric Marines, Plague Marines, Noise Marines) are
   legitimately `faction_id=CSM` but have zero points entries in CSM's own MFM file at all —
   confirmed directly (`grep` for each name against `MFM_Chaos_Space_Marines_v1.1.txt` returns
   nothing) — and ship via a deliberate, separately-scoped MFM append against their own Legion's
   book, specifically because `wahapedia_transform.py --faction CSM`'s raw selection is expected to
   surface them by faction_id first. Confirmed by direct set comparison, not just counts: that raw
   selection is currently byte-identical to CSM's shipped 58-unit roster. The generalized filter
   would have silently dropped all four out of that selection on any future rebuild — a live
   regression to an already-shipped, intentionally-engineered mechanism, not a hypothetical one.
   Chaos Daemons' 21 and Chaos Knights' 7 CSM-Faction-Pack-sourced candidates are dormant either
   way (confirmed absent from CD's shipped 53-unit roster; the Shadow Legion allied-unlock in
   `detachment_effects.json` reads CSM's own `units.json` by keyword at the engine level, never this
   raw selection) — so only Aeldari→Drukhari is a real, live mistag today.

4. **Shipped the targeted fix instead.** A small `FOREIGN_SOURCE_OWNER` map in
   `wahapedia_transform.py` (`source_id -> the one faction_id it legitimately belongs to`; one entry
   today, Aeldari's `source_id` → `AE`), threaded through `source_is_excluded(src_row, faction)`.
   Verified by exact datasheet-id-set comparison across every faction_id, old vs new: **DRU is the
   only faction that changes** (37→23, exactly the 14 Aeldari-tagged datasheets dropped, nothing
   added); every other faction_id, built or not, is byte-identical.

5. **Downstream re-verified, not just the selection count.** Running the fixed transform +
   `mfm_points_parser.py` against the corrected 23-datasheet selection reports **zero** "datasheets
   with no MFM points" (was 14), the same 7 Legends-only MFM entries with no datasheet match, and
   the same one attach-list drop (Archon → Court of the Archon, B73/D260) — an exact match to
   S222's numbers, now proven by rerun rather than carried forward as prose.

6. **Full baseline re-run with the fix in place.** All three repro checks byte-identical,
   `rules_assertions` 121/122 (the one red was the expected P3 manifest-drift for the just-edited
   `wahapedia_transform.py`, cleared by `--write` at this session's close), every harness clean —
   zero regression to any already-built faction.

7. **No units or detachments build started**, per the tooling-only turn type and the prompt's
   explicit instruction not to begin the Drukhari data turn this session.

## Not investigated this session

B113, B114, GK §6/§7 remain untouched — none intersected with B115 directly, and each is a
different turn type (engine or scoping), which the tooling-only turn type this session doesn't
mix with per the standing rule.

## State at close

- `wahapedia_transform.py`: `FOREIGN_SOURCE_OWNER` map added; `source_is_excluded` and
  `select_datasheets` now faction-aware. Only call site of `source_is_excluded` in the codebase;
  no other file imports it, confirmed by search before editing.
- `pipeline_manifest.json`: regenerated twice this session — once to reconcile the open-time drift
  (`SESSION_HANDOFF_222.md`, `wargear_points.json`), once more at close for
  `wahapedia_transform.py` and this handoff.
- `40K_Decision_Log.md`: D317 appended (open-time reconciliation + B115 fix, full account).
  `DECISION_INDEX.md`: D317 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S223, count **24 → 23**. B115 removed from Open
  Items, full body moved to Closed / Shipped with a **Closed S223 (D317)** paragraph appended,
  per standing convention.
- `units.json`, `unit_loadouts.json`, `detachments.json`, `detachment_effects.json`,
  `faction_taxonomy.json`, `mfm_points_parser.py`, `detachment_parser.py`: untouched.
- `index.html`: untouched.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged).
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (still outstanding
   from S220).
3. Push this session's new/changed files to the public repo, **including `pipeline_manifest.json`**
   — the open-time reconciliation means the copy currently in the repo does not yet match the local
   copy for two entries (`SESSION_HANDOFF_222.md`, `wargear_points.json`); `repo_check.py` will flag
   this as a `DIFFERS` finding until pushed, which is expected, not a new problem.

## Decisions waiting on Ryan

**B116** — unchanged from S222 (Drukhari's Harlequins/Anhrathe allied-inclusion mechanic; see
`DRUKHARI_BUILD_SCOPE.md` §6). Not touched this session.

## Files (SHA-256, first 12)

Verify these at S224 open.

| file | sha256:12 | note |
|------|-----------|------|
| `wahapedia_transform.py` | `a42271eaf8a7` | `FOREIGN_SOURCE_OWNER` map + faction-aware `source_is_excluded` (B115) |
| `40K_Decision_Log.md` | `d2e80f51b4d7` | D317 appended |
| `DECISION_INDEX.md` | `0babb646eb1b` | D317 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `b315594ddfae` | ledger header S223, 24 → 23 (B115 closed) |
| `pipeline_manifest.py` | (computed after this row is written, see note) | `SESSION_HANDOFF_223.md` appended to GUARDED |
| `pipeline_manifest.json` | (hash not self-referential — same reason as this handoff's own row) | regenerated by `--write` at close |
| `NEXT_SESSION_PROMPT.md` | (informational only, never guarded — see `pipeline_manifest.py`'s documented exclusions) | S224 |
| `SESSION_HANDOFF_223.md` | (this file, hash not self-referential) | |

**Note on `pipeline_manifest.py`'s own row:** left uncomputed here deliberately. Filling it in would
mean editing this file after typing the value, which is exactly the class of post-write edit that
produced this session's open-time drift (D317) — this file's own final hash is only known once
`--write` has run against it, by which point editing this table further would invalidate the hash
`--write` just banked for this handoff. Verify `pipeline_manifest.py` and `pipeline_manifest.json`
directly against `pipeline_manifest.json` itself at S224 open (`python3 pipeline_manifest.py`) —
that check doesn't depend on this table being complete.

## Net New Files

None this session. `wahapedia_transform.py`, the decision log, decision index, backlog,
`pipeline_manifest.py`/`.json`, and the next-session prompt are all updates to files the project
has held before — no new role created.

## Backlog

24 open at S222 close; **23 open at S223 close** (B115 closed — `wahapedia_transform.py`'s Drukhari
faction-selection bug, fixed and verified with zero regression to any built faction; nothing new
opened).

Beginning: B116, B115, B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17 (24). Resolved: B115 (1). Added: none (0). Ending: B116,
B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23,
B67b, E12, B17 (23).
