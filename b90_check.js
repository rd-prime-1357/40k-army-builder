// b90_check.js — B90 turn 1 (D276). Loads the real applyChapterPointOverrides +
// resolveUnits out of index.html and proves the two-tier chapter model
// STRUCTURALLY, not by spot-check:
//
//   1. A 'complete'-mode chapter resolves to EXACTLY its own units.json block —
//      no generic Adeptus Astartes unit leaks in.
//   2. A 'complete'-mode chapter NEVER reads unitsByArmy['Adeptus Astartes'] and
//      NEVER calls applyChapterPointOverrides(). Proven with tripwires: a Proxy
//      that counts reads of the generic key, and a call-counting wrapper on the
//      override map. Both must be zero on the complete path.
//   3. A 'union'-mode chapter still unions generic + chapter (chapter wins on a
//      shared name) and still applies the override map — byte-identical to the
//      pre-B90 behavior (regression guard).
//   4. A subfaction with a missing or unrecognized roster_mode falls SAFELY to
//      the union path — the code's defensive default; the data contract that
//      forbids that state is pinned separately by rules_assertions.py B90-1.
//
// No real chapter is flagged 'complete' in this turn's data (the five flip in the
// B90 data turn), so this fixture is how the complete path is exercised now.
//
// Build-time only; not part of the served app.
// Usage: node b90_check.js index.html
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function load(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const overrideSrc = slice(lines, 'function applyChapterPointOverrides', 'function resolveUnits');
  const resolveSrc  = slice(lines, 'function resolveUnits', 'function setActiveUnits');
  const prelude = `
    let __genericReads = 0, __overrideCalls = 0;
    const __blocks = {};
    // Proxy tripwire: every read of the generic key is counted, so the complete
    // path's isolation from the generic pool is provable, not assumed.
    const unitsByArmy = new Proxy(__blocks, {
      get(t, k) { if (k === 'Adeptus Astartes') __genericReads++; return t[k]; }
    });
    function setBlocks(b) { for (const k in b) __blocks[k] = b[k]; }
  `;
  // Wrap the real override function so any call is counted. resolveUnits closes
  // over the same binding, so it sees the wrapper.
  const wrap = `
    const __origACPO = applyChapterPointOverrides;
    applyChapterPointOverrides = function (u, a) { __overrideCalls++; return __origACPO(u, a); };
  `;
  return new Function(
    prelude + overrideSrc + '\n' + wrap + '\n' + resolveSrc + '\n' +
    'return { resolveUnits, setBlocks,' +
    ' stats: () => ({ genericReads: __genericReads, overrideCalls: __overrideCalls }),' +
    ' reset: () => { __genericReads = 0; __overrideCalls = 0; } };'
  )();
}

let fails = 0;
function ok(cond, msg) { if (!cond) { fails++; console.log('  FAIL: ' + msg); } }
const names = arr => arr.map(u => u.unit_name).sort();

const E = load(process.argv[2] || 'index.html');

E.setBlocks({
  'Adeptus Astartes': [
    { unit_name: 'Generic Marine', unit_id: 'g1', points: {} },
    { unit_name: 'Shared',         unit_id: 'g2', points: {} },
  ],
  'Test Complete': [
    { unit_name: 'CompleteOnly', unit_id: 'c1', points: {} },
    // carries an override entry to prove it is NOT applied on the complete path
    { unit_name: 'Shared', unit_id: 'c2', points: {},
      chapter_point_overrides: { 'Test Complete': { sizes: [{ size: 1, first_unit: 999 }] } } },
  ],
  'Test Union': [
    { unit_name: 'UnionOnly', unit_id: 'u1', points: {} },
    { unit_name: 'Shared',    unit_id: 'u2', points: {} },
  ],
});

// 1 + 2 — complete-mode: own block only, no generic read, no override call.
E.reset();
const rc = E.resolveUnits({ name: 'Test Complete', data_army: 'Test Complete', is_subfaction: true, roster_mode: 'complete' });
ok(JSON.stringify(names(rc)) === JSON.stringify(['CompleteOnly', 'Shared']),
   'complete-mode returns exactly its own block, got ' + JSON.stringify(names(rc)));
ok(!names(rc).includes('Generic Marine'), 'complete-mode leaked a generic-only unit');
let s = E.stats();
ok(s.genericReads === 0, 'complete-mode read unitsByArmy["Adeptus Astartes"] (' + s.genericReads + ' reads)');
ok(s.overrideCalls === 0, 'complete-mode called applyChapterPointOverrides (' + s.overrideCalls + ' calls)');
// the override entry must NOT have been applied (Shared keeps its native points)
const sharedC = rc.find(u => u.unit_name === 'Shared');
ok(!(sharedC.points && sharedC.points.sizes && sharedC.points.sizes[0] && sharedC.points.sizes[0].first_unit === 999),
   'complete-mode applied a chapter point override it should never touch');

// complete-mode returns a copy, not the live block (mutation must not bleed back)
rc.push({ unit_name: 'Injected', unit_id: 'x' });
const rc2 = E.resolveUnits({ name: 'Test Complete', data_army: 'Test Complete', is_subfaction: true, roster_mode: 'complete' });
ok(!names(rc2).includes('Injected'), 'complete-mode returned the live block by reference, not a copy');

// 3 — union-mode regression: union + chapter-wins + override applied.
E.reset();
const ru = E.resolveUnits({ name: 'Test Union', data_army: 'Test Union', is_subfaction: true, roster_mode: 'union' });
ok(JSON.stringify(names(ru)) === JSON.stringify(['Generic Marine', 'Shared', 'UnionOnly']),
   'union-mode roster wrong, got ' + JSON.stringify(names(ru)));
const sharedU = ru.find(u => u.unit_name === 'Shared');
ok(sharedU.unit_id === 'u2', 'union-mode chapter copy did not win on the shared name');
s = E.stats();
ok(s.genericReads > 0, 'union-mode did not read the generic pool');
ok(s.overrideCalls === 1, 'union-mode did not apply the override map exactly once (' + s.overrideCalls + ')');

// 4 — missing/unknown roster_mode falls safely to union.
E.reset();
const rn = E.resolveUnits({ name: 'Test Union', data_army: 'Test Union', is_subfaction: true });
ok(JSON.stringify(names(rn)) === JSON.stringify(['Generic Marine', 'Shared', 'UnionOnly']),
   'missing roster_mode did not fall to the union path, got ' + JSON.stringify(names(rn)));
const rx = E.resolveUnits({ name: 'Test Union', data_army: 'Test Union', is_subfaction: true, roster_mode: 'nonsense' });
ok(JSON.stringify(names(rx)) === JSON.stringify(['Generic Marine', 'Shared', 'UnionOnly']),
   'unrecognized roster_mode did not fall to the union path, got ' + JSON.stringify(names(rx)));

if (fails === 0) console.log('all B90 checks pass');
else { console.log(fails + ' B90 check(s) failed'); process.exit(1); }
