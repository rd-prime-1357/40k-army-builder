#!/usr/bin/env python3
"""
merge_factions.py — assemble the deployed master JSON set from per-faction
converter outputs.

Each converter run (convert_to_json.py) writes a single-or-multi-block units.json
plus four lookup JSONs into its output dir. This script concatenates every faction's
army blocks into one master units.json and unions the four lookups, so the app loads
one master set. It replaces the manual hand-merge that previously risked silently
overwriting a faction's deployed data.

Lookup conflicts: earlier --in dirs win (list them in priority order; the first dir's
shared core-rule descriptions are kept).

Validation: every faction marked built:true in the taxonomy must have a matching army
block in the merged units.json (matched on data_army). Missing blocks are reported as
errors — this is the guard that would have caught the dropped-Daemons case.

Usage:
  python merge_factions.py --in out --in dmn_out --taxonomy faction_taxonomy.json --out-dir deploy
"""
import argparse, json, os, sys

LOOKUPS = [
    ("abilities.json", "ability_name"),
    ("rules.json", "rule_name"),
    ("keywords.json", "keyword_name"),
    ("weapon_abilities.json", "weapon_ability_name"),
]

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="dirs", action="append", required=True,
                    help="converter output dir (repeatable, priority order)")
    ap.add_argument("--taxonomy", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # --- units: concatenate all army blocks, first dir's blocks first ---
    merged_units = []
    seen_armies = set()
    for d in args.dirs:
        for blk in load(os.path.join(d, "units.json")):
            if blk["army"] in seen_armies:
                print(f"  WARNING: duplicate army block '{blk['army']}' in {d} — skipped")
                continue
            merged_units.append(blk)
            seen_armies.add(blk["army"])
    with open(os.path.join(args.out_dir, "units.json"), "w", encoding="utf-8") as f:
        json.dump(merged_units, f, ensure_ascii=False, indent=2)

    # --- lookups: union, earlier dirs win ---
    for fname, key in LOOKUPS:
        merged, seen = [], set()
        for d in args.dirs:
            p = os.path.join(d, fname)
            if not os.path.exists(p):
                continue
            for row in load(p):
                if row[key] not in seen:
                    merged.append(row); seen.add(row[key])
        with open(os.path.join(args.out_dir, fname), "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)

    # --- taxonomy: pass through, then validate built ⇒ block present ---
    tax = load(args.taxonomy)
    with open(os.path.join(args.out_dir, "faction_taxonomy.json"), "w", encoding="utf-8") as f:
        json.dump(tax, f, ensure_ascii=False, indent=2)

    errors = []
    for g in tax["groups"]:
        for fac in g["factions"]:
            if not fac.get("built"):
                continue
            da = fac.get("data_army")
            if not da:
                errors.append(f"built faction '{fac['name']}' has no data_army")
            elif da not in seen_armies:
                errors.append(f"built faction '{fac['name']}' -> no army block '{da}' in merged units.json")

    total = sum(len(b["units"]) for b in merged_units)
    print(f"Merged: {len(merged_units)} army blocks, {total} units -> {args.out_dir}/units.json")
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("Validation OK: every built faction has a matching army block.")

if __name__ == "__main__":
    main()
