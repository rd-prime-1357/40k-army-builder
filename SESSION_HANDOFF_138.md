# Session Handoff 138

## Baseline at open

All four S137 hashes verified byte-identical against `SESSION_HANDOFF_137.md` before anything
started. Full baseline ran clean, 23/23, before any new work began.

E21d piece 3 (the stranded-allied roster warning) was not confirmed by Ryan in-conversation at
session open, so per the S137 prompt's own fallback instruction the session opened elsewhere in
the backlog: **B62**.

## What shipped — B62

**Turn type: data-only.** `index.html` untouched.

**Finding: the D205 quirk was not harmless.** Keeper of Secrets' Shining Aegis and Soul Grinder's
Warpclaw carried the literal string `"FALSE"` in `Is Base Equipment`, filed at D205 as inert. It
was not — a non-empty string is truthy in both Python and JavaScript, so `is_base_equipment`
evaluated as **true** for both weapons everywhere it was read truthily. Checked against
`Unit_Wargear_Options.csv` to confirm the correct value: both are replacement options (Shining
Aegis replaces Witstealer sword, Warpclaw replaces Warpsword), so `false` is right.
`shouldDimWeapon` was shielded by a second, independent replacement-detection check, so nothing
visibly broke there — but `activeWeaponStatOverrides` had no such second check, and Shining
Aegis's stat effect could apply even when the weapon wasn't selected. Live since the CSVs were
rebuilt at D205.

**The fix.** `convert_to_json.py`'s `clean()` now recognises `true`/`false` (any case) as booleans
alongside `yes`/`no`. `units.json` regenerated through the full documented pipeline and the
committed file overwritten — verified the rebuild changed **only** the two expected weapon records;
every other unit and all four merged glossary lookups byte-identical before trusting the overwrite.
`units_repro_check.py` re-verified clean against the new fixed point. No `index.html` change was
needed — both read sites already treat the field by truthiness, so correcting the data was
sufficient.

**Presence-and-parse gate.** New assertion `B62-1` in `rules_assertions.py`: checks each of the
nine Gen-1 Chaos Daemons root CSVs is present, non-empty, and carries its expected header columns.
Verified it fires by removing `Rules.csv` and confirming a named failure, then restored and
confirmed a clean pass. This is the gate D205 asked for — a missing or truncated CD root CSV now
fails loudly and by name instead of surfacing as a confusing `units.json` repro mismatch.

`pipeline_manifest.json` reissued for the three changed guarded files. **B62 closes.** Recorded as
**D216**.

## Gap: `BACKLOG_ARCHIVE.md` not in the project mount this session

B62's full ticket body should move from `OPEN_ITEMS_BACKLOG.md` into `BACKLOG_ARCHIVE.md` per the
S126 (T5) convention, with a one-line pointer left behind. The pointer is done — added to
`OPEN_ITEMS_BACKLOG.md`'s Closed/Shipped section — but `BACKLOG_ARCHIVE.md` itself was not present
in `/mnt/project` this session (confirmed via project knowledge search: the file exists and is
indexed, so this reads as a mount staleness gap per D210, not a real loss). Per the standing rule,
this is not assumed either way — B62's full body was **not** appended to a reconstructed archive
file, to avoid risking a duplicate or a bad merge against content this session couldn't see.
**Ryan: if convenient, re-upload/refresh `BACKLOG_ARCHIVE.md` to the project area** — next session
will append B62's body once it's confirmed present, and check nothing else silently dropped out of
the mount the same way.

## Decisions needed

None blocking. The `BACKLOG_ARCHIVE.md` gap above is a small housekeeping item, not a decision.

**Still outstanding from S137:** E21d piece 3 — D214's recommendation (flag a stranded Plague
Legions unit as a visible roster error, never a silent trim or a blocked deselect) needs your
confirmation before it's built. Same lasting-precedent reasoning as before.

## Shipped / changed

`convert_to_json.py` — `clean()` extended to recognise `true`/`false` as booleans. `units.json` —
regenerated; only the two Chaos Daemons weapon records changed. `rules_assertions.py` — new
`B62-1` assertion (101/101 total). `pipeline_manifest.json` — reissued. `40K_Decision_Log_v3_0.md`
— **D216** appended. `DECISION_INDEX.md` — D216 indexed. `OPEN_ITEMS_BACKLOG.md` — B62 removed from
Open Items, pointer added to Closed/Shipped, header count 8 → 7.

### Net New Files
None.

### Files (SHA-256, first 12 chars)
- `convert_to_json.py` — `8456dcefa7f7`
- `units.json` — `999c5c2c37dc`
- `rules_assertions.py` — `c74ce18a1aaa`
- `pipeline_manifest.json` — `1dff84b9a83b`
- `40K_Decision_Log_v3_0.md` — `54b9f327675d`
- `DECISION_INDEX.md` — `0849aafa6c1d`
- `OPEN_ITEMS_BACKLOG.md` — `086a9760f17c`

## Backlog summary

- **Beginning (8 open):** B62, P2, P4, E21 (piece 3 only), E23, B60, E12, B17
- **Resolved (1 fully closed):** B62 (D216)
- **Added (0 new this session):** none
- **Ending (7 open):** P2, P4, E21 (piece 3 only), E23, B60, E12, B17
