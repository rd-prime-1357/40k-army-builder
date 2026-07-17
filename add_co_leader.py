#!/usr/bin/env python3
"""
B38a (D143/D144) — populate `co_leader_eligible_with` for the 12 built SM units
that carry a named co-leader clause in their `leader_footer` (the Captain /
Chapter Master / Lieutenant / Execrator role-word families, plus the Cato
Sicarius -> Marneus Calgar named pair).

Resolution method (matches B49's precedent for `leader_eligible_units`: read
the real rules text, expand role-words to the family of built datasheets that
carry the matching keyword, hand-verify against source, hardcode the result --
not a runtime footer-text parser). Verified against Datasheets_keywords.csv:

  CAPTAIN keyword    -> 25 built datasheets (Captain and its armour variants,
                         plus every Captain-rank named Epic Hero)
  CHAPTER MASTER kw  -> 8 built datasheets (all named Epic Heroes; no built
                         datasheet is literally named "Chapter Master" -- the
                         current codex folded it into named Epic Heroes only)
  LIEUTENANT keyword -> 5 built datasheets (Lieutenant and its variants, plus
                         Castellan, which carries the Lieutenant keyword)
  EXECRATOR keyword  -> 1 built datasheet (Execrator)

No two of these four keyword sets overlap on any built datasheet (checked).
Cato Sicarius's footer names Marneus Calgar specifically, not a role-word
family, so gets a single-name list.

This script is idempotent and part of the canonical units.json rebuild chain
(run after add_loadout_groups.py, before the file is committed).
units_repro_check.py invokes it as the final step.
"""
import argparse
import json
import sys

# Built unit_names carrying the CAPTAIN keyword (Datasheets_keywords.csv, verified 2026-07).
_CAPTAIN = [
    "Adrax Agatone", "Belial", "Blood Angels Captain", "Caanok Var", "Captain",
    "Captain In Gravis Armour", "Captain In Phobos Armour", "Captain In Terminator Armour",
    "Captain Titus", "Captain With Jump Pack", "Cato Sicarius", "Darnath Lysander",
    "Death Company Captain", "Death Company Captain with Jump Pack", "Kor’sarro Khan",
    "Lazarus", "Ragnar Blackmane", "Sammael", "Suboden Khan", "Tor Garadon",
    "Uriel Ventris", "Vulkan He’stan", "Watch Captain Artemis", "Watch Master",
]
# Built unit_names carrying the CHAPTER MASTER keyword.
_CHAPTER_MASTER = [
    "Aethon Shaan", "Azrael", "Commander Dante", "High Marshal Helbrecht",
    "Kayvaan Shrike", "Logan Grimnar", "Marneus Calgar in Armour of Antilochus",
    "Pedro Kantor",
]
# Built unit_names carrying the LIEUTENANT keyword.
_LIEUTENANT = [
    "Castellan", "Lieutenant", "Lieutenant In Phobos Armour",
    "Lieutenant In Reiver Armour", "Lieutenant With Combi-weapon",
]
# Built unit_names carrying the EXECRATOR keyword.
_EXECRATOR = ["Execrator"]

_GROUP_A = sorted(set(_CAPTAIN) | set(_CHAPTER_MASTER))                       # "Captain or Chapter Master"
_GROUP_B = sorted(set(_CAPTAIN) | set(_CHAPTER_MASTER) | set(_LIEUTENANT))    # "...or Lieutenant"
_GROUP_D = sorted(set(_GROUP_B) | set(_EXECRATOR))                            # "...Execrator or Lieutenant"

# unit_id -> resolved co_leader_eligible_with list
MAPPING = {
    "000000060": _GROUP_A,  # Apothecary Biologis           -- "Captain or Chapter Master"
    "000001345": _GROUP_A,  # Lieutenant In Reiver Armour    -- "Captain or Chapter Master"
    "000001346": _GROUP_A,  # Lieutenant                     -- "Captain or Chapter Master"
    "000002530": _GROUP_A,  # Lieutenant In Phobos Armour    -- "Captain or Chapter Master"
    "000002793": _GROUP_A,  # Castellan                      -- "Captain or Chapter Master"
    "000001165": _GROUP_B,  # Bladeguard Ancient             -- "...or Lieutenant"
    "000002677": _GROUP_B,  # Ancient In Terminator Armour   -- "...or Lieutenant"
    "000002773": _GROUP_B,  # Apothecary                     -- "...or Lieutenant"
    "000002775": _GROUP_B,  # Ancient                        -- "...or Lieutenant"
    "000000158": _GROUP_B,  # Sanguinary Priest              -- "...or Lieutenant"
    "000004184": ["Marneus Calgar in Armour of Antilochus"],  # Cato Sicarius -- named pair
    "000004136": _GROUP_D,  # Crusade Ancient                -- "...Execrator or Lieutenant"
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", default="units.json")
    args = ap.parse_args()

    with open(args.units, encoding="utf-8") as f:
        units = json.load(f)

    built_names = set()
    by_id = {}
    for army in units:
        for unit in army.get("units", []):
            built_names.add(unit.get("unit_name"))
            by_id[unit.get("unit_id")] = unit

    # Guard: every mapped unit_id must exist, and every name in every mapping
    # list must be a real built unit_name (catches drift if the roster changes).
    missing_units = [uid for uid in MAPPING if uid not in by_id]
    if missing_units:
        print(f"ERROR mapped unit_id(s) not found in units.json: {missing_units}", file=sys.stderr)
        sys.exit(1)
    for uid, names in MAPPING.items():
        dangling = [n for n in names if n not in built_names]
        if dangling:
            print(f"ERROR {uid}: co-leader name(s) not found among built units: {dangling}", file=sys.stderr)
            sys.exit(1)
        self_name = by_id[uid].get("unit_name")
        if self_name in names:
            print(f"ERROR {uid} ({self_name}): self-reference in its own co_leader_eligible_with list", file=sys.stderr)
            sys.exit(1)

    touched = []
    for uid, names in MAPPING.items():
        unit = by_id[uid]
        for mg in unit.get("model_groups", []):
            mg["co_leader_eligible_with"] = list(names)
            touched.append((uid, unit.get("unit_name"), mg.get("model_group")))

    if len(touched) != len(MAPPING):
        # every one of these 12 units is a single-model_group Character, so 1:1 is expected
        print(f"ERROR expected 12 model-groups tagged (one per unit), tagged {len(touched)}", file=sys.stderr)
        sys.exit(1)

    with open(args.units, "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2, ensure_ascii=False)

    print(f"OK   set co_leader_eligible_with on {len(touched)} units ({len(MAPPING)} target unit_ids)")


if __name__ == "__main__":
    main()
