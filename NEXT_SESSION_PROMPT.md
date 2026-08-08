# NEXT SESSION PROMPT — Session 213

## Recommended turn type: data-only (B89 — Space Marines-group detachment v1.1 confirm-and-fix) or engine-only (B109)

Read `SESSION_HANDOFF_212.md` first. S212 fixed the CSM/Death Guard/Thousand Sons portion of B89's
detachments-side v1_0-sourcing gap — 7 records corrected, diff-guarded clean. Two candidates are
ready with no scoping needed; pick per your own sequencing judgment (dev-manager call, not something
to bring back to Ryan).

## Candidate 1: B89 — Space Marines-group detachment v1.1 confirm-and-fix

`ARMY_TO_MFM` still points the six-file Space Marines group (base Adeptus Astartes, Black Templars,
Blood Angels, Dark Angels, Deathwatch, Space Wolves) at their v1_0 MFM files for detachments, even
though all six factions' `units.json` migrated to v1.1 under B89's units-side arc (S198, D291). D291
already flagged one item in prose (Black Templars gains a new Vengeful Hosts detachment in v1.1,
several enhancement re-prices) but this has never been confirmed/quantified by a direct
parse-and-diff the way S212 did for CSM/DG/TS.

1. Direct parse-and-diff each of the six registered v1_0 files against its v1.1 counterpart before
   touching anything — do not assume D291's prose note is exhaustive.
2. Re-point `ARMY_TO_MFM`'s six entries at the v1.1 filenames (`MFM_Space_Marines_v1.1.txt`,
   `MFM_Black_Templars_v1.1.txt`, `MFM_Blood_Angels_v1.1.txt`, `MFM_Dark_Angels_v1.1.txt`,
   `MFM_Death_Watch_v1.1.txt`, `MFM_Space_Wolves_v1.1.txt`), mirroring the CSM/DG/TS and Emperor's
   Children precedent.
3. Re-run `detachment_parser.py`, diff-guard against committed `detachments.json` at record-key
   level. Six armies means a wider blast radius than the three-faction CSM/DG/TS turn — do not
   assume the diff will be small; check every changed key against source before accepting.
4. Check whether any of the six factions' `detachment_effects.json` entries (Space
   Marines/Black Templars/Blood Angels/Dark Angels/Deathwatch/Space Wolves' Headhunter Task Force
   entries, plus Blood Angels' Lost Brethren and Dark Angels' Company of Hunters) reference a
   detachment whose disposition, DP, or enhancement price changed — confirm directly, don't assume.
5. Check `rules_assertions.py` for any pinned value on a detachment or enhancement in these six
   factions that this fix would touch.
6. `faction_taxonomy.json`: no change expected, all six factions already `built: true` — confirm
   rather than assume.
7. This is existing-faction data correction, not a new-faction build — no scope doc needed.
8. If the six-file diff turns out substantially larger or messier than the CSM/DG/TS pattern (per
   D291's own caution that the SM-family group cannot split faction-by-faction the way CD/DG/TS
   could), stop cleanly and bank what confirms cleanly rather than half-finishing — a scoped partial
   fix beats a rushed six-faction one.

## Candidate 2: B109 — "My Army Lists" page label fix

XS, engine-only, `index.html`'s `renderMyLists()`. Still not touched after five sessions running.
One-line label change: "Target ####" → "#### Points". Doesn't block or get blocked by anything else
open.

## Also open, at your discretion

- **B110** — Grey Knights' `faction_taxonomy.json` flag stays `built: false` until it has
  detachments (`detachments.json` currently has zero Grey Knights entries). No new information since
  S211 — standard faction priority order still says World Eaters is next in the Heretic Astartes
  sequence.
- **World Eaters** — next faction in standard priority order after Emperor's Children, once B89
  and/or B109 are sequenced. Needs its own scoping pass first (`CSM_BUILD_SCOPE.md` pattern).
- **B111** — `mfm_points_parser.py`'s `WARGEAR_RE` regex doesn't match v1.1's bullet-less
  `WARGEAR OPTIONS` lines. Tooling turn; re-running the wargear pass afterward needs diff-guarding
  across every already-shipped faction, not just EC's Defiler.
- **Chaos Daemons' LORDS OF THE WARP** disposition item stays unverified — no v1.1 detachment file
  exists for Chaos Daemons to diff against. Not actionable until GW publishes one.

## Standing reminders

- `./baseline.sh --fetch --data-turn` at open if doing B89 (data turn); plain `./baseline.sh --fetch`
  is sufficient for B109 (engine-only, no GW sources needed).
- All 34 gates should be green at S212 close except `repo_check` (B108, Ryan action) — confirm before
  starting new work.
- Re-derive from source, don't trust prior-session prose — S211 and S212 both caught real gaps by
  checking `ARMY_TO_MFM` registrations directly rather than assuming the existing pattern was safe.
- Turn typing: B89 is data-only (`detachments.json`/`detachment_effects.json`/`detachment_parser.py`'s
  registration dict only — no other engine file). B109 is engine-only (`index.html` only). Do not
  combine them in one session even though both are small.

## Close

Produce the four documents, register `SESSION_HANDOFF_213.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
