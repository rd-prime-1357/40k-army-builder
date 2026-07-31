#!/usr/bin/env python3
"""
repo_check.py — public-repo custody check (T1, S126).

WHY THIS FILE EXISTS
--------------------
The pipeline manifest guards against a bad *local* sync (H3). It has no idea what is
actually sitting in the public repo. Session-to-session, files have gone missing from
the repo, drifted out of byte-sync, or (the one that matters most) GW-derived source
material has come close to being committed to a repo that is served publicly over
GitHub Pages. This script clones the real repo and checks it against the project
working area so that class of problem is caught here, not discovered later by someone
browsing the repo by hand.

FOUR STATES, PER FILE
----------------------
  match              — same bytes in the repo and the project area
  differs            — both exist, bytes differ
  missing from repo   — expected in the repo (see SCOPE below), not found there
  repo-only           — exists in the repo, not found in the project area

SCOPE
-----
This does not walk "everything on disk." Most of the project working area is GW /
Wahapedia source material that must never be committed (Wahapedia CSV exports, MFM
points files, faction web-composition files, GW faction packs, core rules text,
third-party product references) — walking all of it and reporting each as "missing
from repo" would just be noise around files that are correctly, permanently excluded.

"Missing from repo" is only checked against a deliberately narrow expected set:
  - every file in pipeline_manifest.json's guarded list (read live, not hardcoded here —
    see H3; the guarded set is free to grow without this file needing an edit)
  - pipeline_manifest.json itself
  - the fixed set of living/reference docs (DOC_FILES below)
  - every SESSION_HANDOFF_*.md present in the project area (these accumulate; every one
    that exists locally is expected to exist in the repo too, per project convention)

match/differs/repo-only are NOT limited to that expected set — every file the clone
actually contains gets classified, so files outside the guarded+docs scope (harnesses,
one-off migration scripts, secondary JSON outputs, fixtures) still get a real
byte-comparison; they are just not required to be present.

GW-DERIVED EXCLUDE PATTERNS: ONE SOURCE, NOT TWO
-------------------------------------------------
Rather than hand-maintaining a second pattern list that could quietly drift from
.gitignore, this script reads .gitignore straight out of the clone and buckets its
patterns by the section comments already in that file (the comment headers already
say which block is "GW-derived" vs. "local scratch"). If a GW-derived file slips into
the repo, matching the live .gitignore, it is reported as a distinct, louder finding —
that is a publication problem, not a sync problem.

NETWORK
-------
If the clone fails, this fails clearly with that reason. It does not fall back to
reporting a false "clean" result — an unreachable network is not the same thing as a
repo with no problems.

    python3 repo_check.py                       # check '.' against the real repo
    python3 repo_check.py --dir /path/to/area    # check another directory
"""

import argparse, fnmatch, json, os, re, subprocess, sys, tempfile, shutil, hashlib

REPO_URL = 'https://github.com/rd-prime-1357/40k-army-builder.git'
MANIFEST = 'pipeline_manifest.json'

# The read-only private-sources-repo token (P4/D231, M0/S149) lives in the project
# area as this exact filename, and only there — it must never reach a file list
# bound for the *public* repo. TOKEN_PATTERN is a second, content-shaped check:
# GitHub fine-grained tokens all start with this literal prefix, so a rename of
# the file doesn't defeat the guard.
TOKEN_FILENAME = 'SOURCE_REPO_TOKEN.txt'
TOKEN_PATTERN = re.compile(r'github_pat_[A-Za-z0-9_]+')

# Fixed, non-accumulating docs. SESSION_HANDOFF_*.md accumulates and is discovered
# live from the project area instead of listed here (see docstring).
DOC_FILES = [
    '40K_Decision_Log.md',
    'OPEN_ITEMS_BACKLOG.md',
    'NEXT_SESSION_PROMPT.md',
    '40K_Functional_Spec.md',
    '40K_Architecture_Overview.md',
    '40K_Data_Dictionary.md',
    '40K_Data_Pipeline_Process.md',
    'OUTPUT_FORMAT_SPEC_for_project_instructions.md',
    'E1_DETACHMENT_SCOPE.md',
    'MFM_Chapter_Pass.md',
    'MFM_FW_Reconciliation.md',
    'MFM_Standalone_Pass.md',
    # T5 (S126) net-new indices — added here so a future drop of either is caught
    # the same way any other doc's would be.
    'DECISION_INDEX.md',
    'BACKLOG_ARCHIVE.md',
]

