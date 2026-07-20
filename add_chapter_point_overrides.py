#!/usr/bin/env python3
"""
add_chapter_point_overrides.py -- B56c (D167/D169).

Derives the per-chapter points override map fresh from source every build and
stamps it onto the matching generic (Adeptus Astartes) units in units.json.
Never hand-maintained -- the map is recomputed on every run, so a chapter MFM
change is picked up automatically instead of going stale (D107).

Why this exists: mfm_points_parser.py's --scope-to-army chapter run (B56a)
correctly DROPS any chapter MFM entry with no chapter-owned datasheet, because
writing it under the chapter's own army name would leave it unreachable --
the unit's only datasheet lives in the Adeptus Astartes block, and
resolveUnits in index.html unions that block into every chapter's view at
selection time. Those dropped entries are exactly the override candidates: a
chapter MFM re-prices a generic unit without ever owning its own copy of the
datasheet.

Method: re-parse each chapter MFM file directly with mfm_points_parser's own
parse_mfm()/to_points_row() (the same functions the real pipeline run uses --
no re-implementation of the bracket/tier grammar). For every costed chapter
unit whose name is NOT a chapter-owned datasheet (checked against the SM
Unit_Stats.csv army-ownership, matching the B56a scope rule exactly) and DOES
have a generic Adeptus Astartes price to compare against, tag it as an
override candidate. Only candidates whose price actually differs from the
generic price get written -- a chapter agreeing with the base has nothing to
override.

Multiple chapters can override the same unit (Repulsor Executioner: SW, BA,
DA, DW all price it 230/250 against a base of 240/260) -- one unit can carry
several chapter keys in its override map, so the unit count and the row count
are different numbers; both are reported.

Field shape mirrors convert_to_json.py's "points" field exactly, so B56d can
later swap it in with no reshaping:
    "chapter_point_overrides": {
        "<Chapter Army Name>": {"sizes": [{"size":N,"first_unit":x,
                                            "second_unit":y,"third_plus":z}, ...]}
    }
Only units that actually gain at least one override get the field at all --
it is never defaulted onto the other 262 units.

Idempotent; part of the canonical units.json rebuild chain. Runs after
add_bodyguard_stat_flags.py, last step before the file is committed.
units_repro_check.py invokes it as the final step.

Usage:
  add_chapter_point_overrides.py --units units.json --stats sm_dir/Unit_Stats.csv
    --points sm_dir/Unit_Points.csv --mfm-dir .
"""
import argparse
import csv
import importlib.util
import json
import os
import sys

CHAPTERS = [
    ("MFM_Space_Wolves_v1_0.txt", "Space Wolves"),
    ("MFM_Blood_Angels_v1_0.txt", "Blood Angels"),
    ("MFM_Black_Templars_v1_0.txt", "Black Templars"),
    ("MFM_Dark_Angels_v1_0.txt", "Dark Angels"),
    ("MFM_Death_Watch_v1_0.txt", "Deathwatch"),
]
GENERIC_ARMY = "Adeptus Astartes"


