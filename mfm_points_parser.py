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

# Manual name overrides: MFM name -> datasheet name
POINT_NAME_OVERRIDES = {
    'Myphitic Blight-Haulers': 'Myphitic Blight-hauler',
    'Death Guard Chaos Lord': None,             # Legends, skip
    'Death Guard Chaos Lord In Terminator Armour': None,  # Legends
    'Death Guard Cultists': None,               # Legends
    'Death Guard Possessed': None,              # Legends
    'Death Guard Sorcerer In Terminator Armour': None,    # Legends
}

ARMY_DEFAULT = "Adeptus Astartes"

COST_RE = re.compile(r"^[•\-\*]\s*(\d+)\s*models?\s*(\d+)\s*pts", re.I)
# B56b. A composition-shaped bracket line names roles instead of a bare model count:
#     • 1 Sword Brother, 4 Neophytes, 5 Initiates150 pts
# One or more "<count> <label>" groups, comma-separated, with the cost jammed onto the
# end of the last label exactly as in COST_RE. Label chars exclude digits so the count/
# cost boundary is unambiguous even with no separating space. Bracket size = sum of the
# counts (matches how Size_1..3 are read elsewhere). Tried only after COST_RE misses.
COMPOSITION_RE = re.compile(
    r"^[•\-\*]\s*(\d+\s+[^,\d]+(?:,\s*\d+\s+[^,\d]+)*)(\d+)\s*pts\s*$", re.I
)
COMPOSITION_COUNT_RE = re.compile(r"(\d+)\s+[^,\d]+")
# B56g. Split a composition string into its individual (count, label) groups so the
# resolver can tell a genuine escort line ("3 Wolf Guard Headtakers, 3 Hunting Wolves")
# from an ordinary multi-role composition where every printed line has several groups
# and none stands alone (Crusader Squad's "1 Sword Brother, 4 Neophytes, 5 Initiates").
GROUP_SPLIT_RE = re.compile(r"(\d+)\s+([^,\d]+)")
# B59b. An additive add-on line prices a standalone extra model on top of the unit's
# printed size brackets, rather than naming a bracket of its own:
#     • + 1 Invader ATV60 pts
# Distinguished from COST_RE/COMPOSITION_RE by the leading "+" before the count. The
# name and cost are jammed together exactly as elsewhere; the printed count (typically
# 1) is not the unit's size -- it counts copies of the add-on itself. Previously
# unmatched by any line-shape and silently dropped (a defect predating and separate
# from B58). Tried only after COST_RE and COMPOSITION_RE both miss.
ADDON_RE = re.compile(r"^[•\-\*]\s*\+\s*(\d+)\s+([^\d]+?)(\d+)\s*pts\s*$", re.I)

def _parse_groups(text):
    groups = []
    for cnt, label in GROUP_SPLIT_RE.findall(text):
        lbl = label.strip().rstrip(",").strip()
        groups.append((int(cnt), lbl))
    return groups

