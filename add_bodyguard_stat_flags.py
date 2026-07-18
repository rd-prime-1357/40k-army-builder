#!/usr/bin/env python3
"""
B7b (D157/D159) -- populate `bodyguard_stat_flags` on the first model group of
every built SM+DG leader unit whose unit abilities modify a bodyguard stat on
the markable-stat list (INV, FNP, LD, T, M, OC) when the leader is attached.

Resolution method: hand-audit of every leader's unit-ability text against the
five markable characteristics. Flags recorded here as a hardcoded map keyed by
unit_id -- no runtime ability-text parser -- following the add_co_leader.py
precedent (D144/D147, B49).

Every non-flagged leader unit (and every non-leader unit) gets an empty
`bodyguard_stat_flags` list on each of its model groups, so the field is always
present and consumers can read it unconditionally. This matches the
`co_leader_any` default-False handling in convert_to_json.py.

Idempotent; part of the canonical units.json rebuild chain. Runs after
add_co_leader.py, before the file is committed. units_repro_check.py invokes
it as the final step.

Ambiguity calls made this pass (D159, all reversible if Ryan overrides):
  - Conditional FNP (vs Psychic Attacks / vs mortal wounds) flagged.
  - Wind Walker's temporary M mod flagged.
  - Grimaldus Column from the Major Altar (Temple Relic choice) T flagged.
  - Ravenwing Command Squad "this unit contains X" OC flagged when merged unit
    per rules 19.02-19.04 treats "this unit" as the whole Attached unit.
"""
import argparse
import json
import sys

# unit_id -> list of stat-name strings; only the flags that fire.
# Every unit_id here must be a built SM+DG leader carrying at least one aura
# that modifies a bodyguard stat on the markable-stat list.
FLAG_MAP = {
    # === Space Marines / Adeptus Astartes ===
    "000000079": ["FNP"],                # Librarian In Terminator Armour (Psychic Hood, conditional)
    "000000115": ["FNP"],                # Chaplain In Terminator Armour (Recitation of Faith, conditional)
    "000000119": ["FNP"],                # Librarian In Phobos Armour (Psychic Hood, conditional)
    "000000127": ["FNP"],                # Iron Father Feirros (Rites of Tempering, unconditional 5+)
    "000000158": ["FNP"],                # Sanguinary Priest (unconditional 5+)
    "000000226": ["FNP"],                # Ezekiel (Psychic Hood, conditional)
    "000001165": ["OC"],                 # Bladeguard Ancient (Astartes Banner +1 OC)
    "000001611": ["FNP"],                # Chief Librarian Tigurius (Hood of Hellfire, conditional)
    "000002266": ["INV", "FNP"],         # Librarian (Mental Fortress 4+ INV; Psychic Hood conditional FNP)
    "000002677": ["OC"],                 # Ancient In Terminator Armour (Astartes Banner +1 OC)
    "000002748": ["OC"],                 # Ravenwing Command Squad (Astartes Banner, contains-clause)
    "000002775": ["OC"],                 # Ancient (Astartes Banner +1 OC)
    "000002792": ["T"],                  # Chaplain Grimaldus (Column from the Major Altar +1 T, relic choice)

    # === Death Guard ===
    "000001058": ["M"],                  # Noxious Blightbringer (Sickening Vitality +1" Move)
    "000002750": ["OC"],                 # Icon Bearer (Unclean Icon +1 OC)

    # === Space Wolves ===
    "000000292": ["M"],                  # Njal Stormcaller (Wind Walker +6" Move during Advance)
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", required=True)
    args = ap.parse_args()

    with open(args.units, encoding="utf-8") as f:
        units = json.load(f)

    by_id = {}
    for army in units:
        for unit in army.get("units", []):
            by_id[unit.get("unit_id")] = unit

    # Guard: every flagged unit_id must exist (catches drift if the roster changes).
    missing = [uid for uid in FLAG_MAP if uid not in by_id]
    if missing:
        print(f"ERROR flagged unit_id(s) not found in units.json: {missing}", file=sys.stderr)
        sys.exit(1)

    # Default all units' model groups to an empty flag list so downstream code
    # can read the field unconditionally. Non-list existing values are replaced.
    for army in units:
        for unit in army.get("units", []):
            for mg in unit.get("model_groups", []):
                if not isinstance(mg.get("bodyguard_stat_flags"), list):
                    mg["bodyguard_stat_flags"] = []

    # Populate the flagged leaders on the first model group only (matches the
    # single-Character-model shape of every flagged unit in SM+DG today; the
    # first model group is the Character panel for RCS as well).
    touched = []
    for uid, flags in FLAG_MAP.items():
        unit = by_id[uid]
        mgs = unit.get("model_groups", [])
        if not mgs:
            print(f"ERROR {uid} ({unit.get('unit_name')}): no model_groups", file=sys.stderr)
            sys.exit(1)
        mgs[0]["bodyguard_stat_flags"] = list(flags)
        touched.append((uid, unit.get("unit_name"), flags))

    if len(touched) != len(FLAG_MAP):
        print(f"ERROR expected {len(FLAG_MAP)} units tagged, tagged {len(touched)}", file=sys.stderr)
        sys.exit(1)

    with open(args.units, "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2, ensure_ascii=False)

    print(f"OK   set bodyguard_stat_flags on {len(touched)} leader units")


if __name__ == "__main__":
    main()
