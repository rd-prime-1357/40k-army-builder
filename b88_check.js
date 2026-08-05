#!/usr/bin/env node
/*
 * b88_check.js — executable form of the B88 acceptance facts (D274 arc, MFM v1.1
 * DETACHMENTS-block layout support in detachment_parser.py, rescoped in from B87
 * at D283/S190).
 *
 * Same convention as b87_check.js: a JS harness driving the Python parser through a
 * one-shot and asserting on the JSON it prints. No parser internals are duplicated
 * here; the harness only pins observable output.
 *
 * Facts pinned (any regression fails the baseline):
 *
 *  1. Every one of the 15 banked v1.1 MFM files' DETACHMENTS block parses without
 *     raising, and yields at least one detachment with at least one enhancement.
 *     Before B88 every one of these raised (the reader only understood the v1_0
 *     jammed-line shape).
 *
 *  2. v1_0 output is unchanged. The two files currently live in ARMY_TO_MFM
 *     (Black Templars, Space Marines) still parse their first detachment to the
 *     exact name/DP/disposition/enhancement-count B88 found before editing the
 *     parser.
 *
 *  3. Two v1.1-exclusive quirks beyond the ones B87 already handles for the points
 *     file are parsed correctly, not silently dropped or mis-joined:
 *       - Thousand Sons HEXWARP THRALLBAND: a DP line carrying a bare trailing
 *         change marker with no parenthesised delta ("3DP \u25b2") still reads as
 *         DP 3, not folded into the enhancement block or left as a stray line.
 *       - World Eaters BRAZEN ENGINES: the "UNIQUE TAG REMOVED" editorial note
 *         (missed on a first pass keyed only off the Space Marines file) is
 *         dropped as noise, not left as an unrecognised line that aborts the parse.
 *       - Thousand Sons WARPMELD PACT: an ordinary "UNIQUE: MUTANT" tag still reads
 *         correctly on a v1.1 file (the note-stripping doesn't over-match).
 *
 * Usage:  node b88_check.js
 * Exit 0 if every fact holds, 1 otherwise.
 */

'use strict';
const { execFileSync } = require('child_process');

function py(code) {
  return JSON.parse(execFileSync('python3', ['-c', code], { encoding: 'utf8' }));
}

const V11_FILES = [
  'MFM_Space_Marines_v1.1.txt', 'MFM_Black_Templars_v1.1.txt', 'MFM_Blood_Angels_v1.1.txt',
  'MFM_Dark_Angels_v1.1.txt', 'MFM_Death_Watch_v1.1.txt', 'MFM_Space_Wolves_v1.1.txt',
  'MFM_Grey_Knights_v1.1.txt', 'MFM_Chaos_Space_Marines_v1.1.txt', 'MFM_Death_Guard_v1.1.txt',
  'MFM_Thousand_Sons_v1.1.txt', 'MFM_Emperors_Children_v1.1.txt', 'MFM_World_Eaters_v1.1.txt',
  'MFM_Chaos Daemons_v1.1.txt', 'MFM_Drukhari_v1.1.txt', 'MFM_Chaos_Knights_v1.1.txt',
];

let failures = [];

// ---- Fact 1: every v1.1 file's DETACHMENTS block parses without raising -----
{
  const code = `
import json, sys
sys.path.insert(0, '.')
import detachment_parser as d
out = {}
for f in ${JSON.stringify(V11_FILES)}:
    try:
        dets = d.parse_mfm_detachments(f)
        n_enh = sum(len(x["enhancements"]) for x in dets)
        out[f] = {"ok": True, "n_det": len(dets), "n_enh": n_enh}
    except SystemExit as e:
        out[f] = {"ok": False, "error": str(e)}
print(json.dumps(out))
`;
  const res = py(code);
  for (const f of V11_FILES) {
    const r = res[f];
    if (!r.ok) failures.push(`fact1: ${f} failed to parse: ${r.error}`);
    else if (r.n_det === 0) failures.push(`fact1: ${f} produced 0 detachments`);
    else if (r.n_enh === 0) failures.push(`fact1: ${f} produced 0 enhancements`);
  }
}

// ---- Fact 2: v1_0 output unchanged for the two live ARMY_TO_MFM files -------
{
  const code = `
import json, sys
sys.path.insert(0, '.')
import detachment_parser as d
bt = d.parse_mfm_detachments('MFM_Black_Templars_v1_0.txt')[0]
sm = d.parse_mfm_detachments('MFM_Space_Marines_v1_0.txt')[0]
print(json.dumps({
    'bt': [bt['name_raw'], bt['dp'], bt['force_disposition'], len(bt['enhancements'])],
    'sm': [sm['name_raw'], sm['dp'], sm['force_disposition'], len(sm['enhancements'])],
}))
`;
  const res = py(code);
  const wantBT = ['ANVIL SIEGE FORCE', 2, 'TAKE AND HOLD', 4];
  const wantSM = ['1ST COMPANY TASK FORCE', 2, 'PRIORITY ASSETS', 4];
  if (JSON.stringify(res.bt) !== JSON.stringify(wantBT)) {
    failures.push(`fact2: BT v1_0 first detachment changed: ${JSON.stringify(res.bt)}`);
  }
  if (JSON.stringify(res.sm) !== JSON.stringify(wantSM)) {
    failures.push(`fact2: SM v1_0 first detachment changed: ${JSON.stringify(res.sm)}`);
  }
}

// ---- Fact 3: the three v1.1-exclusive quirks parse correctly ----------------
{
  const code = `
import json, sys
sys.path.insert(0, '.')
import detachment_parser as d
ts = d.parse_mfm_detachments('MFM_Thousand_Sons_v1.1.txt')
we = d.parse_mfm_detachments('MFM_World_Eaters_v1.1.txt')
def find(dets, name):
    for x in dets:
        if x['name_raw'] == name:
            return x
    return None
hex_ = find(ts, 'HEXWARP THRALLBAND')
warp = find(ts, 'WARPMELD PACT')
brazen = find(we, 'BRAZEN ENGINES')
print(json.dumps({
    'hex': [hex_['dp'], hex_['force_disposition']] if hex_ else None,
    'warp': [warp['dp'], warp['unique_tag']] if warp else None,
    'brazen': [brazen['dp'], brazen['force_disposition'], brazen['unique_tag']] if brazen else None,
}))
`;
  const res = py(code);
  if (!res.hex || res.hex[0] !== 3 || res.hex[1] !== 'TAKE AND HOLD') {
    failures.push(`fact3: Hexwarp Thrallband bare-marker DP line mis-parsed: ${JSON.stringify(res.hex)}`);
  }
  if (!res.warp || res.warp[0] !== 2 || res.warp[1] !== 'MUTANT') {
    failures.push(`fact3: Warpmeld Pact UNIQUE tag mis-parsed: ${JSON.stringify(res.warp)}`);
  }
  if (!res.brazen || res.brazen[0] !== 1 || res.brazen[1] !== 'DISRUPTION' || res.brazen[2] !== null) {
    failures.push(`fact3: Brazen Engines UNIQUE TAG REMOVED note not dropped cleanly: ${JSON.stringify(res.brazen)}`);
  }
}

if (failures.length) {
  console.log('b88_check FAIL:');
  for (const f of failures) console.log('  ' + f);
  process.exit(1);
}
console.log('all B88 checks pass (v1.1 DETACHMENTS parsing across 15 files; v1_0 stable; ' +
  'bare-marker DP line, UNIQUE TAG REMOVED note, and UNIQUE tag all handled)');
process.exit(0);
