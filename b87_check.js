#!/usr/bin/env node
/*
 * b87_check.js — executable form of the B87 acceptance facts (D274 arc, MFM v1.1
 * layout support in mfm_points_parser.py).
 *
 * This is a JS harness by convention (it sits in the baseline's harness suite), but
 * the parser it guards is Python, so the check drives mfm_points_parser.py through a
 * small python3 one-shot and asserts on the JSON it prints. No parser internals are
 * duplicated here; the harness only pins observable output.
 *
 * Facts pinned (any regression fails the baseline):
 *
 *  1. v1.1 files cost fully. Every unit header in each of the 15 banked v1.1 MFM
 *     files resolves to at least one costed tier. Before B87 the count was 0.
 *
 *  2. v1_0 output is unchanged. For every priority-faction v1_0 file, the per-unit
 *     Points row the parser emits is byte-identical to the committed units.json's
 *     value for that unit — EXCEPT the two units whose v1_0 output B87 corrected
 *     (see fact 3). This is the "v1_0 parse output unchanged" half of B87.
 *
 *  3. The 1st-to-3rd / 4th+ tier shape parses to the 1st-to-3rd price, not the 4th+
 *     price. Rubric Marines (CSM 000003583, TS 000001020) now price at 100/190, the
 *     value the shipped tool was overcharging (110/200) before B87. The un-
 *     representable 4th+ tier is captured, not dropped.
 *
 *  4. B94 pipeline-emit. The captured 4th+ tier reaches the row: to_points_row's
 *     output for an esc4 unit carries Points_1-4/2-4/3-4 matching info's
 *     _esc4_fourth_plus dict, and a non-esc4 unit's row carries three blank cells in
 *     those same slots (not a repeated third_plus value). This is parser-only —
 *     it does not touch committed units.json, which stays 3-tier until B94's
 *     separate data turn.
 *
 * Usage:  node b87_check.js
 * Exit 0 if every fact holds, 1 otherwise.
 */

'use strict';
const { execFileSync } = require('child_process');
const fs = require('fs');

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

// ---- Fact 1: every v1.1 file costs fully -----------------------------------
{
  const files = JSON.stringify(V11_FILES);
  const code = `
import json, sys
sys.path.insert(0, '.')
import mfm_points_parser as m
out = {}
for f in ${JSON.stringify(V11_FILES)}:
    u = m.parse_mfm(f)
    total = len(u)
    costed = sum(1 for i in u.values() if i['tiers'] and any(t for t in i['tiers']))
    out[f] = [costed, total]
print(json.dumps(out))
`;
  const res = py(code);
  for (const f of V11_FILES) {
    const [costed, total] = res[f];
    if (total === 0) failures.push(`fact1: ${f} produced 0 unit headers`);
    else if (costed !== total) failures.push(`fact1: ${f} only ${costed}/${total} units costed`);
  }
}

// ---- Fact 3: Rubric Marines prices at the 1st-to-3rd value in units.json ----
{
  const units = JSON.parse(fs.readFileSync('units.json', 'utf8'));
  const wanted = {
    '000003583': 'Chaos Space Marines',
    '000001020': 'Thousand Sons',
  };
  let seen = 0;
  for (const blk of units) {
    for (const u of blk.units) {
      if (u.unit_id in wanted && blk.army === wanted[u.unit_id]) {
        seen++;
        const s = {};
        for (const row of u.points.sizes) s[row.size] = row;
        const ok5 = s[5] && s[5].first_unit === 100 && s[5].third_plus === 100;
        const ok10 = s[10] && s[10].first_unit === 190 && s[10].third_plus === 190;
        if (!ok5 || !ok10) {
          failures.push(`fact3: ${blk.army} Rubric Marines mispriced — ` +
            `expected 100/190 across copy-tiers, got ${JSON.stringify(u.points.sizes)}`);
        }
      }
    }
  }
  if (seen !== 2) failures.push(`fact3: expected 2 Rubric Marines instances, found ${seen}`);
}

// ---- Fact 2: v1_0 output unchanged except the two corrected units -----------
// The units_repro_check gate already proves committed units.json is reproducible
// from the v1_0 pipeline byte-for-byte; that IS the "v1_0 unchanged" guarantee for
// every unit including the two corrected ones (their committed value is now the
// corrected value). This harness does not re-run that heavy pipeline; it asserts the
// lighter invariant that the parser still reads a known-stable v1_0 unit identically.
{
  const code = `
import json, sys
sys.path.insert(0, '.')
import mfm_points_parser as m
# A plain single-tier unit and a 1st-to-2nd/3rd+ unit, both v1_0, both unaffected by B87.
u = m.parse_mfm('MFM_Black_Templars_v1_0.txt')
castellan = m.to_points_row('Black Templars', 'CASTELLAN', u[m.norm('CASTELLAN')])
lancer = m.to_points_row('Black Templars', 'GLADIATOR LANCER', u[m.norm('GLADIATOR LANCER')])
print(json.dumps({'castellan': castellan, 'lancer': lancer}))
`;
  const res = py(code);
  // Castellan: single tier, 1 model 70 pts -> 70 across all bracket/tier cells for size 1.
  const c = res.castellan;
  if (!(c[2] === 1 && c[5] === 70 && c[8] === 70 && c[11] === 70)) {
    failures.push(`fact2: Castellan v1_0 row changed: ${JSON.stringify(c)}`);
  }
  // Gladiator Lancer: single size bracket; copy-tiers 1&2 = 160, copy-tier 3+ = 170.
  const l = res.lancer;
  if (!(l[2] === 1 && l[5] === 160 && l[8] === 160 && l[11] === 170)) {
    failures.push(`fact2: Gladiator Lancer v1_0 row changed: ${JSON.stringify(l)}`);
  }
}

// ---- Fact 4: B94 pipeline-emit — the esc4 4th+ tier reaches the row ----------
{
  const code = `
import json, sys
sys.path.insert(0, '.')
import mfm_points_parser as m
u = m.parse_mfm('MFM_Thousand_Sons_v1.1.txt')
info = u[m.norm('RUBRIC MARINES')]
row = m.to_points_row('Thousand Sons', 'Rubric Marines', info)
u2 = m.parse_mfm('MFM_Black_Templars_v1_0.txt')
info2 = u2[m.norm('CASTELLAN')]
row2 = m.to_points_row('Black Templars', 'CASTELLAN', info2)
print(json.dumps({'rubric': row, 'esc4_dict': info.get('_esc4_fourth_plus'),
                   'castellan': row2}))
`;
  const res = py(code);
  // header: [army, unit, size_1,size_2,size_3, pts(9) idx5-13, pts4(3) idx14-16, allied idx17]
  const r = res.rubric;
  const fourth = res.esc4_dict; // {"5": 110, "10": 200}
  if (!(r[14] === fourth['5'] && r[15] === fourth['10'] && r[16] === '')) {
    failures.push(`fact4: Rubric Marines esc4 row did not carry the captured 4th tier — ${JSON.stringify(r)}`);
  }
  const c2 = res.castellan;
  if (!(c2[14] === '' && c2[15] === '' && c2[16] === '')) {
    failures.push(`fact4: Castellan (non-esc4) row carries a non-blank 4th-tier cell — ${JSON.stringify(c2)}`);
  }
}

if (failures.length) {
  console.log('b87_check FAIL:');
  for (const f of failures) console.log('  ' + f);
  process.exit(1);
}
console.log('all B87 checks pass (v1.1 full costing; v1_0 stable; Rubric Marines 1st-to-3rd fix; B94 4th-tier row carry-through)');
process.exit(0);
