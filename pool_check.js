// pool_check.js — B18e. The coverage gap that let B18b's bug survive: a shared
// pool_id spanning TWO OR MORE model groups on COUNT options. B18b/D126 taught only
// the multi-model count branch and the add branches about pools; the fixed-1 count
// branch stayed pool-blind, so a generic capped swap fanned onto a leader/sergeant
// over-emitted (every group granted the full swap independently).
//
// Loads the real loRollup + wargearCostForRollup out of index.html and drives them
// against the two fanned fixture defs (000000241, 000002748) from B18c_repro_fixture.json
// — the exact cross-group pooled-count case. Seeds every pooled count high so the
// engine's own cap governs, then asserts the UNIT-WIDE cap on both emitted weapons
// and points. A synthetic price on the grenade launcher gives the points assertion
// teeth (real data leaves these units unpriced).
//
// MUST FAIL on the pre-B18e engine, PASS on the fixed one.
// Usage: node pool_check.js index.html B18c_repro_fixture.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  return lines.slice(s, e).join('\n');
}
function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const rollup = slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.');
  const cost   = slice(lines, 'function wargearCostForRollup', 'function wargearCostForEntry');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
let wargearPoints = {};`;
  return new Function(prelude + rollup + '\n' + cost +
    '\nreturn {loRollup, wargearCostForRollup, setPts:(p)=>{wargearPoints=p;}};')();
}

const E = loadEngine(process.argv[2] || 'index.html');
const FIX = JSON.parse(fs.readFileSync(process.argv[3] || 'B18c_repro_fixture.json', 'utf8'));

const GL = 'Astartes grenade launcher';
const PRICE = 5;   // synthetic, so cost tracks the capped weapon count

// Price the grenade launcher for both fixture units.
const pts = {};
for (const uid of Object.keys(FIX)) pts[uid] = { items: { [GL.toLowerCase()]: { cost: PRICE } } };
E.setPts(pts);

// Seed every pooled count high; the engine's cap must clamp it.
function seedAllHigh(def) {
  const s = { choiceById: {}, countById: {}, addById: {} };
  for (const o of def.options) {
    if (o.type === 'count') s.countById[o.id] = 99;
    else if (o.type === 'add') s.addById[o.id] = 99;
  }
  return s;
}
function rollGL(uid, size) {
  const def = FIX[uid];
  const roll = E.loRollup(def, size, seedAllHigh(def));
  const gl = roll.weapons.get(GL) || 0;
  const cost = E.wargearCostForRollup(uid, roll);
  return { gl, cost, over: roll.overAllocated };
}

let fail = 0;
const ck = (name, got, want) => {
  const ok = got === want;
  if (!ok) fail++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${name}: got ${got} want ${want}`);
};

// Command Squad 000002748: three fixed-1 groups, one pooled count each. Legal 1 per 3.
{
  const r = rollGL('000002748', 3);
  ck('Command Squad @3 grenade launchers', r.gl, 1);
  ck('Command Squad @3 points', r.cost, 1 * PRICE);
}
// Ravenwing Black Knights 000000241: fixed-1 Huntmaster + fills_to_size body, pooled count on each.
{
  const r3 = rollGL('000000241', 3);
  ck('RBK @3 grenade launchers', r3.gl, 1);
  ck('RBK @3 points', r3.cost, 1 * PRICE);
  const r6 = rollGL('000000241', 6);
  ck('RBK @6 grenade launchers', r6.gl, 2);
  ck('RBK @6 points', r6.cost, 2 * PRICE);
}

console.log(fail ? `\n${fail} FAILURES` : '\nall pool checks pass');
process.exit(fail ? 1 : 0);
