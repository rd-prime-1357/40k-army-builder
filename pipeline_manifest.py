#!/usr/bin/env python3
"""
pipeline_manifest.py — SHA-256 custody for every guarded pipeline file (D123).

WHY THIS FILE EXISTS, AND WHY IT KEPT NOT EXISTING
--------------------------------------------------
The manifest is the cheap first line the reproduction gates back up: it names the
file that arrived as the wrong copy, before anything spends minutes rebuilding
outputs to discover the same thing. Assertion P3 in rules_assertions.py imports
this module and calls check().

For many consecutive sessions this script was absent from the synced project
files while pipeline_manifest.json was present. That combination is the worst of
both: P3 failed unconditionally, so the manifest could not verify anything, and
it could not be regenerated either, so it silently went stale. By S123 thirteen
of its twenty-four hashes no longer matched the committed files. S123 refreshed
them; the refresh did not sync, and S124 opened with the pre-S123 manifest again.

Two consequences are designed around here:

1. The GUARDED SET LIVES IN THIS FILE, not in the JSON. If only the JSON survives
   a sync, the set of guarded files is still recoverable from source. If only this
   file survives, `--write` rebuilds the JSON from scratch.
2. `--write` FAILS LOUDLY on a missing file rather than quietly dropping it from
   the manifest. Silently shrinking the guarded set is how a manifest stops
   guarding the thing that actually broke.

Regenerating blesses whatever copy is present — that is what regeneration means.
Do it at session close, after the repro gates and assertions have passed, never
as a way of making a failure go away.

    python3 pipeline_manifest.py            # verify, exit 0 / 1
    python3 pipeline_manifest.py --write    # regenerate pipeline_manifest.json
    python3 pipeline_manifest.py --dir ..   # both, against another directory

M0 EXTENSION (P4/D231, S149) — FROM PIPELINE OUTPUTS TO THE WHOLE PUBLIC REPO
------------------------------------------------------------------------------
Originally this guarded only the 41 files a repro/gate run touches. The new
fetch-open (baseline.sh) pulls the *entire* public repo as one tarball and
needs to verify the whole tree came across intact before anything is
overlaid or gated — a corrupted or short fetch has to be caught here, before
any gate spends time on a tree that was never right to begin with. GUARDED
now lists every repo-resident file a session consumes (101 files); the four
files that are deliberately never guarded are documented at the end of the
list, with the reason each is excluded.

Adding a new session's handoff: append its filename to the list at session
close, same turn the handoff is written — the guarded set is append-only by
design (D-log precedent: prose claims drift, the list is the executable
record of what "the whole repo" means).
"""

import argparse, hashlib, json, os, sys

MANIFEST = 'pipeline_manifest.json'

NOTE = ('SHA-256 of every guarded pipeline file. Regenerated at session close '
        '(python3 pipeline_manifest.py --write). manifest_check verifies it at baseline; '
        'a mismatch names the file that arrived as the wrong copy.')

# The guarded set. Grouped by what each file is, so a future session adding a
# file knows where it belongs and why the group is guarded at all.
GUARDED = [
    # Deployed app + the data it loads at runtime.
    'index.html',
    'list_store.js',
    'units.json',
    'unit_loadouts.json',
    'wargear_points.json',
    'datasheet_wargear_abilities.json',
    'detachments.json',
    # Hand-authored input, not a pipeline output — no repro gate can regenerate it,
    # which is exactly why it needs the manifest. A bad sync of this file changes
    # legality silently (E21a, D209).
    'detachment_effects.json',

    # Parsers and transforms — the things the repro gates run.
    'loadout_parser.py',
    'equipped_parser.py',
    'wahapedia_transform.py',
    'mfm_points_parser.py',
    'convert_to_json.py',
    'merge_factions.py',
    'ds_wargear_abilities_parser.py',
    'mfm_reconcile.py',
    'add_loadout_groups.py',
    'detachment_parser.py',

    # The gates themselves. A tampered or stale gate is worse than no gate, so
    # the checkers are guarded on the same terms as the things they check.
    'rules_assertions.py',
    'repro_check.py',
    'units_repro_check.py',
    'detachments_repro_check.py',
    'integrity_check.py',
    'pipeline_manifest.py',

    # Build-time harnesses run at every session baseline.
    'pts_check.js',
    'stat_check.js',
    'bundle_check.js',
    'limit_check.js',
    'default_check.js',
    'pool_check.js',
    'e10_check.js',
    'b18d_check.js',
    'b31_check.js',
    'b56g_check.js',
    'b58_check.js',
    'required_size_check.js',
    'e1b_check.js',
    'e1c_check.js',
    'e4b_check.js',
    'e4c_check.js',
    'e21b_check.js',
    'e21c_check.js',
    'harness.js',
    'sweep.js',
    'baseline.sh',
    'repo_check.py',

    # Additional parsers/transforms (repo-only, same treatment as the group above).
    'add_bodyguard_stat_flags.py',
    'add_chapter_point_overrides.py',
    'add_co_leader.py',
    'build_cd_ability_details.py',
    'equipped_parser_B18c_banked.py',

    # Additional built data / fixtures (repo-only; not loaded at runtime by index.html
    # but consumed by parsers, gates, or fixtures above).
    'abilities.json',
    'rules.json',
    'weapon_abilities.json',
    'bundled_swaps.json',
    'core_glossary.json',
    'faction_taxonomy.json',
    'keywords.json',
    'B18c_repro_fixture.json',
    'B18d_fixture.json',

    # Reference docs and specs — repo-only, read by sessions as needed.
    '40K_Architecture_Overview_v0_5.md',
    '40K_Data_Dictionary_v2_0.md',
    '40K_Data_Pipeline_Process_v0_6.md',
    '40K_Decision_Log_v3_0.md',
    '40K_Functional_Spec_v0_7.md',
    'BACKLOG_ARCHIVE.md',
    'CSM_BUILD_SCOPE.md',
    'D231_entry.md',
    'DECISION_INDEX.md',
    'E1_DETACHMENT_SCOPE.md',
    'MFM_Chapter_Pass.md',
    'MFM_FW_Reconciliation.md',
    'MFM_Standalone_Pass.md',
    'OPEN_ITEMS_BACKLOG.md',
    'OUTPUT_FORMAT_SPEC_for_project_instructions.md',
    'P4_ARCHITECTURE_SCOPE.md',
    'PROCESS_IMPROVEMENT_PLAN.md',

    # The handoff chain — one entry per session, append-only. A new handoff file is
    # added to this list at the session that creates it (see write_addendum below).
    'SESSION_HANDOFF_125.md', 'SESSION_HANDOFF_126.md', 'SESSION_HANDOFF_127.md',
    'SESSION_HANDOFF_128.md', 'SESSION_HANDOFF_129.md', 'SESSION_HANDOFF_130.md',
    'SESSION_HANDOFF_131.md', 'SESSION_HANDOFF_132.md', 'SESSION_HANDOFF_133.md',
    'SESSION_HANDOFF_134.md', 'SESSION_HANDOFF_135.md', 'SESSION_HANDOFF_136.md',
    'SESSION_HANDOFF_137.md', 'SESSION_HANDOFF_138.md', 'SESSION_HANDOFF_139.md',
    'SESSION_HANDOFF_140.md', 'SESSION_HANDOFF_141.md', 'SESSION_HANDOFF_142.md',
    'SESSION_HANDOFF_143.md', 'SESSION_HANDOFF_144.md', 'SESSION_HANDOFF_145.md',
    'SESSION_HANDOFF_146.md', 'SESSION_HANDOFF_147.md', 'SESSION_HANDOFF_148.md',
]

