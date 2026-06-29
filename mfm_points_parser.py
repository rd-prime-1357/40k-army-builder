#!/usr/bin/env python3
"""
Munitorum Field Manual (MFM) points parser -> Unit_Points.csv

GW is authoritative for points, so points are sourced here, NOT from Wahapedia.
Designed to be reusable: it handles both the current per-faction web format and a
future all-faction MFM dump, because both reduce to the same structure:

    UNIT NAME (caps)
    YOUR UNIT COSTS                 (single copy-tier)
       -- or --
    YOUR 1ST TO 2ND UNITS COST      (tier 1-2)
    YOUR 3RD + UNIT COSTS           (tier 3)
       -- or --
    YOUR 1ST UNIT COSTS             (escalation: first copy)
    YOUR 2ND + UNIT COSTS           (escalation: 2nd copy onward, incl. 3rd+)
    • N models PPP pts              (one per size bracket; count & pts may be jammed)
    SUPPORT                         (character only: verbatim attach-eligible list)
    <comma-separated unit list>

Outputs Unit_Points.csv (Size_1..3, Points_b-t for brackets 1-3 x tiers 1-3) and,
when given the transformer's Unit_Stats.csv, patches its "Leader Eligible Units"
column with the verbatim SUPPORT lists. Names are matched to the datasheet set;
mismatches in either direction are flagged.

Stdlib only.  python mfm_points_parser.py --help
"""

import argparse
import csv
import os
import re
import sys
from collections import OrderedDict

ARMY_DEFAULT = "Adeptus Astartes"

COST_RE = re.compile(r"^[•\-\*]\s*(\d+)\s*models?\s*(\d+)\s*pts", re.I)
TIER_SINGLE = re.compile(r"your unit costs", re.I)
TIER_12 = re.compile(r"1st to 2nd", re.I)
TIER_3 = re.compile(r"3rd", re.I)
# Escalation-after-first scheme: "YOUR 1ST UNIT COSTS" / "YOUR 2ND + UNIT COSTS".
# TIER_1ST matches only "1st unit" (absent from the "1st to 2nd" line);
# TIER_2PLUS requires "2nd +"/"2nd+" (absent from "1st to 2nd units cost"),
# so neither collides with TIER_12.
TIER_1ST = re.compile(r"1st unit", re.I)
TIER_2PLUS = re.compile(r"2nd\s*\+", re.I)
SKIP_HEADERS = re.compile(r"^(your |munitorum|points value|wargear|enhancement)", re.I)

