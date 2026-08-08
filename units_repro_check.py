#!/usr/bin/env python3
"""
units_repro_check.py — the executable form of "units.json is fresh" (P4).

Runs the real per-faction pipeline from source and asserts the result is byte-identical
to the committed units.json:

  1. Space Marines: wahapedia_transform.py (--faction SM) -> mfm_points_parser.py ->
     convert_to_json.py, all in one working dir (out == in, matching the documented
     single-army-name command).
  2. Death Guard: wahapedia_transform.py (--faction DG) -> mfm_points_parser.py
     (against MFM_Death_Guard_v1.1.txt, B94/B89's second MFM v1.1 migration, S196/D289)
     -> convert_to_json.py --emit-fourth-plus, in its own working dir. Fully self-sourced
     (41/41, no cross-file append, no chapter points).
  3. Thousand Sons: wahapedia_transform.py (--faction TS) -> mfm_points_parser.py
     (against MFM_Thousand_Sons_v1.1.txt, B94/B89's first MFM v1.1 migration, S195/D288)
     -> convert_to_json.py --emit-fourth-plus, in its own working dir. Fully self-sourced
     (34/34, no cross-file append, no chapter points) — mirrors the Death Guard block
     exactly (THOUSAND_SONS_BUILD_SCOPE.md §4/§8). The six Scintillating Legions carrier
     units get their allied_group tag automatically from the MFM file's own section
     header, the same generic ALLIED_GROUP_HEADERS mechanism Death Guard's Plague
     Legions tag uses (D208) — confirmed unchanged under v1.1's layout, no TS-specific
     tagging code needed here.
  4. Grey Knights: wahapedia_transform.py (--faction GK) -> mfm_points_parser.py (against
     MFM_Grey_Knights_v1.1.txt, per D293's standing rule to always build from the newest
     MFM) -> convert_to_json.py --emit-fourth-plus, in its own working dir. Fully
     self-sourced (25/25, no cross-file append, no chapter points) — mirrors the Death
     Guard and Thousand Sons blocks exactly (GREY_KNIGHTS_BUILD_SCOPE.md §3/§4). No
     dedicated faction composition-paste file needed: confirmed this session (not
     assumed) that the six multi-group units (Strike Squad, Brotherhood Terminator
     Squad, Purifier Squad, Paladin Squad, Interceptor Squad, Purgation Squad) gap-fill
     completely and correctly from Datasheets.csv alone in equipped_parser.py's final
     --datasheets pass, since each one's groups carry identical default gear per the
     datasheet's own "Every model is equipped with" wording — not a parser gap, so
     repro_check.py's WEB_PASSES list does not need a Grey Knights entry either.
  4b. Emperor's Children: wahapedia_transform.py (--faction EC) -> mfm_points_parser.py
     (against MFM_Emperors_Children_v1.1.txt, D293) -> convert_to_json.py
     --emit-fourth-plus, in its own working dir. Fully self-sourced (23/23, zero LEGENDS
     exclusions, no cross-file append, no chapter points) — mirrors the Grey Knights
     block exactly (EMPEROR_S_CHILDREN_BUILD_SCOPE.md). No dedicated composition-paste
     file needed: confirmed this session (S210) that the real loadout_parser.py run
     resolves every multi-group unit's options cleanly from Datasheets.csv alone, so
     repro_check.py's WEB_PASSES list needs no Emperor's Children entry either.
  4c. World Eaters: wahapedia_transform.py (--faction WE) -> mfm_points_parser.py
     (against MFM_World_Eaters_v1.1.txt, D293) -> convert_to_json.py --emit-fourth-plus,
     in its own working dir. Fully self-sourced (30/30, 28 LEGENDS exclusions confirmed
     both directions, no cross-file append, no chapter points) — mirrors the Grey
     Knights/Emperor's Children blocks exactly (WORLD_EATERS_BUILD_SCOPE.md §1/§6). The
     five Blood Legions carrier units get their allied_group tag automatically from the
     MFM file's own section header, the same generic ALLIED_GROUP_HEADERS mechanism
     Death Guard's Plague Legions and Thousand Sons' Scintillating Legions use — no
     World Eaters-specific tagging code needed. No dedicated composition-paste file
     needed: `loadout_parser.py --factions WE` flagged exactly 2 of 30 (Jakhals,
     Helbrute), both authored directly into `unit_loadouts.json`'s HAND_AUTHORED set
     (repro_check.py) rather than needing a WEB_PASSES entry.
  5. Chaos Daemons: convert_to_json.py run DIRECTLY against the project root's own
     Unit_Stats.csv / Unit_Points.csv / Unit_Wargear_Options.csv / Unit_Other_Options.csv /
     Unit_Weapons.csv / Unit_Abilities.csv / Keywords.csv / Rules.csv / Weapon_Abilities.csv.
     CD is Gen-1 hand-built data in Wahapedia-shaped CSVs; it is NEVER routed through
     wahapedia_transform.py — that script pulls the raw Wahapedia CD-faction dump instead,
     which includes ~21 CSM/cultist allied units that were never part of the shipped
     roster (see D132). Running wahapedia_transform.py --faction CD anywhere near this
     input directory would silently overwrite these same CSV filenames with the wrong
     source; this check never does that.
  6. merge_factions.py across the five outputs.
  7. cmp the merged result against the committed units.json.

All work happens in a temp dir; nothing in the project directory is touched.

Usage:  python3 units_repro_check.py [--dir .]
Exit 0 on byte-identical reproduction, 1 otherwise.
Importable: repro(dir_) -> (ok, message).
"""
import argparse, csv, json, os, shutil, subprocess, sys, tempfile

