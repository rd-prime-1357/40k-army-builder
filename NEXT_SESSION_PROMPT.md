# NEXT SESSION PROMPT — Session 211

## Recommended turn type: data-only (Emperor's Children detachments)

Read `SESSION_HANDOFF_210.md` first. S210 shipped Emperor's Children's 23 units
(21 auto-parsed + 2 hand-authored, `unit_loadouts.json` byte-identical repro) and closed
out every scoped loadout gap with zero engine changes needed. Detachments are the
remaining piece before Emperor's Children can be marked `built: true`.

## Primary task: build Emperor's Children detachments

Per `EMPEROR_S_CHILDREN_BUILD_SCOPE.md` §7 and its suggested sequencing (§9 step 2):

1. Register `EC` in `detachment_parser.py`'s three maps (`FACTION_FILES`,
   `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`), mirroring the Grey Knights/Thousand Sons
   pattern.
2. Build from `MFM_Emperors_Children_v1.1.txt` (D293). 10 detachments, DP costs 1–3, zero
   unique tags (confirmed by direct text search at S209, re-verify rather than trust).
3. Verify the four force-disposition changes land correctly: Carnival of Excess
   (Priority Assets→Disruption), Coterie of the Conceited (Purge the Foe→Priority
   Assets), Frenzied Host (Disruption→Reconnaissance), Spectacle of Slaughter (Purge the
   Foe→Disruption).
4. Diff-guard against committed `detachments.json`/`detachment_effects.json`: expect
   exactly Emperor's Children's block added, 0 changed/removed elsewhere.
5. Once detachments are clean, update `faction_taxonomy.json`: flip Emperor's Children's
   `built` flag to `true` and set `data_army: "Emperor's Children"` — this is the point
   at which the flag flip is actually correct (units + detachments both complete), unlike
   the Grey Knights B110 situation flagged below.

## Also open, at your discretion

- **B110 (correction, not yet resolved)** — Grey Knights' `faction_taxonomy.json` flag
  is `built: false`, and per S210's finding it must **stay** false until Grey Knights has
  its own detachments (`detachments.json` currently has zero Grey Knights entries).
  Ryan's S210 answer on sequencing (Grey Knights detachments vs. Emperor's Children
  detachments first) determines whether this rides alongside this session or is deferred
  again — check the handoff/decision log for Ryan's response before assuming either way.
- **B109** (XS, engine-only) — `index.html`'s `renderMyLists()`, one-line label change.
  Still not touched (three sessions running now); could ride as a standalone engine-only
  turn, doesn't block or get blocked by anything else open.
- **B111** (new, tooling/engine) — `mfm_points_parser.py`'s `WARGEAR_RE` regex only
  matches `WARGEAR OPTIONS` lines with a leading bullet character, which every v1.1 MFM
  file dropped. This has silently kept the entire project's wargear pricing pass sourced
  from v1_0 text since the v1.1 migration — currently harmless everywhere except EC's
  Defiler (10 pts shipped, should be 15 pts per v1.1). Fixing the regex is a clean,
  narrowly-scoped tooling turn; re-running the wargear pass afterward would need
  diff-guarding across every already-shipped faction, not just EC, in case any other
  v1.1-only price change is hiding behind the same gap — check for that rather than
  assuming EC's Defiler is the only casualty.

## Standing reminders

- `./baseline.sh --fetch --data-turn` at open — data turn, sources must load or the gate
  fails by design.
- All 34 gates should be green at S210 close except `repo_check` (B108, Ryan action) —
  confirm before starting new work.
- Re-derive from source, don't trust prior-session prose — S210 found the real build
  needed far less manual authoring than S209's scope doc estimated by doing exactly this.
- Turn typing: this is data-only. Do not touch `index.html`, `loadout_parser.py`,
  `equipped_parser.py`, or `mfm_points_parser.py` this session even if B109 or B111 look
  tempting to fold in — register each as its own turn instead.

## Close

Produce the four documents, register `SESSION_HANDOFF_211.md` in `pipeline_manifest.py`'s
GUARDED list **before** running `--write`, and run `pipeline_manifest.py
--freshness-check` as the **last** command.
