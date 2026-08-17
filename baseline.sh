#!/usr/bin/env bash
# baseline.sh — every session-open gate in one command (T3, S126; fetch-open + tiering, M0/S149).
#
# WHY: the session prompt used to list each gate's command separately, several with
# positional arguments that are easy to get wrong — several harnesses take three or
# four arguments and print a bare Node stack trace when called without them, which
# currently reads identically to a real failure. This encodes the correct argument
# shape for every gate in one place, so nobody re-derives them per session.
#
# One line of output per gate: "PASS <gate>: <the gate's own summary line>" or
# "FAIL <gate>: <the gate's own summary line>". Exits non-zero if any gate fails.
#
#   ./baseline.sh                # old path: everything local, repo_check via git clone
#   ./baseline.sh --no-repo      # old path, skip repo_check.py (offline / sandboxed)
#   ./baseline.sh --fetch        # new path (P4/D231, M0): fetch the public repo as one
#                                 tarball, verify it against pipeline_manifest.json,
#                                 overlay (area copy wins), then gate as usual
#   ./baseline.sh --fetch --data-turn   # new path; also fetch/verify GW sources (token,
#                                 falling back to gw_sources.zip) and FAIL if neither the
#                                 private repo nor the zip nor already-local sources are
#                                 available — a data turn must not silently start tier-A-only
#
# TIERING (P4/D231): rules_assertions.py and the three repro rebuilds (repro_check,
# units_repro_check, detachments_repro_check) need the 70-odd GW source files. Whether
# those are loaded is detected from source_manifest.json's own file list, not assumed
# from which flag was passed — so both paths report the same tier truthfully in a
# session where sources are simply still sitting in the area (true throughout M0).

set -u
cd "$(dirname "$0")"

SKIP_REPO=0
FETCH=0
DATA_TURN=0
for arg in "$@"; do
  case "$arg" in
    --no-repo)   SKIP_REPO=1 ;;
    --fetch)     FETCH=1 ;;
    --data-turn) DATA_TURN=1 ;;
  esac
done

FAILS=0
TOTAL=0
SKIPS=0

gate() {
  local name="$1"; shift
  TOTAL=$((TOTAL+1))
  local out
  out="$("$@" 2>&1)"
  local rc=$?
  local summary
  summary="$(printf '%s\n' "$out" | awk 'NF{line=$0} END{print line}')"
  if [ $rc -eq 0 ]; then
    printf 'PASS %-24s %s\n' "$name" "$summary"
  else
    FAILS=$((FAILS+1))
    printf 'FAIL %-24s %s\n' "$name" "$summary"
  fi
}

# Prints a loud, counted skip line instead of silence — a skip must never read like a
# pass, and must never look identical to ordinary output that scrolled past.
skip_gate() {
  local name="$1"; shift
  TOTAL=$((TOTAL+1))
  SKIPS=$((SKIPS+1))
  printf 'SKIP %-24s SKIP (tier B — sources not loaded)\n' "$name"
}

# ── sources-loaded detection (P4/D231) ─────────────────────────────────────────
# True tier is whatever is actually on disk right now, checked against
# source_manifest.json's own file list — never assumed from a flag.
sources_loaded() {
  [ -f source_manifest.json ] || return 1
  python3 - <<'PYEOF'
import json, os, sys
try:
    files = json.load(open('source_manifest.json', encoding='utf-8'))['files']
except Exception:
    sys.exit(1)
sys.exit(0 if all(os.path.exists(f) for f in files) else 1)
PYEOF
}

SOURCES_OK=0
if sources_loaded; then
  SOURCES_OK=1
fi