CD_ROOT_CSVS = [
    'Unit_Stats.csv', 'Unit_Points.csv', 'Unit_Wargear_Options.csv',
    'Unit_Other_Options.csv', 'Unit_Weapons.csv', 'Unit_Abilities.csv',
    'Keywords.csv', 'Rules.csv', 'Weapon_Abilities.csv',
]

# The four glossary lookups merge_factions.py unions alongside units.json, plus the
# taxonomy pass-through. Same run, same fixed point (B55 / D164).
LOOKUPS = [
    ('abilities.json', 'ability_name'),
    ('rules.json', 'rule_name'),
    ('keywords.json', 'keyword_name'),
    ('weapon_abilities.json', 'weapon_ability_name'),
    ('faction_taxonomy.json', None),
]

REQUIRED = [
    'wahapedia_transform.py', 'mfm_points_parser.py', 'convert_to_json.py',
    'merge_factions.py', 'add_loadout_groups.py', 'add_co_leader.py',
    'add_bodyguard_stat_flags.py', 'add_chapter_point_overrides.py',
    'units.json', 'unit_loadouts.json',
    'bundled_swaps.json', 'faction_taxonomy.json',
    'MFM_Space_Marines_v1.1.txt',
    # B94/B89 (S195, D288): Thousand Sons migrated to its v1.1 source. v1_0 stays
    # REQUIRED too — CSM's cult-troop cross-legion pricing (CSM_CULT_TROOP_POINTS
    # below) still prices Rubric Marines' CSM-army datasheet off TS's v1_0 file
    # until CSM's own B89 turn migrates it.
    'MFM_Thousand_Sons_v1.1.txt',
    # B94/B89 (S196, D289): Death Guard migrated to its v1.1 source. v1_0 stays
    # REQUIRED too — CSM's cult-troop cross-legion pricing (CSM_CULT_TROOP_POINTS
    # below) still prices Plague Marines' CSM-army datasheet off DG's v1_0 file
    # until CSM's own B89 turn migrates it.
    'MFM_Death_Guard_v1.1.txt',
    # B100 (S204): Grey Knights, built directly from v1.1 per D293 — the first faction
    # with no v1_0 migration debt, since it is the first one built after D293 was set.
    'MFM_Grey_Knights_v1.1.txt',
    # B100 (S209): Emperor's Children, built directly from v1.1 per D293.
    'MFM_Emperors_Children_v1.1.txt',
    # B100 (S218): World Eaters, built directly from v1.1 per D293.
    'MFM_World_Eaters_v1.1.txt',
    # B56a: the five Space Marines chapter point files. Correctly-scoped, they are
    # purely additive on top of the base SM run (D167/D168) and sit inside the fixed
    # point from here on — this is exactly the kind of input that goes stale silently
    # if it is outside the gate (D107).
    # B89/S198 (D291): migrated to v1.1 together with the base SM file — the chapter
    # override mechanism (add_chapter_point_overrides.py) compares each chapter's
    # shared-unit prices against the current generic Adeptus Astartes price, so base
    # and all five chapters must move as one atomic group or the comparison is
    # version-mismatched. See D291 for the full chaining analysis.
    'MFM_Space_Wolves_v1.1.txt', 'MFM_Blood_Angels_v1.1.txt',
    'MFM_Black_Templars_v1.1.txt', 'MFM_Dark_Angels_v1.1.txt',
    'MFM_Death_Watch_v1.1.txt',
    # D229 / S147 turn A: CSM's own MFM. Prices 54 of CSM's 58 current-edition
    # datasheets; the four cult-troop units (Khorne Berzerkers, Rubric Marines,
    # Plague Marines, Noise Marines) are priced in their god-legion's own MFM and
    # are deliberately withheld from this run — see CSM_CULT_TROOP_IDS below.
    'MFM_Chaos_Space_Marines_v1_0.txt',
    # D240 (S147 turn B): the four sibling-legion MFMs the cult-troop points come from.
    'MFM_World_Eaters_v1_0.txt', 'MFM_Death_Guard_v1_0.txt',
    'MFM_Thousand_Sons_v1_0.txt', 'MFM_Emperors_Children_v1_0.txt',
] + CD_ROOT_CSVS

