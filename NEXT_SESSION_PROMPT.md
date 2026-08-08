# NEXT SESSION PROMPT — Session 220

## Recommended turn type: data-only (Grey Knights detachments)

Read `SESSION_HANDOFF_219.md` and `GREY_KNIGHTS_BUILD_SCOPE.md` first. S219 shipped World Eaters
detachments clean — with World Eaters now built, **all five Heretic Astartes factions are
complete** (Chaos Space Marines, Thousand Sons, Death Guard, Emperor's Children, World Eaters).

This surfaces an unfinished item further back: Grey Knights' **units** were built and completed at
S208 (D302, 25/25 units, zero residual `_parser_flags`), but Grey Knights' **detachments** were
never built — `detachment_parser.py`'s `ARMY_TO_MFM`/`MFM_SOURCE_NAME`/`ARMY_TO_WAHA_FACTION` carry
no Grey Knights entry today, and `detachments.json` has zero Grey Knights records. This is
`GREY_KNIGHTS_BUILD_SCOPE.md` §10 step 4, sitting undone since S200's scoping pass. Per this
project's faction priority order, Adeptus Astartes must be fully complete before Chaos Daemons/
Drukhari work — Grey Knights' detachments are the one remaining gap in that group and should be
closed before B112 (Chaos Daemons) or any Imperium/Drukhari faction is picked up.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting — should be fully
green except the pre-existing B108 finding (unchanged, Ryan's action).

## Grey Knights detachments — the work

Per `GREY_KNIGHTS_BUILD_SCOPE.md` §8, build from `MFM_Grey_Knights_v1.1.txt` (D293: always the
newest MFM). Register `Grey Knights` in `detachment_parser.py`'s three maps (`ARMY_TO_MFM`,
`MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`), mirroring the World Eaters pattern (D313, this session)
exactly.

What §8 already found, scoped at S200 — verify fresh from source, don't trust the prose:
- **9 detachments in both MFM versions**, identical keys: Argent Assault, Augurium Task Force,
  Banishers, Brotherhood Strike, Fires of Purgation, Hallowed Conclave, Immaterial Interdiction,
  Sanctic Spearhead, Warpbane Task Force. DP costs 1–3, 28 enhancements total (4 Upgrade).
- **Three force-disposition changes**, each carrying v1.1's own `FORCE DISPOSITION(S) CHANGED`
  banner: Argent Assault (Purge the Foe → Priority Assets), Immaterial Interdiction (Priority
  Assets → Reconnaissance), Warpbane Task Force (Purge the Foe → Take and Hold).
- No DP changes, no enhancement re-prices, no detachments added/removed, **no unique tags anywhere
  in the faction** — confirm by direct text search, not assumed (same discipline as S219's World
  Eaters check).
- Grey Knights carries 3 gaps (Argent Assault, Fires of Purgation, Immaterial Interdiction —
  1DP detachments with no rule text in either source, `text_source: none`) — expected, not a
  finding, same shape as CSM/DG/other factions' own MFM-only detachments.

Diff-guard `detachments.json` before banking: confirm exactly Grey Knights' 9 detachments added, 0
changed/removed elsewhere.

**Check `detachment_effects.json` directly — do not assume none needed.** S219's World Eaters turn
found a construction-effect gap the scope doc's own §8 analysis didn't mention (Cult of Blood's
BATTLELINE grant), caught only because `rules_assertions.py`'s `e21a_coverage` assertion scans
every built detachment's `rule_text`/`restrictions` automatically. Scan all 9 Grey Knights
detachments for an allied-unlock or BATTLELINE-grant pattern before banking, and let the full
baseline re-run catch anything missed by manual scan — it did exactly that this session.

**Once detachments ship clean:** flip `faction_taxonomy.json`'s Grey Knights `built` flag to `true`
and set `data_army: "Grey Knights"` — same sequencing as D298 (original attempt, corrected at D303
when detachments turned out to be zero), D305 (Emperor's Children), and this session's World
Eaters. This closes out the entire Adeptus Astartes group.

## Also open, at your discretion

- **B112** — Chaos Daemons LORDS OF THE WARP disposition, unblocked since S217 (a v1.1 CD MFM file
  exists in the private repo). Same-pattern data-only fix mirroring D306/D307. Its own turn, and
  per faction priority order should follow Grey Knights, not precede it.
- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances now: CSM ×2, TS ×1, EC ×1, World Eaters ×2). Engine turn, small. Not urgent —
  pre-existing and unenforced on six shipped detachments already.
- **GK §6** — the Nemesis Dreadknight "cannot take duplicates" gap (a pre-existing D0 violation
  affecting 3 already-shipped Chaos Space Marines units too) was recommended as an engine ticket
  ahead of the Grey Knights units build, back at S200. Units shipped anyway (S208) without it,
  apparently capped-but-not-distinct — worth confirming current state before assuming it's still
  open, rather than trusting the four-session-old scope doc's snapshot.
- **GK §7** — `detachment_parser.py --report`'s `KeyError` on any run that produces a gap record
  (reads `g["army"]`, the actual key is `g["source_faction"]`). One-line fix, XS, tooling turn. Has
  never fired in a gate (`detachments_repro_check.py` never passes `--report`) but will fire the
  moment this session's own build turn runs the parser with `--report` for diagnostics — either
  avoid `--report` this session, or fix it first as a two-minute tooling aside (still don't mix
  turn types: if fixed, that's a one-line tooling change, not folded into the data turn's own
  commit reasoning).

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's own numbers.
- Turn typing: Grey Knights detachments is data-only. If it surfaces an engine or tooling need
  (e.g. GK §6 or §7), note it for its own typed session — don't fold it into this one.
- No decisions currently waiting on Ryan from S219.
- Construction-effect rows: check `detachment_effects.json` directly for every built detachment
  this session touches, per the S219 finding — a manual read-through of rule text is not
  sufficient on its own; let the full baseline (`rules_assertions.py`'s `e21a_coverage`) confirm.

## Close

Produce the four documents, register `SESSION_HANDOFF_220.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
