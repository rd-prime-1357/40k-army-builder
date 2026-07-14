#!/usr/bin/env python3
"""Emit per-datasheet Wargear ability text.

Source: Datasheets_abilities.csv, rows with type == 'Wargear'.
Output: datasheet_wargear_abilities.json  ->  { unit_id: { ability_name: description } }

Why this file exists (D105 / B15): weapon_abilities.json is keyed by ability NAME and
is therefore flattened across datasheets. 'Storm Shield' collapses to one string
("Wounds characteristic of 4" - the Terminator Assault Squad text) while the real
per-datasheet texts are three different things. Any name-keyed lookup of a conferred
characteristic is provably wrong. This file restores the datasheet key.

Restricted to the unit_ids present in units.json so the app payload stays small.

Usage:  python3 ds_wargear_abilities_parser.py --dir .
"""
import argparse
import json
import os

TYPE_COL = 'Wargear'


def load_unit_ids(path):
    ids = set()
    with open(path, encoding='utf-8') as fh:
        blocks = json.load(fh)
    for blk in blocks:
        for u in blk.get('units', []):
            if u.get('unit_id'):
                ids.add(u['unit_id'])
    return ids


def parse(csv_path, keep_ids):
    out = {}
    with open(csv_path, encoding='utf-8-sig') as fh:
        for line in fh:
            parts = line.rstrip('\r\n').split('|')
            # datasheet_id|line|ability_id|model|name|description|type|parameter|
            if len(parts) < 8:
                continue
            ds_id, name, desc, kind = parts[0], parts[4], parts[5], parts[6]
            if kind != TYPE_COL:
                continue
            if ds_id not in keep_ids:
                continue
            if not name or not desc:
                continue
            out.setdefault(ds_id, {})[name] = desc
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.')
    args = ap.parse_args()
    d = args.dir

    keep = load_unit_ids(os.path.join(d, 'units.json'))
    data = parse(os.path.join(d, 'Datasheets_abilities.csv'), keep)

    payload = {'_source': 'Datasheets_abilities.csv (type=Wargear)'}
    for k in sorted(data):
        payload[k] = {n: data[k][n] for n in sorted(data[k])}

    dest = os.path.join(d, 'datasheet_wargear_abilities.json')
    with open(dest, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write('\n')

    n_units = len(data)
    n_rows = sum(len(v) for v in data.values())
    print(f'{dest}: {n_units} datasheets, {n_rows} wargear ability rows')


if __name__ == '__main__':
    main()
