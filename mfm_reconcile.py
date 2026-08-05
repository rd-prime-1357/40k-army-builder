#!/usr/bin/env python3
"""
MFM v1.1 reconciliation (B88, D274/D283) — analysis only, writes a report, changes
nothing else.

Generalizes the earlier one-off SM-only pass (which compared a since-superseded
`mfm_sm.txt` against `MFM_Space_Marines_v1_0.txt`) across every faction the app is
currently built from. For each such faction, compares its newest capture (the v1.1
file) against the version the app was actually built from (the v1_0 file the live
`ARMY_TO_MFM` / points pipeline reads), across:

  - roster: units the v1.1 file prices that v1_0 didn't, and vice versa
  - points: tier/bracket cost changes on units present in both
  - wargear: per-item WARGEAR OPTIONS cost changes on units present in both
  - attach lists: LEADER/SUPPORT eligible-unit list changes, including flips
    (a unit gaining or losing the Leader or Support ability outright)
  - detachments: DP, force disposition, and unique-tag changes; enhancements
    added/removed/repriced

Every faction-file pair is scoped to the 10 distinct MFM files the app's built
armies (`faction_taxonomy.json` armies backed by real `units.json` data) actually
read, per `source_manifest.json`'s registered v1_0/v1.1 pairs — not all 15 v1.1
files banked, since the other 5 have no "built from" version to diff against.

Every delta is classified:
  - adopt-mechanically: a numeric value changed on a record both files agree exists
    under the same name (points, wargear cost, DP, enhancement cost) — safe to pull
    straight through the normal per-faction adoption turn (B89).
  - investigate-first: anything structural — a unit/detachment/enhancement/wargear
    item added or removed, an attach-list change (including a Leader/Support flip),
    or a force-disposition/unique-tag change on a matched detachment. Disposition
    and unique-tag are rules-shape properties, not values (a disposition swap can
    change which missions a detachment is even legal for), so they are never
    adopt-mechanically even though they sit on an otherwise-matched record. These
    need a human look before B89 adopts them: they can be a genuine rules change, or
    a name-normalization miss that would otherwise silently orphan or duplicate a
    record.

Output is B89's work order, per the ticket: every delta classified so B89 knows
what's a mechanical pull-through vs what needs a decision first.

Stdlib only.  python3 mfm_reconcile.py [--root .] [--out PATH]
"""

import argparse
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(modname, filename, root):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(root, filename))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# Faction file pairs: MFM source name -> (v1_0 filename, v1.1 filename). Scoped to
# the 10 distinct MFM files the app's currently-built armies read (ARMY_TO_MFM's
# deduplicated value set, per detachment_parser.py) — the remaining 5 v1.1 files
# registered in source_manifest.json (Chaos Knights, Drukhari, Emperor's Children,
# Grey Knights, World Eaters) have no live "built from" version to diff against and
# are out of scope for this ticket.
FACTION_FILES = [
    ("Space Marines",       "MFM_Space_Marines_v1_0.txt",       "MFM_Space_Marines_v1.1.txt"),
    ("Black Templars",      "MFM_Black_Templars_v1_0.txt",      "MFM_Black_Templars_v1.1.txt"),
    ("Blood Angels",        "MFM_Blood_Angels_v1_0.txt",        "MFM_Blood_Angels_v1.1.txt"),
    ("Dark Angels",         "MFM_Dark_Angels_v1_0.txt",         "MFM_Dark_Angels_v1.1.txt"),
    ("Deathwatch",          "MFM_Death_Watch_v1_0.txt",         "MFM_Death_Watch_v1.1.txt"),
    ("Space Wolves",        "MFM_Space_Wolves_v1_0.txt",        "MFM_Space_Wolves_v1.1.txt"),
    ("Chaos Space Marines", "MFM_Chaos_Space_Marines_v1_0.txt", "MFM_Chaos_Space_Marines_v1.1.txt"),
    ("Death Guard",         "MFM_Death_Guard_v1_0.txt",         "MFM_Death_Guard_v1.1.txt"),
    ("Chaos Daemons",       "MFM_Chaos_Daemons_v1_0.txt",       "MFM_Chaos Daemons_v1.1.txt"),
    ("Thousand Sons",       "MFM_Thousand_Sons_v1_0.txt",       "MFM_Thousand_Sons_v1.1.txt"),
]


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def det_norm(s):
    # Mirrors detachment_parser.norm_key closely enough for this report's matching
    # purpose: case/space-fold and drop parentheticals, without pulling in the
    # accented-character machinery this analysis doesn't need.
    s = re.sub(r"\([^)]*\)", " ", s or "")
    return re.sub(r"[^A-Za-z0-9]+", " ", s).split()


