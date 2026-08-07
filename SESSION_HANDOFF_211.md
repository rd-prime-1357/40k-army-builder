# SESSION HANDOFF 211

**Turn type:** data-only (Emperor's Children detachments, D305). `detachment_parser.py`,
`detachments.json`, `detachment_effects.json`, and `faction_taxonomy.json` changed. No engine
file (`index.html`, `loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`) touched.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 34 gates, sources
   loaded (85 files verified against `source_manifest.json`), 122/122 assertions, all three
   repro checks byte-identical. `repo_check` red on exactly the pre-existing B108 finding
   (`Thousand_Sons_web.txt` in the public repo), unchanged. Public repo confirmed current
   through S210 via direct clone and SHA-256 verification against S210's handoff table — all
   nine listed hashes matched exactly, not assumed from the mount.

2. **Emperor's Children registered in `detachment_parser.py`'s three maps** — `ARMY_TO_MFM`,
   `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION` — pointed at `MFM_Emperors_Children_v1.1.txt` per
   D293. This deliberately does **not** mirror the existing Thousand Sons/Chaos Space
   Marines/Death Guard registrations, which turned out to still point at v1_0 files (see
   finding #5 below) — confirmed by direct `sniff_is_v1_1()` check against the actual
   registered file content before assuming the existing pattern was safe to copy.

3. **Built cleanly from v1.1.** 10 detachments parsed, DP costs 1–3, zero unique tags — matching
   the S209 scope doc's prediction exactly. All four predicted force-disposition changes landed
   correctly on first build: Carnival of Excess (Priority Assets → Disruption), Coterie of the
   Conceited (Purge the Foe → Priority Assets), Frenzied Host (Disruption → Reconnaissance),
   Spectacle of Slaughter (Purge the Foe → Disruption). Diff-guarded against the committed
   `detachments.json` at army-block level: **exactly Emperor's Children's block added (10
   detachments), 0 changed/removed elsewhere** — 179 total distinct detachment records across
   17 armies (was 16). `detachments_repro_check.py` passes byte-identical.

4. **One hand-authored `detachment_effects.json` entry.** Scanned all 10 EC detachments' full
   `rule_text` directly (not assumed) for army-construction-relevant shapes — unlock, forbid,
   battleline, warlord, tank_ace. Only Carnival of Excess qualifies: its "Daemonic Empowerment"
   rule carries a Legions of Excess allied-group unlock (500/1000/1500 pts cap by battle size,
   matching Death Guard's Plague Legions and Thousand Sons' Scintillating Legions exactly) plus
   a "no Legions of Excess model can be your Warlord" restriction. Authored
   `Emperor's Children|CARNIVAL OF EXCESS` using the identical `unlock` + `warlord: cannot_be`
   two-effect shape as Thousand Sons' `CHANGEHOST OF DECEIT` entry. Appended at file end,
   preserving the file's existing (non-alphabetical) insertion-order convention so the diff is
   a pure addition. Diff-guarded: **exactly one key added, 0 changed/removed elsewhere.**

5. **Real, pre-existing bug found in three already-shipped factions — NOT fixed this session.**
   Direct parse-and-diff of each registered v1_0 detachment file against its v1.1 counterpart
   (Chaos Space Marines, Death Guard, Thousand Sons — Chaos Daemons has no v1.1 detachment file
   to compare against) surfaced real, already-shipped discrepancies beyond the disposition drift
   `MFM_v1_1_Reconciliation.md` (B89's own work order) already flagged at migration time:
   - **Thousand Sons — Hexwarp Thrallband priced 2 DP, should be 3 DP** (a real cost bug, not
     just flavor drift).
   - **Chaos Space Marines — Soulforged Warpack's Tempting Addendum enhancement priced 25 pts,
     should be 40 pts.**
   - Six force-disposition mismatches: Thousand Sons (Ritual of Regeneration, Sekhetar Cohort,
     Warpforged Cabal), Chaos Space Marines (Murdertalon Raiders, Soulforged Warpack), Death
     Guard (Contagion Engines).
   Not new — B89 already flagged all of these as "investigate-first" at migration time and has
   stayed open since; this session's direct comparison confirms the detachment-side work for
   these three factions was never finished. Not fixed here: three different factions' committed
   data, out of scope for an Emperor's-Children-only data turn — would violate turn typing.
   Added a dated note to B89's body in `OPEN_ITEMS_BACKLOG.md` with the confirmed specifics
   rather than opening a new ticket, and recommended it as B89's next data turn.

6. **`faction_taxonomy.json` updated.** Emperor's Children's entry: `built: false` → `true`,
   `data_army: "Emperor's Children"` added — matching the shape every other built Chaos faction
   entry already has. This is the point at which the flip is correct: both units (D304) and
   detachments (D305, this session) are complete. Grey Knights' entry is untouched and stays
   `built: false` — B110 remains unresolved, still needs Ryan's sequencing call (Grey Knights
   detachments vs. next-in-priority faction).

## State at close

- `detachments.json`: +10 Emperor's Children detachments, 0 changed/removed elsewhere.
  `detachments_repro_check.py` byte-identical. 179 total detachment records, 17 armies.
- `detachment_effects.json`: +1 entry (`Emperor's Children|CARNIVAL OF EXCESS`), 0
  changed/removed elsewhere, insertion order preserved.
- `detachment_parser.py`: `EC` added to `ARMY_TO_MFM` (pointed at v1.1), `MFM_SOURCE_NAME`,
  `ARMY_TO_WAHA_FACTION`.
- `faction_taxonomy.json`: Emperor's Children `built: true`, `data_army` added. Grey Knights
  unchanged (`built: false`, per B110).
- `40K_Decision_Log.md`: D305 appended.
- `DECISION_INDEX.md`: D305 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: top summary updated (24 open, unchanged count — nothing closed,
  nothing new opened); B89's body gained a dated finding with the confirmed v1_0-sourcing
  evidence for CSM/DG/TS detachments.
- `units.json`, `unit_loadouts.json`, `abilities.json`, `weapon_abilities.json`,
  `wargear_points.json`, `datasheet_wargear_abilities.json`, `rules_assertions.py`,
  `index.html`, `loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`,
  `bundled_swaps.json`: **untouched.**
- 122/122 assertions pass (unchanged count — no new assertion needed this session).
- `units_repro_check.py`, `repro_check.py`, `detachments_repro_check.py`: all byte-identical.
- All 26 JS harness gates re-run and pass with correct arguments per `baseline.sh`.
- Emperor's Children is **fully built**: 23/23 units, 10/10 detachments, `built: true`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding,
   unchanged; ideally scrub git history).
2. Push this session's changed files to the public repo (listed below).

## Decisions waiting on Ryan

1. **B110 (unchanged from S210).** Grey Knights' `faction_taxonomy.json` flag stays `built:
   false` until it has detachments. Question: prioritize Grey Knights' detachments next, or
   hold per standard faction priority order (World Eaters is next in the Heretic Astartes
   sequence after Emperor's Children)? Proceeding on standard priority order (World Eaters next)
   unless you say otherwise — reversible and cheap to change.
2. **B89 (new evidence, not a new decision).** The CSM/DG/TS detachment v1_0→v1.1 fix
   (confirmed real DP and enhancement-price bugs, not just disposition drift) is recommended as
   the next data turn under B89. No decision needed — flagging for awareness; sequencing it
   ahead of or alongside World Eaters is a dev-manager call I'll make next session unless you
   have a preference.

## Files (SHA-256, first 12)

Verify these at S212 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachments.json` | `448f941e7be6` | +10 EC detachments, 0 changed/removed elsewhere |
| `detachment_effects.json` | `ad7aae235836` | +1 entry (Carnival of Excess), 0 changed/removed |
| `detachment_parser.py` | `9570ef5fcdf0` | EC added to three maps, pointed at v1.1 |
| `faction_taxonomy.json` | `a682a88f1c5c` | EC `built: true`, `data_army` added |
| `40K_Decision_Log.md` | (regenerated at close) | D305 full prose entry appended |
| `DECISION_INDEX.md` | (regenerated at close) | D305 entry |
| `OPEN_ITEMS_BACKLOG.md` | (regenerated at close) | B89 gained dated finding; nothing closed/opened |
| `pipeline_manifest.py` | (regenerated at close) | `SESSION_HANDOFF_211.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S212 |
| `SESSION_HANDOFF_211.md` | (this file) | |

`units.json`, `unit_loadouts.json`, `abilities.json`, `weapon_abilities.json`,
`wargear_points.json`, `datasheet_wargear_abilities.json`, `rules_assertions.py`, `index.html`,
`loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`, `bundled_swaps.json`,
`source_manifest.json`, `baseline.sh`: **untouched**, no entry needed.

## Backlog

24 open at S210 close; 24 open here (nothing closed, nothing new opened — B89 gained confirmed
evidence, not a new ticket). Beginning: B111, B110, B109, B108, B99, B98, B97, B103, E28, B93,
B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (24). Resolved: none. Added:
none. Ending: B111, B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85, B86,
B69, B70, B75, P2, P4, E23, B67b, E12, B17 (24).
