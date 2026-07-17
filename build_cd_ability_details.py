#!/usr/bin/env python3
"""
B1b: build Unit_Ability_Details.csv rows for Chaos Daemons from
chaos_daemons_reference.md, mirroring the SM/DG unit_abil_desc pattern
(D141 / D-new). Only touches CD; SM/DG rows (if any exist elsewhere)
are untouched -- this script only emits CD rows.

Unit_Abilities.csv (CD's flat global lookup) supplies the VALID name
list used to split the reference doc's prose "Abilities:" line, but is
NOT used as text fallback -- 33 of its 96 entries are themselves
truncated at the source (cut off mid-sentence, e.g. "...within 6\" of
this model"), a far bigger corruption than the 3+1 instances D141
flagged. chaos_daemons_reference.md's own full-text occurrences are the
only reliable source; where the doc shorthands a repeat as "As above."
(god-aura abilities are identical across every unit of that god), the
fallback is the first FULL text found anywhere else in the same
document for that name, never the flat CSV.
"""
import csv
import re

REF = "chaos_daemons_reference.md"
FLAT = "Unit_Abilities.csv"
STATS = "Unit_Stats.csv"
OUT = "Unit_Ability_Details.csv"

def slug_id(army_name, unit_name):
    def _s(x):
        return re.sub(r"[^a-z0-9]+", "-", (x or "").strip().lower()).strip("-")
    return f"local:{_s(army_name)}:{_s(unit_name)}"

# 1. canonical flat name -> desc (CD's own global lookup; authoritative text)
flat = {}
with open(FLAT, encoding="utf-8-sig") as f:
    r = csv.reader(f)
    next(r)
    for row in r:
        if row and row[0].strip():
            flat[row[0].strip()] = row[1].strip()

known_names = list(flat.keys())
# longest-first so "Daemon Lord of Nurgle (Aura)" isn't shadowed by a shorter partial match
known_names.sort(key=len, reverse=True)

# 2. built CD unit names (exact case) from Unit_Stats.csv
cd_units = []
with open(STATS, encoding="utf-8-sig") as f:
    r = csv.DictReader(f)
    for row in r:
        if row["Army Name"] == "Chaos Daemons":
            cd_units.append(row["Unit Name"])
cd_units = sorted(set(cd_units))
upper_to_proper = {u.upper().replace("'", "").replace(chr(8217), ""): u for u in cd_units}

# 3. parse reference doc into unit blocks
text = open(REF, encoding="utf-8").read()
blocks = re.split(r"^### ", text, flags=re.M)[1:]

# escaped alternation pattern of all known ability names, longest first
name_pat = "|".join(re.escape(n) for n in known_names)
name_re = re.compile(name_pat)

def extract_unit_entries(b):
    """Return (unit_name_or_None, [(name, seg), ...]) for one block."""
    lines = b.split("\n")
    header = lines[0].strip()
    header_key = header.upper().replace("'", "").replace(chr(8217), "")
    unit_name = upper_to_proper.get(header_key)
    if unit_name is None:
        return None, []
    ab_lines = [l for l in lines if l.startswith("Abilities:")]
    if not ab_lines:
        return unit_name, []
    ab_text = ab_lines[0][len("Abilities:"):].strip()

    matches = []
    for m in name_re.finditer(ab_text):
        end = m.end()
        rest = ab_text[end:end + 3]
        if rest.startswith(" \u2014") or rest.startswith(" -"):
            matches.append((m.start(), m.end(), m.group(0)))

    filtered = []
    last_end = -1
    for start, end, nm in matches:
        if start < last_end:
            continue
        filtered.append((start, end, nm))
        last_end = end

    entries = []
    for i, (start, end, nm) in enumerate(filtered):
        seg_start = end
        seg_end = filtered[i + 1][0] if i + 1 < len(filtered) else len(ab_text)
        seg = ab_text[seg_start:seg_end].strip()
        seg = re.sub(r"^[\u2014\-]\s*", "", seg)
        seg = seg.rstrip()
        entries.append((nm, seg))
    return unit_name, entries

GENERIC_UNIT_INVARIANT_NAMES = {
    # Fortification is the core-rules generic Fortification-terrain ability,
    # identical for every Fortification-type unit -- not something that varies
    # per datasheet. The reference doc spells it out in full for one unit
    # (Skull Altar) and abbreviates it for the other (Feculent Gnarlmaw); the
    # abbreviation is a shorter restatement of the same fact, not a different
    # rule, so both units get the fuller version.
    "Fortification",
}

# Pass 1: parse every block once, collect the first FULL (non-shorthand)
# text found anywhere in the document for each ability name.
parsed_blocks = [extract_unit_entries(b) for b in blocks]
full_text_by_name = {}
for unit_name, entries in parsed_blocks:
    for nm, seg in entries:
        is_shorthand = seg in ("As above.", "As above", "") or seg.startswith("As above")
        if is_shorthand and nm not in full_text_by_name:
            continue
        if is_shorthand:
            continue
        if nm not in full_text_by_name or (nm in GENERIC_UNIT_INVARIANT_NAMES and len(seg) > len(full_text_by_name[nm])):
            full_text_by_name[nm] = seg

# Pass 2: emit rows, resolving shorthand via full_text_by_name (never the flat CSV).
rows_out = []
unmatched_units = []
unresolved_names = []
fallback_used = []

for unit_name, entries in parsed_blocks:
    if unit_name is None:
        continue
    if not entries:
        unmatched_units.append(unit_name)
        continue
    ds_id = slug_id("Chaos Daemons", unit_name)
    for nm, seg in entries:
        is_shorthand = seg in ("As above.", "As above", "") or seg.startswith("As above")
        if is_shorthand:
            if nm in full_text_by_name:
                seg = full_text_by_name[nm]
                fallback_used.append((unit_name, nm))
            else:
                unresolved_names.append((unit_name, nm))
                continue
        elif nm in GENERIC_UNIT_INVARIANT_NAMES and nm in full_text_by_name and len(full_text_by_name[nm]) > len(seg):
            seg = full_text_by_name[nm]
            fallback_used.append((unit_name, nm))
        rows_out.append({
            "Datasheet ID": ds_id,
            "Unit Ability Name": nm,
            "Unit Ability Description": seg,
        })

with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["Datasheet ID", "Unit Ability Name", "Unit Ability Description"])
    w.writeheader()
    for row in rows_out:
        w.writerow(row)

print(f"Built {len(rows_out)} ability-detail rows across {len(set(r['Datasheet ID'] for r in rows_out))} units.")
print(f"Fallback-to-flat-text used {len(fallback_used)} times (expected for shared god-aura abilities).")
if unresolved_names:
    print(f"UNRESOLVED (no fallback available): {unresolved_names}")
if unmatched_units:
    print(f"Units with no Abilities: line: {unmatched_units}")

missing = set(cd_units) - set(u for u in cd_units if slug_id("Chaos Daemons", u) in set(r["Datasheet ID"] for r in rows_out))
if missing:
    print(f"Built CD units with ZERO rows produced: {sorted(missing)}")
