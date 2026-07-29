# Thousand Sons — Build Scope

Scoping-only pass (S158, D241). No committed file changed except a reconciliation fix found and
closed at baseline open (see Baseline note). All roster/points/detachment numbers below come from
live dry runs of `wahapedia_transform.py` and `mfm_points_parser.py` against this session's source
files, cross-checked against `MFM_Standalone_Pass.md`'s prior audit — not assumed from that audit
alone.

Thousand Sons is a clean, fully self-sourced single-faction build, simpler than CSM. It has no
chapter/sub-faction split, no cross-faction points sourcing at all (the reciprocal-gap concern this
session was asked to check comes back clean — see §4), and needs no new engine or UI mechanism. The
one real gap is missing source material for loadout defaults (§5) — a Ryan dependency, not a build
decision.

---

## 1. Real roster size: 34, not 60

`Datasheets.csv` carries 60 rows tagged `faction_id == TS`. Of those, **26 are Warhammer Legends**
(22 from the Space Marines Legends source, 4 from the Chaos Space Marines Legends source, both
edition `0`) and are excluded by the transform's existing filter. `wahapedia_transform.py --faction
TS` dry run selected **34**, matching `MFM_Standalone_Pass.md`'s "60 (34 current / 26 Legends-FW)."

Role breakdown across the 34 (37 stat rows — three datasheets carry a second profile, e.g. a
damaged state): 11 Vehicle, 9 Character, 5 Battleline, 4 Infantry, 3 Epic Hero, 2 Beast, 2 Mounted, 1
Monster. 7 units carry a Leader ability. This is a more vehicle- and character-heavy roster than
CSM's, consistent with Thousand Sons' daemon-engine-and-sorcerer style, but nothing here needs new
leader/co-leader/bodyguard machinery beyond what CSM and SM already exercise.

## 2. No selectable Cabal Points / Mark mechanism needed

Thousand Sons carries two faction-wide passive rules, `Cabal of Sorcerers` and `Pact of Sorcery`
(`Abilities.csv`, faction_id TS), in the same shape as CSM's `Blessings of Khorne` — army-wide
descriptive ability text applied automatically, not a build-time choice. Grepped all 105 TS rows in
`Datasheets_options.csv` for anything resembling a selectable Cabal-point or Mark-of-Chaos option:
**zero** hits. No new selection mechanism is needed.

## 3. Detachments: 9 current, same D192 pattern as CSM — not a Ryan call

The MFM and the Wahapedia dump disagree on which detachments exist, exactly as with CSM:

- **In MFM, not in Wahapedia (3):** Ritual of Regeneration, Sekhetar Cohort, Servants of Change — new
  in 11th ed.
- **In Wahapedia, not in MFM (3):** Chosen Cabal, Devoted Thralls, Fateseekers — removed in 11th ed.
- **In both (6):** Changehost of Deceit, Grand Coven, Hexwarp Thrallband, Rubricae Phalanx, Warpforged
  Cabal, Warpmeld Pact.

Per D192 (MFM is source of record; content in a text source but absent from MFM is a stale leftover),
the three Wahapedia-only detachments are dropped and the three MFM-only ones are included: current
count **9**. `detachment_parser.py` needs no code change, only TS's three config lines (§6).

### The one prose gap (mirrors CSM's, not flagged to Ryan)

Checked `Detachment_abilities.csv`, `Stratagems.csv`, and `Enhancements.csv` directly: only the 6
detachments Wahapedia already knew about have rule text, stratagems, or enhancement descriptions. The
3 MFM-only detachments have none of the three — same shape as CSM's two prose-less detachments. If
built, each renders as a legal, selectable detachment with its enhancements named and priced (from the
MFM) but with an empty rule and description-less enhancements, and no stratagems. This follows the
CSM precedent (D192/§3) directly and isn't a fresh call.

## 4. Points: fully self-sourced, 34/34 — the reciprocal-gap check comes back clean

This session was asked to check whether Thousand Sons has a reciprocal version of CSM's cult-troop
gap, since Thousand Sons' own MFM prices Rubric Marines (CSM's cult troop). It does not. Dry-running
`mfm_points_parser.py` against `MFM_Thousand_Sons_v1_0.txt` and TS's own 34-unit stats block produced
**34 unit point rows — full coverage, zero misses.** `MFM_Standalone_Pass.md` already listed Thousand
Sons among its "clean factions (self-sourced)"; this session confirms that's still true, not stale.
No cross-file points call, and no `_scope_stats_csv()`-style isolation, is needed anywhere in the TS
build.

## 5. Loadout defaults: BLOCKED — no source file exists (the one real gap)

Every existing per-faction loadout-defaults pass (`Space_Marines_web.txt`, `Death_Guard_web.txt`,
`Black_Templars_web.txt`, `Dark_Angels_web.txt`, `Space_Wolves_web.txt`, `Chaos_Space_Marines_web.txt`)
is a hand-pasted Wahapedia datasheet composition dump — `equipped_parser.py`'s only source for
per-model-group default-weapon attribution, since the Wahapedia CSV export drops that wording
entirely. **No `Thousand_Sons_web.txt` exists in the project or the repo.** Without it, TS units
would fall back to the flat wargear-pool baseline instead of correct per-model defaults — a real
legality gap (D0: exact composition matters), not cosmetic.

This needs Ryan to source the composition text from Wahapedia's Thousand Sons datasheet pages (the
same paste-from-site process used for the other six factions) before the loadout-defaults turn of
the TS build can run. Everything else in this scope doc can proceed without it; only turn B (§8)
is blocked.

## 6. Exact build surface — every file the build turns touch

**Pipeline config edits (three files, one-to-three lines each), mirroring CSM's §6:**
- `units_repro_check.py` — add a TS per-faction block (transform → mfm points → convert); a fifth
  `--in` to the merge call. No cross-file append step needed (§4).
- `repro_check.py` — add `TS` to `FACTIONS`; add `Thousand_Sons` to `WEB_PASSES` once §5 is unblocked.
- `detachment_parser.py` — add TS rows to `ARMY_TO_MFM`, `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`.
- `detachments_repro_check.py` — add `MFM_Thousand_Sons_v1_0.txt` to its required-inputs list.

**Regenerated outputs (three files):**
- `units.json` — +~240 KB (34 units at ~7 KB each), 328 → 362 units.
- `detachments.json` — +~50 KB (9 detachments at ~5.5 KB each), 160 → 169.
- `unit_loadouts.json` — +~24 KB (TS defaults) — deferred until §5 is unblocked.

**Assertions / manifest:** new TS-specific assertions in `rules_assertions.py` (roster count 34,
detachment count 9, the three prose-less detachments recorded as such, same shape as `CSM-1`–`CSM-3`);
`pipeline_manifest.json` reissued for each regenerated output.

**`index.html`:** no change expected. TS uses only existing mechanisms — same conclusion as CSM §6.

## 7. Capacity

Real project-area growth from turns A and C (units + detachments, before loadout defaults): **~290
KB.** Turn B (loadout defaults, once unblocked) adds a further ~24 KB. Total build growth ~314 KB,
noticeably smaller than CSM's ~540 KB reflecting the smaller 34-unit roster. At current project-area
capacity, this is the number to confirm fits before running the build — same standing lever
(`BACKLOG_ARCHIVE.md`/decision-log archive split) applies if it doesn't.

## 8. Turn plan for the build

1. **Data turn A** — transform → mfm points (self, fully self-sourced, no append step) → convert →
   merge → post-processors; all 34 units. Add the config lines, regenerate, diff, trace every
   difference. Bank.
2. **Data turn B** — loadout defaults, **blocked on §5** until `Thousand_Sons_web.txt` exists.
3. **Data turn C** — detachment build: config lines in `detachment_parser.py`, regenerate
   `detachments.json`, verify the 9/dropped-3 split and the three prose-less detachments.
4. **Tooling turn** — TS assertions into `rules_assertions.py`, manifest reissue, harness pass.

Turns A and C do not depend on turn B and can ship in either order; turn B can slot in whenever the
source text arrives without blocking the rest of the build. Turns must not mix with the tooling turn,
per the standing rule.
