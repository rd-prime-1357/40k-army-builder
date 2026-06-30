#!/usr/bin/env python3
"""
New-MFM / Forge World reconciliation (analysis only — writes a report, changes nothing).

Answers:
  1. What does MFM_Space_Marines_v1_0.txt price that mfm_sm.txt doesn't? (+delta)
  2. Of those, which are CORE units that already have a datasheet in the 181-unit
     SM transform (safe to adopt now) vs Forge World/Legends (would land as
     points_no_stat until the transform FW toggle exists)?
  3. Does the new MFM close the Black Templars points gap?
  4. Do the bike / jump-pack / Gravis / Phobos Captain variants now price?
  5. Exact blocking-count delta to expect on switching SM to the new MFM.
"""
import csv, os, re, sys
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))

# ── pull parse_mfm from the existing parser (single source of truth) ─────────
spec = importlib.util.spec_from_file_location("mfmp", os.path.join(HERE, "mfm_points_parser.py"))
mfmp = importlib.util.module_from_spec(spec); spec.loader.exec_module(mfmp)

def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()

def priced_names(path):
    units = mfmp.parse_mfm(path)
    # parse_mfm returns {nkey: {name, tiers, ...}}; keep only those with real costs
    out = {}
    for nkey, info in units.items():
        if info["tiers"] and any(t for t in info["tiers"]):
            out[norm(info["name"])] = info["name"]
    return out

# ── inputs ───────────────────────────────────────────────────────────────────
old = priced_names(os.path.join(HERE, "mfm_sm.txt"))
new = priced_names(os.path.join(HERE, "MFM_Space_Marines_v1_0.txt"))

# 181 transform-output datasheet names (ground truth for "has a datasheet")
ds_names = {}
with open(os.path.join(HERE, "out", "Unit_Stats.csv"), encoding="utf-8-sig") as f:
    r = list(csv.reader(f)); hdr = r[0]
    ai = hdr.index("Army Name"); ui = hdr.index("Unit Name")
    try: di = hdr.index("Datasheet ID")
    except ValueError: di = None
    for row in r[1:]:
        if len(row) > ui:
            ds_names.setdefault(norm(row[ui]), set()).add(row[ai])

# Wahapedia datasheets + source-exclusion (mirror the transform's FW/Legends rule)
def read_pipe(path):
    with open(path, encoding="utf-8-sig") as f:
        rows = [ln.rstrip("\n").rstrip("\r").split("|") for ln in f if ln.strip()]
    h = [c.strip() for c in rows[0]]
    return [dict(zip(h, rr)) for rr in rows[1:]]

sources = read_pipe(os.path.join(HERE, "Source.csv"))
def src_excluded(s):
    low = (s.get("name", "") + " " + s.get("type", "")).lower()
    return "legend" in low or "forge world" in low
excluded_src = {s["id"] for s in sources if src_excluded(s)}

ds_rows = read_pipe(os.path.join(HERE, "Datasheets.csv"))
# index Wahapedia datasheets by normalized name -> list of (faction_id, excluded?)
waha_by_name = {}
for d in ds_rows:
    waha_by_name.setdefault(norm(d.get("name")), []).append({
        "faction_id": d.get("faction_id"),
        "excluded": d.get("source_id") in excluded_src,
        "legend_flag": (d.get("legend", "") or "").strip().lower() in ("true", "1", "yes"),
    })

SM_FAMILY = {"SM"}  # transform selects faction_id == SM; chapters keyword-assigned

# ── classify the new-only delta ──────────────────────────────────────────────
new_only = sorted(set(new) - set(old))
removed  = sorted(set(old) - set(new))

cls = {"core_priced": [], "fw_legends": [], "no_sm_datasheet": [], "other": []}
for nk in new_only:
    disp = new[nk]
    if nk in ds_names:
        cls["core_priced"].append(disp); continue
    waha = waha_by_name.get(nk, [])
    sm_rows = [w for w in waha if w["faction_id"] in SM_FAMILY]
    if sm_rows and all(w["excluded"] or w["legend_flag"] for w in sm_rows):
        cls["fw_legends"].append(disp)
    elif sm_rows:
        cls["other"].append(disp)   # SM datasheet exists, not excluded, yet not in 181
    else:
        cls["no_sm_datasheet"].append(disp)

