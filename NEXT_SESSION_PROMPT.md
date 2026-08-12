# NEXT SESSION PROMPT — Session 230

## Recommended turn type: data-only — build B114 (Shadow Legion unlock), or scoping — GK §6/§7.
## Neither is blocked on a Ryan decision.

B114 was scoped, not built, at S229 (D323): read `SESSION_HANDOFF_229.md` and
`B114_SHADOW_LEGION_SCOPE.md` first. Short version — the stored `unlock` effect's `target:
{"keyword": "HERETIC ASTARTES"}` shape has no consuming engine code at all (only `allied_group` is
read); the real unlockable set, pulled from the actual ability text rather than the paraphrase, is
21 CSM units (14 named directly, 7 more via the "Damned units" keyword group), all already shipped
and priced. Recommended build: tag those 21 units with a new `allied_group` (e.g. "Shadow Legion
Thralls") in `units.json`, retarget the effect to `{"allied_group": "Shadow Legion Thralls"}` in
`detachment_effects.json`, flip `enforced: true`. No new engine code — reuses the same machinery
already shipping for Death Guard's Plague Legions and Thousand Sons' Scintillating Legions. Do NOT
add a Warlord-ban effect for this group — checked directly, the ability carries no such clause
(unlike Plague Legions). Add a pinned census assertion for the 21-unit set, same shape as B113's
E4b-6/E4b-7, so a future Wahapedia/MFM regeneration can't silently drift it.

Open with `./baseline.sh --fetch`. Verify S229's Files table hashes against
`pipeline_manifest.json` before starting. This is a data-only turn (units.json + detachment_
effects.json changes, plus a rules_assertions.py addition) — keep it separate from any engine work.

## Open, at your discretion

- **B114 build** — per the recommendation above, ready to go. Re-derive the 21-unit set from source
  yourself at build time rather than trusting this prompt's numbers — standing practice, and the
  set was hand-cross-referenced this session, worth a second look before it's baked into
  `units.json`.
- **GK §6 / §7** — carried unchanged for several sessions; still not investigated. Different turn
  type from B114's build — don't mix.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's numbers.
- Turn typing stays strict. B114's build is data-only; GK §6/§7 (if picked up first) is scoping;
  don't mix in one session.
- Diff-guard the `units.json` change: the 21 units getting `allied_group` tags should be the ONLY
  change — zero removals, zero other fields touched. Same discipline as every prior data turn.

## Decisions waiting on Ryan

- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic (see
  `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides. Does not block
  anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction is
  queued. Recommendation stands: clear the remaining engine/scoping backlog (B114's build, GK
  §6/§7) before revisiting which faction, if any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_230.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
