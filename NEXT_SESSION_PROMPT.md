# NEXT SESSION PROMPT — Session 212

## Recommended turn type: data-only (B89 — CSM/DG/TS detachment v1.1 fix) or engine-only (B109)

Read `SESSION_HANDOFF_211.md` first. S211 shipped Emperor's Children's 10 detachments and closed
the faction out entirely — 23/23 units, 10/10 detachments, `faction_taxonomy.json` flipped to
`built: true`. Two candidates are ready with no scoping needed; pick per your own sequencing
judgment (dev-manager call, not something to bring back to Ryan).

## Candidate 1: B89 — fix CSM/Death Guard/Thousand Sons detachment sourcing

S211 found (not fixed) that `detachment_parser.py`'s `ARMY_TO_MFM` still points these three
factions at their v1_0 MFM files for detachments, despite their units already being on v1.1.
Confirmed real, already-shipped bugs — not just disposition drift:

1. Re-point `ARMY_TO_MFM`'s three entries at the v1.1 filenames (`MFM_Chaos_Space_Marines_v1.1
   .txt`, `MFM_Death_Guard_v1.1.txt`, `MFM_Thousand_Sons_v1.1.txt`), mirroring how Emperor's
   Children is now registered.
2. Re-run `detachment_parser.py`, diff-guard against committed `detachments.json` — expect DP,
   disposition, and enhancement-price changes on exactly these known items: Thousand Sons'
   Hexwarp Thrallband (2→3 DP), three TS disposition changes, Chaos Space Marines' Murdertalon
   Raiders + Soulforged Warpack (disposition + Tempting Addendum 25→40 pts), Death Guard's
   Contagion Engines disposition. Anything beyond this known list is a surprise — investigate
   before accepting, don't assume the S211 diff was exhaustive.
3. Check whether any of the three factions' `detachment_effects.json` entries reference a
   detachment whose disposition or DP changed — none should, since effects don't encode
   disposition/DP, but confirm rather than assume.
4. `faction_taxonomy.json`: no change needed, these three factions are already `built: true`.
5. This is existing-faction data correction, not a new-faction build — no scope doc needed.

## Candidate 2: B109 — "My Army Lists" page label fix

XS, engine-only, `index.html`'s `renderMyLists()`. Still not touched after four sessions
running. One-line label change: "Target ####" → "#### Points". Doesn't block or get blocked by
anything else open.

## Also open, at your discretion

- **B110** — Grey Knights' `faction_taxonomy.json` flag stays `built: false` until it has
  detachments (`detachments.json` currently has zero Grey Knights entries). S211 proceeded on
  standard faction priority order (World Eaters next in the Heretic Astartes sequence) absent
  Ryan's input — check the handoff/decision log for any response before assuming either way.
- **World Eaters** — next faction in standard priority order after Emperor's Children, once B89
  and/or B109 are sequenced. Needs its own scoping pass first (`CSM_BUILD_SCOPE.md` pattern).
- **B111** — `mfm_points_parser.py`'s `WARGEAR_RE` regex doesn't match v1.1's bullet-less
  `WARGEAR OPTIONS` lines. Tooling turn; re-running the wargear pass afterward needs
  diff-guarding across every already-shipped faction, not just EC's Defiler.

## Standing reminders

- `./baseline.sh --fetch --data-turn` at open if doing B89 (data turn); plain `./baseline.sh
  --fetch` is sufficient for B109 (engine-only, no GW sources needed).
- All 34 gates should be green at S211 close except `repo_check` (B108, Ryan action) — confirm
  before starting new work.
- Re-derive from source, don't trust prior-session prose — S211 caught the TS/CSM/DG v1_0
  sourcing bug by checking `sniff_is_v1_1()` directly rather than assuming the existing
  `ARMY_TO_MFM` registrations were already correct.
- Turn typing: B89 is data-only (detachments.json/detachment_effects.json/detachment_parser.py's
  registration dict only — no other engine file). B109 is engine-only (index.html only). Do not
  combine them in one session even though both are small.

## Close

Produce the four documents, register `SESSION_HANDOFF_212.md` in `pipeline_manifest.py`'s
GUARDED list **before** running `--write`, and run `pipeline_manifest.py
--freshness-check` as the **last** command.
