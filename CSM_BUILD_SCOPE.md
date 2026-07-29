# Chaos Space Marines — Build Scope

Scoping-only pass (S146, D227). No committed file changed. All numbers below come from command
output against the S145 baseline (23/23 gates, 104/104 assertions clean at open). Dry-run transforms
were written only to a throwaway temp dir.

CSM is a clean single-faction build in the mould of **Death Guard**, not a second Space Marines. It
has no chapter/sub-faction split, no allied-codex problem, and no new engine or UI mechanism. Every
piece it needs already exists in the pipeline. The one genuinely new piece of build work is
cross-file points sourcing for four cult-troop units (see §4).

---

## 1. Real roster size: 58, not 112

The "112 datasheets" figure is a raw row count of `faction_id == CSM` in `Datasheets.csv`. Of those,
**54 are Warhammer Legends** (32 from the CSM Legends source, 22 from the SM Legends source — both
edition `0`) and are correctly excluded by the transform's existing Legends/Forge-World filter. The
`wahapedia_transform.py --faction CSM` dry run selected **58**, which is the correct current-edition
count. This matches the standalone-pass audit (`MFM_Standalone_Pass.md`: "112 (58 current / 54
Legends-FW)").

Roles across the 58: 35 Characters, ~17 Other, 6 Battleline, 2 Dedicated Transports (Chaos Rhino,
Terrax-pattern Termite), 1 Fortification. 92 leader-attachment rows — a character-heavy faction that
leans hard on the existing leader / co-leader / bodyguard-stat-flag machinery, all of which is built.

## 2. Marks of Chaos are not a build-time choice

The current codex does not expose Mark of Chaos as a selectable, priced per-unit upgrade. There are
**zero** "Mark of …" option rows in `Datasheets_options.csv`. Marks appear only as (a) god keywords
baked onto a minority of datasheets (6 Khorne, 7 Nurgle, 3 Slaanesh, 3 Tzeentch, 6 Chaos Undivided)
and (b) three detachment enhancements already handled by the E4 enhancement engine. **No new
mark-selection mechanism is needed.** This was the largest potential complication and it is ruled out.

## 3. Detachments: 17 current, reconciled by D192 — not a Ryan call

The 11th-ed MFM and the 10th-ed Wahapedia dump disagree on which detachments exist:

- **In MFM, not in Wahapedia (2):** Devotees of Destruction, Murdertalon Raiders — new in 11th ed.
- **In Wahapedia, not in MFM (3):** Champions of Chaos, Infernal Reavers, Underdeck Uprising —
  removed in 11th ed.

E1 / D192 settles this as an engineering rule, explicitly "not a Ryan call": **MFM is the source of
record for which detachments exist; content in a text source but absent from MFM is dropped as a stale
leftover.** So the three Wahapedia-only detachments are dropped, the two MFM-only ones are included,
and the current-edition CSM detachment count is **17**. The `detachment_parser.py` already works this
way — it iterates the MFM list and pulls Wahapedia prose only as fallback — so this needs no code
change, only the three config-line additions in §6.

### The one real product decision (D228, see Decisions)

Fifteen of the 17 detachments have full Wahapedia prose (rule text, enhancement descriptions,
stratagems). The **two new ones (Devotees of Destruction, Murdertalon Raiders) have none** — no
detachment ability row, no enhancement rows, zero stratagems. The CSM MFM carries no rule prose for
them either (it carries no rule prose for any detachment — structure + enhancement names/points only,
exactly like DG). So if built, each renders as a legal, selectable detachment with its two enhancements
named and priced but with an empty rule and description-less enhancements, and no stratagems.

## 4. Points: 4 cult-troop units are priced in sibling MFM files — **CLOSED (D240, S157)**

`mfm_points_parser.py` on the CSM MFM prices 85 rows, covering 54 of the 58. The four it misses are the
cult troops, whose points live in their god-legion MFMs (confirmed present in each):

- Khorne Berzerkers → `MFM_World_Eaters_v1_0.txt`
- Plague Marines → `MFM_Death_Guard_v1_0.txt`
- Rubric Marines → `MFM_Thousand_Sons_v1_0.txt`
- Noise Marines → `MFM_Emperors_Children_v1_0.txt`

**Shipped.** Each unit priced via its own `--scope-to-army --append` call against its own legion's
MFM, isolated to a single-row `Unit_Stats.csv` scope (new `_scope_stats_csv()` in
`units_repro_check.py`) so the call can only ever match that one unit — not any of CSM's other 54
already-priced units, several of which (Chaos Rhino, Helbrute, Defiler, etc.) are also priced,
separately, in one or more of these same four legion MFMs. `units.json` now carries all 58; see
D240 for the full account.

## 5. Loadout defaults

`Chaos_Space_Marines_web.txt` is present (89 KB, CRLF — the hand-sourced convention, not Ryan's newer
LF script output), 5,350 lines, structure consistent with the other web passes. It becomes a sixth
`equipped_parser.py` pass. `loadout_parser.py --factions` gains `CSM`. Both are single-line additions
to the config lists (§6).

## 6. Exact build surface — every file the build turn touches

**Pipeline config edits (three files, one-to-three lines each):**
- `units_repro_check.py` — add a CSM per-faction block (transform → mfm points → cult-troop append →
  convert) and a fourth `--in` to the merge call.
- `repro_check.py` — add `CSM` to `FACTIONS`; add `Chaos_Space_Marines` to `WEB_PASSES`.
- `detachment_parser.py` — add CSM rows to `ARMY_TO_MFM`, `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`.
- `detachments_repro_check.py` — add `MFM_Chaos_Space_Marines_v1_0.txt` to its required-inputs list.

**Regenerated outputs (three files):**
- `units.json` — +~404 KB (58 units at ~7 KB each), 270 → 328 units.
- `detachments.json` — +~94 KB (17 detachments at ~5.5 KB each), 143 → 160.
- `unit_loadouts.json` — +~40 KB (CSM defaults).

**Assertions / manifest:** new CSM-specific assertions in `rules_assertions.py` (roster count 58,
detachment count 17, the four cross-sourced points, the two prose-less detachments recorded as such);
`pipeline_manifest.json` reissued for the three regenerated outputs.

**`index.html`:** no change expected. CSM uses only existing mechanisms.

## 7. Capacity

Real project-area growth from the build is the three regenerated outputs: **~540 KB total.** All source
inputs (CSM MFM, the four sibling MFMs, the web file) are already loaded. The browser data payload
grows from ~2.6 MB to ~3.1 MB (+~19%); `index.html` is unchanged. At 96% project-area capacity, ~540 KB
of output growth is the number to confirm fits before running the build for real — the P4 decision-log
archive split is the standing lever if it doesn't.

## 8. Turn plan for the build

1. **Data turn A** — transform → mfm points (self) → convert → merge → post-processors; the 54
   self-priced units. Add the config lines, regenerate, diff, trace every difference. Bank.
2. **Data turn B** — cult-troop cross-file points append (the four units). Bank.
3. **Data turn C** — detachment build: config lines in `detachment_parser.py`, regenerate
   `detachments.json`, verify the 17/dropped-3 split and the two prose-less detachments.
4. **Tooling turn** — CSM assertions into `rules_assertions.py`, manifest reissue, harness pass.

Turns A–C are data-only and must not mix with the tooling turn. If cult-troop pricing (turn B) proves
fiddly it stays its own turn rather than bleeding into A.