# ── fetch-unpack-verify-overlay (P4/D231, M0) ──────────────────────────────────
if [ "$FETCH" -eq 1 ]; then
  TMP_REPO="$(mktemp -d)"
  trap 'rm -rf "$TMP_REPO"' EXIT
  if curl -sL --fail -o "$TMP_REPO/repo.tar.gz" \
      https://codeload.github.com/rd-prime-1357/40k-army-builder/tar.gz/main; then
    tar -xzf "$TMP_REPO/repo.tar.gz" -C "$TMP_REPO"
    FETCHED_DIR="$(find "$TMP_REPO" -mindepth 1 -maxdepth 1 -type d | head -1)"
    if [ -z "$FETCHED_DIR" ]; then
      echo "FAIL fetch-verify           tarball unpacked but no directory found inside"
      FAILS=$((FAILS+1)); TOTAL=$((TOTAL+1))
    else
      TOTAL=$((TOTAL+1))
      # Overlay-scoped verify (S151 fix): only the guarded files actually absent from
      # the workspace are checked against the manifest, using the fetched copy as their
      # source. Files already resident locally are never checked here — area-ahead-of-
      # repo drift on files we are not overlaying (e.g. an edited backlog doc not yet
      # pushed) must not block recovering files that were genuinely evicted (M1).
      # B139 (D352, S255): the overlay runs on FAILURE as well as success. --overlay-check
      # prints its summary on line 1 and the files it verified from line 2 on, in both
      # cases, so recovery no longer depends on the gate being green. One unpushed file
      # used to withhold every other file, which meant units.json and friends never
      # arrived and ~25 downstream gates crashed on absent inputs — 26 failures for one
      # defect, and the 25 were indistinguishable from real ones. The gate below still
      # fails and still names the problem; it just does not take the rest down with it.
      if VERIFY_OUT="$(python3 pipeline_manifest.py --dir "$FETCHED_DIR" --overlay-check . 2>&1)"; then
        VERIFY_RC=0
      else
        VERIFY_RC=1
      fi
      SUMMARY_LINE="$(printf '%s\n' "$VERIFY_OUT" | head -1)"
      printf '%s\n' "$VERIFY_OUT" | tail -n +2 | while IFS= read -r rel; do
        [ -z "$rel" ] && continue
        mkdir -p "$(dirname "$rel")"
        [ -f "$FETCHED_DIR/$rel" ] || continue
        cp "$FETCHED_DIR/$rel" "$rel"
      done
      if [ "$VERIFY_RC" -eq 0 ]; then
        printf 'PASS %-24s %s\n' fetch-verify "$SUMMARY_LINE"
      else
        printf 'FAIL %-24s %s\n' fetch-verify "$SUMMARY_LINE"
        FAILS=$((FAILS+1))
      fi
    fi
  else
    echo "FAIL fetch-verify           could not fetch the public repo tarball (network / repo unreachable)"
    FAILS=$((FAILS+1)); TOTAL=$((TOTAL+1))
  fi

  # ── private sources repo (data turns): token first, zip fallback, then already-
  # local sources — never silently proceed tier-A-only on a data turn.
  if [ "$DATA_TURN" -eq 1 ] && [ "$SOURCES_OK" -eq 0 ]; then
    TOTAL=$((TOTAL+1))
    if [ -f SOURCE_REPO_TOKEN.txt ]; then
      TOKEN="$(cat SOURCE_REPO_TOKEN.txt)"
      TMP_SRC="$(mktemp -d)"
      if curl -sL --fail -H "Authorization: Bearer $TOKEN" \
          -o "$TMP_SRC/src.tar.gz" \
          https://codeload.github.com/rd-prime-1357/rd-prime-1357-data-sources/tar.gz/main; then
        tar -xzf "$TMP_SRC/src.tar.gz" -C "$TMP_SRC"
        SRC_DIR="$(find "$TMP_SRC" -mindepth 1 -maxdepth 1 -type d | head -1)"
        if SRC_VERIFY="$(python3 - "$SRC_DIR" <<'PYEOF'
import json, hashlib, os, sys
d = sys.argv[1]
files = json.load(open('source_manifest.json', encoding='utf-8'))['files']
def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()
bad = [f for f, want in files.items()
       if not os.path.exists(os.path.join(d, f)) or sha256(os.path.join(d, f)) != want]
if bad:
    print('FAIL', len(bad), 'source file(s) failed verification:', ', '.join(sorted(bad)[:5]))
    sys.exit(1)