# Never guarded, on purpose — not a gap, a documented exclusion (P4/M0, D231):
#   NEXT_SESSION_PROMPT.md — legitimately edited after the handoff/manifest that
#     covered it was finalized (D231). Verifying it against a pin can only ever
#     match by luck or false-alarm, exactly like the handoff hash list it was
#     dropped from. The fetch-open always overlays the area's live copy over
#     whatever the repo holds, unconditionally, without checking this manifest.
#   README.md, .gitignore, _headers — repo/hosting metadata; no session logic,
#     parser, gate, or harness reads these, so there is nothing to protect by
#     hashing them.
#   pipeline_manifest.json — the manifest cannot guard itself (build() writes it
#     from the state of every *other* guarded file).


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def build(d):
    """Hash every guarded file. Raises on any that is absent — a manifest that
    quietly omits a missing file is a manifest that stops guarding it."""
    missing = [f for f in GUARDED if not os.path.exists(os.path.join(d, f))]
    if missing:
        raise FileNotFoundError('cannot build the manifest, these guarded files are absent: '
                                + ', '.join(missing))
    return {f: sha256(os.path.join(d, f)) for f in GUARDED}


def write(d):
    files = build(d)
    payload = {'_note': NOTE, 'files': files}
    with open(os.path.join(d, MANIFEST), 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=1)
        f.write('\n')
    return len(files)


def check(d):
    """(ok, message). The shape rules_assertions.py's P3 expects.

    Three failure kinds, reported separately because they mean different things:
      absent    — a guarded file is not here at all
      mismatch  — the file is here but is a different copy than the one blessed
      unguarded — the file is here and is in GUARDED but not in the JSON, i.e.
                  the JSON is older than this script and needs regenerating
    """
    p = os.path.join(d, MANIFEST)
    if not os.path.exists(p):
        return False, f'{MANIFEST} not found — nothing to verify against'
    try:
        recorded = json.load(open(p, encoding='utf-8')).get('files', {})
    except Exception as e:
        return False, f'{MANIFEST} is unreadable: {type(e).__name__}: {e}'

    absent, mismatch = [], []
    for f, want in recorded.items():
        fp = os.path.join(d, f)
        if not os.path.exists(fp):
            absent.append(f)
        elif sha256(fp) != want:
            mismatch.append(f)

    unguarded = [f for f in GUARDED
                 if f not in recorded and os.path.exists(os.path.join(d, f))]
    stale_entries = [f for f in recorded if f not in GUARDED]

    problems = []
    if absent:
        problems.append(f'{len(absent)} guarded file(s) absent: ' + ', '.join(sorted(absent)))
    if mismatch:
        problems.append(f'{len(mismatch)} file(s) do not match the manifest: ' + ', '.join(sorted(mismatch)))
    if unguarded:
        problems.append(f'{len(unguarded)} file(s) in the guarded set are missing from '
                        f'{MANIFEST} — regenerate it: ' + ', '.join(sorted(unguarded)))
    if stale_entries:
        problems.append(f'{len(stale_entries)} manifest entry/entries are no longer in the '
                        f'guarded set: ' + ', '.join(sorted(stale_entries)))

    if problems:
        return False, '; '.join(problems)
    return True, f'{len(recorded)} guarded files all match'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.', help='directory holding the guarded files')
    ap.add_argument('--write', action='store_true', help='regenerate pipeline_manifest.json')
    a = ap.parse_args()

    if a.write:
        try:
            n = write(a.dir)
        except FileNotFoundError as e:
            print('FAIL ', e)
            return 1
        print(f'OK   wrote {MANIFEST} with {n} guarded files')
        return 0

    ok, msg = check(a.dir)
    print(('OK   ' if ok else 'FAIL ') + msg)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
