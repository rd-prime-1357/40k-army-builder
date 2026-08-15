#!/usr/bin/env python3
"""
add_chapter_keyword_additions.py -- B130 (D342).

Derives the per-chapter keyword-restoration map fresh from source every build and
stamps it onto the matching generic (Adeptus Astartes) units in units.json.
Never hand-maintained -- the map is recomputed on every run from the raw
Wahapedia keyword export, so a source change is picked up automatically instead
of going stale (D107).

Why this exists
---------------
wahapedia_transform.py carries SUBFACTION_KEYWORD_ARMY: a sub-faction keyword
that belongs to exactly one owning chapter (Deathwing, Ravenwing -> Dark Angels).
When a datasheet carries one of those keywords but resolves to the generic
Adeptus Astartes army rather than the owning chapter, the transform strips it,
because the generic record is one shared object that every chapter's roster
unions in at selection time -- leaving Deathwing on it would hand an Ultramarines
list a DEATHWING Terminator Squad.

The strip is correct for the generic pool and wrong for the owning chapter.
Confirmed against the held army-composition sources, not inferred: the generic
Space Marines composition carries zero Deathwing/Ravenwing keyword rows, while
the Dark Angels composition carries the keyword on every one of the units this
script tags. Black Templars and Space Wolves compositions carry zero, matching
the one-chapter shape of SUBFACTION_KEYWORD_ARMY.

So the restoration cannot live on the shared record's own keyword_names. It is
emitted as a per-army map instead, structurally the mirror of
add_chapter_point_overrides.py's chapter_point_overrides:

    "chapter_keyword_additions": {
        "<Chapter Army Name>": ["<Keyword>", ...]
    }

Only units that actually gain at least one keyword get the field at all -- it is
never defaulted onto the rest of the generic pool.

Consumption is a separate (engine) ticket. Until that ships this field is inert
data: nothing reads it, and units.json's behaviour is unchanged.

Derivation
----------
The map is the exact inverse of the transform's own strip, re-derived from the
same three raw exports the transform reads (Datasheets_keywords.csv,
Datasheets.csv, Source.csv) and using the transform's own constants and its own
source_is_excluded() -- imported, never re-implemented, so an edit to
SUBFACTION_KEYWORD_ARMY, KNOWN_CHAPTERS or the exclusion rule cannot leave this
script disagreeing with the build it is post-processing.

A datasheet qualifies when all of the following hold:
  - it carries a SUBFACTION_KEYWORD_ARMY keyword as a non-faction, all-models
    keyword row (model-scoped rows are deliberately not handled: none exist
    today, and one appearing is a genuinely different shape that should fail
    loudly rather than be silently flattened onto the whole unit);
  - its source row is not excluded by the transform's own rule (Legends, Forge
    World, non-current edition);
  - its resolved army is the generic pool, not a chapter -- a chapter-owned
    datasheet keeps the keyword natively and needs no restoration;
  - a unit of that name is actually present in units.json's generic block.

Idempotent; part of the canonical units.json rebuild chain. Runs after
add_chapter_point_overrides.py, last step before the file is committed.
units_repro_check.py invokes it as the final step.

Usage:
  add_chapter_keyword_additions.py --units units.json --csv-dir .
"""
import argparse
import csv
import importlib.util
import json
import os
import sys

GENERIC_ARMY = "Adeptus Astartes"
ALLMODELS = {"", "ALL", "ALL MODELS"}