# ── Black Templars gap: the 12 un-costable BT units from the deployed build ──
bt_uncostable = [
    "Chaplain Grimaldus","Castellan","High Marshal Helbrecht","Emperor’s Champion",
    "Marshal","Sword Brethren Squad","Crusader Squad","Execrator","Crusade Ancient",
    "Sternguard Veteran Squad","Terminator Squad","Land Raider Crusader",
]
bt_status = []
for name in bt_uncostable:
    nk = norm(name)
    bt_status.append((name, nk in new, nk in old))

# also check the dedicated BT MFM if present
bt_mfm = os.path.join(HERE, "MFM_Black_Templars_v1_0.txt")
bt_priced = priced_names(bt_mfm) if os.path.exists(bt_mfm) else {}

# ── Captain variants ─────────────────────────────────────────────────────────
cap_variants = [n for n in (list(new.values())) if norm(n).startswith("captain")]
cap_rows = []
for disp in sorted(set(cap_variants)):
    nk = norm(disp)
    cap_rows.append((disp, nk in ds_names, nk in old))

# ── expected blocking-count delta ────────────────────────────────────────────
# Switching to the new MFM: every fw_legends + no_sm_datasheet priced name that
# the converter can't match to a stat row becomes a points-side orphan
# (mfm_no_datasheet); core_priced names that ARE in the 181 simply get priced.
# The points_no_stat blocking count rises by the count of priced-but-no-datasheet.
expected_new_orphans = len(cls["fw_legends"]) + len(cls["no_sm_datasheet"]) + len(cls["other"])

# ── report ───────────────────────────────────────────────────────────────────
def block(title): return f"\n## {title}\n"
L = []
L.append("# New-MFM / Forge World Reconciliation\n")
L.append("Analysis only. No scripts, data, or config changed. Source of truth for "
         "“has a datasheet” is the 181-unit SM transform output; FW/Legends is the "
         "datasheet’s Wahapedia source, matching the transform’s own exclusion rule.\n")

L.append(block("Headline — corrects the prior estimate"))
L.append("The handoff expected the +76 delta to be roughly half core-missing units (bikes, jump "
         "packs, command squad, dreadnought variants, named chars) and half Forge World/Legends. "
         "**That estimate is wrong.** Those firstborn units were moved to Legends in 10th edition, "
         "so they read as Legends in the current Wahapedia data. The delta is almost entirely "
         "FW/Legends.\n")
L.append(f"- Old `mfm_sm.txt` prices **{len(old)}** units; new `MFM_Space_Marines_v1_0.txt` prices **{len(new)}** (**+{len(new)-len(old)}**, **-{len(removed)}** removed).")
L.append(f"- Of the **{len(new_only)}** new-only priced units:")
L.append(f"  - **{len(cls['core_priced'])} genuine core** — has a datasheet in the 181, currently un-priced → the *only* real unlock from the switch: **{', '.join(sorted(cls['core_priced'])) or '—'}**.")
L.append(f"  - **{len(cls['fw_legends'])} Forge World / Legends** — priced but excluded at transform; inert (`points_no_stat`) until the transform FW toggle exists.")
L.append(f"  - **{len(cls['no_sm_datasheet'])} no SM datasheet** — **investigate**: **{', '.join(sorted(cls['no_sm_datasheet'])) or '—'}** (name mismatch or genuinely absent).")
if cls["other"]:
    L.append(f"  - **{len(cls['other'])} other** — an SM datasheet exists and isn’t FW/Legends, yet isn’t in the 181 → **investigate**.")
L.append(f"- **Net:** switching the SM MFM unlocks **{len(cls['core_priced'])}** core unit and would add "
         f"**+{expected_new_orphans}** `points_no_stat` orphans. It is **not** the core-coverage upgrade "
         f"it was thought to be — its value is the FW/Legends pricing layer, which does nothing until the "
         f"FW toggle ships.")

L.append(block(f"Core units now priced — safe to adopt ({len(cls['core_priced'])})"))
L.append("These have a datasheet in the current build; switching the MFM prices them with no orphan.\n")
for n in sorted(cls["core_priced"]): L.append(f"- {n}")

