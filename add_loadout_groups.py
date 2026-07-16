#!/usr/bin/env python3
"""
B44 (D135) — add a `loadout_groups` shared key to units.json statline model
groups, so a statline group can be mapped to the unit_loadouts.json loadout
group(s) it corresponds to.

Only the 8 units whose datasheet is split into more than one statline group
need a mapping (a single statline group already covers the whole unit; the
existing engine logic handles that trivially). The correspondence below was
verified by hand against Datasheets_models.csv / Datasheets_unit_composition.csv
and the committed unit_loadouts.json group names — it is not derivable by
string-matching alone (that is exactly what was failing before, per D112 /
the original B44 note).

Pink Horrors (local:chaos-daemons:pink-horrors) is also a multi-statline-group
unit but carries no unit_loadouts.json entry at all (Chaos Daemons has no
loadout data yet) — out of scope, left untouched.

This script is idempotent and part of the canonical units.json rebuild chain
(run after convert_to_json.py / wahapedia_transform.py, before the file is
committed). units_repro_check.py invokes it as the final step.
"""
import argparse
import json
import sys

# unit_id -> { statline model_group name : [loadout group names] }
MAPPING = {
    "000002712": {  # Outrider Squad
        "OUTRIDER": ["Outrider Sergeant", "Outriders"],
        "INVADER ATV": ["Invader ATV"],
    },
    "000004188": {  # Wardens of Ultramar
        "Ancient Gadriel, Veteran Sergeant Metaurus": [
            "Ancient Gadriel - EPIC HERO", "Veteran Sergeant Metaurus - EPIC HERO",
        ],
        "Gaius Silva, Aemelia Minervas, Dainal Kornelius, Lucia Vestha": [
            "Gaius Silva - EPIC HERO", "Aemelia Minervas - EPIC HERO",
            "Dainal Kornelius - EPIC HERO", "Lucia Vestha - EPIC HERO",
        ],
    },
    "000004131": {  # Wolf Guard Headtakers
        "Wolf Guard Headtakers": ["Wolf Guard Headtakers"],
        "Hunting Wolves": ["Hunting Wolves"],
    },
    "000004182": {  # Wolf Scouts
        "WOLF SCOUTS": ["Wolf Scout Pack Leader", "Wolf Scouts"],
        "HUNTING WOLVES": ["Hunting Wolves"],
    },
    "000003874": {  # Talonstrike Kill Team
        "KILL TEAM SERGEANT WITH JUMP PACK AND KILL TEAM INTERCESSORS WITH JUMP PACKS": [
            "Kill Team Sergeant with Jump Pack", "Kill Team Intercessors with Jump Packs",
        ],
        "KILL TEAM HEAVY INTERCESSORS WITH JUMP PACKS": [
            "Kill Team Heavy Intercessors with Jump Packs",
        ],
    },
    "000004175": {  # Decimus Kill Team
        "KILL TEAM SERGEANT, DEATHWATCH VETERAN": [
            "Kill Team Sergeant", "Deathwatch Veterans",
        ],
        "GRAVIS VETERAN": ["Gravis Veterans"],
    },
    "000002792": {  # Chaplain Grimaldus
        "GRIMALDUS": ["Chaplain Grimaldus - EPIC HERO"],
        "CENOBYTE SERVITOR": ["Cenobyte Servitors*"],
    },
    "000002799": {  # Crusader Squad
        "NEOPHYTES": ["Neophytes"],
        "OTHER MODELS": ["Sword Brother", "Initiates"],
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", default="units.json")
    ap.add_argument("--loadouts", default="unit_loadouts.json")
    args = ap.parse_args()

    with open(args.units, encoding="utf-8") as f:
        units = json.load(f)
    with open(args.loadouts, encoding="utf-8") as f:
        loadouts = json.load(f)

    touched = []
    for army in units:
        for unit in army.get("units", []):
            uid = unit.get("unit_id")
            if uid not in MAPPING:
                continue
            per_group = MAPPING[uid]
            def_ = loadouts.get(uid)
            loadout_names = set(g["name"] for g in def_.get("model_groups", [])) if def_ else set()
            for mg in unit.get("model_groups", []):
                name = mg.get("model_group")
                if name in per_group:
                    lgs = per_group[name]
                    missing = [n for n in lgs if n not in loadout_names]
                    if missing:
                        print(f"ERROR {uid} '{name}': loadout group(s) not found: {missing}", file=sys.stderr)
                        sys.exit(1)
                    mg["loadout_groups"] = lgs
                    touched.append((uid, unit.get("unit_name"), name, lgs))

    expected = sum(len(v) for v in MAPPING.values())
    if len(touched) != expected:
        print(f"ERROR expected to tag {expected} statline groups, tagged {len(touched)}", file=sys.stderr)
        sys.exit(1)

    with open(args.units, "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2, ensure_ascii=False)

    print(f"OK   tagged {len(touched)} statline groups across {len(MAPPING)} units with loadout_groups")


if __name__ == "__main__":
    main()
