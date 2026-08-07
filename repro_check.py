#!/usr/bin/env python3
"""
repro_check.py — the executable form of "the parser is fresh."

Runs the real pipeline from source and asserts the result is byte-identical to the
committed unit_loadouts.json:

  1. Seed a working copy of unit_loadouts.json with ONLY the four hand-authored
     entries (000001157, 000001044, 000004131, 000002712) — the ones loadout_parser.py
     cannot regenerate.
  2. Run loadout_parser.py against source (Datasheets_options.csv + the roster
     units.json), which regenerates every other entry and preserves the two seeds.
  3. Run equipped_parser.py across the seven faction web.txt passes in order
     (SM -> DG -> BT -> DA -> SW -> CSM -> TS), then the final --datasheets Datasheets.csv pass.
  4. cmp the result against the committed unit_loadouts.json.

This does not care what the parser file is called or which functions it defines —
only whether the file on disk still produces what is committed. No wrong copy,
stale or partial, can pass it. It subsumes P1's old function-name check.

All work happens in a temp dir; nothing in the project directory is touched.

Usage:  python3 repro_check.py [--dir .]
Exit 0 on byte-identical reproduction, 1 otherwise.
Importable: repro(dir_) -> (ok, message).
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
from collections import OrderedDict

HAND_AUTHORED = ['000001157', '000001044', '000004131', '000002712',
                  '000004079', '000004080']
# 000004079/000004080 (Tormentors, Infractors) added S210 (Emperor's Children): both
# carry the single sentence "1 <unit name> can be equipped with 1 icon of excess." --
# the generic word "model" is replaced with the unit's own singular name, a sentence
# shape none of the 19 CLASSIFIERS match (classify_one_model_add hard-codes the literal
# word "model"). The emitted shape itself needs no new schema -- it's the same
# add + equipment + max_total:1 pattern already shipped for 000001044's Icon of Despair
# -- so this is authored directly rather than adding a 20th regex classifier for a
# two-unit sentence shape.
# 000002712 (Outrider Squad) added B59b/D184: its "Invader ATV" model group carries
# non_consuming + a literal MFM price_per_model, neither derivable from Wahapedia
# source (Datasheets_options.csv doesn't know MFM pricing or "does not consume the
# bracket") — same class of problem as 000004131 (D175).
# B100 (S206): Grey Knights added to FACTIONS. Needs no WEB_PASSES entry — its
# multi-group units gap-fill completely and correctly from the final --datasheets
# pass alone. B104 (S205) fixed the cross-faction scoped_name2id bug that blocked
# this; reverified clean against the fixed parser before this session's regen.
WEB_PASSES = ['Space_Marines', 'Death_Guard', 'Black_Templars', 'Dark_Angels', 'Space_Wolves', 'Chaos_Space_Marines', 'Thousand_Sons']
# B100/S210 (S209): Emperor's Children added to FACTIONS. Needs no WEB_PASSES entry --
# confirmed this session (not assumed from EMPEROR_S_CHILDREN_BUILD_SCOPE.md's dry run)
# that the real loadout_parser.py + equipped_parser.py --datasheets pass resolves every
# multi-group EC unit cleanly, mirroring the Grey Knights precedent exactly.
FACTIONS = ['SM', 'DG', 'CSM', 'TS', 'GK', 'EC']


def _run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


def repro(dir_):
    dir_ = os.path.abspath(dir_)
    committed = os.path.join(dir_, 'unit_loadouts.json')
    for req in ['loadout_parser.py', 'equipped_parser.py', 'units.json',
                'Datasheets_options.csv', 'Datasheets_unit_composition.csv',
                'Datasheets_models_cost.csv', 'Datasheets.csv', 'unit_loadouts.json',
                'weapon_abilities.json'] + [f'{f}_web.txt' for f in WEB_PASSES]:
        if not os.path.exists(os.path.join(dir_, req)):
            return False, f'missing pipeline input: {req}'

    full = json.load(open(committed), object_pairs_hook=OrderedDict)
    for hid in HAND_AUTHORED:
        if hid not in full:
            return False, f'hand-authored seed {hid} absent from committed unit_loadouts.json'

    tmp = tempfile.mkdtemp(prefix='repro_')
    try:
        # units.json must sit inside the --units-dir the parser reads.
        udir = os.path.join(tmp, 'work')
        os.makedirs(udir)
        shutil.copy(os.path.join(dir_, 'units.json'), os.path.join(udir, 'units.json'))
        # weapon_abilities.json is read next to --datasheets; run with cwd=dir_ so all
        # source paths resolve, and write only into tmp.
        seed = OrderedDict()
        seed['_schema'] = full.get('_schema')
        for hid in HAND_AUTHORED:
            seed[hid] = full[hid]
        seed_path = os.path.join(tmp, 'seed.json')
        json.dump(seed, open(seed_path, 'w'), indent=2, ensure_ascii=False)

        step = os.path.join(tmp, 'loadouts.json')
        rc, out = _run([sys.executable, 'loadout_parser.py',
                        '--options', 'Datasheets_options.csv',
                        '--units-dir', udir,
                        '--comp', 'Datasheets_unit_composition.csv',
                        '--cost', 'Datasheets_models_cost.csv',
                        '--datasheets', 'Datasheets.csv',
                        '--factions', *FACTIONS,
                        '--existing', seed_path,
                        '--out', step,
                        '--report', os.path.join(tmp, 'lo_report.md')], cwd=dir_)
        if rc != 0:
            return False, 'loadout_parser.py failed:\n' + out[-600:]

        for f in WEB_PASSES:
            rc, out = _run([sys.executable, 'equipped_parser.py',
                            '--composition', f'{f}_web.txt',
                            '--units', 'units.json',
                            '--loadouts', step,
                            '--out', step,
                            '--report', os.path.join(tmp, f'eq_{f}.md')], cwd=dir_)
            if rc != 0:
                return False, f'equipped_parser.py ({f}) failed:\n' + out[-600:]

        rc, out = _run([sys.executable, 'equipped_parser.py',
                        '--composition', os.devnull,
                        '--units', 'units.json',
                        '--loadouts', step,
                        '--out', step,
                        '--report', os.path.join(tmp, 'eq_ds.md'),
                        '--datasheets', 'Datasheets.csv'], cwd=dir_)
        if rc != 0:
            return False, 'equipped_parser.py (datasheets pass) failed:\n' + out[-600:]

        a = open(step, 'rb').read()
        b = open(committed, 'rb').read()
        if a == b:
            return True, 'pipeline reproduces committed unit_loadouts.json byte-for-byte'
        # Locate the divergence for a useful message.
        da = json.loads(a.decode('utf-8')); db = json.loads(b.decode('utf-8'))
        ka = set(da) - {'_schema'}; kb = set(db) - {'_schema'}
        if ka != kb:
            extra = sorted(ka - kb)[:5]; miss = sorted(kb - ka)[:5]
            return False, f'keyset differs — repro-only {extra}, committed-only {miss}'
        changed = [k for k in kb if da.get(k) != db.get(k)][:8]
        return False, f'{len(a)} vs {len(b)} bytes; first differing units: {changed}'
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.')
    a = ap.parse_args()
    ok, msg = repro(a.dir)
    print(('OK   ' if ok else 'FAIL ') + msg)
    sys.exit(0 if ok else 1)
