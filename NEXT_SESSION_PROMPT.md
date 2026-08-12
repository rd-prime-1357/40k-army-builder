# NEXT SESSION PROMPT — Session 231

## Recommended turn type: pipeline (build B114 for real), or scoping — GK §6/§7.
## Neither is blocked on a Ryan decision.

B114 was scoped twice without building: S229 (D323) found the stored effect had no consuming
engine code and pulled the real 21-unit set from source; S230 (D324) attempted the build and found
S229's "tag the existing CSM entries" plan was wrong about the size of the job. Read
`SESSION_HANDOFF_230.md` and `B114_SHADOW_LEGION_SCOPE.md` §6 first.

Short version: the four shipped allied_group precedents (Plague Legions, Scintillating Legions,
Legions of Excess, Blood Legions) each source their allied entries from a separate, real Wahapedia
datasheet ID — the destination faction's own book-variant of the unit, with faction-flavored
ability text — not the native entry copied with a tag added. `Datasheets.csv` carries a distinct
`CD`-faction, `source_id 000000012` row for all 21 Shadow Legion units (14 named + 7 "Damned"),
confirmed present, none yet in `units.json`. Supporting source files (abilities, models,
models_cost, options, unit_composition, wargear) confirmed present for a 5-unit spot check.

Recommended build: run the pipeline (`wahapedia_transform.py`, `loadout_parser.py`,
`equipped_parser.py`, `convert_to_json.py`, `merge_factions.py`) against the 21 CD-faction datasheet
IDs to generate 21 new entries in the Chaos Daemons block of `units.json`, tagged
`allied_group: "Shadow Legion Thralls"`. Then retarget `detachment_effects.json`'s Shadow Legion
unlock to `{"allied_group": "Shadow Legion Thralls"}`, `enforced: true` (points_cap table unchanged,
already correct). Add a pinned census assertion (same shape as B113's E4b-6/E4b-7) checking the
21-unit set against source. Do NOT add a Warlord-ban effect — checked directly, the ability carries
no such clause (unlike Plague Legions).

This is sized like a small faction-build turn, not a two-file data edit — treat it as its own
session rather than folding it into something else. Open with `./baseline.sh --fetch --data-turn`.
Verify S230's Files table hashes against `pipeline_manifest.json` before starting.

## Open, at your discretion

- **B114 build** — per the recommendation above. Re-derive the 21-unit set and the 21 CD-faction
  datasheet IDs from source yourself at build time rather than trusting this prompt's numbers —
  they've now been independently confirmed twice (S229, S230), but standing practice still applies.
- **GK §6 / §7** — carried unchanged for several sessions; still not investigated. Different turn
  type from B114's build — don't mix.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's numbers.
- Turn typing stays strict. B114's build touches the pipeline and `units.json` and
  `detachment_effects.json` — treat as its own turn type (pipeline/data), separate from GK §6/§7
  scoping if both are considered.
- Diff-guard the `units.json` change: the 21 new Chaos Daemons-block entries should be the ONLY
  addition — zero removals, zero other fields touched anywhere else in the file. Same discipline as
  every prior data turn, and the same discipline the original Plague Legions/Scintillating
  Legions/Legions of Excess/Blood Legions builds were held to.

## Decisions waiting on Ryan

- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic (see
  `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides. Does not block
  anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction is
  queued. Recommendation stands: clear the remaining engine/scoping backlog (B114's build, GK
  §6/§7) before revisiting which faction, if any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_231.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