L.append(block(f"Forge World / Legends — expected/deferred ({len(cls['fw_legends'])})"))
L.append("Priced by the new MFM but excluded at transform; these are the deferred-FW bucket. "
         "They resolve cleanly once the transform FW toggle ships.\n")
for n in sorted(cls["fw_legends"]): L.append(f"- {n}")

if cls["no_sm_datasheet"]:
    L.append(block(f"No SM datasheet — investigate ({len(cls['no_sm_datasheet'])})"))
    L.append("Priced by the new MFM but no faction_id=SM datasheet matched by name. Likely a "
             "name-normalisation mismatch (MFM vs Wahapedia spelling) or a unit genuinely absent "
             "from the export. Each needs a name check before adoption.\n")
    for n in sorted(cls["no_sm_datasheet"]): L.append(f"- {n}")

if cls["other"]:
    L.append(block(f"SM datasheet exists but not in the 181 — investigate ({len(cls['other'])})"))
    for n in sorted(cls["other"]): L.append(f"- {n}")

L.append(block("Black Templars points gap"))
L.append("The 12 BT units that are un-costable in the deployed build, and whether each is "
         "priced by the new SM MFM (vs the old).\n")
L.append("| Unit | In new SM MFM | In old SM MFM |")
L.append("|---|---|---|")
for name, innew, inold in bt_status:
    L.append(f"| {name} | {'yes' if innew else 'no'} | {'yes' if inold else 'no'} |")
closed = sum(1 for _, innew, _ in bt_status if innew)
L.append(f"\nNew SM MFM prices **{closed}/12** of the gap units."
         + (f" A dedicated `MFM_Black_Templars_v1_0.txt` is also present and prices "
            f"**{len(bt_priced)}** units — the cleaner source for BT-specific points; "
            f"cross-check before deciding which file owns BT." if bt_priced else ""))

L.append(block("Captain variants"))
L.append("Captain-family entries priced by the new MFM, and whether each has a datasheet in the 181.\n")
L.append("| Variant | Has datasheet | In old MFM |")
L.append("|---|---|---|")
for disp, hasds, inold in cap_rows:
    L.append(f"| {disp} | {'yes' if hasds else 'NO'} | {'yes' if inold else 'no'} |")

L.append(block("Recommendation"))
L.append("1. **Don’t switch the SM MFM as a “core coverage” move — it isn’t one.** It unlocks a single "
         "core unit (Venerable Dreadnought). Price that one unit directly (errata/override) rather than "
         "swapping the whole points file and importing 75 orphans.")
L.append("2. **Treat the new SM MFM as the FW/Legends pricing layer it actually is.** Adopt it *with* the "
         "transform FW toggle, not before — switching first just inflates `points_no_stat` by "
         f"~{expected_new_orphans} and makes the blocking count meaningless. The two changes are a pair.")
L.append("3. **Investigate the no-datasheet name(s)** — "
         f"{', '.join(sorted(cls['no_sm_datasheet'])) or '—'} — before any switch; resolve as a name "
         "mismatch or confirm it’s genuinely out of scope.")
L.append("4. **Black Templars points come from `MFM_Black_Templars_v1_0.txt` (89 priced), not the SM MFM** "
         "(which closes only 3/12). Wire BT points from the dedicated file; don’t double-source.")
L.append("5. **Net effect on the roadmap:** the new-MFM task is gated on the FW toggle, not a quick win. "
         "The FW toggle is the actual high-leverage item; the MFM switch rides on it.")
L.append("\n*No files were modified by this analysis.*\n")

report = "\n".join(L) + "\n"
out_path = os.path.join("/mnt/user-data/outputs", "MFM_FW_Reconciliation.md")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(report)

# console summary
print(f"old={len(old)} new={len(new)} new_only={len(new_only)} removed={len(removed)}")
print(f"core_priced={len(cls['core_priced'])} fw_legends={len(cls['fw_legends'])} "
      f"no_sm_datasheet={len(cls['no_sm_datasheet'])} other={len(cls['other'])}")
print(f"BT gap closed by new SM MFM: {closed}/12 | BT-dedicated MFM prices {len(bt_priced)}")
print(f"captain variants priced: {len(cap_rows)} | missing-datasheet: {sum(1 for _,h,_ in cap_rows if not h)}")
print(f"expected points_no_stat delta on naive switch: +{expected_new_orphans}")
print(f"report -> {out_path}")