def _norm_label(s):
    return re.sub(r"\s+", " ", (s or "").strip()).lower()
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
# B35 / D107. A unit's WARGEAR OPTIONS block prices individual items:
#     WARGEAR OPTIONS
#     • per Macro plasma incinerator10 pts
# The item name and the cost are jammed together, exactly as in the size-bracket
# lines. MFM_Instructions.txt: "these costs are per item taken, and are applied on
# top of the unit's main points cost" -- so the cost hangs off the ITEM, and a
# default-issue item is an item taken (Terminator Assault Squad can never ADD a
# thunder hammer, only swap it away, so its 5 pts can only be pricing the default).
# SKIP_HEADERS keeps "WARGEAR OPTIONS" from being read as a unit name; the block is
# collected separately below and attached to the preceding unit.
WARGEAR_RE = re.compile(r"^[\u2022\-\*]\s*per\s+(.+?)\s*(\d+)\s*pts\s*$", re.I)

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
        return {"name": name, "tiers": [], "support_lines": [], "mode": "single", "wargear": []}

    collecting_wargear = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if collecting_wargear:
            m = WARGEAR_RE.match(line)
            if m and cur is not None:
                cur["wargear"].append({
                    "item": m.group(1).strip(),
                    "cost": int(m.group(2)),
                    "line": i + 1,
                })
                i += 1
                continue
            collecting_wargear = False

        if line.upper() == "WARGEAR OPTIONS":
            collecting_wargear = True
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

        m = COMPOSITION_RE.match(line)
        if m and cur and cur["tiers"]:
            groups = _parse_groups(m.group(1))
            size = sum(c for c, _ in groups)
            cost = int(m.group(2))
            # Composition lines are staged, not written straight into the tier dict.
            # Two different compositions can sum to the same bracket size (e.g. a
            # base count vs. base+optional-escort count both totalling 6 models) —
            # picking whichever line came first would silently ship whichever cost
            # happened to be first in the file, which is not "the" price for that
            # bracket. Stage everything and resolve per-tier after the unit is fully
            # read, so a same-size collision voids that tier instead of guessing. D106.
            cur.setdefault("composition_pending", []).append(
                {"tier_idx": len(cur["tiers"]) - 1, "size": size, "cost": cost,
                 "line": i + 1, "text": line, "groups": groups}
            )
            i += 1; continue

        m = ADDON_RE.match(line)
        if m and cur and cur["tiers"]:
            cur.setdefault("addons", []).append({
                "count": int(m.group(1)),
                "item": m.group(2).strip(),
                "cost": int(m.group(3)),
                "line": i + 1,
                "text": line,
            })
            i += 1; continue

        if is_real_unit_header(i):
            cur = new_unit(line)
            units[norm(line)] = cur
            collecting_support = False
            i += 1; continue

        i += 1

    # Resolve staged composition lines per unit, per tier: if every entry for a
    # given size agrees, write it; if a size has two different costs within the
    # same tier, void that whole unit's composition contribution rather than
    # guess a winner or ship a partial bracket table.
    for info in units.values():
        pending = info.pop("composition_pending", None)
        if not pending:
            continue

        # B56g. A single-group line ("6 Wolf Guard Headtakers") stands alone. A
        # multi-group line is an escort candidate only if its FIRST group exactly
        # matches (count and label) a single-group line in the same tier — that is
        # the signature of "primary count, optionally with an add-on group", as
        # opposed to Crusader Squad where every line has several groups and none
        # ever appears alone. Only matched escort lines are pulled out of the normal
        # size/collision resolution; everything else is untouched.
        singles_by_tier = {}
        for e in pending:
            if len(e["groups"]) == 1:
                singles_by_tier.setdefault(e["tier_idx"], []).append(e)

        escort_entries, normal_entries = [], []
        for e in pending:
            match = None
            if len(e["groups"]) > 1:
                first_count, first_label = e["groups"][0]
                for s in singles_by_tier.get(e["tier_idx"], []):
                    if s["groups"][0][0] == first_count and _norm_label(s["groups"][0][1]) == _norm_label(first_label):
                        match = s
                        break
            if match:
                escort_count = sum(c for c, _ in e["groups"][1:])
                escort_label = ", ".join(l for _, l in e["groups"][1:])
                escort_entries.append({
                    "tier_idx": e["tier_idx"], "primary_count": first_count,
                    "escort_count": escort_count, "escort_label": escort_label,
                    "escort_cost": e["cost"] - match["cost"],
                    "line": e["line"], "text": e["text"],
                })
            else:
                normal_entries.append(e)

        by_tier = {}
        for e in normal_entries:
            by_tier.setdefault(e["tier_idx"], {}).setdefault(e["size"], []).append(e)
        conflicted = False
        for tier_idx, by_size in by_tier.items():
            for size, entries in by_size.items():
                costs = {e["cost"] for e in entries}
                if len(costs) > 1:
                    conflicted = True
                    info.setdefault("composition_conflicts", []).extend(entries)
        if conflicted:
            # Void every staged composition value for this unit — do not mix
            # resolved and unresolved brackets in one price table.
            continue
        for tier_idx, by_size in by_tier.items():
            for size, entries in by_size.items():
                info["tiers"][tier_idx][size] = entries[0]["cost"]

        # Derive the escort's per-model rate from the printed difference. Every
        # escort line for this unit must agree on the rate (evenly divisible, same
        # value across brackets and tiers) or it is flagged rather than guessed —
        # no invented price, matching D106.
        if escort_entries:
            rates = set()
            for ee in escort_entries:
                if ee["escort_count"] > 0 and ee["escort_cost"] % ee["escort_count"] == 0:
                    rates.add(ee["escort_cost"] // ee["escort_count"])
                else:
                    rates.add(None)
            if len(rates) == 1 and None not in rates:
                info["escort_group"] = {
                    "label": escort_entries[0]["escort_label"],
                    "rate_per_model": next(iter(rates)),
                    "brackets": sorted({(ee["primary_count"], ee["escort_count"]) for ee in escort_entries}),
                    "source_lines": [ee["line"] for ee in escort_entries],
                }
            else:
                info["escort_conflicts"] = escort_entries

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


# ---------------------------------------------------------------------------
# B35 -- paid wargear (D107).
#
# The MFM prices items, not options. The same item can be free on one unit and
# priced on another (a Terminator Assault Squad's storm shield is free; a Wolf
# Guard Terminator's costs 5), so the map is keyed by datasheet id, never by
# item name alone -- the same discipline as D70 for ability text.
#
# The chapter MFM files repeat the shared Space Marines datasheets (Redemptor
# Dreadnought is priced in six files). They collapse onto one datasheet id and
# must agree; a disagreement is a flag, not a silent last-writer-wins.
# ---------------------------------------------------------------------------

def _split_parts(name):
    """A compound loadout name ('Thunder hammer + Storm Shield') is several items."""
    return [p.strip() for p in str(name or "").split(" + ") if p.strip()]

def reachable_items(loadout):
    """Every item name a configured unit could end up carrying, from unit_loadouts.json.

    Includes swap SOURCES as well as replacements: a source item is carried until
    it is swapped away, and Terminator Assault Squad's priced thunder hammer only
    ever appears as a default and as a swap source.
    Returns lowercased-name -> preferred display casing.
    """
    out = {}
    def put(name):
        for p in _split_parts(name):
            k = p.lower()
            if k not in out:
                out[k] = p
    for g in loadout.get("model_groups", []):
        for w in g.get("default_weapons", []) or []:
            put(w)
        for w in g.get("default_wargear", []) or []:
            put(w)
    for o in loadout.get("options", []):
        for key in ("adds_weapon", "adds_wargear", "replaces", "replacement"):
            if o.get(key):
                put(o[key])
        for key in ("choices", "replacement_choices", "equipment_parts", "equipment_choices"):
            for c in o.get(key, []) or []:
                put(c)
    return out

# An MFM file names one faction's units. Datasheet NAMES are not unique across
# factions -- "Defiler" is five separate datasheets (CSM 000000969, DG 000004209,
# EC 000004208, TS 000001030, WE 000004207; Datasheets.csv). Resolving a wargear
# cost by unit name alone would silently attach the CSM Defiler's price to the DG
# Defiler. So the file's faction is part of the key. The Space Marine chapter files
# (Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) all carry
# faction SM -- chapters are not separate faction ids in Factions.csv.
FACTION_BY_MFM = {
    'MFM_Space_Marines_v1_0.txt': 'SM',
    'MFM_Black_Templars_v1_0.txt': 'SM',
    'MFM_Blood_Angels_v1_0.txt': 'SM',
    'MFM_Dark_Angels_v1_0.txt': 'SM',
    'MFM_Death_Watch_v1_0.txt': 'SM',
    'MFM_Space_Wolves_v1_0.txt': 'SM',
    'MFM_Grey_Knights_v1_0.txt': 'GK',
    'MFM_Chaos_Space_Marines_v1_0.txt': 'CSM',
    'MFM_Death_Guard_v1_0.txt': 'DG',
    'MFM_Thousand_Sons_v1_0.txt': 'TS',
    'MFM_Emperors_Children_v1_0.txt': 'EC',
    'MFM_World_Eaters_v1_0.txt': 'WE',
    'MFM_Chaos_Daemons_v1_0.txt': 'CD',
    'MFM_Drukhari_v1_0.txt': 'DRU',
}

def _datasheet_index(datasheets_csv):
    """(faction_id, NORMED NAME) -> datasheet id, plus normed name -> set(ids)."""
    by_fac, by_name = {}, {}
    with open(datasheets_csv, encoding='utf-8-sig') as f:
        head = f.readline().rstrip('\r\n').split('|')
        ix, nx, fx = head.index('id'), head.index('name'), head.index('faction_id')
        for line in f:
            p = line.rstrip('\r\n').split('|')
            if len(p) <= fx:
                continue
            k = norm(p[nx])
            by_fac[(p[fx], k)] = p[ix]
            by_name.setdefault(k, set()).add(p[ix])
    return by_fac, by_name

def build_wargear_points(mfm_paths, units_path, loadouts_path, datasheets_csv):
    """Return (wargear_map, flags). wargear_map: datasheet_id -> {lower_item: cost}."""
    import json
    with open(units_path, encoding="utf-8") as f:
        blocks = json.load(f)
    with open(loadouts_path, encoding="utf-8") as f:
        loadouts = json.load(f)
    by_fac, by_name = _datasheet_index(datasheets_csv)

    in_data = set()
    for b in blocks:
        for u in b.get("units", []):
            in_data.add(u["unit_id"])

    wargear, display, provenance = {}, {}, {}
    # B59b. Additive add-on lines (e.g. Invader ATV) are collected in parallel to
    # WARGEAR OPTIONS items, but kept in their own map: the add-on's name is a model
    # group's own label, not a reachable swap/wargear item name in unit_loadouts.json
    # (D173's rejection of that shape stands), so it is never gated on reachable_items.
    # This map exists to give the parsed, cross-chapter-validated fact an executable
    # home (D107) -- the engine-facing price still ships as a literal price_per_model
    # on the model group, per D182.
    addons, addon_display, addon_provenance = {}, {}, {}
    flags = {"unit_not_in_scope": [], "item_unmatched": [], "cost_conflict": [],
             "no_loadout": [], "unknown_faction_file": [], "name_ambiguous": [],
             "no_datasheet": [], "addon_cost_conflict": [], "addon_no_datasheet": []}

    for path in mfm_paths:
        base = os.path.basename(path)
        fac = FACTION_BY_MFM.get(base)
        if fac is None:
            flags["unknown_faction_file"].append(base)
        units = parse_mfm(path)
        for nkey, info in units.items():
            for w in info.get("wargear", []):
                src = "%s:%d" % (base, w["line"])
                if fac is not None:
                    ds = by_fac.get((fac, nkey))
                else:
                    ids = by_name.get(nkey, set())
                    if len(ids) > 1:
                        flags["name_ambiguous"].append((info["name"], sorted(ids), src))
                        continue
                    ds = next(iter(ids)) if ids else None
                if not ds:
                    flags["no_datasheet"].append((info["name"], fac, w["item"], src))
                    continue
                if ds not in in_data:
                    flags["unit_not_in_scope"].append((info["name"], ds, w["item"], w["cost"], src))
                    continue
                lo = loadouts.get(ds)
                if not lo:
                    flags["no_loadout"].append((info["name"], ds, w["item"], src))
                    continue
                reach = reachable_items(lo)
                key = w["item"].strip().lower()
                if key not in reach:
                    flags["item_unmatched"].append((info["name"], ds, w["item"], src,
                                                    sorted(reach.values())))
                    continue
                prev = wargear.setdefault(ds, {}).get(key)
                if prev is not None and prev != w["cost"]:
                    flags["cost_conflict"].append((info["name"], ds, w["item"], prev,
                                                   w["cost"], provenance[(ds, key)], src))
                    continue
                wargear[ds][key] = w["cost"]
                display[(ds, key)] = reach[key]
                provenance.setdefault((ds, key), src)

            for a in info.get("addons", []):
                src = "%s:%d" % (base, a["line"])
                if fac is not None:
                    ds = by_fac.get((fac, nkey))
                else:
                    ids = by_name.get(nkey, set())
                    ds = next(iter(ids)) if len(ids) == 1 else None
                if not ds:
                    flags["addon_no_datasheet"].append((info["name"], fac, a["item"], src))
                    continue
                if ds not in in_data:
                    continue
                key = a["item"].strip().lower()
                prev = addons.setdefault(ds, {}).get(key)
                if prev is not None and (prev["cost"] != a["cost"] or prev["count"] != a["count"]):
                    flags["addon_cost_conflict"].append(
                        (info["name"], ds, a["item"], prev["cost"], a["cost"],
                         addon_provenance[(ds, key)], src))
                    continue
                addons[ds][key] = {"cost": a["cost"], "count": a["count"]}
                addon_display[(ds, key)] = a["item"]
                addon_provenance.setdefault((ds, key), src)

    out = {}
    for ds in sorted(wargear):
        out[ds] = {
            "items": {
                k: {"cost": v,
                    "display": display[(ds, k)],
                    "source": provenance[(ds, k)]}
                for k, v in sorted(wargear[ds].items())
            }
        }

    addons_out = {}
    for ds in sorted(addons):
        addons_out[ds] = {
            k: {"cost": v["cost"],
                "count": v["count"],
                "display": addon_display[(ds, k)],
                "source": addon_provenance[(ds, k)]}
            for k, v in sorted(addons[ds].items())
        }
    return out, addons_out, flags

def cmd_wargear(args):
    import json
    paths = list(args.wargear)   # explicit order: generic faction file before its chapter files, so provenance cites the generic source
    out, addons_out, flags = build_wargear_points(paths, args.units, args.loadouts, args.datasheets)
    doc = {
        "_meta": {
            "source": "MFM WARGEAR OPTIONS blocks; see MFM_Instructions.txt (UNITS > Wargear)",
            "rule": "cost is per item TAKEN, applied on top of the unit's main points cost; "
                    "default-issue items are taken items and are priced (D107 / B35)",
            "key": "datasheet_id -> items -> lowercased item name -> {cost, display, source}",
            "engine": "match rollup weapon/equipment names by weaponBase(name).toLowerCase()",
        },
        "_addons": {
            "source": "MFM additive add-on lines ('• + 1 <name><cost> pts'); see B59b, D182, D184",
            "rule": "cross-chapter-validated audit trail only -- the engine reads a literal "
                    "price_per_model on the unit_loadouts.json model group, not this file, "
                    "for this shape (D173's rejection of the reachable-item lookup for "
                    "model-group pricing still stands)",
            "key": "datasheet_id -> lowercased add-on name -> {cost, count, display, source}",
            "data": addons_out,
        },
    }
    doc.update(out)
    with open(args.wargear_out, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
        f.write("\n")

    priced = sum(len(v["items"]) for v in out.values())
    addon_count = sum(len(v) for v in addons_out.values())
    print("wargear_points.json: %d units, %d priced items, %d validated add-ons" %
          (len(out), priced, addon_count))
    for name, items in [("MFM FILE WITH NO FACTION MAPPING", flags["unknown_faction_file"]),
                        ("MFM NAME AMBIGUOUS ACROSS FACTIONS", flags["name_ambiguous"]),
                        ("NO DATASHEET FOR MFM NAME + FACTION", flags["no_datasheet"]),
                        ("UNIT NOT IN units.json (out of v1 data scope)", flags["unit_not_in_scope"]),
                        ("UNIT HAS NO unit_loadouts.json ENTRY", flags["no_loadout"]),
                        ("ITEM NOT FOUND IN UNIT'S REACHABLE LOADOUT", flags["item_unmatched"]),
                        ("COST CONFLICT ACROSS MFM FILES", flags["cost_conflict"]),
                        ("ADD-ON: NO DATASHEET FOR MFM NAME + FACTION", flags["addon_no_datasheet"]),
                        ("ADD-ON: COST CONFLICT ACROSS MFM FILES", flags["addon_cost_conflict"])]:
        print("  %s: %d" % (name, len(items)))
        for it in items:
            print("     ", it)
    return 0


def main():
    ap = argparse.ArgumentParser(description="MFM -> Unit_Points.csv (+ Leader Eligible Units patch)")
    ap.add_argument("--mfm", required=False, help="MFM text file (GW points)")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--army", default=ARMY_DEFAULT, help="Army Name for generic units in Unit_Points")
    ap.add_argument("--stats", default=None, help="Unit_Stats.csv to (a) match names and (b) patch Leader Eligible Units")
    ap.add_argument("--append", action="store_true",
                    help="B56a: append rows to an existing Unit_Points.csv in --out-dir (chapter run) "
                         "instead of overwriting it. Written with no header and no BOM, since the base "
                         "file (from the un-scoped run) already carries both. If the file does not yet "
                         "exist, falls back to a fresh write with header, exactly as without this flag.")
    ap.add_argument("--scope-to-army", action="store_true",
                    help="B56a: restrict the name->army map to --army's own Unit_Stats.csv rows only "
                         "(chapter runs). An MFM entry with no datasheet in that block is DROPPED, not "
                         "written under --army as a fallback. Without this flag, a name ambiguous across "
                         "armies prefers Adeptus Astartes (base-run behavior, unchanged).")
    ap.add_argument("--wargear", nargs="+", default=None,
                    help="B35: MFM files to harvest WARGEAR OPTIONS costs from (wargear mode)")
    ap.add_argument("--units", default="units.json", help="units.json (wargear mode: MFM name -> datasheet id)")
    ap.add_argument("--loadouts", default="unit_loadouts.json", help="unit_loadouts.json (wargear mode: item name matching)")
    ap.add_argument("--wargear-out", default="wargear_points.json", help="wargear mode output")
    ap.add_argument("--datasheets", default="Datasheets.csv",
                    help="wargear mode: name+faction -> datasheet id (names are NOT unique across factions)")
    args = ap.parse_args()

    if args.wargear:
        sys.exit(cmd_wargear(args))
    if not args.mfm:
        ap.error("--mfm is required unless --wargear is given")
    os.makedirs(args.out_dir, exist_ok=True)

    units = parse_mfm(args.mfm)
    if not units:
        sys.exit("No units parsed from MFM file.")

    flags = {"no_costs": [], "mfm_no_datasheet": [], "datasheet_no_mfm": [], "support_filled": [],
              "out_of_scope_dropped": [], "composition_conflicts": [], "escort_groups": [],
              "escort_conflicts": []}
    for info in units.values():
        for c in info.get("composition_conflicts", []):
            flags["composition_conflicts"].append(
                (info["name"], c["line"], c["text"], c["size"], c["cost"]))
        eg = info.get("escort_group")
        if eg:
            flags["escort_groups"].append((info["name"], eg))
        for ec in info.get("escort_conflicts", []):
            flags["escort_conflicts"].append((info["name"], ec["line"], ec["text"]))

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
                if len(r) > ui:
                    k = norm(r[ui]); a = r[ai]
                    if args.scope_to_army:
                        # B56a: chapter run. Only this army's own rows are eligible for
                        # the name->army map; a name shared with another army (e.g. Black
                        # Templars' Gladiator Lancer vs. the Adeptus Astartes datasheet of
                        # the same name) must not resolve outside this block.
                        if a == args.army:
                            ds_army_by_norm[k] = a
                        continue
                    # Fix 1: prefer the generic (Adeptus Astartes) army when a unit
                    # name appears under multiple armies. First-seen otherwise wins,
                    # but a generic row always takes precedence over a chapter row.
                    if k not in ds_army_by_norm or a == ARMY_DEFAULT:
                        ds_army_by_norm[k] = a

    # build Unit_Points rows
    point_rows = []
    seen = set()
    for nkey, info in units.items():
        if not info["tiers"] or not any(t for t in info["tiers"]):
            flags["no_costs"].append(info["name"])
            continue
        # Apply name overrides before any matching
        display_name = info["name"].title() if info["name"].isupper() else info["name"]
        override = POINT_NAME_OVERRIDES.get(display_name)
        if override is None and display_name in POINT_NAME_OVERRIDES:
            # Explicitly mapped to None = skip (Legends)
            continue
        if override:
            display_name = override
            nkey = norm(display_name)
        army = ds_army_by_norm.get(nkey)
        if army is None:
            if args.scope_to_army:
                # B56a: no datasheet in this chapter's own block. Drop rather than
                # write under --army — a fallback here is exactly the bug that let
                # Black Templars rows overwrite generic Adeptus Astartes prices.
                flags.setdefault("out_of_scope_dropped", []).append(display_name)
                continue
            army = args.army
            if ds_army_by_norm:
                flags["mfm_no_datasheet"].append(display_name)
        point_rows.append(to_points_row(army, display_name, info))
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
    append_mode = args.append and os.path.exists(out_points)
    if append_mode:
        # B56a: a chapter row whose (Army, Unit) key already exists in the target file
        # is a genuine override, not a duplicate. Per D42 as written (confirmed S101
        # after B56f: "faction points always override generic"), the chapter row wins.
        # Remove the base row, append the chapter row, and log the override so it's
        # visible in the validation report rather than silent.
        with open(out_points, encoding="utf-8-sig", newline="") as rf:
            existing = list(csv.reader(rf))
        existing_keys = {(r[0], r[1]) for r in existing[1:] if len(r) >= 2}
        overrides = {(row[0], row[1]): row for row in point_rows
                     if (row[0], row[1]) in existing_keys}
        if overrides:
            # Rewrite the file with the base row(s) for each colliding key stripped.
            kept = [existing[0]]  # header (with BOM)
            for r in existing[1:]:
                if len(r) >= 2 and (r[0], r[1]) in overrides:
                    flags.setdefault("chapter_override_applied", []).append(
                        (r[0], r[1], r[5] if len(r) > 5 else "",
                         overrides[(r[0], r[1])][5]))
                    continue
                kept.append(r)
            with open(out_points, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f, lineterminator="\r\n")
                w.writerows(kept)
        # Append every chapter row: new keys are additive, overriding keys are now the
        # sole row for that key after the strip.
        with open(out_points, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\r\n")
            w.writerows(point_rows)
    else:
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
                # Non-destructive: transform is authoritative for leader lists from
                # Datasheets_leader.csv; only backfill cells the transform left blank.
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
            ("out_of_scope_dropped", "MFM entries dropped: no datasheet in this --scope-to-army block"),
        ]:
            items = flags[key]
            f.write(f"## {title} — {len(items)}\n")
            for it in sorted(items):
                f.write(f"- {it}\n")
            f.write("\n")
        comp = flags.get("composition_conflicts", [])
        f.write(f"## Composition-bracket collisions — {len(comp)} (B56b, held for a follow-up ticket)\n")
        f.write("Unit's entire composition-based price table is voided when any bracket size "
                "has more than one candidate cost within the same copy-tier.\n\n")
        for name, line, text, size, cost in sorted(comp):
            f.write(f"- {name} (line {line}): `{text}` sums to bracket size {size}, cost {cost} pts\n")
        f.write("\n")
        collisions = flags.get("chapter_override_applied", [])
        f.write(f"## Chapter overrides applied (append mode, base row replaced) — {len(collisions)}\n")
        for army, unit, base_pts1, chap_pts1 in sorted(collisions):
            f.write(f"- {army} / {unit}: base row {base_pts1} at 1-2 replaced by chapter {chap_pts1} (D42, D169)\n")
        f.write("\n")
        escorts = flags.get("escort_groups", [])
        f.write(f"## Escort model groups derived (B56g phase 1) — {len(escorts)}\n")
        f.write("Primary bracket is keyed on the primary group's count only; the escort group's "
                "per-model rate is re-derived from the printed price difference, never hand-entered. "
                "Not yet wired into unit_loadouts.json or units.json as a purchasable group — that is "
                "phase 2/3, per D173.\n\n")
        for name, eg in sorted(escorts):
            brackets = ", ".join(f"{p}+{e}" for p, e in eg["brackets"])
            f.write(f"- {name}: {eg['label']} at {eg['rate_per_model']} pts/model "
                    f"(brackets primary+escort: {brackets})\n")
        f.write("\n")
        econf = flags.get("escort_conflicts", [])
        f.write(f"## Escort rate conflicts (voided, not derived) — {len(econf)}\n")
        for name, line, text in sorted(econf):
            f.write(f"- {name} (line {line}): `{text}`\n")
        f.write("\n")

    print(f"Done. {len(point_rows)} unit point rows -> {out_points}")
    print(f"  leader lists patched: {len(flags['support_filled'])} | see points_validation_report.md")


if __name__ == "__main__":
    main()
