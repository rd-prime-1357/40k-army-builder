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

CLOSE-TIME FRESHNESS CHECK (B81, S168)
---------------------------------------
D251's ordering rule — finish the decision log and handoff text, THEN run
`--write`, touching nothing after — depends on nobody editing either file
after the write. That has slipped three times (D239, and twice more folded
into D256) because nothing checked it; the drift was only ever caught by
the *next* session's baseline, after the wrong hash was already banked.

`--freshness-check` closes that gap. Run it as the last command of session
close, after `--write` and after any other file this turn touches:

    python3 pipeline_manifest.py --write
    python3 pipeline_manifest.py --freshness-check

It re-hashes only the decision log and the highest-numbered
`SESSION_HANDOFF_*.md` file present and compares each against what
`--write` just banked. A mismatch means one of those two files was touched
after the write — reissue the manifest and check again before delivering.
It does not replace `--write`; it verifies `--write` was truly last.

HANDOFF COVERAGE CHECK (S180)
------------------------------
`--freshness-check` catches a stale hash on the *latest* handoff, but S177-179
showed a different failure: three handoffs in a row were written and simply never
appended to GUARDED at all, so the plain `pipeline_manifest.py` gate — the one
baseline.sh runs every session — had nothing to check them against and stayed
green while they went completely unguarded for three sessions. The plain `check()`
run now also flags any `SESSION_HANDOFF_N.md` present on disk that GUARDED doesn't
list, so a forgotten append fails the very next session's baseline instead of
sitting silent until someone happens to run --freshness-check and reads the result.