def det_key(s):
    return " ".join(det_norm(s)).upper()


# ---------------------------------------------------------------------------
# Points/roster/wargear/attach delta, per faction file pair
# ---------------------------------------------------------------------------

def points_delta(mfmp, old_path, new_path):
    old = mfmp.parse_mfm(old_path)
    new = mfmp.parse_mfm(new_path)

    old_keys, new_keys = set(old), set(new)
    added_units = sorted(new[k]["name"] for k in (new_keys - old_keys))
    removed_units = sorted(old[k]["name"] for k in (old_keys - new_keys))

    points_changed = []
    wargear_changed = []
    attach_changed = []
    leader_support_flips = []

    for k in sorted(old_keys & new_keys):
        o, n = old[k], new[k]
        if o["tiers"] != n["tiers"] or o.get("mode") != n.get("mode"):
            points_changed.append({
                "unit": o["name"], "old_tiers": o["tiers"], "old_mode": o.get("mode"),
                "new_tiers": n["tiers"], "new_mode": n.get("mode"),
            })

        ow = {(w["item"], w["cost"]) for w in o.get("wargear", [])}
        nw = {(w["item"], w["cost"]) for w in n.get("wargear", [])}
        if ow != nw:
            added_items = sorted(nw - ow)
            removed_items = sorted(ow - nw)
            # A same-name item at a different cost shows as one remove + one add;
            # surface it as a repriced item (mechanical) rather than two structural
            # changes so it doesn't inflate the investigate-first bucket.
            added_by_name = {name: cost for name, cost in added_items}
            removed_by_name = {name: cost for name, cost in removed_items}
            repriced = sorted(set(added_by_name) & set(removed_by_name))
            added_only = sorted(name for name in added_by_name if name not in repriced)
            removed_only = sorted(name for name in removed_by_name if name not in repriced)
            wargear_changed.append({
                "unit": o["name"],
                "repriced": [(name, removed_by_name[name], added_by_name[name]) for name in repriced],
                "added": added_only,
                "removed": removed_only,
            })

        old_lead, new_lead = o.get("leader_lines", ""), n.get("leader_lines", "")
        old_sup, new_sup = o.get("support_lines", ""), n.get("support_lines", "")
        if old_lead != new_lead or old_sup != new_sup:
            attach_changed.append({
                "unit": o["name"], "old_leader": old_lead, "new_leader": new_lead,
                "old_support": old_sup, "new_support": new_sup,
            })
            if bool(old_lead) != bool(new_lead):
                leader_support_flips.append((o["name"], "Leader",
                                              "gained" if new_lead else "lost"))
            if bool(old_sup) != bool(new_sup):
                leader_support_flips.append((o["name"], "Support",
                                              "gained" if new_sup else "lost"))

    return {
        "added_units": added_units, "removed_units": removed_units,
        "points_changed": points_changed, "wargear_changed": wargear_changed,
        "attach_changed": attach_changed, "leader_support_flips": leader_support_flips,
        "old_count": len(old), "new_count": len(new),
    }


# ---------------------------------------------------------------------------
# Detachment delta, per faction file pair
# ---------------------------------------------------------------------------

