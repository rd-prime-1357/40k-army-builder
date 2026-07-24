# Session 133 handoff — B61 shipped: Plague Legions tagged at the parser

**Turn type: parser-only.** `mfm_points_parser.py`, `convert_to_json.py` (minimal pass-through of the
new field), `units.json` re-banked, four new assertions. No engine, no `index.html`. `index.html`
stays at **6.5**, assertions **88/88**, baseline **21/21** at close. Authoritative write-up is **D208**
in `40K_Decision_Log_v3_0.md`.

---

## What shipped

`mfm_points_parser.py` gained `ALLIED_GROUP_HEADERS`, a known-label lookup recognising the six
allied-group section headers Wahapedia carries across the priority factions: Plague Legions (Death
Guard), Scintillating Legions (Thousand Sons), Blood Legions (World Eaters), Legions of Excess
(Emperor's Children), Harlequins and Ynnari (Aeldari). Written generally per the ticket, not as a
Death-Guard special case.

**A structural rule was tried first and rejected.** The obvious general check — any all-caps line
whose next real line is itself a unit header — was scanned against every MFM file the pipeline
actually runs before being written into the parser. It fires far beyond the five intended headers: it
also matches every LEADER eligible-unit comma-list and every chapter-name divider (Imperial Fists,
Iron Hands, Salamanders, Raven Guard, Ultramarines, White Scars, plus every `LEGENDS`/`SPACE MARINES`
divider) across the Space Marines and chapter files — dozens of false positives per file. The known-
label lookup has none, and is exactly as general as the ticket asked for: adding Thousand Sons/World
Eaters/Emperor's Children/Aeldari to the built roster needs no parser change, only their own MFM files
running through the existing pipeline.

**Boundary and tagging.** A recognised header opens the section; `DETACHMENTS` or `LEGENDS` closes it
— confirmed as the closing marker in all five files carrying an allied-group header, not just Death
Guard's. Every unit created while the section is open is tagged `allied_group: "<Label>"`; every other
unit carries no such key at all, matching the file's existing convention that optional per-unit fields
(`co_leader_eligible_with`, `bodyguard_stat_flags`) are absent rather than present-with-null.

**Threaded through, not hand-patched.** `Unit_Points.csv` gained a trailing `Allied_Group` column
(empty on every row except the six). `convert_to_json.py` reads it and sets `allied_group` on the unit
object only when non-empty — a minimal pass-through change, no other converter logic touched. Ran the
full pipeline exactly as `units_repro_check.py` runs it and copied its output over the committed
`units.json`. Diffed old against new before committing: the only substantive change anywhere in the
catalogue is six unit_ids — Beasts of Nurgle, Great Unclean One, Nurglings, Plaguebearers, Plague
Drones, Rotigus — each gaining exactly one new key (`allied_group`), no existing key touched anywhere.
All four merged lookups and `faction_taxonomy.json` stayed byte-identical. `units_repro_check.py` now
reports byte-identical reproduction again.

**Four assertions filed** — B61-1 through B61-4 in `rules_assertions.py`: the exact six-unit census in
Death Guard and nowhere else in that army; no other army block carries the field at all; Chaos
Daemons' own native copies of the same six units carry distinct `unit_id`s and no tag (confirming
Wahapedia's double-listing, not a merge collision); and `ALLIED_GROUP_HEADERS` still names all six
labels, guarding the general mechanism against silently narrowing back to a Death-Guard-only check.

## Still open for Ryan

Nothing new needs your input this session — no product or rules-legality call came up.

The two standing items from S132 remain unresolved: the Soul Grinder god-weapon render is still
unverified (confirmed with you at session open — you flagged it as looked-at and good), and D199's
four batched calls have now gone unreviewed since S127.

---

## Decided

* A known-label lookup over a structural rule, before either was written into the parser — the
  structural version was prototyped read-only against every in-scope MFM file first, and its false-
  positive rate (dozens per file, mostly LEADER lists and chapter dividers) settled the choice without
  needing a judgment call (D208).
* `allied_group` absent rather than present-as-null on untagged units, matching the file's existing
  convention for optional per-unit fields rather than the weapon-level `allegiance_condition: null`
  convention D207 set a session earlier — the two sit at different levels of the schema (per-unit vs.
  per-weapon) and D208 records why the same session didn't default to the more recent precedent.
* `DETACHMENTS` and `LEGENDS` as the section-close markers — verified against all five files carrying
  an allied-group header, not asserted from the one Death Guard case.

---

## Files

Changed:

| File | SHA-256 (first 12) |
| --- | --- |
| `mfm_points_parser.py` | `6b6a28edf54a` |
| `convert_to_json.py` | `9af5832f6df7` |
| `units.json` | `881919dfa5e4` |
| `rules_assertions.py` | `2bf6a3a6b65b` |
| `pipeline_manifest.json` | `7a2add134c41` |
| `40K_Decision_Log_v3_0.md` | `ba180597709b` |
| `DECISION_INDEX.md` | `c601e5d1eb31` |
| `OPEN_ITEMS_BACKLOG.md` | `f61b79508a0d` |
| `BACKLOG_ARCHIVE.md` | `26753a961f9c` |
| `SESSION_HANDOFF_133.md` | *self* |
| `NEXT_SESSION_PROMPT.md` | `c4c85f07710c` |

Net new: none. (`detachment_effects.json` is next session's net-new file, not this one's.)

**Repo custody.** All eleven changed documents/scripts/JSON above are project-generated and
repo-eligible. No GW-derived source material was touched this session — `MFM_Death_Guard_v1_0.txt`
and the other four allied-group-bearing MFM files were read, not written.

## Backlog

**7 open:** B62, P2, E21, E22 (E22a done, E22b remains), B60, E12, B17.

- Beginning tickets: B61, B62, P2, E21, E22, B60, E12, B17 (8)
- Resolved tickets: B61
- Added tickets: none
- Ending tickets: B62, P2, E21, E22, B60, E12, B17 (7)