def norm(s):
    s = (s or "").upper()
    s = s.replace("’", "'").replace("–", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def is_unit_header(line):
    """A unit name line: mostly uppercase letters, not a bullet/tier/known keyword."""
    t = line.strip()
    if not t or t.startswith(("•", "-", "*")):
        return False
    if t.upper() in ("SUPPORT",):
        return False
    if SKIP_HEADERS.match(t):
        return False
    letters = [c for c in t if c.isalpha()]
    if not letters:
        return False
    upper_ratio = sum(c.isupper() for c in letters) / len(letters)
    return upper_ratio > 0.9

def parse_mfm(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = [ln.rstrip("\n").rstrip("\r") for ln in f]

    def next_meaningful(idx):
        j = idx + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        return lines[j].strip() if j < len(lines) else ""

    def is_tier(s):
        return bool(TIER_SINGLE.search(s) or TIER_12.search(s) or TIER_3.search(s)
                    or TIER_1ST.search(s) or TIER_2PLUS.search(s))

    def is_real_unit_header(idx):
        # A unit name is an all-caps line immediately followed (next meaningful
        # line) by a tier header. Separates unit names from SUPPORT lists and
        # from detachment/enhancement sections.
        return is_unit_header(lines[idx].strip()) and is_tier(next_meaningful(idx))

    units = OrderedDict()
    cur = None
    collecting_support = False

    def new_unit(name):
        return {"name": name, "tiers": [], "support_lines": [], "mode": "single"}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if collecting_support:
            if is_real_unit_header(i) or is_tier(line) or COST_RE.match(line) or line.upper() == "SUPPORT":
                collecting_support = False
            else:
                cur["support_lines"].append(line)
                i += 1
                continue

        if line.upper() == "SUPPORT" and cur:
            collecting_support = True
            i += 1; continue

        if TIER_SINGLE.search(line):
            if cur:
                cur["mode"] = "single"; cur["tiers"].append({})
            i += 1; continue
        if TIER_1ST.search(line):
            if cur:
                cur["mode"] = "esc1"; cur["tiers"].append({})
            i += 1; continue
        if TIER_12.search(line):
            if cur:
                cur["mode"] = "split"; cur["tiers"].append({})
            i += 1; continue
        if TIER_2PLUS.search(line):
            if cur:
                cur["tiers"].append({})
            i += 1; continue
        if TIER_3.search(line):
            if cur:
                cur["tiers"].append({})
            i += 1; continue

        m = COST_RE.match(line)
        if m and cur and cur["tiers"]:
            cur["tiers"][-1][int(m.group(1))] = int(m.group(2))
            i += 1; continue

        if is_real_unit_header(i):
            cur = new_unit(line)
            units[norm(line)] = cur
            collecting_support = False
            i += 1; continue

        i += 1

    return units

def to_points_row(army, unit_name, info):
    """Map parsed tiers -> Size_1..3 + Points_b-t schema."""
    tiers = info["tiers"]
    # collect ordered bracket sizes (union across tiers, sorted)
    sizes = sorted({b for t in tiers for b in t})
    sizes = sizes[:3]
    size_cells = [sizes[i] if i < len(sizes) else "" for i in range(3)]

    # normalize tier list to 3 copy-tiers
    if info["mode"] == "esc1" and len(tiers) >= 2:
        # "1st unit" / "2nd + unit": first copy = t1; every copy from the 2nd
        # on (incl. 3rd+) = t2, so copy-tier-3 mirrors copy-tier-2.
        t1 = tiers[0]; t2 = tiers[1]
        eff = [t1, t2, t2]
    elif info["mode"] == "single" or len(tiers) == 1:
        t1 = tiers[0] if tiers else {}
        eff = [t1, t1, t1]
    else:
        t12 = tiers[0] if len(tiers) >= 1 else {}
        t3 = tiers[1] if len(tiers) >= 2 else t12
        eff = [t12, t12, t3]

    # Points_b-t : bracket b (1..3), tier t (1..3)
    pts = []
    for t in range(3):
        for b in range(3):
            size = sizes[b] if b < len(sizes) else None
            pts.append(eff[t].get(size, "") if size is not None else "")
    # schema column order is Points_1-1,2-1,3-1, 1-2,2-2,3-2, 1-3,2-3,3-3
    # eff index t already iterates tier; inner b iterates bracket -> matches col order
    return [army, unit_name] + size_cells + pts

def read_stats_unitnames(path):
    """Return ordered list of (army, unit) and the raw rows for patching."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    return header, rows

def main():
    ap = argparse.ArgumentParser(description="MFM -> Unit_Points.csv (+ Leader Eligible Units patch)")
    ap.add_argument("--mfm", required=True, help="MFM text file (GW points)")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--army", default=ARMY_DEFAULT, help="Army Name for generic units in Unit_Points")
    ap.add_argument("--stats", default=None, help="Unit_Stats.csv to (a) match names and (b) patch Leader Eligible Units")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    units = parse_mfm(args.mfm)
    if not units:
        sys.exit("No units parsed from MFM file.")

    flags = {"no_costs": [], "mfm_no_datasheet": [], "datasheet_no_mfm": [], "support_filled": []}

    # name set from datasheets (if provided) for matching + army-name lookup
    ds_army_by_norm = {}
    stats_header = stats_rows = None
    if args.stats and os.path.exists(args.stats):
        stats_header, stats_rows = read_stats_unitnames(args.stats)
        try:
            ai = stats_header.index("Army Name"); ui = stats_header.index("Unit Name")
            lei = stats_header.index("Leader Eligible Units")
        except ValueError:
            ai = ui = lei = None
        if ai is not None:
            for r in stats_rows[1:]:
                if len(r) > max(ui, ai):
                    nk = norm(r[ui])
                    army_val = r[ai]
                    existing = ds_army_by_norm.get(nk)
                    # A unit name can appear in multiple stat rows (e.g. generic
                    # "Adeptus Astartes" plus a chapter variant like "Black Templars").
                    # The single MFM points row is generic and must file under the
                    # generic army so the app's chapter->generic fallback resolves.
                    # Prefer "Adeptus Astartes" whenever it appears among a name's rows;
                    # otherwise keep the first-seen (chapter-only units stay correct).
                    if existing is None or army_val == "Adeptus Astartes":
                        ds_army_by_norm[nk] = army_val

    # build Unit_Points rows
    point_rows = []
    seen = set()
    for nkey, info in units.items():
        if not info["tiers"] or not any(t for t in info["tiers"]):
            flags["no_costs"].append(info["name"])
            continue
        army = ds_army_by_norm.get(nkey, args.army)
        if ds_army_by_norm and nkey not in ds_army_by_norm:
            flags["mfm_no_datasheet"].append(info["name"])
        point_rows.append(to_points_row(army, info["name"].title() if info["name"].isupper() else info["name"], info))
        seen.add(nkey)

    # datasheets with no MFM points
    if ds_army_by_norm:
        for nkey in ds_army_by_norm:
            if nkey not in units:
                flags["datasheet_no_mfm"].append(nkey)

    header = ["Army Name","Unit Name","Size_1","Size_2","Size_3",
              "Points_1-1","Points_2-1","Points_3-1",
              "Points_1-2","Points_2-2","Points_3-2",
              "Points_1-3","Points_2-3","Points_3-3"]
    out_points = os.path.join(args.out_dir, "Unit_Points.csv")
    with open(out_points, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(point_rows)

    # patch Leader Eligible Units into Unit_Stats (verbatim SUPPORT list)
    if stats_rows is not None and lei is not None:
        support_by_norm = {}
        for nkey, info in units.items():
            sup = " ".join(info["support_lines"]).strip()
            if sup:
                support_by_norm[nkey] = re.sub(r"\s*,\s*", ", ", sup)
        for r in stats_rows[1:]:
            if len(r) > max(ui, lei):
                key = norm(r[ui])
                # Datasheets_leader.csv (consumed by the transform) is authoritative.
                # Only fill from MFM where the transform left the cell blank, so we
                # never clobber the authoritative leader-attach lists.
                if key in support_by_norm and not (r[lei] or "").strip():
                    r[lei] = support_by_norm[key]
                    flags["support_filled"].append(r[ui])
        with open(args.stats, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, lineterminator="\r\n")
            w.writerows(stats_rows)

    # report
    rep = os.path.join(args.out_dir, "points_validation_report.md")
    with open(rep, "w", encoding="utf-8") as f:
        f.write("# MFM Points — Validation Report\n\n")
        f.write(f"- Units parsed with costs: {len(point_rows)}\n")
        f.write(f"- Leader Eligible Units patched: {len(flags['support_filled'])}\n\n")
        for key, title in [
            ("no_costs", "MFM entries with no parsable cost"),
            ("mfm_no_datasheet", "MFM units with NO matching datasheet (check name/scope)"),
            ("datasheet_no_mfm", "Datasheets with NO MFM points (missing or name mismatch)"),
        ]:
            items = flags[key]
            f.write(f"## {title} — {len(items)}\n")
            for it in sorted(items):
                f.write(f"- {it}\n")
            f.write("\n")

    print(f"Done. {len(point_rows)} unit point rows -> {out_points}")
    print(f"  leader lists patched: {len(flags['support_filled'])} | see points_validation_report.md")


if __name__ == "__main__":
    main()