# D229 (S147 turn A) / D240 (S147 turn B). These four CSM datasheets carry no cost in
# the CSM MFM — GW prices them once, in their parent god-legion's own MFM. Turn A
# shipped only the 54 units the CSM MFM prices on its own (these four filtered out of
# Unit_Stats.csv before pointing/converting, to keep b56a_residual_nulls from tripping
# on unpriced rows). Turn B (below) prices them properly via --scope-to-army --append
# against each unit's own legion MFM, one unit at a time, each isolated to a
# single-row Unit_Stats.csv via _scope_stats_csv — see that function's docstring for
# why the full 58-row CSM stats block can't be used here.
CSM_CULT_TROOP_POINTS = [
    ('000003582', 'MFM_World_Eaters_v1_0.txt'),      # Khorne Berzerkers
    ('000003584', 'MFM_Death_Guard_v1_0.txt'),        # Plague Marines
    ('000003583', 'MFM_Thousand_Sons_v1_0.txt'),      # Rubric Marines
    ('000004099', 'MFM_Emperors_Children_v1_0.txt'),  # Noise Marines
]


def _filter_stats_csv(path, exclude_ids):
    """Drop rows whose Datasheet ID is in exclude_ids, in place. CRLF, utf-8-sig,
    matching the transform's own output convention."""
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    header = rows[0]
    di = header.index('Datasheet ID')
    kept = [header] + [r for r in rows[1:] if r[di] not in exclude_ids]
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, lineterminator='\r\n')
        w.writerows(kept)


def _scope_stats_csv(src_path, out_path, include_ids):
    """D240 (S147 turn B): write a Unit_Stats.csv containing ONLY the rows whose
    Datasheet ID is in include_ids. Isolates a single cult-troop unit as the --stats
    input for one --scope-to-army --append call, so that call can only ever match
    that one name against the sibling legion's MFM — never any of CSM's other 54
    already-priced units. Several of those (Chaos Rhino, Helbrute, Defiler, etc.)
    are generic Chaos vehicles also separately priced in every god-legion's own MFM;
    passing the full CSM stats block here would let those names resolve in scope and
    get silently overridden by append mode's same-key-wins rule. This file exists to
    make that unreachable."""
    with open(src_path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    header = rows[0]
    di = header.index('Datasheet ID')
    kept = [header] + [r for r in rows[1:] if r[di] in include_ids]
    with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, lineterminator='\r\n')
        w.writerows(kept)

