# Session Handoff 152

## Baseline at open

`baseline.sh --fetch` came up exactly as the S152 prompt anticipated: 22/25 green, with
`repro_check` and `rules_assertions` both failing on the same seven B68 unit_ids
(`000001046`–`000001050`, `000002461`, `000004209`) and `repo_check` failing. No unexpected
regression. `repo_check` was down to a single push-pending drift (`40K_Data_Pipeline_Process_v0_6.md`)
— `baseline.sh` and `pipeline_manifest.py` had been pushed since S151, clearing two of the three the
S151 handoff flagged. Nothing to reconcile; started B68.

The fetch overlay recovered the M1-evicted repo-resident set (including `40K_Decision_Log_v3_0.md`,
`repro_check.py`, and the numbered handoffs), so the full decision log is workspace-resident again this
session.

## What shipped — D235, B68 closed (engine-only)

**Diagnosis corrected.** D230 named both `loadout_parser.py` and `equipped_parser.py`. The bug is in
`equipped_parser.py` alone. `loadout_parser.py` is unit_id-keyed throughout; its one name-keyed
structure (`ds_by_name`) is dead — built at the top of `main()`, never read. Byte-identical
reproduction with the `equipped_parser.py` change alone proves it needs no change for B68. The dead
`ds_by_name` is left in place (removing it is tidiness, not a positive reason).

**Root cause.** `load_roster` built one flat `name2id` (name → unit_id, last-write-wins across every
army block). `find_titles`/`segment` resolve each web-composition datasheet title through it. Death
Guard and Chaos Space Marines each carry their own datasheet for seven generic Chaos vehicles
(Helbrute, Chaos Rhino, Chaos Spawn, Chaos Land Raider, Chaos Predator Annihilator, Chaos Predator
Destructor, Defiler) — same name, distinct unit_ids. CSM sits after DG in `units.json`, so once CSM
was present the flat map pointed all seven names at the CSM unit_id. The Death Guard web pass then
routed its equipped lines to CSM ids that aren't in the SM+DG loadouts dict; the update silently
vanished and the seven DG entries kept the loadout-parser default (`_defaults_source` unset) instead
of the committed `equipped` values. That is the entire seven-unit divergence.

**Fix.** `load_roster` now also returns every candidate per name (`name_cands`) and the set of army
block names (`army_blocks`). A new `scoped_name2id(name_cands, army_blocks, composition_path)` infers
the owning faction from the composition filename (`<Army_Name>_web.txt` → `<Army Name>`, used only if
that string is a real block in `units.json`) and, for a name with more than one candidate, prefers the
candidate in that block. Single-candidate names, and passes with no inferable block scope (Space
Marines — codex spans many blocks, no single block; the datasheets pass over `os.devnull`), fall
through to the old flat last-write-wins behaviour unchanged. `main()` builds `name2id` via this helper;
`find_titles`/`segment` are untouched. Added `os` to the import line.

**No caller changed.** The scope is read from the `--composition` filename the chain already passes, so
`repro_check.py`, `baseline.sh`, and any production invocation keep the same argument shape — this
stayed a pure `equipped_parser.py` engine turn with no tooling edit, as turn typing requires.

**Proven surgical, then proven correct.** Before editing the parser: a simulation of scoped-vs-flat
resolution across all five web passes differed on exactly the seven Death Guard collisions and nothing
else. After the fix: `repro_check.py` reproduces the committed `unit_loadouts.json` byte-for-byte. No
data file was regenerated — the committed file predates CSM co-presence and was already correct; the
fix only restores the parser's ability to reproduce it.

**Durable for CSM turn B.** The same mechanism routes the future CSM web pass correctly:
`Chaos_Space_Marines_web.txt` infers the "Chaos Space Marines" block (which exists), so its shared
vehicles resolve to CSM ids while Death Guard's continue resolving to DG ids. **The CSM web file must
keep exactly that name for the inference to hold.**

## Manifest / backlog housekeeping

- Re-blessed `pipeline_manifest.json` for the edited `equipped_parser.py`; appended
  `SESSION_HANDOFF_152.md` to `GUARDED` and regenerated (105 guarded files).
- D235 recorded directly in `40K_Decision_Log_v3_0.md` (canonical log, now workspace-resident) and in
  `DECISION_INDEX.md`. **The standalone `D2NN_entry.md` pattern (D231–D234) was a workaround for the log
  being evicted under M1; that condition no longer holds. Recommend retiring it and folding
  `D232`–`D234` back into the main log next session** (D231 is already guarded/appended; D232–D234 are
  strays). No standalone `D235_entry.md` was created.
- B68 moved to Closed / Shipped. P4 heading's stale "B68 NEXT" tag corrected to "M2 NEXT".

## Decisions needed

- **Push `equipped_parser.py`, `pipeline_manifest.json`, `pipeline_manifest.py`,
  `40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, and
  `SESSION_HANDOFF_152.md`** in the next batch, plus the still-pending
  `40K_Data_Pipeline_Process_v0_6.md`. Closes every live `repo_check` drift. Recommend yes; low-cost,
  reversible. Proceeding on this unless you object.

## Net New Files

None. `SESSION_HANDOFF_152.md` is a rolling handoff (role the project has always held); every other
touched file is an update.

## Files (SHA-256, first 12 chars)

- `equipped_parser.py` — `8c9a5049f9eb`
- `pipeline_manifest.json` — `425cffd2a2d4`
- `pipeline_manifest.py` — `71f0403ed9de`
- `40K_Decision_Log_v3_0.md` — `9a571f8d31a1`
- `DECISION_INDEX.md` — `c8265fc6a84c`
- `OPEN_ITEMS_BACKLOG.md` — `4c364cfa28fd`
- `SESSION_HANDOFF_152.md` — self-referential; authoritative hash is in `pipeline_manifest.json` (guarded)
