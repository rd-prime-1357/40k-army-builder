# NEXT SESSION PROMPT — Session 222

## Recommended turn type: scoping (Drukhari — first faction build pass)

Read `SESSION_HANDOFF_221.md` first. S221 shipped Chaos Daemons' LORDS OF THE WARP detachment
disposition clean — **Chaos Daemons is now fully built (units + detachments both complete)**,
closing B112. Per the project's faction priority order (all Adeptus Astartes, then all Heretic
Astartes, then Chaos Daemons, then Drukhari), **Drukhari is the only faction left in the priority
list**, and it has no scope doc yet — `MFM_Drukhari_v1.1.txt` and `MFM_Drukhari_v1_0.txt` are both
present in the project area, but nothing has scoped a units or detachments build against them.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting.

## Drukhari scoping — the work

Follow the same shape as the existing `*_BUILD_SCOPE.md` docs (`CSM_BUILD_SCOPE.md`,
`THOUSAND_SONS_BUILD_SCOPE.md`, `EMPEROR_S_CHILDREN_BUILD_SCOPE.md`, `WORLD_EATERS_BUILD_SCOPE.md`,
`GREY_KNIGHTS_BUILD_SCOPE.md`) as templates for section structure, but re-derive every number from
`MFM_Drukhari_v1.1.txt` directly — do not assume Drukhari's shape mirrors any prior faction's.
Per the standing discipline (reinforced hard at S220/S221: two different sibling scope docs were
each found wrong on re-check despite careful prior passes), every count in the scope doc must come
from a fresh read of the source, not carried over from memory of how another faction's build went.

Cover at minimum: unit count and Leader/Support attachment map; detachment count, DP range, and
whether any carry `UNIQUE:` tags; enhancement count per detachment; whether Drukhari has any
allied-codex or BATTLELINE-grant pattern requiring `detachment_effects.json` rows (check directly,
don't assume none); whether any units have Requisition Threshold or Wargear point-scaling shapes
not yet seen in a built faction; confirm Drukhari's Wahapedia faction code before use (do not guess
— derive it from `mfm_points_parser.py`/`repro_check.py`/`units_repro_check.py` per the standing
pattern used for every prior faction's registration in `detachment_parser.py`'s three maps).

This is a scoping turn only — do not start the units or detachments build itself this session.
Produce `DRUKHARI_BUILD_SCOPE.md` and stop there for Ryan's review of any product/legality calls it
surfaces, per the same handoff shape used for prior scope docs.

## Also open, at your discretion

- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances: CSM ×2, TS ×1, EC ×1, World Eaters ×2; Grey Knights and Chaos Daemons both confirmed to
  add 0 more). Engine turn, small. Not urgent — pre-existing and unenforced on six shipped
  detachments already.
- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock (`detachment_effects.json`) is
  recorded `enforced: false` on a stale premise (its own reason names Chaos Space Marines as
  not-built, which has been false since S212). Needs its own scoping pass to determine whether
  flipping `enforced: true` is safe as-is or needs the detachment's CSM unit list resolved from rule
  text first — found while checking B112, not investigated further this session.
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

- Re-derive from source, don't trust prior-session prose — including this prompt's own assumptions
  about Drukhari's shape. S220 and S221 both found inherited forecasts wrong on re-check (Grey
  Knights' enhancement count off by 2 despite a careful S200 pass; treat any assumption about
  Drukhari mirroring another faction the same way).
- Turn typing: this is a scoping turn. If it surfaces engine or tooling needs, note them for their
  own typed session — don't fold them in, and don't start the units/detachments build itself this
  session.
- No decisions currently waiting on Ryan from S221.

## Close

Produce the four documents, register `SESSION_HANDOFF_222.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