def _load_mfm_module():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "mfm_points_parser", os.path.join(here, "mfm_points_parser.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _norm_cell(x):
    return "" if x is None else str(x).strip()


def _to_int_or_none(s):
    s = _norm_cell(s)
    return int(s) if s != "" else None


def _row_to_sizes(row):
    """row = [army, name, Size_1..3, Points_1-1..3-3] (to_points_row's shape)."""
    size_slots = [_to_int_or_none(v) for v in row[2:5]]
    pts = row[5:14]
    sizes = []
    for b in range(3):
        sz = size_slots[b]
        if sz is None:
            continue
        sizes.append({
            "size": sz,
            "first_unit":  _to_int_or_none(pts[b]),
            "second_unit": _to_int_or_none(pts[3 + b]),
            "third_plus":  _to_int_or_none(pts[6 + b]),
        })
    return {"sizes": sizes}


def derive_overrides(mfm, stats_path, points_path, mfm_dir):
    # Chapter-owned name sets (B56a's own scope rule, restated): a name is
    # "owned" by a chapter only if that chapter's own Unit_Stats.csv rows
    # carry it under that exact Army Name.
    with open(stats_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    ai = header.index("Army Name")
    ui = header.index("Unit Name")
    owned_by_army = {}
    for r in rows[1:]:
        if len(r) > ui:
            owned_by_army.setdefault(r[ai], set()).add(mfm.norm(r[ui]))

    # Generic (Adeptus Astartes) base price for every unit, post-chapter-append.
    # Override candidates were dropped by --scope-to-army, so their base row is
    # still the untouched Adeptus Astartes price at this point in the file.
    with open(points_path, encoding="utf-8-sig", newline="") as f:
        prows = list(csv.reader(f))
    base_points = {}
    for r in prows[1:]:
        if len(r) >= 2 and r[0] == GENERIC_ARMY:
            base_points[mfm.norm(r[1])] = r

    # unit_name_norm -> { chapter_army: sizes_obj }
    overrides = {}
    row_count = 0
    per_chapter_count = {}
    for mfm_file, army in CHAPTERS:
        path = os.path.join(mfm_dir, mfm_file)
        units = mfm.parse_mfm(path)
        owned = owned_by_army.get(army, set())
        for nkey, info in units.items():
            if not info["tiers"] or not any(t for t in info["tiers"]):
                continue
            if nkey in owned:
                continue  # chapter-native datasheet, not an override case
            if nkey not in base_points:
                continue  # no generic datasheet to override either
            display_name = info["name"].title() if info["name"].isupper() else info["name"]
            override_row = mfm.to_points_row(army, display_name, info)
            base_row = base_points[nkey]
            ov_cells = [_norm_cell(c) for c in override_row[2:]]
            base_cells = [_norm_cell(c) for c in base_row[2:]]
            if ov_cells == base_cells:
                continue  # chapter agrees with generic -- nothing to override
            overrides.setdefault(nkey, {"name": display_name, "chapters": {}})
            overrides[nkey]["chapters"][army] = _row_to_sizes(override_row)
            row_count += 1
            per_chapter_count[army] = per_chapter_count.get(army, 0) + 1

    return overrides, row_count, per_chapter_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", required=True)
    ap.add_argument("--stats", required=True)
    ap.add_argument("--points", required=True)
    ap.add_argument("--mfm-dir", default=".")
    args = ap.parse_args()

    mfm = _load_mfm_module()
    overrides, row_count, per_chapter = derive_overrides(
        mfm, args.stats, args.points, args.mfm_dir)

    with open(args.units, encoding="utf-8") as f:
        units = json.load(f)

    by_norm = {}
    for army_block in units:
        if army_block.get("army") != GENERIC_ARMY:
            continue
        for unit in army_block.get("units", []):
            by_norm[mfm.norm(unit.get("unit_name", ""))] = unit

    missing = [v["name"] for k, v in overrides.items() if k not in by_norm]
    if missing:
        print(f"ERROR override unit(s) not found in {GENERIC_ARMY} block: {missing}",
              file=sys.stderr)
        sys.exit(1)

    touched = []
    for nkey, info in overrides.items():
        unit = by_norm[nkey]
        unit["chapter_point_overrides"] = info["chapters"]
        touched.append((unit.get("unit_id"), info["name"], sorted(info["chapters"])))

    with open(args.units, "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2, ensure_ascii=False)

    print(f"OK   {len(touched)} unit(s) tagged, {row_count} chapter-override row(s) "
          f"({', '.join(f'{k} {v}' for k, v in sorted(per_chapter.items()))})")
    for uid, name, chapters in touched:
        print(f"  {uid}  {name}  <- {', '.join(chapters)}")


if __name__ == "__main__":
    main()