Chose this over replacing the static per-filename list with discovery (e.g.
`latest_handoff`'s pattern applied to the whole set): GUARDED's `build()`
deliberately raises on a *missing* guarded file — that is the mechanism that
catches a handoff lost from the repo. Auto-discovering "whatever handoffs are
present" would guard files correctly but could never notice one going missing,
trading a real failure mode for the one this fixes. The static list stays; this
check makes forgetting to update it loud instead of silent.
"""

import argparse, hashlib, json, os, re, sys

MANIFEST = 'pipeline_manifest.json'
_HANDOFF_RE = re.compile(r'^SESSION_HANDOFF_(\d+)\.md$')

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
    'e25_check.js',
    'b71_check.js',
    'b72_check.js',
    'b90_check.js',
    'b87_check.js',
    'b88_check.js',
    'b101_check.js',
    'b106_check.js',
    'b99_check.js',
    'b119_check.js',
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
    '40K_Architecture_Overview.md',
    '40K_Data_Dictionary.md',
    '40K_Data_Pipeline_Process.md',
    '40K_Decision_Log.md',
    '40K_Functional_Spec.md',
    'BACKLOG_ARCHIVE.md',
    'CSM_BUILD_SCOPE.md',
    'DECISION_INDEX.md',
    'E1_DETACHMENT_SCOPE.md',
    'B99_SCOPE.md',
    'GREY_KNIGHTS_BUILD_SCOPE.md',
    # B121 (S237): six scope documents that were never added to GUARDED when they were
    # written. Each verified present in the repo before appending — a GUARDED entry for
    # an absent file turns this gate permanently red. Emperor's Children's filename
    # carries a literal apostrophe in the repo (the project-area mount silently
    # sanitises it to an underscore on upload); the apostrophe form is the real filename
    # and is what belongs here.
    'B113_LEADER_RESTRICTION_SCOPE.md',
    'B114_SHADOW_LEGION_SCOPE.md',
    'DRUKHARI_BUILD_SCOPE.md',
    "EMPEROR'S_CHILDREN_BUILD_SCOPE.md",
    'THOUSAND_SONS_BUILD_SCOPE.md',
    'WORLD_EATERS_BUILD_SCOPE.md',
    'MFM_Chapter_Pass.md',
    'MFM_FW_Reconciliation.md',
    'MFM_Standalone_Pass.md',
    'MFM_v1_1_Reconciliation.md',
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
    'SESSION_HANDOFF_149.md', 'SESSION_HANDOFF_150.md', 'SESSION_HANDOFF_151.md',
    'SESSION_HANDOFF_152.md', 'SESSION_HANDOFF_153.md', 'SESSION_HANDOFF_154.md',
    'SESSION_HANDOFF_155.md', 'SESSION_HANDOFF_156.md', 'SESSION_HANDOFF_157.md',
    'SESSION_HANDOFF_158.md', 'SESSION_HANDOFF_159.md', 'SESSION_HANDOFF_160.md',
    'SESSION_HANDOFF_161.md', 'SESSION_HANDOFF_162.md', 'SESSION_HANDOFF_163.md',
    'SESSION_HANDOFF_164.md',
    'SESSION_HANDOFF_165.md',
    'SESSION_HANDOFF_166.md',
    'SESSION_HANDOFF_167.md',
    'SESSION_HANDOFF_168.md',
    'SESSION_HANDOFF_169.md',
    'SESSION_HANDOFF_170.md',
    'SESSION_HANDOFF_171.md',
    'SESSION_HANDOFF_172.md',
    'SESSION_HANDOFF_173.md', 'SESSION_HANDOFF_174.md',
    'SESSION_HANDOFF_175.md', 'SESSION_HANDOFF_176.md',
    'SESSION_HANDOFF_177.md', 'SESSION_HANDOFF_178.md', 'SESSION_HANDOFF_179.md',
    'SESSION_HANDOFF_180.md',
    'SESSION_HANDOFF_181.md',
    'SESSION_HANDOFF_182.md',
    'SESSION_HANDOFF_183.md',
    'SESSION_HANDOFF_184.md',
    'SESSION_HANDOFF_185.md',
    'SESSION_HANDOFF_186.md',
    'SESSION_HANDOFF_187.md',
    'SESSION_HANDOFF_188.md',
    'SESSION_HANDOFF_189.md',
    'SESSION_HANDOFF_190.md',
    'SESSION_HANDOFF_191.md',
    'SESSION_HANDOFF_192.md',
    'SESSION_HANDOFF_193.md',
    'SESSION_HANDOFF_194.md',
    'SESSION_HANDOFF_195.md',
    'SESSION_HANDOFF_196.md',
    'SESSION_HANDOFF_197.md',
    'SESSION_HANDOFF_198.md',
    'SESSION_HANDOFF_199.md',
    'SESSION_HANDOFF_200.md',
    'SESSION_HANDOFF_201.md',
    'SESSION_HANDOFF_202.md',
    'SESSION_HANDOFF_204.md',
    'SESSION_HANDOFF_205.md',
    'SESSION_HANDOFF_206.md',
    'SESSION_HANDOFF_207.md',
    'SESSION_HANDOFF_208.md',
    'SESSION_HANDOFF_209.md',
    'SESSION_HANDOFF_210.md',
    'SESSION_HANDOFF_211.md',
    'SESSION_HANDOFF_212.md',
    'SESSION_HANDOFF_213.md',
    'SESSION_HANDOFF_214.md',
    'SESSION_HANDOFF_215.md',
    'SESSION_HANDOFF_216.md',
    'SESSION_HANDOFF_217.md',
    'SESSION_HANDOFF_218.md',
    'SESSION_HANDOFF_219.md',
    'SESSION_HANDOFF_220.md',
    'SESSION_HANDOFF_221.md',
    'SESSION_HANDOFF_222.md',
    'SESSION_HANDOFF_223.md',
    'SESSION_HANDOFF_224.md',
    'SESSION_HANDOFF_225.md',
    'SESSION_HANDOFF_226.md',
    'SESSION_HANDOFF_227.md',
    'SESSION_HANDOFF_228.md',
    'SESSION_HANDOFF_229.md',
    'SESSION_HANDOFF_230.md',
    'SESSION_HANDOFF_231.md',
    'SESSION_HANDOFF_232.md',
    'SESSION_HANDOFF_233.md',
    'SESSION_HANDOFF_234.md',
    'SESSION_HANDOFF_235.md',
    'SESSION_HANDOFF_236.md',
    'SESSION_HANDOFF_237.md',
    'SESSION_HANDOFF_238.md',
    'SESSION_HANDOFF_239.md',
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
#   SESSION_HANDOFF_203.md — removed S206 (D299). Never committed to the repo and
#     no longer present in the project area (confirmed via a fresh clone, twice,
#     across S205 and S206); genuinely unrecoverable, not a housekeeping gap. Its
#     substance was already reconstructed into 40K_Decision_Log.md as D296 by S204,
#     verified line-for-line against the handoff before the file itself was lost.
#     Removing the GUARDED entry rather than leaving the gate permanently red.


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def unguarded_handoffs(d):
    """SESSION_HANDOFF_N.md files present in d that GUARDED does not list at all —
    not a stale JSON entry (that's `unguarded` inside check()), a handoff GUARDED
    itself has never heard of. This is the S177-179 failure: three handoffs were
    written and never appended to GUARDED, so the plain gate had nothing to check
    them against and stayed green while they went completely unguarded. Folded into
    check() so the very next session's baseline catches a forgotten append
    immediately, instead of relying on --freshness-check (which only looks at the
    single latest handoff) to eventually notice."""
    present = {f for f in os.listdir(d) if _HANDOFF_RE.match(f)}
    guarded = {f for f in GUARDED if _HANDOFF_RE.match(f)}
    return sorted(present - guarded)


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
    orphan_handoffs = unguarded_handoffs(d)

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
    if orphan_handoffs:
        problems.append(f'{len(orphan_handoffs)} session handoff(s) present but not in GUARDED — '
                        f'add to pipeline_manifest.py: ' + ', '.join(orphan_handoffs))

    if problems:
        return False, '; '.join(problems)
    return True, f'{len(recorded)} guarded files all match'


def check_overlay(fetched_dir, local_dir):
    """(ok, message, overlay_targets). Verifies ONLY the guarded files the overlay is
    about to pull in — i.e. files GUARDED lists but that are absent from local_dir.
    Files already present locally are never checked here: per the fetch-open's own
    authority rule ("area copy wins"), a locally-resident file's content is never
    sourced from the fetch, so a fetched copy that differs from the manifest (stale
    manifest, or repo behind local edits not yet pushed) must not block pulling in the
    files that ARE only sourced from the fetch. Scoping verification to the overlay
    set is what makes that rule real instead of just documented (M0 originally
    verified the whole tree unconditionally, which let ordinary area-ahead-of-repo
    drift on unrelated files block every eviction-recovery fetch — S151 finding).
    """
    p = os.path.join(fetched_dir, MANIFEST)
    if not os.path.exists(p):
        p = MANIFEST
    if not os.path.exists(p):
        return False, f'{MANIFEST} not found — nothing to verify against', []
    try:
        recorded = json.load(open(p, encoding='utf-8')).get('files', {})
    except Exception as e:
        return False, f'{MANIFEST} is unreadable: {type(e).__name__}: {e}', []

    overlay_targets = [f for f in GUARDED if not os.path.exists(os.path.join(local_dir, f))]

    absent, mismatch = [], []
    for f in overlay_targets:
        fp = os.path.join(fetched_dir, f)
        if not os.path.exists(fp):
            absent.append(f)
        elif f in recorded and sha256(fp) != recorded[f]:
            mismatch.append(f)

    # Checked against fetched_dir (the whole unpacked repo), not local_dir: a handoff
    # GUARDED forgot to list is routinely deleted from the project area (expected
    # housekeeping) long before anyone would notice it locally. The repo fetch always
    # has the full history, so this is the only point in the pipeline where an S177-179
    # style gap is guaranteed to still be visible regardless of what's resident locally.
    orphan_handoffs = unguarded_handoffs(fetched_dir)

    problems = []
    if absent:
        problems.append(f'{len(absent)} file(s) needed for overlay are absent from the fetch: '
                         + ', '.join(sorted(absent)))
    if mismatch:
        problems.append(f'{len(mismatch)} file(s) needed for overlay do not match the manifest: '
                         + ', '.join(sorted(mismatch)))
    if orphan_handoffs:
        problems.append(f'{len(orphan_handoffs)} session handoff(s) in the repo but not in '
                        f'GUARDED — add to pipeline_manifest.py: ' + ', '.join(orphan_handoffs))

    if problems:
        return False, '; '.join(problems), overlay_targets
    return True, (f'{len(overlay_targets)} overlay-needed file(s) verified '
                  f'({len(GUARDED) - len(overlay_targets)} already local, not checked)'), overlay_targets


DECISION_LOG = '40K_Decision_Log.md'


def latest_handoff(d):
    """Highest-numbered SESSION_HANDOFF_N.md present in d, or None if none exist."""
    nums = []
    for f in os.listdir(d):
        m = _HANDOFF_RE.match(f)
        if m:
            nums.append((int(m.group(1)), f))
    return max(nums)[1] if nums else None


def freshness_check(d):
    """(ok, message). Verifies ONLY the decision log and the latest session handoff
    against pipeline_manifest.json — the two files D251's ordering rule depends on
    being untouched after `--write` (B81, S168). Run this as the last command of
    session close, after --write. A mismatch means one of the two was edited after
    the write ran and the manifest needs reissuing before delivery."""
    targets = [f for f in (DECISION_LOG, latest_handoff(d)) if f]
    if not targets:
        return False, 'neither the decision log nor a session handoff was found'

    p = os.path.join(d, MANIFEST)
    if not os.path.exists(p):
        return False, f'{MANIFEST} not found — run --write first'
    try:
        recorded = json.load(open(p, encoding='utf-8')).get('files', {})
    except Exception as e:
        return False, f'{MANIFEST} is unreadable: {type(e).__name__}: {e}'

    problems = []
    for f in targets:
        fp = os.path.join(d, f)
        if not os.path.exists(fp):
            problems.append(f'{f} absent')
        elif f not in recorded:
            problems.append(f'{f} not in {MANIFEST} — run --write')
        elif sha256(fp) != recorded[f]:
            problems.append(f'{f} does not match the manifest — edited after --write, reissue it')

    if problems:
        return False, '; '.join(problems)
    return True, f'{", ".join(targets)} match the manifest banked by the last --write'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.', help='directory holding the guarded files')
    ap.add_argument('--write', action='store_true', help='regenerate pipeline_manifest.json')
    ap.add_argument('--overlay-check', metavar='LOCAL_DIR',
                     help='verify only the guarded files absent from LOCAL_DIR (the overlay set), '
                          'reading their content from --dir. Prints the overlay file list on OK, '
                          'one per line, after the summary line, for a caller to copy.')
    ap.add_argument('--freshness-check', action='store_true',
                     help='B81: verify only the decision log and the latest session handoff '
                          'against pipeline_manifest.json. Run last at session close, after '
                          '--write, to catch either file being edited after the write ran.')
    a = ap.parse_args()

    if a.freshness_check:
        ok, msg = freshness_check(a.dir)
        print(('OK   ' if ok else 'FAIL ') + msg)
        return 0 if ok else 1

    if a.write:
        try:
            n = write(a.dir)
        except FileNotFoundError as e:
            print('FAIL ', e)
            return 1
        print(f'OK   wrote {MANIFEST} with {n} guarded files')
        return 0

    if a.overlay_check is not None:
        ok, msg, targets = check_overlay(a.dir, a.overlay_check)
        print(('OK   ' if ok else 'FAIL ') + msg)
        if ok:
            for f in targets:
                print(f)
        return 0 if ok else 1

    ok, msg = check(a.dir)
    print(('OK   ' if ok else 'FAIL ') + msg)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
