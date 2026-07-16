#!/usr/bin/env python3
"""
units_repro_check.py — the executable form of "units.json is fresh" (P4).

Runs the real per-faction pipeline from source and asserts the result is byte-identical
to the committed units.json:

  1. Space Marines: wahapedia_transform.py (--faction SM) -> mfm_points_parser.py ->
     convert_to_json.py, all in one working dir (out == in, matching the documented
     single-army-name command).
  2. Death Guard: wahapedia_transform.py (--faction DG) -> mfm_points_parser.py ->
     convert_to_json.py, in its own working dir.
  3. Chaos Daemons: convert_to_json.py run DIRECTLY against the project root's own
     Unit_Stats.csv / Unit_Points.csv / Unit_Wargear_Options.csv / Unit_Other_Options.csv /
     Unit_Weapons.csv / Unit_Abilities.csv / Keywords.csv / Rules.csv / Weapon_Abilities.csv.
     CD is Gen-1 hand-built data in Wahapedia-shaped CSVs; it is NEVER routed through
     wahapedia_transform.py — that script pulls the raw Wahapedia CD-faction dump instead,
     which includes ~21 CSM/cultist allied units that were never part of the shipped
     roster (see D132). Running wahapedia_transform.py --faction CD anywhere near this
     input directory would silently overwrite these same CSV filenames with the wrong
     source; this check never does that.
  4. merge_factions.py across the three outputs.
  5. cmp the merged result against the committed units.json.

All work happens in a temp dir; nothing in the project directory is touched.

Usage:  python3 units_repro_check.py [--dir .]
Exit 0 on byte-identical reproduction, 1 otherwise.
Importable: repro(dir_) -> (ok, message).
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

CD_ROOT_CSVS = [
    'Unit_Stats.csv', 'Unit_Points.csv', 'Unit_Wargear_Options.csv',
    'Unit_Other_Options.csv', 'Unit_Weapons.csv', 'Unit_Abilities.csv',
    'Keywords.csv', 'Rules.csv', 'Weapon_Abilities.csv',
]

REQUIRED = [
    'wahapedia_transform.py', 'mfm_points_parser.py', 'convert_to_json.py',
    'merge_factions.py', 'units.json', 'bundled_swaps.json', 'faction_taxonomy.json',
    'MFM_Space_Marines_v1_0.txt', 'MFM_Death_Guard_v1_0.txt',
] + CD_ROOT_CSVS


def _run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


def repro(dir_):
    dir_ = os.path.abspath(dir_)
    committed = os.path.join(dir_, 'units.json')
    for req in REQUIRED:
        if not os.path.exists(os.path.join(dir_, req)):
            return False, f'missing pipeline input: {req}'

    tmp = tempfile.mkdtemp(prefix='units_repro_')
    try:
        # --- Space Marines: transform -> mfm points -> convert (out dir doubles as in dir) ---
        sm_dir = os.path.join(tmp, 'sm')
        os.makedirs(sm_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', sm_dir, '--faction', 'SM',
                        '--army-name', 'Adeptus Astartes'], cwd=dir_)
        if rc != 0:
            return False, 'wahapedia_transform.py (SM) failed:\n' + out[-600:]
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_Space_Marines_v1_0.txt',
                        '--out-dir', sm_dir, '--stats', os.path.join(sm_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (SM) failed:\n' + out[-600:]
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', sm_dir, '--output-dir', sm_dir,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json')], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (SM) failed:\n' + out[-600:]

        # --- Death Guard: transform -> mfm points -> convert ---
        dg_dir = os.path.join(tmp, 'dg')
        os.makedirs(dg_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', dg_dir, '--faction', 'DG',
                        '--army-name', 'Death Guard'], cwd=dir_)
        if rc != 0:
            return False, 'wahapedia_transform.py (DG) failed:\n' + out[-600:]
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_Death_Guard_v1_0.txt',
                        '--out-dir', dg_dir, '--stats', os.path.join(dg_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (DG) failed:\n' + out[-600:]
        dg_json = os.path.join(tmp, 'dg_json')
        os.makedirs(dg_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', dg_dir, '--output-dir', dg_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json')], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (DG) failed:\n' + out[-600:]

        # --- Chaos Daemons: convert DIRECTLY off the project root's own CSVs. ---
        # No wahapedia_transform.py call here, ever — see module docstring / D132.
        cd_json = os.path.join(tmp, 'cd_json')
        os.makedirs(cd_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', dir_, '--output-dir', cd_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json')], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (CD) failed:\n' + out[-600:]

        # --- Merge ---
        deploy = os.path.join(tmp, 'deploy')
        os.makedirs(deploy)
        rc, out = _run([sys.executable, 'merge_factions.py',
                        '--in', sm_dir, '--in', cd_json, '--in', dg_json,
                        '--taxonomy', 'faction_taxonomy.json',
                        '--out-dir', deploy], cwd=dir_)
        if rc != 0:
            return False, 'merge_factions.py failed:\n' + out[-600:]

        rebuilt_path = os.path.join(deploy, 'units.json')
        a = open(rebuilt_path, 'rb').read()
        b = open(committed, 'rb').read()
        if a == b:
            return True, 'pipeline reproduces committed units.json byte-for-byte'

        ra = json.loads(a.decode('utf-8')); rb = json.loads(b.decode('utf-8'))
        def flat(d):
            out = {}
            for blk in d:
                for u in blk['units']:
                    out[u['unit_id']] = u
            return out
        fa, fb = flat(ra), flat(rb)
        if set(fa) != set(fb):
            extra = sorted(set(fa) - set(fb))[:5]
            miss = sorted(set(fb) - set(fa))[:5]
            return False, f'unit_id sets differ — repro-only {extra}, committed-only {miss}'
        changed = [uid for uid in fb if json.dumps(fa[uid], sort_keys=True, ensure_ascii=False)
                   != json.dumps(fb[uid], sort_keys=True, ensure_ascii=False)][:8]
        return False, f'{len(a)} vs {len(b)} bytes; first differing unit_ids: {changed}'
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.')
    a = ap.parse_args()
    ok, msg = repro(a.dir)
    print(('OK   ' if ok else 'FAIL ') + msg)
    sys.exit(0 if ok else 1)
