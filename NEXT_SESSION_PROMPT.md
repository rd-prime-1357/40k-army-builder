# Next-session prompt — Session 185

**Assigned: B90 turn 1 of 3 — engine turn. Add the chapter roster-mode flag; branch `resolveUnits()`
on it.**
Turn type is **engine-only** — no data-file regeneration, no tooling change this session. The five
Tier-2 chapters will still resolve to their (wrong, union-leaked) roster until the data turn lands —
that's expected; this turn only builds the mechanism, it doesn't fix the five chapters' actual data.

## Open at session start

Read `SESSION_HANDOFF_184.md` first, then `40K_Decision_Log_v3_0.md` **D276** in full — it has the
Black Templars source evidence, the exact leak count, and the three-turn scope. Do not trust
session/version/decision numbers from memory — re-derive from source. `index.html` is at **v6.14**
(unchanged S184).

Run the full baseline: `./baseline.sh --no-repo` is sufficient (sources not needed for an engine-only
turn touching `resolveUnits()` and `faction_taxonomy.json`'s schema — no MFM re-parse this session).
Expect 23/23 green (3 tier-B skipped) at open, matching S184's close state.

## The build (B90 step 1 of 3, per D276)

Add a roster-mode distinction to `faction_taxonomy.json` for the eleven non-generic Adeptus Astartes
factions — `'complete'` for the five dedicated-MFM chapters (Black Templars, Blood Angels, Dark
Angels, Deathwatch, Space Wolves), `'union'` for the six vanilla chapters (Ultramarines, Iron Hands,
Salamanders, Imperial Fists, Raven Guard, White Scars). `is_subfaction` stays as-is (it still governs
other behavior); this is an additional field, not a replacement. Update the taxonomy's misleading
top comment ("chapters union the generic codex at selection time") to state the two-tier rule.

Rewrite `resolveUnits()` in `index.html`: `'union'` factions keep exactly today's behavior (generic
filtered by chapter names, concat, override map applied). `'complete'` factions return their own
`unitsByArmy[faction.data_army]` set only — no generic union, no override-map involvement (Tier-2
chapters price natively per D42's existing "distinct datasheet IDs" language, not via override).

**Do not regenerate `units.json` this session.** The five Tier-2 chapters' data stays exactly as it
is today — still union-shaped, still wrong — until the data turn. Verify the new code path in
isolation: temporarily point a `'complete'`-flagged test chapter at a small fixture if needed, or
verify structurally (the branch is taken, the union code path is provably unreached for
`'complete'` factions) without a full data rebuild.

## Acceptance (facts as executable checks)

- New assertion or harness check: every faction record in `faction_taxonomy.json` classified as
  `is_subfaction: true` has an explicit roster mode (no silent default).
- `resolveUnits()` for a `'complete'`-mode faction never touches `unitsByArmy['Adeptus Astartes']` or
  `applyChapterPointOverrides()` — structurally provable from the code path, not just spot-checked.
- Existing `'union'`-mode behavior byte-identical to today for the six vanilla chapters (pool_check,
  b56g_check and friends must show no diff for Ultramarines/Iron Hands/Salamanders/Imperial
  Fists/Raven Guard/White Scars).
- Baseline green at close. `index.html` version bump (v6.14 → v6.15) since this is a real behavior
  change to the resolution path, even though Tier-2 output is still wrong pending the data turn.

## After this

- **B90 turn 2 (data)** — rebuild the five Tier-2 chapters in `units.json` from their own MFM files.
  Needs sources loaded (`--fetch --data-turn`).
- **B90 turn 3 (assertion)** — pin roster-membership exclusivity for the five.
- B87/B88/B89 (MFM v1.1 refresh arc) resume after B90 closes in full.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_185.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md`. Every changed and net-new file
carries a SHA-256 (first 12) in the handoff Files section. Append `SESSION_HANDOFF_185.md` to
`GUARDED` in `pipeline_manifest.py` this same session, then `python3 pipeline_manifest.py --write`,
then `--freshness-check` at the very end, after all text is finalized — S183 and S156 both shipped a
stale manifest hash by writing before the last edit; run it last, not from habit but because it has
now recurred twice. Repo is public and flat — no GW-derived material committed; state the exclusions
when listing files for the repo.
