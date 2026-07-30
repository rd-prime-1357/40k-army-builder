# Next-session prompt — Session 160

**Assigned: Thousand Sons turn C (detachments), data-only.** Not turn A — the order is inverted from
the original scope doc, deliberately. See "Why turn C first" below.

## Open at session start

Read `SESSION_HANDOFF_159.md` first, then D243–D247 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch --data-turn`. It closed **26/26** at
the end of S159. Expect the manifest to flag the docs S159 changed if Ryan's repo batch has not been
pushed — reconcile, do not work around.

**Ryan cannot download from the project Files panel.** Any file needed in the repo that lives only in
the project area must be re-delivered by Claude. Build this into close.

## Why turn C first (D245)

Turn A adds six Thousand Sons units carrying `allied_group` — Kairos Fateweaver, Lord of Change,
Flamers, Screamers, Pink Horrors, Blue Horrors. Ungated they are a D0 violation. The gate is
detachment-scoped (E22b, shipped S136/D214), and **Thousand Sons has zero detachments in
`detachments.json`**, so there is nothing to hang the unlock on until turn C lands. E24 records this.

## Read before touching the allied units

Three claims made during S159 were wrong and are corrected in the handoff. In short:

- **`allied_group` is deliberate and must be retained.** B61 shipped it (S133, D208) and four assertions
  (B61-1..4) pin its census. Do not reduce it to a provenance field.
- **The six are not duplicates of Chaos Daemons entries.** Different `unit_id`s, and different points:
  Pink Horrors 115 (TS) vs 150 (CD), Blue Horrors 90 vs 125. Never source TS allied points from the CD
  pool.
- **`SCINTILLATING LEGIONS` is a keyword, not a detachment.** Real TS detachments: Changehost of Deceit,
  Grand Coven, Warpforged Cabal, Warpmeld Pact, Hexwarp Thrallband, Rubricae Phalanx, Ritual of
  Regeneration.

## Turn C scope

1. Parse TS detachments into `detachments.json` via `detachment_parser.py`. Source: the TS faction pack
   (converted markdown) plus existing Wahapedia detachment exports. Verify against
   `detachments_repro_check.py` — byte-identical reproduction required.
2. Add the TS allied unlock to `detachment_effects.json`, mirroring `Death Guard|TALLYBAND SUMMONERS`.
   If turn C does not establish which detachment carries the Scintillating Legions unlock, ship it
   `enforced:false` following the `Chaos Daemons|SHADOW LEGION` precedent, and say so.
3. Extend the B61 census assertions (B61-1..4) to cover the six TS carriers.

**Two new mechanisms surfaced in the packs; scope them here, build only if they fit cleanly.** If either
turns out to be more than a small addition, bank turn C and defer:

- **B78 — detachment-granted unit types.** `SERVANTS OF CHANGE`: "Friendly TZAANGORS units have
  BATTLELINE". Must be a detachment effect, not a datasheet field. Interacts with E22b's per-god
  Battleline ratio, so a promotion changes what is legal.
- **B79 — detachment tag exclusivity.** "This detachment has the MUTANT tag and cannot be taken with
  another MUTANT detachment" — also ENGINES (DG Contagion Engines) and FLYBLOWN (DG Flyblown Host).
  D0 applies: illegal pairings unreachable, not flagged.

## Then, in later sessions

- **Turn A** (units, 328 → 362) once E24's gate exists. Pipeline verified working in S159: TS block in
  `units_repro_check.py` is a transform → mfm-points → convert sequence plus a fifth `--in` on the merge
  call, ~26 lines mirroring Death Guard. `abilities.json` +43 and `weapon_abilities.json` +2 ship with it.
- **Turn B** (loadout defaults) — `Thousand_Sons_web.txt` exists now, so `repro_check.py` gains
  `Thousand_Sons` in `WEB_PASSES` and `TS` in `FACTIONS`. Both change `unit_loadouts.json`, so this is
  its own turn.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
- **B75** — Rules Updates column resolution. Awaiting Ryan's flag counts across the pack set to size it.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo. The faction pack PDFs and their converted `.md`
  files are GW-derived.
- `Thousand_Sons_web.txt` currently sits in the project area and is GW-derived; it belongs in the
  private sources repo instead.
