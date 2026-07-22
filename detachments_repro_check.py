#!/usr/bin/env python3
"""
detachments_repro_check.py — the executable form of "detachments.json is fresh" (P5).

The third byte-identical gate, alongside repro_check.py (unit_loadouts.json) and
units_repro_check.py (units.json and the four merged lookups).

Runs detachment_parser.py from source into a temp dir and demands the result match
the committed detachments.json byte for byte. A stale, partial or hand-edited copy
cannot pass. Nothing in the project directory is touched.

detachments.json is a first-generation file: it has no earlier committed version to
reproduce, so the fixed point is established at first generation and this gate is what
holds it from then on.

Usage:  python3 detachments_repro_check.py [--dir .]
Exit 0 on byte-identical reproduction, 1 otherwise.
Importable: repro(dir_) -> (ok, message).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

REQUIRED = [
    'detachment_parser.py',
    'detachments.json',
    # Numbers and structure. MFM wins on DP, points, force disposition, Unique tag
    # and which enhancements exist; these eight files are the source of record.
    'MFM_Space_Marines_v1_0.txt', 'MFM_Black_Templars_v1_0.txt',
    'MFM_Blood_Angels_v1_0.txt', 'MFM_Dark_Angels_v1_0.txt',
    'MFM_Death_Watch_v1_0.txt', 'MFM_Space_Wolves_v1_0.txt',
    'MFM_Chaos_Daemons_v1_0.txt', 'MFM_Death_Guard_v1_0.txt',
    # Tier-1 prose.
    'Space_Marines_Faction_Pack_v1_0.md',
    'Dark_Angels_Faction_Pack_June_2026.md',
    'chaos_daemons_reference.md',
    # Tier-2 prose.
    'Detachments.csv', 'Detachment_abilities.csv', 'Enhancements.csv', 'Stratagems.csv',
    # Army keying.
    'faction_taxonomy.json',
]


def repro(dir_):
    dir_ = os.path.abspath(dir_)
    committed = os.path.join(dir_, 'detachments.json')
    for req in REQUIRED:
        if not os.path.exists(os.path.join(dir_, req)):
            return False, f'missing detachment pipeline input: {req}'

    tmp = tempfile.mkdtemp(prefix='detach_repro_')
    try:
        rebuilt = os.path.join(tmp, 'detachments.json')
        r = subprocess.run(
            [sys.executable, 'detachment_parser.py', '--root', dir_, '--out', rebuilt],
            cwd=dir_, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if r.returncode != 0:
            return False, ('detachment_parser.py failed:\n'
                           + r.stdout.decode('utf-8', 'replace')[-800:])
        a = open(rebuilt, 'rb').read()
        b = open(committed, 'rb').read()
        if a == b:
            return True, 'pipeline reproduces committed detachments.json byte-for-byte'
        return False, (f'detachments.json differs from a fresh parser run '
                       f'(rebuilt {len(a)} bytes, committed {len(b)} bytes) — '
                       f'the committed file is stale or was hand-edited')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dir', default='.')
    a = ap.parse_args()
    ok, msg = repro(a.dir)
    print(('OK   ' if ok else 'FAIL ') + msg)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