# B56a: chapter file -> the Army Name its own Unit_Stats.csv rows carry.
# B89/S198 (D291): v1.1.
CHAPTER_POINTS = [
    ('MFM_Space_Wolves_v1.1.txt', 'Space Wolves'),
    ('MFM_Blood_Angels_v1.1.txt', 'Blood Angels'),
    ('MFM_Black_Templars_v1.1.txt', 'Black Templars'),
    ('MFM_Dark_Angels_v1.1.txt', 'Dark Angels'),
    ('MFM_Death_Watch_v1.1.txt', 'Deathwatch'),
]


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
                        '--mfm', 'MFM_Space_Marines_v1.1.txt',
                        '--out-dir', sm_dir, '--stats', os.path.join(sm_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (SM) failed:\n' + out[-600:]

        # --- B56a: chapter points, scoped and additive, before convert_to_json.py ---
        for mfm_file, army in CHAPTER_POINTS:
            rc, out = _run([sys.executable, 'mfm_points_parser.py',
                            '--mfm', mfm_file, '--army', army, '--scope-to-army', '--append',
                            '--out-dir', sm_dir, '--stats', os.path.join(sm_dir, 'Unit_Stats.csv')],
                            cwd=dir_)
            if rc != 0:
                return False, f'mfm_points_parser.py ({army}) failed:\n' + out[-600:]

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
                        '--mfm', 'MFM_Death_Guard_v1.1.txt',
                        '--out-dir', dg_dir, '--stats', os.path.join(dg_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (DG) failed:\n' + out[-600:]
        dg_json = os.path.join(tmp, 'dg_json')
        os.makedirs(dg_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', dg_dir, '--output-dir', dg_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json'),
                        '--emit-fourth-plus'], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (DG) failed:\n' + out[-600:]

        # --- Thousand Sons: transform -> mfm points -> convert. Fully self-sourced,
        # 34/34 (THOUSAND_SONS_BUILD_SCOPE.md §4) — no chapter points, no cross-file
        # cult-troop append. Mirrors the Death Guard block exactly. ---
        ts_dir = os.path.join(tmp, 'ts')
        os.makedirs(ts_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', ts_dir, '--faction', 'TS',
                        '--army-name', 'Thousand Sons'], cwd=dir_)
        if rc != 0:
            return False, 'wahapedia_transform.py (TS) failed:\n' + out[-600:]
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_Thousand_Sons_v1.1.txt',
                        '--out-dir', ts_dir, '--stats', os.path.join(ts_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (TS) failed:\n' + out[-600:]
        ts_json = os.path.join(tmp, 'ts_json')
        os.makedirs(ts_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', ts_dir, '--output-dir', ts_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json'),
                        '--emit-fourth-plus'], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (TS) failed:\n' + out[-600:]

        # --- Grey Knights: transform -> mfm points -> convert. Fully self-sourced,
        # 25/25 (GREY_KNIGHTS_BUILD_SCOPE.md §3) — no chapter points, no cross-file
        # append. Built straight from v1.1 (D293); mirrors the Death Guard/Thousand
        # Sons blocks exactly. ---
        gk_dir = os.path.join(tmp, 'gk')
        os.makedirs(gk_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', gk_dir, '--faction', 'GK',
                        '--army-name', 'Grey Knights'], cwd=dir_)
        if rc != 0:
            return False, 'wahapedia_transform.py (GK) failed:\n' + out[-600:]
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_Grey_Knights_v1.1.txt',
                        '--out-dir', gk_dir, '--stats', os.path.join(gk_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (GK) failed:\n' + out[-600:]
        gk_json = os.path.join(tmp, 'gk_json')
        os.makedirs(gk_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', gk_dir, '--output-dir', gk_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json'),
                        '--emit-fourth-plus'], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (GK) failed:\n' + out[-600:]

        # --- Emperor's Children: transform -> mfm points -> convert. Fully self-sourced,
        # 23/23 (EMPEROR_S_CHILDREN_BUILD_SCOPE.md), zero LEGENDS exclusions, zero engine
        # gaps -- the first faction where scoping found none. Mirrors the Death Guard/
        # Thousand Sons/Grey Knights blocks exactly. ---
        ec_dir = os.path.join(tmp, 'ec')
        os.makedirs(ec_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', ec_dir, '--faction', 'EC',
                        '--army-name', "Emperor's Children"], cwd=dir_)
        if rc != 0:
            return False, "wahapedia_transform.py (EC) failed:\n" + out[-600:]
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_Emperors_Children_v1.1.txt',
                        '--out-dir', ec_dir, '--stats', os.path.join(ec_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, "mfm_points_parser.py (EC) failed:\n" + out[-600:]
        ec_json = os.path.join(tmp, 'ec_json')
        os.makedirs(ec_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', ec_dir, '--output-dir', ec_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json'),
                        '--emit-fourth-plus'], cwd=dir_)
        if rc != 0:
            return False, "convert_to_json.py (EC) failed:\n" + out[-600:]

        # --- World Eaters: transform -> mfm points -> convert. Fully self-sourced,
        # 30/30 (WORLD_EATERS_BUILD_SCOPE.md §1/§6), 28 LEGENDS exclusions confirmed
        # both directions, zero engine gaps. Mirrors the Grey Knights/Emperor's
        # Children blocks exactly. ---
        we_dir = os.path.join(tmp, 'we')
        os.makedirs(we_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', we_dir, '--faction', 'WE',
                        '--army-name', 'World Eaters'], cwd=dir_)
        if rc != 0:
            return False, 'wahapedia_transform.py (WE) failed:\n' + out[-600:]
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_World_Eaters_v1.1.txt',
                        '--out-dir', we_dir, '--stats', os.path.join(we_dir, 'Unit_Stats.csv')],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (WE) failed:\n' + out[-600:]
        we_json = os.path.join(tmp, 'we_json')
        os.makedirs(we_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', we_dir, '--output-dir', we_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json'),
                        '--emit-fourth-plus'], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (WE) failed:\n' + out[-600:]

        # --- Chaos Space Marines: transform -> mfm points (self, 54 of 58) -> D240
        # cult-troop cross-file append (the remaining 4, one at a time, each isolated
        # to its own single-row stats scope) -> convert. Unit_Stats.csv is left
        # unfiltered now (turn A's exclusion is gone): the four cult-troop datasheets
        # carry real stat rows from Wahapedia regardless of MFM pricing, so nothing
        # needs hiding from convert_to_json.py once all 58 are priced. ---
        csm_dir = os.path.join(tmp, 'csm')
        os.makedirs(csm_dir)
        rc, out = _run([sys.executable, 'wahapedia_transform.py',
                        '--wahapedia-dir', dir_, '--seed-dir', dir_,
                        '--out-dir', csm_dir, '--faction', 'CSM',
                        '--army-name', 'Chaos Space Marines'], cwd=dir_)
        if rc != 0:
            return False, 'wahapedia_transform.py (CSM) failed:\n' + out[-600:]
        csm_stats = os.path.join(csm_dir, 'Unit_Stats.csv')
        rc, out = _run([sys.executable, 'mfm_points_parser.py',
                        '--mfm', 'MFM_Chaos_Space_Marines_v1_0.txt',
                        '--out-dir', csm_dir, '--stats', csm_stats],
                        cwd=dir_)
        if rc != 0:
            return False, 'mfm_points_parser.py (CSM) failed:\n' + out[-600:]
        for ds_id, mfm_file in CSM_CULT_TROOP_POINTS:
            scoped_stats = os.path.join(csm_dir, f'_cult_troop_{ds_id}.csv')
            _scope_stats_csv(csm_stats, scoped_stats, {ds_id})
            rc, out = _run([sys.executable, 'mfm_points_parser.py',
                            '--mfm', mfm_file, '--army', 'Chaos Space Marines',
                            '--scope-to-army', '--append',
                            '--out-dir', csm_dir, '--stats', scoped_stats], cwd=dir_)
            if rc != 0:
                return False, f'mfm_points_parser.py (CSM cult troop {ds_id}) failed:\n' + out[-600:]
        csm_json = os.path.join(tmp, 'csm_json')
        os.makedirs(csm_json)
        rc, out = _run([sys.executable, 'convert_to_json.py',
                        '--input-dir', csm_dir, '--output-dir', csm_json,
                        '--bundles', os.path.join(dir_, 'bundled_swaps.json')], cwd=dir_)
        if rc != 0:
            return False, 'convert_to_json.py (CSM) failed:\n' + out[-600:]

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
                        '--in', sm_dir, '--in', cd_json, '--in', dg_json, '--in', csm_json,
                        '--in', ts_json, '--in', gk_json, '--in', ec_json, '--in', we_json,
                        '--taxonomy', 'faction_taxonomy.json',
                        '--out-dir', deploy], cwd=dir_)
        if rc != 0:
            return False, 'merge_factions.py failed:\n' + out[-600:]

        # --- B44 (D135): tag statline groups with their loadout_groups shared key ---
        rc, out = _run([sys.executable, 'add_loadout_groups.py',
                        '--units', os.path.join(deploy, 'units.json'),
                        '--loadouts', os.path.join(dir_, 'unit_loadouts.json')], cwd=dir_)
        if rc != 0:
            return False, 'add_loadout_groups.py failed:\n' + out[-600:]

        # --- B38a (D143/D144): set co_leader_eligible_with on the 12 SM named-shape units ---
        rc, out = _run([sys.executable, 'add_co_leader.py',
                        '--units', os.path.join(deploy, 'units.json')], cwd=dir_)
        if rc != 0:
            return False, 'add_co_leader.py failed:\n' + out[-600:]

        # --- B7b (D157/D159): populate bodyguard_stat_flags for leader-aura markers ---
        rc, out = _run([sys.executable, 'add_bodyguard_stat_flags.py',
                        '--units', os.path.join(deploy, 'units.json')], cwd=dir_)
        if rc != 0:
            return False, 'add_bodyguard_stat_flags.py failed:\n' + out[-600:]

        # --- B56c (D167/D169): derive and stamp the per-chapter points override
        # map onto the matching generic (Adeptus Astartes) units. Reads sm_dir's
        # own post-chapter-append Unit_Stats.csv / Unit_Points.csv (from the SM
        # build above) so it needs no extra transform step of its own. ---
        rc, out = _run([sys.executable, 'add_chapter_point_overrides.py',
                        '--units', os.path.join(deploy, 'units.json'),
                        '--stats', os.path.join(sm_dir, 'Unit_Stats.csv'),
                        '--points', os.path.join(sm_dir, 'Unit_Points.csv'),
                        '--mfm-dir', dir_], cwd=dir_)
        if rc != 0:
            return False, 'add_chapter_point_overrides.py failed:\n' + out[-600:]

        rebuilt_path = os.path.join(deploy, 'units.json')
        a = open(rebuilt_path, 'rb').read()
        b = open(committed, 'rb').read()
        if a == b:
            # units.json is fresh; the merged lookups ship from the same run, so they are
            # part of the same fixed point (B55 / D164). Any of them drifting is the same
            # class of failure and is reported here rather than left to prose.
            bad = []
            for fname, key in LOOKUPS:
                rp = os.path.join(deploy, fname)
                cp = os.path.join(dir_, fname)
                if not os.path.exists(cp):
                    bad.append(f'{fname}: missing from project dir')
                    continue
                ra_ = open(rp, 'rb').read()
                rb_ = open(cp, 'rb').read()
                if ra_ == rb_:
                    continue
                if key is None:
                    bad.append(f'{fname}: differs ({len(ra_)} vs {len(rb_)} bytes)')
                    continue
                na = {r[key]: r for r in json.loads(ra_.decode('utf-8'))}
                nb = {r[key]: r for r in json.loads(rb_.decode('utf-8'))}
                add = sorted(set(na) - set(nb))
                lost = sorted(set(nb) - set(na))
                chg = sorted(k for k in set(na) & set(nb) if na[k] != nb[k])
                bad.append(f'{fname}: +{len(add)} rebuild-only, -{len(lost)} committed-only, '
                           f'{len(chg)} text changes (e.g. {(add + lost + chg)[:3]})')
            if bad:
                return False, 'units.json is fresh but merged lookups have drifted:\n  ' + \
                              '\n  '.join(bad)
            return True, ('pipeline reproduces committed units.json and all four merged '
                          'lookups byte-for-byte')

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