def detachment_delta(dp, old_path, new_path):
    old = {det_key(x["name_raw"]): x for x in dp.parse_mfm_detachments(old_path)}
    new = {det_key(x["name_raw"]): x for x in dp.parse_mfm_detachments(new_path)}

    old_keys, new_keys = set(old), set(new)
    added = sorted(new[k]["name_raw"] for k in (new_keys - old_keys))
    removed = sorted(old[k]["name_raw"] for k in (old_keys - new_keys))

    dp_changed = []
    struct_changed = []
    enh_changed = []

    for k in sorted(old_keys & new_keys):
        o, n = old[k], new[k]
        # DP is a plain numeric value on a matched record -- safe to pull straight
        # through, same treatment as a points/enhancement reprice. Force disposition
        # and unique tag are rules-shape properties, not values: a disposition swap
        # can change which missions a detachment is even legal for, so it goes in
        # investigate-first with the other structural deltas, never adopt-mechanically.
        if o["dp"] != n["dp"]:
            dp_changed.append({"detachment": o["name_raw"], "old": o["dp"], "new": n["dp"]})
        struct_fields = {}
        if o["force_disposition"] != n["force_disposition"]:
            struct_fields["force_disposition"] = (o["force_disposition"], n["force_disposition"])
        if o["unique_tag"] != n["unique_tag"]:
            struct_fields["unique_tag"] = (o["unique_tag"], n["unique_tag"])
        if struct_fields:
            struct_changed.append({"detachment": o["name_raw"], "fields": struct_fields})

        oe = {det_key(e["name"]): e for e in o["enhancements"]}
        ne = {det_key(e["name"]): e for e in n["enhancements"]}
        oek, nek = set(oe), set(ne)
        added_enh = sorted(ne[k2]["name"] for k2 in (nek - oek))
        removed_enh = sorted(oe[k2]["name"] for k2 in (oek - nek))
        repriced_enh = []
        for k2 in sorted(oek & nek):
            if oe[k2]["points"] != ne[k2]["points"]:
                repriced_enh.append((oe[k2]["name"], oe[k2]["points"], ne[k2]["points"]))
        if added_enh or removed_enh or repriced_enh:
            enh_changed.append({
                "detachment": o["name_raw"], "added": added_enh, "removed": removed_enh,
                "repriced": repriced_enh,
            })

    return {
        "added": added, "removed": removed, "dp_changed": dp_changed,
        "struct_changed": struct_changed, "enh_changed": enh_changed,
        "old_count": len(old), "new_count": len(new),
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def fmt_tiers(tiers):
    return json.dumps(tiers, sort_keys=True)


def build_report(root):
    mfmp = _load("mfmp_b88", "mfm_points_parser.py", root)
    dp = _load("dp_b88", "detachment_parser.py", root)

    L = []
    L.append("# MFM v1.1 Reconciliation — per-faction delta report (B88)\n")
    L.append("Analysis only. No scripts, data, or config changed. Each faction compares its "
             "v1.1 capture against the v1_0 file the app was actually built from. Scope is the "
             "10 distinct MFM files backing the app's currently-built armies (`faction_taxonomy.json` "
             "armies with real `units.json` data) — not all 15 v1.1 files banked in "
             "`source_manifest.json`; the other 5 factions have no built version to diff against.\n")

    totals = {"adopt": 0, "investigate": 0}
    summary_rows = []

    for label, v1_0_name, v1_1_name in FACTION_FILES:
        old_path = os.path.join(root, v1_0_name)
        new_path = os.path.join(root, v1_1_name)
        if not (os.path.exists(old_path) and os.path.exists(new_path)):
            L.append(f"\n## {label}\n\n**SKIPPED** — missing source file "
                     f"({v1_0_name if not os.path.exists(old_path) else v1_1_name} not found).\n")
            continue

        pts = points_delta(mfmp, old_path, new_path)
        det = detachment_delta(dp, old_path, new_path)

        adopt = len(pts["points_changed"]) + sum(len(w["repriced"]) for w in pts["wargear_changed"]) \
            + len(det["dp_changed"]) + sum(len(e["repriced"]) for e in det["enh_changed"])
        investigate = len(pts["added_units"]) + len(pts["removed_units"]) \
            + sum(1 for w in pts["wargear_changed"] if w["added"] or w["removed"]) \
            + len(pts["attach_changed"]) + len(det["added"]) + len(det["removed"]) \
            + len(det["struct_changed"]) \
            + sum(1 for e in det["enh_changed"] if e["added"] or e["removed"])
        totals["adopt"] += adopt
        totals["investigate"] += investigate
        summary_rows.append((label, adopt, investigate))

        L.append(f"\n## {label}\n")
        L.append(f"`{v1_0_name}` ({pts['old_count']} units, {det['old_count']} detachments) vs "
                 f"`{v1_1_name}` ({pts['new_count']} units, {det['new_count']} detachments). "
                 f"**{adopt} adopt-mechanically, {investigate} investigate-first.**\n")

        if pts["added_units"] or pts["removed_units"]:
            L.append("**Roster — investigate-first**")
            if pts["added_units"]:
                L.append(f"- Added ({len(pts['added_units'])}): " + ", ".join(pts["added_units"]))
            if pts["removed_units"]:
                L.append(f"- Removed ({len(pts['removed_units'])}): " + ", ".join(pts["removed_units"]))
            L.append("")

        if pts["points_changed"]:
            L.append(f"**Points changed — adopt-mechanically ({len(pts['points_changed'])})**")
            for c in pts["points_changed"]:
                L.append(f"- {c['unit']}: `{fmt_tiers(c['old_tiers'])}` → `{fmt_tiers(c['new_tiers'])}`"
                         + (f" (mode {c['old_mode']}→{c['new_mode']})" if c['old_mode'] != c['new_mode'] else ""))
            L.append("")

        if pts["wargear_changed"]:
            reprice_lines = []
            struct_lines = []
            for w in pts["wargear_changed"]:
                for name, oc, nc in w["repriced"]:
                    reprice_lines.append(f"- {w['unit']}: {name} {oc} pts → {nc} pts")
                if w["added"]:
                    struct_lines.append(f"- {w['unit']}: added {', '.join(w['added'])}")
                if w["removed"]:
                    struct_lines.append(f"- {w['unit']}: removed {', '.join(w['removed'])}")
            if reprice_lines:
                L.append(f"**Wargear repriced — adopt-mechanically ({len(reprice_lines)})**")
                L.extend(reprice_lines)
                L.append("")
            if struct_lines:
                L.append(f"**Wargear added/removed — investigate-first ({len(struct_lines)})**")
                L.extend(struct_lines)
                L.append("")

        if pts["attach_changed"]:
            L.append(f"**Attach-list changes — investigate-first ({len(pts['attach_changed'])})**")
            for a in pts["attach_changed"]:
                if a["old_leader"] != a["new_leader"]:
                    L.append(f"- {a['unit']} LEADER: `{a['old_leader'] or '(none)'}` → "
                             f"`{a['new_leader'] or '(none)'}`")
                if a["old_support"] != a["new_support"]:
                    L.append(f"- {a['unit']} SUPPORT: `{a['old_support'] or '(none)'}` → "
                             f"`{a['new_support'] or '(none)'}`")
            L.append("")
        if pts["leader_support_flips"]:
            L.append("**Leader/Support flips (subset of the attach-list changes above):**")
            for name, ability, direction in pts["leader_support_flips"]:
                L.append(f"- {name} {direction} {ability}")
            L.append("")

        if det["added"] or det["removed"]:
            L.append("**Detachments — investigate-first**")
            if det["added"]:
                L.append(f"- Added ({len(det['added'])}): " + ", ".join(det["added"]))
            if det["removed"]:
                L.append(f"- Removed ({len(det['removed'])}): " + ", ".join(det["removed"]))
            L.append("")

        if det["dp_changed"]:
            L.append(f"**Detachment DP changed — adopt-mechanically ({len(det['dp_changed'])})**")
            for c in det["dp_changed"]:
                L.append(f"- {c['detachment']}: {c['old']}DP → {c['new']}DP")
            L.append("")

        if det["struct_changed"]:
            L.append(f"**Detachment force disposition / unique tag changed — "
                     f"investigate-first ({len(det['struct_changed'])})**")
            for c in det["struct_changed"]:
                parts = [f"{k} {v[0]}→{v[1]}" for k, v in c["fields"].items()]
                L.append(f"- {c['detachment']}: " + "; ".join(parts))
            L.append("")

        if det["enh_changed"]:
            reprice_lines = []
            struct_lines = []
            for e in det["enh_changed"]:
                for name, oc, nc in e["repriced"]:
                    reprice_lines.append(f"- {e['detachment']}: {name} {oc} pts → {nc} pts")
                if e["added"]:
                    struct_lines.append(f"- {e['detachment']}: added {', '.join(e['added'])}")
                if e["removed"]:
                    struct_lines.append(f"- {e['detachment']}: removed {', '.join(e['removed'])}")
            if reprice_lines:
                L.append(f"**Enhancements repriced — adopt-mechanically ({len(reprice_lines)})**")
                L.extend(reprice_lines)
                L.append("")
            if struct_lines:
                L.append(f"**Enhancements added/removed — investigate-first ({len(struct_lines)})**")
                L.extend(struct_lines)
                L.append("")

        if adopt == 0 and investigate == 0:
            L.append("No deltas.\n")

    L.insert(2, "\n## Summary\n\n| Faction | Adopt-mechanically | Investigate-first |\n|---|---|---|\n"
              + "\n".join(f"| {label} | {a} | {i} |" for label, a, i in summary_rows)
              + f"\n| **Total** | **{totals['adopt']}** | **{totals['investigate']}** |\n")

    return "\n".join(L) + "\n", totals


def main():
    ap = argparse.ArgumentParser(description="B88 per-faction MFM v1.1 reconciliation report.")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=os.path.join("/mnt/user-data/outputs", "MFM_v1_1_Reconciliation.md"))
    a = ap.parse_args()
    report, totals = build_report(a.root)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"adopt-mechanically={totals['adopt']} investigate-first={totals['investigate']}")
    print(f"report -> {a.out}")


if __name__ == "__main__":
    main()