# Section-header comment prefixes in .gitignore that mark GW-derived blocks, as
# opposed to the trailing "local scratch" block. Anything under one of these
# headers, until the next header, is treated as GW-derived for the loud check.
GW_SECTION_MARKERS = (
    'Wahapedia CSV exports',
    'Source text',
    'GW faction packs',
    'Third-party product references',
)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def clone_repo(tmp_dir):
    """Clone REPO_URL into tmp_dir. Raises RuntimeError with a clear reason on failure —
    never returns a partial or fake-clean result."""
    try:
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', REPO_URL, tmp_dir],
            capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        raise RuntimeError('git is not available in this environment')
    except subprocess.TimeoutExpired:
        raise RuntimeError('git clone timed out — network unavailable or repo unreachable')
    if result.returncode != 0:
        raise RuntimeError(f'git clone failed: {result.stderr.strip() or result.stdout.strip()}')


def parse_gitignore_gw_patterns(repo_dir):
    """Read the repo's own .gitignore and return (gw_patterns, other_patterns), bucketed
    by the section-header comments already in the file. No hardcoded duplicate list —
    if .gitignore changes, this changes with it."""
    path = os.path.join(repo_dir, '.gitignore')
    if not os.path.exists(path):
        return [], []

    gw_patterns, other_patterns = [], []
    current_is_gw = False
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            header = line.lstrip('#').strip(' \u2500\u2501-')
            current_is_gw = any(marker in header for marker in GW_SECTION_MARKERS)
            continue
        if line.startswith('!'):
            continue  # no negations in use today; skip rather than mis-handle
        (gw_patterns if current_is_gw else other_patterns).append(line)
    return gw_patterns, other_patterns


def matches_any(name, patterns):
    for pat in patterns:
        p = pat.rstrip('/')
        if fnmatch.fnmatch(name, p) or fnmatch.fnmatch(name, '*/' + p):
            return pat
    return None


def guarded_files(project_dir):
    """Read the live pipeline_manifest.json guarded list. Falls back to an empty list
    (with a warning surfaced by the caller) rather than hardcoding a stale copy here."""
    p = os.path.join(project_dir, MANIFEST)
    if not os.path.exists(p):
        return None
    try:
        return sorted(json.load(open(p, encoding='utf-8')).get('files', {}).keys())
    except Exception:
        return None


def discover_handoffs(project_dir):
    return sorted(f for f in os.listdir(project_dir)
                  if f.startswith('SESSION_HANDOFF_') and f.endswith('.md'))


