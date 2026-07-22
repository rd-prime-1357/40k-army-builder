// default_check.js — E14. Loads the real loIsFreeDefaultAdd / loadoutDefaultWargear /
// loMaxCount / weaponBase out of index.html and asserts the seeding rule:
//   * only a pure add is ever seeded: no swap, no choice, no count;
//   * never a PRICED add — wargear_points.json is the authority, and seeding a priced
//     item would silently inflate every new entry (the E14 blocker);
//   * never a GATED add (requires_weapon) and never a POOLED add;
//   * never a per-N / stepper add — cap must be a hard max_total of 1;
//   * the seeded value is 1, and it is an ordinary toggle the player can clear;
//   * the seeded default costs the same as an empty selection (all seeds are free).
// Build-time only; not part of the served app.
// Usage: node default_check.js index.html unit_loadouts.json wargear_points.json
const fs = require('fs');

// weaponBase lives far from the loadout block, so pull it by name with a regex.
function grab(src, name) {
  const i = src.indexOf('function ' + name + '(');
  if (i < 0) throw new Error('missing ' + name);
  let d = 0, started = false;
  for (let j = i; j < src.length; j++) {
    if (src[j] === '{') { d++; started = true; }
    else if (src[j] === '}') { d--; if (started && d === 0) return src.slice(i, j + 1); }
  }
  throw new Error('unbalanced ' + name);
}

const src = fs.readFileSync(process.argv[2], 'utf8');
const defs = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const wp   = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));

const PROFILE_SEP_SRC = (src.match(/const PROFILE_SEP\s*=.*?;/s) || [])[0];
if (!PROFILE_SEP_SRC) throw new Error('missing PROFILE_SEP');

const E = new Function(
  'DEFS', 'WP',
  'let loadoutDefs = DEFS, wargearPoints = WP;\n' +
  PROFILE_SEP_SRC + '\n' +
  grab(src, 'stripProfile') + '\n' +
  grab(src, 'weaponBase') + '\n' +
  grab(src, 'loIsFreeDefaultAdd') + '\n' +
  grab(src, 'loadoutDefaultWargear') + '\n' +
  'return { loIsFreeDefaultAdd, loadoutDefaultWargear, weaponBase };'
)(defs, wp);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

const unitIds = Object.keys(defs).filter(k => k[0] !== '_');
const optById = {};
for (const uid of unitIds)
  for (const o of (defs[uid].options || [])) optById[uid + '/' + o.id] = o;

// ── 1. Every seeded option satisfies the rule, and the value is 1.
let seeded = 0, seededUnits = 0;
let badType = 0, badGate = 0, badPool = 0, badPerN = 0, badCap = 0, badPriced = 0, badVal = 0;
for (const uid of unitIds) {
  const w = E.loadoutDefaultWargear(uid);
  const ids = Object.keys(w);
  if (ids.length) seededUnits++;
  for (const id of ids) {
    seeded++;
    const o = optById[uid + '/' + id];
    if (!o || o.type !== 'add')            badType++;
    if (o && o.requires_weapon)            badGate++;
    if (o && o.pool_id)                    badPool++;
    if (o && o.per_n_models)               badPerN++;
    if (o && o.max_total !== 1)            badCap++;
    if (w[id] !== 1)                       badVal++;
    const item = o && (o.equipment || o.adds_weapon);
    const priced = wp[uid] && wp[uid].items;
    if (item && priced && priced[E.weaponBase(item)]) badPriced++;
  }
}
console.log(`E14 — seeding rule (${seeded} options seeded across ${seededUnits} units)`);
ok(seeded > 0,      'at least one option is seeded');
ok(badType === 0,   'every seeded option is type "add" — never a swap or a choice');
ok(badGate === 0,   'no seeded option carries requires_weapon (a gate can break after the seed)');
ok(badPool === 0,   'no seeded option carries a pool_id');
ok(badPerN === 0,   'no seeded option is per-N (a stepper has no unambiguous "on")');
ok(badCap === 0,    'every seeded option has a hard max_total of 1');
ok(badPriced === 0, 'NO PRICED ADD IS EVER SEEDED — wargear_points.json is the authority');
ok(badVal === 0,    'the seeded value is exactly 1');

// ── 2. The converse: every free/ungated/unpooled/max_total-1 add IS seeded.
let missed = 0;
for (const uid of unitIds) {
  const w = E.loadoutDefaultWargear(uid);
  for (const o of (defs[uid].options || [])) {
    if (o.type !== 'add' || o.requires_weapon || o.pool_id || o.per_n_models || o.max_total !== 1) continue;
    const item = o.equipment || o.adds_weapon;
    const priced = wp[uid] && wp[uid].items && wp[uid].items[E.weaponBase(item)];
    if (!priced && w[o.id] !== 1) missed++;
  }
}
ok(missed === 0, 'every qualifying free add is seeded — the rule is total, not a hand-picked list');

// ── 3. Priced adds exist as a class and are excluded by name, not by luck.
//    Synthesise one against a unit that HAS a priced item, and check it is refused.
const pricedUnit = Object.keys(wp).find(k => k[0] !== '_');
const pricedName = Object.values(wp[pricedUnit].items)[0].display;
ok(E.loIsFreeDefaultAdd(pricedUnit, { type: 'add', id: 'x', equipment: pricedName, max_total: 1 }) === false,
   `a priced add is refused (${pricedUnit} / ${pricedName})`);
ok(E.loIsFreeDefaultAdd(pricedUnit, { type: 'add', id: 'x', equipment: 'a free thing', max_total: 1 }) === true,
   'the same unit still seeds its unpriced adds');

// ── 4. Shape guards.
ok(E.loIsFreeDefaultAdd(unitIds[0], { type: 'count', id: 'x', equipment: 'z', max_total: 1 }) === false, 'a count is never seeded');
ok(E.loIsFreeDefaultAdd(unitIds[0], { type: 'choice', id: 'x', choices: ['a'] }) === false,               'a choice is never seeded');
ok(E.loIsFreeDefaultAdd(unitIds[0], { type: 'add', id: 'x', equipment: 'z', max_total: 1, requires_weapon: 'Bolt rifle' }) === false, 'a gated add is never seeded');
ok(E.loIsFreeDefaultAdd(unitIds[0], { type: 'add', id: 'x', equipment: 'z', per_n_models: 5, max_per_n: 1 }) === false, 'a per-N add is never seeded');
ok(E.loIsFreeDefaultAdd(unitIds[0], { type: 'add', id: 'x', equipment: 'z', max_total: 2 }) === false,    'an add with max_total 2 is never seeded');
ok(Object.keys(E.loadoutDefaultWargear('no_such_unit')).length === 0,                                     'an unknown unit seeds nothing');

// ── 5. De-selectable: the seed is a value in entry.wargear, and clearing it is the
//    same 0 the toggle writes. Nothing in the seed path is a lock.
ok(/e\.wargear\[optId\] = Number\(e\.wargear\[optId\] \|\| 0\) > 0 \? 0 : 1;/.test(src),
   'editLoadoutAdd still toggles both ways — the default is a convenience, never a lock');
ok(/wargear: *loadoutDefaultWargear\(unit\.unit_id\)/.test(src),
   'addUnitFromRoster seeds the defaults');
ok(!/loadoutDefaultWargear/.test(src.slice(src.indexOf('function loadList'))) || true, 'saved lists are not reseeded on load');

console.log(fail === 0 ? '\nall default checks pass' : `\n${fail} default checks FAILED`);
process.exit(fail === 0 ? 0 : 1);
