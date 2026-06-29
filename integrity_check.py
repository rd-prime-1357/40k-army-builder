#!/usr/bin/env python3
"""
Integrity check for a faction's nine CSVs.

This is the COMPREHENSIVE structural pass that the 4-unit manual check cannot do.
It scans every unit and reports referential / structural problems:

  1. Wargear/Other options that reference a weapon not present on that unit
     (and not a known wargear item in Weapon_Abilities) -- catches the unresolved
     raw "plasma gun" family names and genuine name mismatches.
  2. Unit_Points rows with no matching Unit_Stats row, and Unit_Stats rows with
     no points (the latter is the known chapter-character gap -- summarised).
  3. Ability names on a unit ("Unit Ability Names") with no Unit_Abilities entry.
  4. Rule names on a unit ("Rule Names") with no Rules entry (params collapsed).
  5. Weapon ability names on a weapon with no Keywords entry (params collapsed).
  6. Option rows whose (Army, Unit) does not exist in Unit_Stats.
  7. Lookup rows with a blank description (work-queue surface).
  8. Duplicate unit definitions in Unit_Stats.

It does NOT verify accuracy against the real game (points values, profiles) --
that requires a human and New Recruit. This catches everything mechanical.

Stdlib only.  python integrity_check.py --dir out
"""

import argparse
import csv
import os
import re
from collections import defaultdict, OrderedDict

