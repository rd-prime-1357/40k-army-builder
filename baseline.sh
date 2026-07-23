#!/usr/bin/env bash
# baseline.sh — every session-open gate in one command (T3, S126).
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
#   ./baseline.sh              # run every gate against the current directory
#   ./baseline.sh --no-repo    # skip repo_check.py (e.g. offline / sandboxed run)

set -u
cd "$(dirname "$0")"

SKIP_REPO=0
for arg in "$@"; do
  [ "$arg" = "--no-repo" ] && SKIP_REPO=1
done

FAILS=0
TOTAL=0

# Runs one gate, captures its last non-empty output line as the summary, and prints
# a single PASS/FAIL line. $1 = gate name, remaining args = the command to run.
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

gate repro_check          python3 repro_check.py
gate units_repro_check    python3 units_repro_check.py
gate detachments_repro    python3 detachments_repro_check.py
gate rules_assertions     python3 rules_assertions.py
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
gate e1b_check            node e1b_check.js index.html detachments.json list_store.js
gate e1c_check            node e1c_check.js index.html detachments.json
gate bundle_check         node bundle_check.js index.html unit_loadouts.json units.json
gate pipeline_manifest    python3 pipeline_manifest.py
if [ "$SKIP_REPO" -eq 0 ]; then
  gate repo_check python3 repo_check.py
fi

echo "---"
if [ $FAILS -eq 0 ]; then
  echo "OK   $TOTAL/$TOTAL gates pass"
  exit 0
else
  echo "FAIL $FAILS/$TOTAL gate(s) failed — reconcile before starting work"
  exit 1
fi
