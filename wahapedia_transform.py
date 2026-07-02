#!/usr/bin/env python3
"""
Wahapedia structured-export -> Army Builder 8-CSV transformer.

Produces the eight datasheet-derived CSVs for one faction:
  Unit_Stats, Unit_Weapons, Unit_Wargear_Options, Unit_Other_Options,
  Unit_Abilities, Rules, Keywords, Weapon_Abilities
plus validation_report.md.

Unit_Points and Leader Eligible Units are NOT produced here -- they come from
the separate MFM points parser, because GW (MFM) is authoritative for points and
the verbatim SUPPORT lists.

Design decisions baked in (locked with Ryan):
  - Generic units: Army Name = "Adeptus Astartes"; chapter variants = chapter name.
  - Legends / Forge World excluded (current edition-10 faction packs only).
  - Weapon special rules -> "Weapon Ability Names" col -> Keywords.csv lookup.
  - Wargear-item effects (type=Wargear) -> Weapon_Abilities.csv lookup.
  - Datasheet abilities -> Unit_Abilities.csv lookup + "Unit Ability Names".
  - Core USRs -> Rules.csv lookup + "Rule Names".
  - Faction abilities (Oath of Moment) are ARMY-LEVEL: surfaced in the report,
    added to the Unit_Abilities glossary, but NOT stapled onto every unit.
  - Bundled swaps: two rows sharing an Option Group (handoff approach).
  - Non-weapon wargear lives in Unit_Wargear_Options; its effect in Weapon_Abilities.

Lookup descriptions for universal rules (Keywords, Rules) and wargear abilities
(Weapon_Abilities) are SEEDED from an existing completed faction (e.g. Chaos
Daemons) by name match; genuinely new names are emitted with a blank description
and flagged for Ryan to fill.

Stdlib only. Run locally:  python wahapedia_transform.py --help
"""

import argparse
import csv
import html
import os
import re
import sys
from collections import defaultdict, OrderedDict

# ----------------------------------------------------------------------------
# Config / constants
# ----------------------------------------------------------------------------

KNOWN_CHAPTERS = {
    "Black Templars", "Blood Angels", "Dark Angels", "Deathwatch",
    "Imperial Fists", "Iron Hands", "Raven Guard", "Salamanders",
    "Space Wolves", "Ultramarines", "White Scars",
}
GENERIC_ARMY_NAME = "Adeptus Astartes"

# Sub-faction keywords that belong to a single owning chapter. When a datasheet
# carries one of these but its resolved Army Name is NOT the owner, the keyword is
# spurious bleed (e.g. generic Sternguard carrying Deathwing, generic Stormraven
# carrying Ravenwing) and is stripped from the unit's Keyword Names.
SUBFACTION_KEYWORD_ARMY = {
    "Deathwing": "Dark Angels",
    "Ravenwing": "Dark Angels",
}

# Source rows to EXCLUDE (Legends / Forge World). We keep edition == "10".
def source_is_excluded(src_row):
    name = (src_row.get("name") or "")
    edition = (src_row.get("edition") or "").strip()
    low = name.lower()
    if "legend" in low or "forge world" in low:
        return True
    if edition != "10":
        return True
    return False

BOM = "\ufeff"

# ----------------------------------------------------------------------------
# IO helpers
# ----------------------------------------------------------------------------

