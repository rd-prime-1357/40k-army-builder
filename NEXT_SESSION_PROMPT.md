# NEXT SESSION PROMPT — Session 221

## Recommended turn type: data-only (B112 — Chaos Daemons LORDS OF THE WARP disposition)

Read `SESSION_HANDOFF_220.md` first. S220 shipped Grey Knights detachments clean — **all twelve
Adeptus Astartes armies are now fully built** (units + detachments both complete). Per this
project's faction priority order, Heretic Astartes (already complete since S219) and Adeptus
Astartes are both done; Chaos Daemons is next.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting. `MFM_Chaos
Daemons_v1.1.txt` (note the literal space in the filename, not an underscore) and
`MFM_Chaos_Daemons_v1_0.txt` are both confirmed present and byte-verified against
`source_manifest.json` as of S220's open.

## B112 — the work

Per the ticket (`OPEN_ITEMS_BACKLOG.md`), Chaos Daemons had no v1.1 detachment source to diff
against until the private repo received one at S217. The suspected change is the **LORDS OF THE
WARP** detachment's force disposition, forecast as Purge the Foe → Take and Hold by analogy with
every other faction's v1.1 migration pattern — **verify this directly from the v1.1 text, don't
assume the forecast is right.** S220's Grey Knights turn found the sibling scope doc's own
enhancement count was off by 2 despite being checked at S200; treat any inherited forecast the same
way.

Same pattern as D306/D307 (CSM/DG/TS, then the six-file Space Marines group): re-point
`detachment_parser.py`'s `ARMY_TO_MFM` entry for `"Chaos Daemons"` at
`"MFM_Chaos Daemons_v1.1.txt"` (Chaos Daemons is already registered in all three maps from its
original build — this is a re-point, not a new registration). Diff-guard `detachments.json` before
banking: expect force-disposition and/or enhancement-price changes only, investigate any structural
diff before accepting it. Check `detachment_effects.json` directly for Chaos Daemons per the
standing discipline (D313, D314) — don't assume none needed; let `rules_assertions.py`'s
`e21a_coverage` assertion confirm on the full baseline re-run regardless of the manual scan's
result.

## Also open, at your discretion

- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances: CSM ×2, TS ×1, EC ×1, World Eaters ×2; Grey Knights confirmed to add 0 more at S220).
  Engine turn, small. Not urgent — pre-existing and unenforced on six shipped detachments already.
- **GK §6** (from `GREY_KNIGHTS_BUILD_SCOPE.md`) — the Nemesis Dreadknight "cannot take duplicates"
  gap, a pre-existing D0 violation affecting 3 already-shipped Chaos Space Marines units too. Was
  recommended as an engine ticket ahead of the Grey Knights units build back at S200; units shipped
  anyway (S208) capped-but-not-distinct. Worth confirming current state and opening as its own
  ticket if not already tracked — this prompt does not have a ticket ID for it.
- **GK §7** — `detachment_parser.py --report`'s `KeyError` on any run that produces a gap record
  (reads `g["army"]`, the actual key is `g["source_faction"]`). One-line fix, XS, tooling turn. Has
  never fired in a gate; will fire the moment a session runs the parser with `--report` for
  diagnostics. Avoid `--report` until fixed, or fix it first as its own tooling aside.
- **Repo push** — `OUTPUT_FORMAT_SPEC_for_project_instructions.md` is unpushed (S220 finding,
  Ryan's action) alongside the still-outstanding B108 (`Thousand_Sons_web.txt`).

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's own numbers.
  S220 found the Grey Knights scope doc's enhancement count was wrong (28 forecast, 30 actual)
  despite being a careful S200 scoping pass; the same discipline applies to B112's disposition
  forecast.
- Turn typing: B112 is data-only. If it surfaces an engine or tooling need, note it for its own
  typed session — don't fold it in.
- No decisions currently waiting on Ryan from S220.
- Construction-effect rows: check `detachment_effects.json` directly for every built detachment
  this session touches — a manual read-through of rule text is not sufficient on its own; let the
  full baseline (`rules_assertions.py`'s `e21a_coverage`) confirm.

## Close

Produce the four documents, register `SESSION_HANDOFF_221.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
