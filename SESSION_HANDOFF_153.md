# Session Handoff 153

## Baseline at open

`baseline.sh --fetch --data-turn` fetch-verified cleanly (30 overlay files recovered, 75 already
local). Two failures outside the S153 prompt's anticipated set: `rules_assertions` and
`pipeline_manifest` both failed on `OPEN_ITEMS_BACKLOG.md` not matching its blessed manifest hash,
though `repo_check` confirmed the on-disk copy matched the public repo byte-for-byte. Reconciled before
starting: Ryan had appended tickets B69–B73 to the backlog after S152's manifest was last blessed, and
the reissue never happened — the file itself was correct, the manifest was stale. Reissued
(`pipeline_manifest.py --write`); all 23 non-repo gates green, `repo_check`'s only finding the expected
long-standing `40K_Data_Pipeline_Process_v0_6.md` push-pending drift.

## What shipped — D236, CSM turn B (data-only)

**Loadout defaults built.** `repro_check.py` gained `CSM` in `FACTIONS` and `Chaos_Space_Marines` in
`WEB_PASSES` (sixth `equipped_parser.py` pass), plus a docstring correction (five passes → six).
Regenerating `unit_loadouts.json` against source added exactly CSM's 54 units — 0 removed, 0 existing
entries changed — confirmed by set-diff against the committed file before writing it. The added set
matches CSM's own unit_id list in `units.json` exactly. `repro_check.py` now reproduces the result
byte-for-byte.

**A second gap surfaced once CSM had loadout data: `wargear_points.json` was stale.**
`build_wargear_points()` requires a unit to already carry a `unit_loadouts.json` entry before its MFM
WARGEAR OPTIONS lines can resolve — CSM's wargear had been silently skipped at every prior run for that
reason alone, not a bug. E14-1 (the wargear-rebuilds-from-MFM assertion) caught it correctly the moment
CSM's loadout data landed. Regenerated `wargear_points.json` from all MFM files, matching the
established generic-before-chapter file order (`FACTION_BY_MFM`'s own insertion order, remaining files
appended): +2 entries, `000000967` (Hades lascannon, Heavy reaper autocannon) and `000000969`
(Ectoplasma cannon), both sourced to `MFM_Chaos_Space_Marines_v1_0.txt`, 0 existing entries changed. A
first attempt using a naive alphabetical file order reproduced identical prices but re-cited different
(still-correct) provenance on two pre-existing entries — caught by a byte-level diff before committing,
discarded in favor of the canonical order.

**`rules_assertions.py` E14-2 updated 53/33 → 64/44.** The 11-option delta is exactly CSM's 11 own
units' free-seeded adds (Chaos Icon, Havoc launcher, Chaos Familiar, Plasma pistol) — spot-checked
against `_e14_quals()` output before updating the literal.

**Scope call: `detachment_parser.py` / `detachments_repro_check.py` NOT touched, deliberately.** Both
are listed in `CSM_BUILD_SCOPE.md` §6's full build-surface and were named in the S153 prompt's "config
edits," but `units.json` still has no CSM detachment data to regenerate against this session — adding
the config lines now without a same-session regeneration to prove them would leave an inert, unverified
edit in the codebase. Deferred to CSM turn C, when they land together with the actual
`detachments.json` regeneration and diff-trace.

Full baseline: 23/23 gates green (`--no-repo`). Data-only turn throughout — no engine logic changed in
either parser; `repro_check.py`'s edit is config-list plus a docstring correction, `rules_assertions.py`'s
edit is a literal count update to an existing assertion whose ground truth shifted as a direct,
mechanical consequence of the regeneration.

## Housekeeping

- **D231–D234 folded into `40K_Decision_Log_v3_0.md`.** The standalone `D2NN_entry.md` pattern (a
  workaround for the log being evicted under M1) is retired — the log has been workspace-resident since
  S152's fetch. D234's entry was reformatted from the index's bullet style to the log's own `## DNNN —`
  header convention to match D231–D233 and D235. `D231_entry.md` (the only one of the four that was
  guarded) removed from `pipeline_manifest.py`'s `GUARDED` list and deleted; `D232_entry.md`–`D234_entry.md`
  were never guarded (strays, per D235's note) and are also deleted. `DECISION_INDEX.md` unchanged in
  content — it already carried the correct summaries.
- `pipeline_manifest.py`'s handoff chain gained `SESSION_HANDOFF_153.md`.

## Decisions needed

None. The detachment_parser.py deferral above is a sequencing call, not a product/legality question —
made and recorded, not raised for review.

## Net New Files

None. All touched files are updates to existing rolling documents, existing regenerated outputs, or
existing parsers/harnesses.

## Files (SHA-256, first 12 chars)

- `repro_check.py` — `193f7cac0649`
- `unit_loadouts.json` — `41bd25d38b42`
- `wargear_points.json` — `f8013349aae0`
- `rules_assertions.py` — `171cf58ab2bf`
- `pipeline_manifest.py` — `75422688c18c`
- `pipeline_manifest.json` — `dd42769b71d1`
- `40K_Decision_Log_v3_0.md` — `83118d6aadcc`
- `DECISION_INDEX.md` — `7efb917768c8`
- `OPEN_ITEMS_BACKLOG.md` — `3752c3c38a90`
- `SESSION_HANDOFF_153.md` — self-referential; authoritative hash is in `pipeline_manifest.json` (guarded)

Deleted: `D231_entry.md`, `D232_entry.md`, `D233_entry.md`, `D234_entry.md` (folded into the main log).