def read_pipe(path):
    """Read a Wahapedia pipe-delimited CSV into list[dict]. Tolerates trailing |."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        # Wahapedia rows end with a trailing '|', producing a blank final field.
        reader = csv.reader(f, delimiter="|")
        rows = list(reader)
    if not rows:
        return []
    header = [h.strip() for h in rows[0]]
    out = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        d = {header[i]: (r[i] if i < len(r) else "") for i in range(len(header))}
        out.append(d)
    return out


def read_existing_lookup(path, key_col, desc_col):
    """Seed dict {name: description} from an existing completed-faction lookup CSV."""
    seed = {}
    if not path or not os.path.exists(path):
        return seed
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return seed
        header = [h.strip() for h in header]
        try:
            ki = header.index(key_col)
            di = header.index(desc_col)
        except ValueError:
            return seed
        for row in reader:
            if len(row) <= max(ki, di):
                continue
            name = row[ki].strip()
            if name and name not in seed:
                seed[name] = row[di]
    return seed


def write_csv(path, header, rows, trailing_blank_cols=0):
    """Write a UTF-8 (BOM) CSV matching the existing app convention. CRLF line ends."""
    full_header = list(header) + ["" for _ in range(trailing_blank_cols)]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(full_header)
        for r in rows:
            row = list(r) + ["" for _ in range(trailing_blank_cols)]
            w.writerow(row)

# ----------------------------------------------------------------------------
# Text helpers
# ----------------------------------------------------------------------------

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")

def strip_html(s, list_sep=" | "):
    if s is None:
        return ""
    s = s.replace("</li>", list_sep).replace("<br>", " ").replace("<br/>", " ")
    s = _TAG.sub(" ", s)
    s = html.unescape(s)
    s = s.replace("\u200b", "")
    s = _WS.sub(" ", s).strip()
    s = s.strip(list_sep.strip()).strip()
    return s

def norm_name(s):
    """Lowercased, punctuation-light key for fuzzy matching weapon names."""
    s = (s or "").lower()
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"[^a-z0-9+ ]", " ", s)
    s = _WS.sub(" ", s).strip()
    return s

_PARAM_TOKEN = re.compile(r"^(?:\d*[dD][36]\+?|\d+\+?)$")  # 1, 3+, D6, 2D6, D3+

# Profile suffixes ("Typhoon missile launcher – frag") attach after a SPACED dash.
# Strip them before base-equipment matching so the bare weapon name matches the
# loadout prose. Splits only on a spaced dash, so internal hyphens (multi-melta)
# survive.
_SPACED_DASH = re.compile(r"\s+[\u2013\u2014-]\s+")
def base_weapon_name(name):
    return _SPACED_DASH.split(name or "", 1)[0]

def _cap_word(w):
    # Capitalize across hyphens: 'anti-vehicle' -> 'Anti-Vehicle'
    return "-".join(seg[:1].upper() + seg[1:].lower() if seg else seg for seg in w.split("-"))

def titlecase_ability(s):
    """Normalize a weapon ability token to Title Case, preserving params/dice/+."""
    s = s.strip().strip(".")
    if not s:
        return ""
    out = []
    for p in s.split():
        if _PARAM_TOKEN.match(p):
            out.append(p.upper() if re.search(r"[dD]", p) else p)
        else:
            out.append(_cap_word(p))
    return " ".join(out)

def generic_of(instance):
    """Collapse a parameterized instance to its generic lookup key.
    'Rapid Fire 1' -> 'Rapid Fire'; 'Anti-Infantry 4+' -> 'Anti-Infantry';
    'Melta 2' -> 'Melta'; 'Deadly Demise D6' -> 'Deadly Demise'."""
    g = re.sub(r"\s+[0-9]+\+?$", "", instance)          # trailing number / N+
    g = re.sub(r"\s+[dD][36]\+?$", "", g)               # trailing dice
    g = re.sub(r"\s+[0-9]+\+$", "", g)
    return g.strip()

def comma_safe(name):
    """Names are stored in comma-delimited cells, so a comma inside a name (e.g.
    'Transfixing Gaze (Aura, Psychic)') would be mis-split by the app. Convert
    commas inside parentheses to semicolons. Applied to glossary key AND the unit
    reference identically, so they stay matched."""
    return re.sub(r"\(([^)]*)\)", lambda m: "(" + m.group(1).replace(",", ";") + ")", name)

# ----------------------------------------------------------------------------
# Load + filter datasheets
# ----------------------------------------------------------------------------

def load(args):
    p = lambda n: os.path.join(args.wahapedia_dir, n)
    data = {
        "datasheets": read_pipe(p("Datasheets.csv")),
        "sources": read_pipe(p("Source.csv")),
        "models": read_pipe(p("Datasheets_models.csv")),
        "wargear": read_pipe(p("Datasheets_wargear.csv")),
        "options": read_pipe(p("Datasheets_options.csv")),
        "abilities": read_pipe(p("Datasheets_abilities.csv")),
        "abil_glossary": read_pipe(p("Abilities.csv")),
        "keywords": read_pipe(p("Datasheets_keywords.csv")),
        "leaders": read_pipe(p("Datasheets_leader.csv")),
    }
    return data


def select_datasheets(data, faction):
    excluded_sources = {s["id"] for s in data["sources"] if source_is_excluded(s)}
    selected = OrderedDict()
    skipped_legends = []
    for d in data["datasheets"]:
        if d.get("faction_id") != faction:
            continue
        if d.get("virtual", "").lower() == "true":
            continue
        if d.get("source_id") in excluded_sources:
            skipped_legends.append(d.get("name", d.get("id")))
            continue
        selected[d["id"]] = d
    return selected, skipped_legends

# ----------------------------------------------------------------------------
# Chapter / Army Name resolution
# ----------------------------------------------------------------------------

def build_army_names(selected, kw_rows, flags):
    by_ds = defaultdict(list)
    for k in kw_rows:
        if k["datasheet_id"] in selected and (k.get("is_faction_keyword", "").lower() == "true"):
            by_ds[k["datasheet_id"]].append(k.get("keyword", "").strip())
    army_of = {}
    for ds_id in selected:
        fkw = by_ds.get(ds_id, [])
        chapters = [k for k in fkw if k in KNOWN_CHAPTERS]
        unknown_extra = [k for k in fkw if k not in KNOWN_CHAPTERS and k != "Adeptus Astartes"]
        if len(chapters) == 1:
            army_of[ds_id] = chapters[0]
        elif len(chapters) > 1:
            army_of[ds_id] = chapters[0]
            flags["multi_chapter"].append(
                f"{selected[ds_id]['name']}: multiple chapter keywords {chapters} -> used {chapters[0]}")
        else:
            army_of[ds_id] = GENERIC_ARMY_NAME
            if unknown_extra:
                flags["unknown_chapter_kw"].append(
                    f"{selected[ds_id]['name']}: non-chapter faction keyword(s) {unknown_extra} -> kept generic")
    return army_of

# ----------------------------------------------------------------------------
# Abilities indexing  (route by type)
# ----------------------------------------------------------------------------

def index_abilities(data, selected, flags):
    glossary = {a["id"]: a for a in data["abil_glossary"]}
    # per-datasheet routed abilities
    unit_abil = defaultdict(list)     # datasheet abilities (name+desc on row)
    unit_faction = defaultdict(list)  # faction abilities carried by this datasheet (per-unit display)
    rule_names = defaultdict(list)    # Core USR instances
    fnp = {}                          # ds_id -> (value, condition)
    leader_flag = set()               # ds_id has Leader
    # lookups
    unit_abil_defs = OrderedDict()    # name -> desc  (Datasheet + Faction)
    weapon_abil_defs = OrderedDict()  # name -> desc  (Wargear)
    rule_defs = OrderedDict()         # generic rule name -> desc(blank, seeded later)
    faction_abilities = OrderedDict() # name -> desc   (army-level, surfaced)

    for r in data["abilities"]:
        ds = r["datasheet_id"]
        if ds not in selected:
            continue
        atype = (r.get("type") or "").strip()
        name = strip_html(r.get("name", ""))
        desc = strip_html(r.get("description", ""), list_sep="; ")
        param = (r.get("parameter") or "").strip()
        aid = (r.get("ability_id") or "").strip()
        # resolve name/desc from glossary when row is an id-reference
        if aid and aid in glossary:
            gname = strip_html(glossary[aid].get("name", ""))
            gdesc = strip_html(glossary[aid].get("description", ""), list_sep="; ")
            name = name or gname
            desc = desc or gdesc
        name = comma_safe(name)

        if atype == "Core":
            inst = name if not param else f"{name} {param}".strip()
            if name.lower() == "leader":
                leader_flag.add(ds)
            if name.lower() == "feel no pain":
                fnp[ds] = (param or "", "")
                flags["fnp_from_ability"].append(f"{selected[ds]['name']}: FNP {param} (placed in Rule Names)")
            rule_names[ds].append(inst)
            rule_defs.setdefault(generic_of(inst), desc)
        elif atype == "Datasheet":
            if name:
                unit_abil[ds].append(name)
                unit_abil_defs.setdefault(name, desc)
        elif atype == "Faction":
            if name:
                unit_faction[ds].append(name)        # show under this unit
                faction_abilities.setdefault(name, desc)
                unit_abil_defs.setdefault(name, desc)  # glossary definition
        elif atype == "Wargear":
            if name:
                weapon_abil_defs.setdefault(name, desc)
        else:
            # Special / Fortification / Primarch / Wargear profile / Без заголовка
            flags["unclassified_abilities"].append(
                f"{selected[ds]['name']} | type='{atype}' | name='{name or '(none)'}'")
    return {
        "unit_abil": unit_abil, "unit_faction": unit_faction,
        "rule_names": rule_names, "fnp": fnp,
        "leader_flag": leader_flag, "unit_abil_defs": unit_abil_defs,
        "weapon_abil_defs": weapon_abil_defs, "rule_defs": rule_defs,
        "faction_abilities": faction_abilities,
    }

# ----------------------------------------------------------------------------
# Weapons
# ----------------------------------------------------------------------------

def parse_weapon_abilities(desc):
    """'ANTI-VEHICLE 2+, PISTOL' -> ['Anti-Vehicle 2+', 'Pistol']"""
    desc = strip_html(desc)
    if not desc:
        return []
    out = []
    for tok in desc.split(","):
        t = titlecase_ability(tok)
        if t:
            out.append(t)
    return out

def fmt_range(rng):
    rng = (rng or "").strip()
    if rng.lower() in ("melee", "n/a", ""):
        return rng or "Melee"
    if re.match(r"^[0-9]+$", rng):
        return f'{rng}"'
    return rng

def build_weapons(data, selected, army_of, kw_defs_acc, flags):
    rows = []
    weapon_names_by_ds = defaultdict(list)
    # base-equipment detection from the datasheet loadout prose.
    # Normalize the loadout text through norm_name so it matches the same
    # hyphen->space treatment applied to weapon names below; otherwise
    # hyphenated weapons (e.g. "master-crafted bolter") never match.
    loadout_by_ds = {ds_id: norm_name(strip_html(d.get("loadout", "")))
                     for ds_id, d in selected.items()}
    wg = sorted(
        (w for w in data["wargear"] if w["datasheet_id"] in selected),
        key=lambda w: (w["datasheet_id"], int(w.get("line", "0") or 0),
                       int(w.get("line_in_wargear", "0") or 0)),
    )
    for w in wg:
        ds = w["datasheet_id"]
        name = strip_html(w.get("name", ""))
        if not name:
            continue
        weapon_names_by_ds[ds].append(name)
        wtype = (w.get("type") or "").strip() or "Ranged"
        abilities = parse_weapon_abilities(w.get("description", ""))
        for a in abilities:
            kw_defs_acc.setdefault(generic_of(a), "")
        bs = ws = ""
        bsws = (w.get("BS_WS") or "").strip()
        if wtype.lower() == "melee":
            ws = bsws
        else:
            bs = bsws
        is_base = "Yes" if (loadout_by_ds.get(ds) and norm_name(base_weapon_name(name)) in loadout_by_ds[ds]) else "No"
        rows.append([
            army_of[ds], selected[ds]["name"], "All", wtype, name,
            fmt_range(w.get("range")), (w.get("A") or "").strip(), bs, ws,
            (w.get("S") or "").strip(), (w.get("AP") or "").strip(),
            (w.get("D") or "").strip(), ",".join(abilities), "", is_base, "",
        ])
    return rows, weapon_names_by_ds

# ----------------------------------------------------------------------------
# Stats
# ----------------------------------------------------------------------------

def build_stats(data, selected, army_of, abil, kw_rows, weapon_names_by_ds, leader_attach, flags):
    kw_by_ds = defaultdict(list)
    for k in kw_rows:
        if k["datasheet_id"] in selected:
            kw_by_ds[k["datasheet_id"]].append((int(k.get("line", "0") or 0), k.get("keyword", "").strip()))
    models_by_ds = defaultdict(list)
    for m in data["models"]:
        if m["datasheet_id"] in selected:
            models_by_ds[m["datasheet_id"]].append(m)

    def unit_type(ds_id):
        kws = {k for _, k in kw_by_ds.get(ds_id, [])}
        for kw in ("Epic Hero", "Fortification", "Vehicle", "Monster", "Beast", "Mounted"):
            if kw in kws:
                return kw
        if "Character" in kws:
            return "Character"
        role = (selected[ds_id].get("role") or "").strip()
        if role == "Battleline":
            return "Battleline"
        if "Infantry" in kws:
            return "Infantry"
        flags["unit_type_fallback"].append(f"{selected[ds_id]['name']} -> role '{role}'")
        return role or "Infantry"

    rows = []
    for ds_id, d in selected.items():
        mlist = sorted(models_by_ds.get(ds_id, []), key=lambda m: int(m.get("line", "0") or 0))
        if len(mlist) > 1:
            flags["multi_model_line"].append(
                f"{d['name']}: {len(mlist)} model lines -> weapons emitted as Model Group 'All' (review split)")
        kw_sorted = [k for _, k in sorted(kw_by_ds.get(ds_id, []))]
        # Fix 2a: strip spurious sub-faction keyword bleed (e.g. Deathwing on a
        # generic Adeptus Astartes datasheet) when this unit's army isn't the owner.
        kept_kw = []
        for k in kw_sorted:
            owner = SUBFACTION_KEYWORD_ARMY.get(k)
            if owner and army_of[ds_id] != owner:
                flags["stripped_subfaction_kw"].append(
                    f"{d['name']} [{army_of[ds_id]}]: stripped '{k}' (owner={owner})")
                continue
            kept_kw.append(k)
        kw_sorted = kept_kw
        kw_str = ",".join(kw_sorted)
        ut = unit_type(ds_id)
        abil_names = ",".join(dict.fromkeys(abil["unit_abil"].get(ds_id, [])))
        rule_str = ",".join(dict.fromkeys(
            abil["rule_names"].get(ds_id, []) + abil["unit_faction"].get(ds_id, [])))
        leader_ability = "Leader" if ds_id in abil["leader_flag"] else ""
        # Fix 3: fill Leader Eligible Units from Datasheets_leader.csv. GW's leader
        # map is authoritative for what a datasheet can lead; the generic Captain
        # datasheet is the one chapter armies use, so its graph legitimately spans
        # chapter bodyguards. Lists every attachable that exists in the build, deduped
        # by name. Render-time filtering to the selected army is an app concern.
        leader_elig = ""
        if leader_ability:
            names = []
            for att in leader_attach.get(ds_id, []):
                if att in selected:
                    nm = selected[att]["name"]
                    if nm not in names:
                        names.append(nm)
            leader_elig = " | ".join(sorted(names))
        fnp_v, fnp_c = abil["fnp"].get(ds_id, ("", ""))
        for m in (mlist or [None]):
            grp = "All" if len(mlist) <= 1 else strip_html(m.get("name", "")) if m else "All"
            mv = (m.get("M") if m else "") or ""
            t = (m.get("T") if m else "") or ""
            sv = (m.get("Sv") if m else "") or ""
            inv = (m.get("inv_sv") if m else "") or ""
            inv = "" if inv in ("-", None) else inv
            invc = strip_html(m.get("inv_sv_descr", "")) if m else ""
            wv = (m.get("W") if m else "") or ""
            ld = (m.get("Ld") if m else "") or ""
            oc = (m.get("OC") if m else "") or ""
            rows.append([
                army_of[ds_id], d["name"], grp, ut, mv, t, sv, inv, invc,
                fnp_v, fnp_c, wv, ld, oc, leader_ability,
                leader_elig,   # Leader Eligible Units (from Datasheets_leader.csv)
                "",   # Co-Leader Eligible With (manual / surfaced)
                "",   # Leader Restrictions     (manual / surfaced)
                abil_names, rule_str, kw_str,
                ds_id,   # Datasheet ID (Wahapedia stable id; durable saved-list ref)
            ])
    return rows

# ----------------------------------------------------------------------------
# Wargear / Other options  (prose parse + flag)
# ----------------------------------------------------------------------------

_RATIO = re.compile(r"for every\s+(\d+)\s+models", re.I)
_UPTO = re.compile(r"up to\s+(\d+)", re.I)
_ANYNUM = re.compile(r"any number of", re.I)
_ALLMODELS = re.compile(r"\ball models\b", re.I)
# replaced-weapon lead-in patterns (ordered)
_PAT_OWNS = re.compile(r"(?:the\s+)?[\w\s]+?(?:'s|’s)\s+(?P<weapon>[\w\s/–-]+?)\s+can be replaced with", re.I)
_PAT_HAVE = re.compile(r"have (?:its|their)\s+(?P<weapon>[\w\s/–-]+?)\s+replaced(?:\s+with)?", re.I)
_PAT_REPLACE_ITS = re.compile(r"replace (?:its|their)\s+(?P<weapon>[\w\s/–-]+?)\s+with", re.I)
_REPL_SINGLE = re.compile(r"replaced?\s+(?:with\s+)?1\s+(?P<repl>.+?)\.?$", re.I)
_EQUIP_ONE = re.compile(r"equipped with\s+1\s+(?P<item>.+?)\.?$", re.I)
_EQUIP_CHOICE = re.compile(r"equipped with one of the following", re.I)
_HAS_AND = re.compile(r"\band\b|,", re.I)

def _strip_count(s):
    return re.sub(r"^\d+\s+", "", s).strip().rstrip(".")

def resolve_weapon(name, ds_weapon_names, ds_norm_index, flags, unit, where):
    """Map a prose weapon name to a canonical weapon name on this datasheet."""
    n = norm_name(name)
    if n in ds_norm_index:
        cands = ds_norm_index[n]
        if len(cands) == 1:
            return cands[0], True
    partial = [orig for orig in ds_weapon_names if n and n in norm_name(orig)]
    if len(partial) == 1:
        return partial[0], True
    if len(partial) > 1:
        flags["ambiguous_weapon_match"].append(
            f"{unit} [{where}]: '{name}' matches {partial} -> stored raw, needs manual pick")
        return name, False
    return name, False

def parse_options(data, selected, army_of, weapon_names_by_ds, flags):
    wargear_rows = []
    other_rows = []
    ds_norm_index = {}
    for ds, names in weapon_names_by_ds.items():
        idx = defaultdict(list)
        for nm in names:
            idx[norm_name(nm)].append(nm)
        ds_norm_index[ds] = idx

    opts_by_ds = defaultdict(list)
    for o in data["options"]:
        if o["datasheet_id"] in selected:
            opts_by_ds[o["datasheet_id"]].append(o)

    for ds_id, olist in opts_by_ds.items():
        unit = selected[ds_id]["name"]
        army = army_of[ds_id]
        wnames = weapon_names_by_ds.get(ds_id, [])
        nidx = ds_norm_index.get(ds_id, {})
        group_letter = ord("A")

        def rw(name, where):
            return resolve_weapon(name, wnames, nidx, flags, unit, where)

        for o in sorted(olist, key=lambda x: int(x.get("line", "0") or 0)):
            button = (o.get("button") or "").strip()
            raw = o.get("description", "")
            items = [strip_html(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", raw, re.S)]
            lead = strip_html(re.sub(r"<ul.*?</ul>", "", raw, flags=re.S))
            grp = chr(group_letter)
            low = lead.lower()

            if button == "*" or lead.strip().startswith("*"):
                flags["option_footnotes"].append(f"{unit}: constraint note -> '{lead[:120]}'")
                continue

            # triggers
            ratio = _RATIO.search(lead)
            upto = _UPTO.search(lead)
            mpt = ratio.group(1) if ratio else ""
            mst = ""
            if upto:
                mst = upto.group(1)
            elif _ANYNUM.search(lead) or _ALLMODELS.search(lead):
                mst = "Any"

            # ---- identify the replaced weapon (if this is a replacement) ----
            replaced = ""
            is_replacement = "replac" in low
            if is_replacement:
                wm = _PAT_OWNS.search(lead) or _PAT_HAVE.search(lead) or _PAT_REPLACE_ITS.search(lead)
                if wm:
                    rwname = _strip_count(strip_html(wm.group("weapon")))
                    # bail out if the replaced side itself names two weapons
                    if re.search(r"\band\b", rwname, re.I):
                        flags["bundled_swap"].append(f"{unit} [grp {grp}]: two-weapon replaced side '{rwname}' -> two-row manual")
                        group_letter += 1
                        continue
                    replaced, _ = rw(rwname, f"grp {grp} replaced")
                else:
                    flags["unparsed_options"].append(f"{unit} [grp {grp}]: '{lead[:160]}' | items={items}")
                    group_letter += 1
                    continue

            # ---- ADDITION (equip-with), choice list ----
            if not is_replacement and _EQUIP_CHOICE.search(lead) and items:
                for it in items:
                    repl = _strip_count(it)
                    if re.search(r"\band\b", repl, re.I):
                        flags["compound_replacement"].append(f"{unit} [grp {grp}]: compound add '{it}'")
                        continue
                    canon, matched = rw(repl, f"grp {grp} add")
                    wargear_rows.append([army, unit, "All", mpt, mst, "", canon, "", "Yes", grp])
                    if not matched:
                        flags["nonweapon_or_unmatched"].append(f"{unit}: add '{repl}' (no weapon profile; wargear item)")
                group_letter += 1
                continue

            # ---- ADDITION, single ----
            if not is_replacement and "equipped with" in low and not items:
                eq = _EQUIP_ONE.search(lead)
                item = _strip_count(strip_html(eq.group("item"))) if eq else lead
                if re.search(r"\band\b", item, re.I) or len(item) > 60:
                    flags["unparsed_options"].append(f"{unit} [grp {grp}]: '{lead[:160]}'")
                    group_letter += 1
                    continue
                canon, matched = rw(item, "equip-add")
                wargear_rows.append([army, unit, "All", mpt, mst, "", canon, "", "No", ""])
                if not matched:
                    flags["nonweapon_or_unmatched"].append(f"{unit}: equip '{item}' (no weapon profile; wargear item)")
                group_letter += 1
                continue

            # ---- REPLACEMENT, choice list ----
            if is_replacement and items:
                emitted = 0
                for it in items:
                    repl = _strip_count(it)
                    if re.search(r"\band\b", repl, re.I):
                        flags["compound_replacement"].append(f"{unit} [grp {grp}]: compound replacement '{it}'")
                        continue
                    canon, _ = rw(repl, f"grp {grp} repl")
                    wargear_rows.append([army, unit, "All", mpt, mst, replaced, canon, "", "Yes", grp])
                    emitted += 1
                if emitted == 0:
                    flags["unparsed_options"].append(f"{unit} [grp {grp}]: replacement list all-compound | items={items}")
                group_letter += 1
                continue

            # ---- REPLACEMENT, single ----
            if is_replacement and not items:
                r1 = _REPL_SINGLE.search(lead)
                if r1:
                    repl = _strip_count(strip_html(r1.group("repl")))
                    if re.search(r"\band\b", repl, re.I):
                        flags["compound_replacement"].append(f"{unit} [grp {grp}]: '{lead[:140]}'")
                    else:
                        canon, _ = rw(repl, "single repl")
                        wargear_rows.append([army, unit, "All", mpt, mst, replaced, canon, "", "No", ""])
                        group_letter += 1
                        continue
                flags["unparsed_options"].append(f"{unit} [grp {grp}]: '{lead[:160]}'")
                group_letter += 1
                continue

            # ---- fallback ----
            flags["unparsed_options"].append(f"{unit} [grp {grp}]: '{lead[:160]}' | items={items}")
            group_letter += 1
    return wargear_rows, other_rows

# ----------------------------------------------------------------------------
# Lookups assembly
# ----------------------------------------------------------------------------

def assemble_lookup(names_with_desc, seed, flags, label):
    rows = []
    missing = []
    for name, desc in names_with_desc.items():
        if not name:
            continue
        final_desc = desc or seed.get(name, "")
        if not final_desc:
            missing.append(name)
        rows.append([name, final_desc])
    rows.sort(key=lambda r: r[0].lower())
    if missing:
        flags[f"missing_desc_{label}"].extend(sorted(set(missing)))
    return rows

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Wahapedia -> Army Builder 8-CSV transformer")
    ap.add_argument("--wahapedia-dir", default=".", help="folder with Wahapedia export CSVs")
    ap.add_argument("--seed-dir", default=".", help="folder with a completed faction's lookup CSVs (Keywords/Rules/Weapon_Abilities) for description reuse")
    ap.add_argument("--out-dir", default="out", help="output folder")
    ap.add_argument("--faction", default="SM", help="Wahapedia faction id (SM = Space Marines)")
    ap.add_argument("--army-name", default="Adeptus Astartes", help="Generic army name for units without a chapter keyword (use the faction name for non-SM factions, e.g. 'Death Guard')")
    args = ap.parse_args()
    global GENERIC_ARMY_NAME
    GENERIC_ARMY_NAME = args.army_name

    os.makedirs(args.out_dir, exist_ok=True)
    flags = defaultdict(list)

    data = load(args)
    if not data["datasheets"]:
        sys.exit(f"No Datasheets.csv found in {args.wahapedia_dir}")

    selected, skipped_legends = select_datasheets(data, args.faction)
    flags["skipped_legends_fw"] = skipped_legends
    army_of = build_army_names(selected, data["keywords"], flags)
    abil = index_abilities(data, selected, flags)

    kw_defs_acc = OrderedDict()  # weapon ability generic name -> "" (seeded later)
    weapons_rows, weapon_names_by_ds = build_weapons(data, selected, army_of, kw_defs_acc, flags)
    # Fix 3: leader -> attached-bodyguard map from Datasheets_leader.csv.
    leader_attach = defaultdict(list)
    for r in data["leaders"]:
        lid = (r.get("leader_id") or "").strip()
        aid = (r.get("attached_id") or "").strip()
        if lid and aid:
            leader_attach[lid].append(aid)
    stats_rows = build_stats(data, selected, army_of, abil, data["keywords"], weapon_names_by_ds, leader_attach, flags)

    # Fix 2b: additive chapter-variant ability inheritance. A chapter variant unions
    # the generic (Adeptus Astartes) same-named datasheet's abilities (base first)
    # with its own, deduped. Operates on the assembled Unit Ability Names column (18).
    AB = 18
    generic_abil_by_name = {}
    for row in stats_rows:
        if row[0] == GENERIC_ARMY_NAME:
            generic_abil_by_name.setdefault(
                row[1], [a for a in row[AB].split(",") if a])
    for row in stats_rows:
        if row[0] != GENERIC_ARMY_NAME and row[1] in generic_abil_by_name:
            own = [a for a in row[AB].split(",") if a]
            merged = list(dict.fromkeys(generic_abil_by_name[row[1]] + own))
            if merged != own:
                flags["additive_chapter_abilities"].append(
                    f"{row[1]} [{row[0]}]: inherited {merged}")
            row[AB] = ",".join(merged)

    wargear_rows, other_rows = parse_options(data, selected, army_of, weapon_names_by_ds, flags)

    # seeds from completed faction
    seed_kw = read_existing_lookup(os.path.join(args.seed_dir, "Keywords.csv"), "Keyword Name", "Keyword Description")
    seed_rules = read_existing_lookup(os.path.join(args.seed_dir, "Rules.csv"), "Rule Name", "Rule Description")
    seed_wa = read_existing_lookup(os.path.join(args.seed_dir, "Weapon_Abilities.csv"), "Weapon Ability Name", "Weapon Ability Description")

    keywords_rows = assemble_lookup(kw_defs_acc, seed_kw, flags, "keywords")
    rules_rows = assemble_lookup(abil["rule_defs"], seed_rules, flags, "rules")
    weapon_abil_rows = assemble_lookup(abil["weapon_abil_defs"], seed_wa, flags, "weapon_abilities")
    unit_abil_rows = assemble_lookup(abil["unit_abil_defs"], {}, flags, "unit_abilities")

    O = lambda n: os.path.join(args.out_dir, n)
    write_csv(O("Unit_Stats.csv"),
              ["Army Name","Unit Name","Model Group","Unit Type","M","T","SV","INV","INV_Condition","FNP","FNP_Condition","W","LD","OC","Leader Ability Name","Leader Eligible Units","Co-Leader Eligible With","Leader Restrictions","Unit Ability Names","Rule Names","Keyword Names","Datasheet ID"],
              stats_rows, trailing_blank_cols=2)
    write_csv(O("Unit_Weapons.csv"),
              ["Army Name","Unit Name","Model Group","Weapon Type","Weapon Name","Range","A","BS","WS","S","AP","D","Weapon Ability Names","Weapon Keyword Names","Is Base Equipment","Allegiance_Condition"],
              weapons_rows)
    write_csv(O("Unit_Wargear_Options.csv"),
              ["Army Name","Unit Name","Model Group","Models Per Trigger","Max Substitutions Per Trigger","Weapon Replaced","Replacement Weapon Name","Points Cost","Is Choice","Option Group"],
              wargear_rows)
    write_csv(O("Unit_Other_Options.csv"),
              ["Army Name","Unit Name","Model Group","Option Name","Points Cost","Max Per Unit","Carrier Notes","Ability Name","Is Mutually Exclusive","Exclusion Group"],
              other_rows)
    write_csv(O("Unit_Abilities.csv"), ["Unit Ability Name","Unit Ability Description"], unit_abil_rows, trailing_blank_cols=5)
    write_csv(O("Rules.csv"), ["Rule Name","Rule Description"], rules_rows, trailing_blank_cols=1)
    write_csv(O("Keywords.csv"), ["Keyword Name","Keyword Description"], keywords_rows)
    write_csv(O("Weapon_Abilities.csv"), ["Weapon Ability Name","Weapon Ability Description"], weapon_abil_rows)

    write_report(O("validation_report.md"), selected, army_of, weapons_rows, wargear_rows, stats_rows,
                 keywords_rows, rules_rows, unit_abil_rows, weapon_abil_rows, abil, flags)

    print(f"Done. {len(selected)} datasheets -> {args.out_dir}")
    print(f"  stats rows: {len(stats_rows)} | weapon rows: {len(weapons_rows)} | wargear-option rows: {len(wargear_rows)}")
    print(f"  flags: see validation_report.md")


def write_report(path, selected, army_of, weapons, wargear, stats, kw, rules, ua, wa, abil, flags):
    chapters = defaultdict(int)
    for ds in selected:
        chapters[army_of[ds]] += 1
    L = []
    L.append("# Space Marines Transform — Validation Report\n")
    L.append(f"- Datasheets processed: **{len(selected)}**")
    L.append(f"- Stat rows: {len(stats)} | Weapon rows: {len(weapons)} | Wargear-option rows auto-built: {len(wargear)}")
    L.append(f"- Lookups: Keywords {len(kw)}, Rules {len(rules)}, Unit_Abilities {len(ua)}, Weapon_Abilities {len(wa)}")
    L.append("\n## Army Name distribution")
    for name, n in sorted(chapters.items(), key=lambda x: -x[1]):
        L.append(f"- {name}: {n}")
    L.append("\n## Faction (army-level) abilities found — place at army level, NOT per unit")
    for nm in abil["faction_abilities"]:
        L.append(f"- {nm}")
    order = [
        ("missing_desc_keywords", "Weapon abilities (Keywords.csv) needing a description"),
        ("missing_desc_rules", "USRs (Rules.csv) needing a description"),
        ("missing_desc_weapon_abilities", "Wargear abilities (Weapon_Abilities.csv) needing a description"),
        ("unparsed_options", "Wargear options NOT auto-parsed (build manually)"),
        ("bundled_swap", "Bundled two-weapon swaps (build two-row manually)"),
        ("compound_replacement", "Compound replacements ('X and Y')"),
        ("ambiguous_weapon_match", "Ambiguous weapon-name matches"),
        ("nonweapon_or_unmatched", "Equip/add items with no weapon profile"),
        ("option_footnotes", "Option footnotes / constraints (not options)"),
        ("multi_model_line", "Multi model-line units (weapon model-group split to review)"),
        ("unit_type_fallback", "Unit Type fell back to role"),
        ("fnp_from_ability", "Feel No Pain placed in Rule Names"),
        ("unclassified_abilities", "Abilities not routed (Special/Fortification/Primarch/etc)"),
        ("unknown_chapter_kw", "Non-chapter faction keywords"),
        ("multi_chapter", "Multiple chapter keywords"),
        ("skipped_legends_fw", "Skipped (Legends / Forge World)"),
    ]
    for key, title in order:
        items = flags.get(key, [])
        L.append(f"\n## {title} — {len(items)}")
        for it in items[:400]:
            L.append(f"- {it}")
        if len(items) > 400:
            L.append(f"- ...and {len(items)-400} more")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