print('OK', len(files), 'source files verified against source_manifest.json')
PYEOF
        )"; then
          printf 'PASS %-24s %s\n' source-fetch "$SRC_VERIFY"
          cp -n "$SRC_DIR"/* . 2>/dev/null
          SOURCES_OK=1
        else
          printf 'FAIL %-24s %s\n' source-fetch "$SRC_VERIFY"
          FAILS=$((FAILS+1))
        fi
      else
        echo "FAIL source-fetch            token present but the private-repo fetch failed"
        FAILS=$((FAILS+1))
      fi
      rm -rf "$TMP_SRC"
    elif [ -f gw_sources.zip ]; then
      TMP_SRC="$(mktemp -d)"
      unzip -q gw_sources.zip -d "$TMP_SRC"
      if SRC_VERIFY="$(python3 - "$TMP_SRC" <<'PYEOF'
import json, hashlib, os, sys
d = sys.argv[1]
files = json.load(open('source_manifest.json', encoding='utf-8'))['files']
def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()
bad = [f for f, want in files.items()
       if not os.path.exists(os.path.join(d, f)) or sha256(os.path.join(d, f)) != want]
if bad:
    print('FAIL', len(bad), 'source file(s) failed verification:', ', '.join(sorted(bad)[:5]))
    sys.exit(1)
print('OK', len(files), 'source files verified against source_manifest.json (zip fallback)')
PYEOF
      )"; then
        printf 'PASS %-24s %s\n' source-fetch "$SRC_VERIFY"
        cp -n "$TMP_SRC"/* . 2>/dev/null
        SOURCES_OK=1
      else
        printf 'FAIL %-24s %s\n' source-fetch "$SRC_VERIFY"
        FAILS=$((FAILS+1))
      fi
      rm -rf "$TMP_SRC"
    else
      echo "FAIL source-fetch            data turn with no SOURCE_REPO_TOKEN.txt and no gw_sources.zip — refusing to start"
      FAILS=$((FAILS+1))
    fi
  fi
fi

# ── tiered gates ────────────────────────────────────────────────────────────
# B96: b87_check/b88_check drive mfm_points_parser.py/detachment_parser.py against
# the raw GW MFM sources, exactly like the three repro rebuilds below — they belong
# in this same sources-loaded conditional, not the always-run block, so a
# sources-absent open reads them as SKIP instead of a crash misread as FAIL.
if [ "$SOURCES_OK" -eq 1 ]; then
  gate repro_check          python3 repro_check.py
  gate units_repro_check    python3 units_repro_check.py
  gate detachments_repro    python3 detachments_repro_check.py
  gate rules_assertions     python3 rules_assertions.py --tier all
  gate b87_check            node b87_check.js
  gate b88_check            node b88_check.js
else
  skip_gate repro_check
  skip_gate units_repro_check
  skip_gate detachments_repro
  gate rules_assertions     python3 rules_assertions.py --tier a
  skip_gate b87_check
  skip_gate b88_check
  if [ "$DATA_TURN" -eq 1 ]; then
    echo "FAIL data-turn-gate          sources not loaded — a data turn must not start tier-A-only"
    FAILS=$((FAILS+1)); TOTAL=$((TOTAL+1))
  fi
fi

gate pool_check           node pool_check.js index.html B18c_repro_fixture.json
gate e10_check            node e10_check.js index.html
gate b18d_check           node b18d_check.js index.html B18d_fixture.json
gate required_size_check  node required_size_check.js index.html unit_loadouts.json
gate b31_check            node b31_check.js index.html units.json unit_loadouts.json datasheet_wargear_abilities.json
gate stat_check           node stat_check.js index.html unit_loadouts.json units.json datasheet_wargear_abilities.json
gate default_check        node default_check.js index.html unit_loadouts.json wargear_points.json
gate pts_check            node pts_check.js index.html unit_loadouts.json wargear_points.json units.json
gate limit_check          node limit_check.js index.html units.json
gate b56g_check           node b56g_check.js index.html unit_loadouts.json
gate b58_check            node b58_check.js index.html unit_loadouts.json
gate b72_check            node b72_check.js index.html unit_loadouts.json
gate b90_check            node b90_check.js index.html
gate b101_check           node b101_check.js index.html
gate b132_check           node b132_check.js index.html
gate b106_check           node b106_check.js index.html
gate b99_check            node b99_check.js index.html detachments.json units.json unit_loadouts.json
gate b119_check           node b119_check.js index.html detachments.json units.json unit_loadouts.json
gate b123_check           node b123_check.js index.html detachments.json units.json unit_loadouts.json
gate e1b_check            node e1b_check.js index.html detachments.json list_store.js
gate e1c_check            node e1c_check.js index.html detachments.json
gate e4b_check            node e4b_check.js index.html detachments.json units.json
gate e4c_check            node e4c_check.js index.html detachments.json
gate e21b_check           node e21b_check.js index.html detachment_effects.json units.json
gate e21c_check           node e21c_check.js index.html detachment_effects.json units.json
gate e25_check            node e25_check.js index.html detachments.json list_store.js
gate b128_check           node b128_check.js index.html detachment_effects.json
gate b126_check           node b126_check.js index.html detachment_effects.json units.json
gate b103_check           node b103_check.js index.html unit_loadouts.json units.json wargear_points.json
gate b71_check             node b71_check.js index.html
gate bundle_check         node bundle_check.js index.html unit_loadouts.json units.json
gate pipeline_manifest    python3 pipeline_manifest.py
if [ "$SKIP_REPO" -eq 0 ]; then
  gate repo_check python3 repo_check.py
fi

echo "---"
GATED=$((TOTAL-SKIPS))
if [ $FAILS -eq 0 ]; then
  if [ $SKIPS -gt 0 ]; then
    echo "OK   $((GATED))/$((GATED)) gates pass ($SKIPS tier-B skipped)"
  else
    echo "OK   $TOTAL/$TOTAL gates pass"
  fi
  exit 0
else
  echo "FAIL $FAILS/$TOTAL gate(s) failed — reconcile before starting work"
  exit 1
fi