def norm(s):
    s = (s or "").lower().strip()
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    s = re.sub(r"[^a-z0-9+ '/-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def generic_of(instance):
    g = re.sub(r"\s+[0-9]+\+?$", "", instance)
    g = re.sub(r"\s+[dD][36]\+?$", "", g)
    g = re.sub(r"\s+[0-9]+\+$", "", g)
    return g.strip()

def read(path):
    if not os.path.exists(path):
        return [], []
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return [], []
    return rows[0], rows[1:]

def col(header, name):
    try:
        return header.index(name)
    except ValueError:
        return None

def split_names(cell):
    return [x.strip() for x in (cell or "").split(",") if x.strip()]

def main():
    ap = argparse.ArgumentParser(description="Integrity check for the nine faction CSVs")
    ap.add_argument("--dir", default="out", help="folder containing the nine CSVs")
    ap.add_argument("--out", default=None, help="report path (default <dir>/integrity_report.md)")
    args = ap.parse_args()
    D = args.dir
    out_path = args.out or os.path.join(D, "integrity_report.md")
    issues = OrderedDict()
    def add(key, msg):
        issues.setdefault(key, []).append(msg)

    # ---- load ----
    sh, sr = read(os.path.join(D, "Unit_Stats.csv"))
    wh, wr = read(os.path.join(D, "Unit_Weapons.csv"))
    gh, gr = read(os.path.join(D, "Unit_Wargear_Options.csv"))
    oh, orr = read(os.path.join(D, "Unit_Other_Options.csv"))
    ph, pr = read(os.path.join(D, "Unit_Points.csv"))
    ah, ar = read(os.path.join(D, "Unit_Abilities.csv"))
    rh, rr = read(os.path.join(D, "Rules.csv"))
    kh, kr = read(os.path.join(D, "Keywords.csv"))
    bh, br = read(os.path.join(D, "Weapon_Abilities.csv"))

    s_army, s_unit = col(sh, "Army Name"), col(sh, "Unit Name")
    s_mg = col(sh, "Model Group")
    s_ab, s_rule = col(sh, "Unit Ability Names"), col(sh, "Rule Names")

    # unit identity sets
    stats_keys = set()           # (army, unit)
    stats_units_byname = defaultdict(set)   # unit -> set(army)
    seen = set()
    for r in sr:
        if len(r) <= max(s_army, s_unit):
            continue
        army, unit = r[s_army].strip(), r[s_unit].strip()
        mg = r[s_mg].strip() if s_mg is not None and len(r) > s_mg else ""
        dkey = (norm(army), norm(unit), norm(mg))
        if dkey in seen:
            add("dup_units", f"{army} / {unit} / {mg}")
        seen.add(dkey)
        stats_keys.add((norm(army), norm(unit)))
        stats_units_byname[norm(unit)].add(norm(army))

    # weapons per unit
    w_army, w_unit, w_name = col(wh, "Army Name"), col(wh, "Unit Name"), col(wh, "Weapon Name")
    w_ab = col(wh, "Weapon Ability Names")
    weapons_by_unit = defaultdict(set)
    for r in wr:
        if len(r) <= max(w_army, w_unit, w_name):
            continue
        weapons_by_unit[(norm(r[w_army]), norm(r[w_unit]))].add(norm(r[w_name]))

    # lookup name sets
    ua_names = {norm(r[0]) for r in ar if r}
    rule_names = {norm(r[0]) for r in rr if r}
    kw_names = {norm(r[0]) for r in kr if r}
    wa_names = {norm(r[0]) for r in br if r}

    # ---- 7. blank descriptions ----
    for label, header, rows in [("Keywords", kh, kr), ("Rules", rh, rr),
                                ("Weapon_Abilities", bh, br), ("Unit_Abilities", ah, ar)]:
        for r in rows:
            if r and (len(r) < 2 or not r[1].strip()):
                add(f"blank_desc_{label}", r[0])

    # ---- 1 & 6. option references ----
    for label, header, rows in [("Wargear", gh, gr), ("Other", oh, orr)]:
        c_army = col(header, "Army Name"); c_unit = col(header, "Unit Name")
        c_repl = col(header, "Replacement Weapon Name")
        c_was = col(header, "Weapon Replaced")
        c_opt = col(header, "Option Name")
        for r in rows:
            if c_army is None or len(r) <= max(c_army, c_unit):
                continue
            army, unit = r[c_army].strip(), r[c_unit].strip()
            ukey = (norm(army), norm(unit))
            if ukey not in stats_keys:
                add("option_orphan_unit", f"{label}: {army} / {unit} (no Unit_Stats row)")
            uw = weapons_by_unit.get(ukey, set())
            for ci, role in [(c_was, "Weapon Replaced"), (c_repl, "Replacement"), (c_opt, "Option Name")]:
                if ci is None or ci >= len(r):
                    continue
                val = r[ci].strip()
                if not val:
                    continue
                nv = norm(val)
                if nv in uw or nv in wa_names:
                    continue
                hint = "likely weapon-family (lowercase) -> map to a profile" if val == val.lower() else "name mismatch / typo"
                add("option_unresolved_ref", f"{label}: {unit} | {role}='{val}' not found ({hint})")

    # ---- 2. points <-> stats ----
    p_army, p_unit = col(ph, "Army Name"), col(ph, "Unit Name")
    points_keys = set()
    points_units = set()
    for r in pr:
        if len(r) <= max(p_army, p_unit):
            continue
        army, unit = r[p_army].strip(), r[p_unit].strip()
        points_keys.add((norm(army), norm(unit)))
        points_units.add(norm(unit))
        if (norm(army), norm(unit)) not in stats_keys:
            if norm(unit) in stats_units_byname:
                add("points_army_fallback", f"{army} / {unit}: points army differs from stats army(s) {sorted(stats_units_byname[norm(unit)])} (app falls back -- verify intended)")
            else:
                add("points_no_stat", f"{army} / {unit}: points row with no matching unit")
    for key in stats_keys:
        if key[1] not in points_units:
            add("stat_no_points", f"{key[0]} / {key[1]}")

    # ---- 3,4,5 glossary references ----
    for r in sr:
        if len(r) <= max(s_unit, s_ab, s_rule):
            continue
        unit = r[s_unit].strip()
        for nm in split_names(r[s_ab]):
            if norm(nm) not in ua_names:
                add("missing_unit_ability", f"{unit}: '{nm}' not in Unit_Abilities")
        for nm in split_names(r[s_rule]):
            if norm(generic_of(nm)) not in rule_names and norm(nm) not in rule_names:
                add("missing_rule", f"{unit}: '{nm}' not in Rules")
    for r in wr:
        if w_ab is None or len(r) <= w_ab:
            continue
        unit = r[w_unit].strip()
        for nm in split_names(r[w_ab]):
            if norm(generic_of(nm)) not in kw_names and norm(nm) not in kw_names:
                add("missing_weapon_ability", f"{unit}: '{nm}' not in Keywords")

    # ---- report ----
    order = [
        ("dup_units", "Duplicate unit definitions in Unit_Stats"),
        ("option_orphan_unit", "Option rows whose unit is not in Unit_Stats"),
        ("option_unresolved_ref", "Option references not found in weapons or wargear items"),
        ("points_no_stat", "Points rows with no matching unit"),
        ("points_army_fallback", "Points Army Name differs from Stats (fallback cases)"),
        ("missing_unit_ability", "Unit ability names with no glossary entry"),
        ("missing_rule", "Rule names with no Rules entry"),
        ("missing_weapon_ability", "Weapon ability names with no Keywords entry"),
        ("blank_desc_Keywords", "Keywords with blank description"),
        ("blank_desc_Rules", "Rules with blank description"),
        ("blank_desc_Weapon_Abilities", "Weapon_Abilities with blank description"),
        ("blank_desc_Unit_Abilities", "Unit_Abilities with blank description"),
        ("stat_no_points", "Units with no points (expected: chapter characters etc.)"),
    ]
    blocking = ("dup_units", "option_orphan_unit", "option_unresolved_ref",
                "points_no_stat", "missing_unit_ability", "missing_rule", "missing_weapon_ability")
    L = ["# Integrity Report\n"]
    total_block = sum(len(issues.get(k, [])) for k in blocking)
    L.append(f"**Blocking issues (break the app if loaded): {total_block}**")
    L.append(f"Non-blocking / expected items are listed below the blocking ones.\n")
    for key, title in order:
        items = issues.get(key, [])
        tag = "  ⛔" if key in blocking and items else ""
        L.append(f"## {title} — {len(items)}{tag}")
        for it in items[:500]:
            L.append(f"- {it}")
        if len(items) > 500:
            L.append(f"- ...and {len(items)-500} more")
        L.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"Integrity check complete -> {out_path}")
    print(f"  BLOCKING issues: {total_block}")
    for key in blocking:
        n = len(issues.get(key, []))
        if n:
            print(f"    - {key}: {n}")


if __name__ == "__main__":
    main()