def run(project_dir):
    tmp_dir = tempfile.mkdtemp(prefix='repo_check_')
    try:
        clone_repo(tmp_dir)
    except RuntimeError as e:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f'NETWORK FAIL — could not verify the repo: {e}')
        return 2

    try:
        gw_patterns, _other_patterns = parse_gitignore_gw_patterns(tmp_dir)

        repo_files = sorted(
            os.path.relpath(os.path.join(root, f), tmp_dir)
            for root, dirs, files in os.walk(tmp_dir)
            if '.git' not in root.split(os.sep)
            for f in files
        )

        gw_found = []
        matches, differs, repo_only = [], [], []
        for rel in repo_files:
            gw_pat = matches_any(rel, gw_patterns)
            if gw_pat:
                gw_found.append((rel, gw_pat))
                continue  # GW-derived material is reported separately, not as ordinary drift
            local_path = os.path.join(project_dir, rel)
            repo_path = os.path.join(tmp_dir, rel)
            if not os.path.exists(local_path):
                repo_only.append(rel)
            elif sha256(local_path) == sha256(repo_path):
                matches.append(rel)
            else:
                differs.append(rel)

        expected = set(DOC_FILES) | {MANIFEST} | set(discover_handoffs(project_dir))
        guarded = guarded_files(project_dir)
        manifest_missing_warning = guarded is None
        if guarded:
            expected |= set(guarded)

        missing_from_repo = sorted(f for f in expected if f not in repo_files)

        # ---- token custody guard (P4/D231, M0/S149) ----
        # Three independent ways the token could reach the public repo, each checked
        # separately so a fail names exactly which one happened:
        #   (a) it is already sitting in the live clone — an actual leak, worst case.
        #   (b) its filename is in one of the file lists this script treats as
        #       "public-repo-bound" (DOC_FILES, the discovered handoffs, or the
        #       pipeline_manifest.json guarded set) — a mistake that would leak it
        #       on the next push, caught before that push happens.
        #   (c) a token-shaped string (github_pat_...) sits in the content of any
        #       file this check already reads byte-for-byte in the local area —
        #       catches a pasted-into-the-wrong-file accident even under a renamed
        #       filename.
        token_leaked_in_repo = TOKEN_FILENAME in repo_files
        token_in_bound_lists = TOKEN_FILENAME in expected
        token_in_content = []
        for rel in sorted(set(matches) | set(differs)):
            local_path = os.path.join(project_dir, rel)
            try:
                with open(local_path, encoding='utf-8', errors='ignore') as f:
                    if TOKEN_PATTERN.search(f.read()):
                        token_in_content.append(rel)
            except (OSError, UnicodeDecodeError):
                continue
        token_problem = token_leaked_in_repo or token_in_bound_lists or bool(token_in_content)

        # ---- report ----
        problems = 0

        if token_problem:
            problems += 1
            print('CRITICAL — SOURCE_REPO_TOKEN.txt custody guard tripped (credential exposure risk):')
            if token_leaked_in_repo:
                print(f'    {TOKEN_FILENAME} is present in the live public-repo clone — revoke this '
                      f'token on GitHub now, then investigate.')
            if token_in_bound_lists:
                print(f'    {TOKEN_FILENAME} appears in a public-repo-bound file list (DOC_FILES, the '
                      f'handoff set, or the pipeline_manifest.json guarded set) — remove it before the '
                      f'next push.')
            if token_in_content:
                print(f'    a token-shaped string (github_pat_...) was found inside: '
                      + ', '.join(token_in_content))

        if gw_found:
            problems += len(gw_found)
            print(f'CRITICAL — {len(gw_found)} GW-derived file(s) found committed to the PUBLIC repo '
                  f'(publication problem, not a sync problem):')
            for rel, pat in sorted(gw_found):
                print(f'    {rel}  (matches .gitignore pattern: {pat})')

        if missing_from_repo:
            problems += len(missing_from_repo)
            print(f'MISSING FROM REPO — {len(missing_from_repo)} expected file(s) not found in the clone:')
            for f in missing_from_repo:
                print(f'    {f}')

        if differs:
            problems += len(differs)
            print(f'DIFFERS — {len(differs)} file(s) exist in both places with different bytes:')
            for f in differs:
                print(f'    {f}')

        if manifest_missing_warning:
            print(f'WARNING — {MANIFEST} not found in the project area; the guarded-set portion '
                  f'of the expected set could not be checked (see H3).')

        if repo_only:
            print(f'repo-only — {len(repo_only)} file(s) in the repo have no counterpart in the '
                  f'project area (informational, not a failure): ' + ', '.join(repo_only))

        print(f'match — {len(matches)} file(s) byte-identical')

        if problems == 0:
            print('OK   repo matches the project area; no GW-derived material found')
            return 0
        print(f'FAIL {problems} problem(s) found — see above')
        return 1
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.', help='project working directory to compare against')
    a = ap.parse_args()
    sys.exit(run(a.dir))


if __name__ == '__main__':
    main()