def _load_transform_module():
    """Import wahapedia_transform.py as a module so its constants and its
    exclusion rule are the single definition, shared with the real build."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "wahapedia_transform.py")
    if not os.path.exists(path):
        print(f"ERROR wahapedia_transform.py not found next to this script ({here})",
              file=sys.stderr)
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("wahapedia_transform", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="|"))


def derive_additions(wt, csv_dir):
    """Return {unit_name: {army_name: [keyword, ...]}} plus a flat row count."""
    ds_rows = _read_csv(os.path.join(csv_dir, "Datasheets.csv"))
    kw_rows = _read_csv(os.path.join(csv_dir, "Datasheets_keywords.csv"))
    src_rows = _read_csv(os.path.join(csv_dir, "Source.csv"))

    datasheets = {r["id"]: r for r in ds_rows}
    sources = {r["id"]: r for r in src_rows}

    # Resolved army per datasheet, by the transform's own rule: a single known
    # chapter faction keyword names the chapter, anything else is the generic pool.
    faction_kw = {}
    for r in kw_rows:
        if (r.get("is_faction_keyword") or "").strip().lower() == "true":
            faction_kw.setdefault(r["datasheet_id"], set()).add(r["keyword"])

    def army_of(ds_id):
        chapters = [k for k in faction_kw.get(ds_id, ()) if k in wt.KNOWN_CHAPTERS]
        return chapters[0] if chapters else GENERIC_ARMY

    additions = {}
    row_count = 0
    model_scoped = []
    for r in kw_rows:
        owner = wt.SUBFACTION_KEYWORD_ARMY.get(r["keyword"])
        if not owner:
            continue
        if (r.get("is_faction_keyword") or "").strip().lower() == "true":
            continue
        ds_id = r["datasheet_id"]
        d = datasheets.get(ds_id)
        if not d:
            continue
        src_row = sources.get(d.get("source_id"), {})
        if wt.source_is_excluded(src_row):
            continue
        if army_of(ds_id) != GENERIC_ARMY:
            continue
        if (r.get("model") or "").upper() not in ALLMODELS:
            model_scoped.append(f"{d['name']}: '{r['keyword']}' on model '{r['model']}'")
            continue
        by_army = additions.setdefault(d["name"], {})
        kws = by_army.setdefault(owner, [])
        if r["keyword"] not in kws:
            kws.append(r["keyword"])
            row_count += 1

    return additions, row_count, model_scoped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", required=True)
    ap.add_argument("--csv-dir", default=".")
    args = ap.parse_args()

    wt = _load_transform_module()
    additions, row_count, model_scoped = derive_additions(wt, args.csv_dir)

    if model_scoped:
        print("ERROR model-scoped sub-faction keyword row(s) found -- this script only "
              "handles all-models rows, and a model-scoped one is a different shape "
              "that must be designed, not flattened:", file=sys.stderr)
        for line in model_scoped:
            print(f"  {line}", file=sys.stderr)
        sys.exit(1)

    with open(args.units, encoding="utf-8") as f:
        units = json.load(f)

    generic = {}
    for army_block in units:
        if army_block.get("army") != GENERIC_ARMY:
            continue
        for unit in army_block.get("units", []):
            generic[unit.get("unit_name", "")] = unit

    # Idempotence: clear any previously-stamped field across every block before
    # re-stamping, so a unit that stops qualifying does not keep a stale map.
    for army_block in units:
        for unit in army_block.get("units", []):
            unit.pop("chapter_keyword_additions", None)

    touched = []
    skipped = []
    for name in sorted(additions):
        unit = generic.get(name)
        if unit is None:
            # A datasheet that qualifies in the raw export but is not in the built
            # generic block (not selected into any shipped faction) is not an error;
            # there is nothing to stamp. Reported so the count is never silent.
            skipped.append(name)
            continue
        by_army = {a: sorted(k) for a, k in sorted(additions[name].items())}
        unit["chapter_keyword_additions"] = by_army
        touched.append((unit.get("unit_id"), name, by_army))

    with open(args.units, "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2, ensure_ascii=False)

    per_army = {}
    for _uid, _name, by_army in touched:
        for a, kws in by_army.items():
            per_army[a] = per_army.get(a, 0) + len(kws)
    print(f"OK   {len(touched)} unit(s) tagged, {row_count} keyword-restoration row(s) "
          f"({', '.join(f'{k} {v}' for k, v in sorted(per_army.items())) or 'none'})"
          + (f"; {len(skipped)} qualifying datasheet(s) absent from the built generic "
             f"block: {', '.join(skipped)}" if skipped else ""))
    for uid, name, by_army in touched:
        detail = "; ".join(f"{a}: {', '.join(kws)}" for a, kws in by_army.items())
        print(f"  {uid}  {name}  <- {detail}")


if __name__ == "__main__":
    main()
