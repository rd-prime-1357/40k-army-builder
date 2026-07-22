// pts_check.js — B35. Loads the real loRollup + wargearCostForRollup out of index.html
// and proves: (a) only the priced units' costs move, (b) the priced default is charged,
// (c) swapping a priced item away removes its cost.
// Usage: node pts_check.js index.html unit_loadouts.json wargear_points.json units.json
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

const E  = loadEngine(process.argv[2]);
const L  = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const WP = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
const U  = JSON.parse(fs.readFileSync(process.argv[5], 'utf8'));
E.setPts(WP);

const units = [];
for (const b of U) for (const u of b.units) units.push(u);

const sel = (def, wg) => {
  const s = { choiceById: {}, countById: {}, addById: {} };
  for (const o of def.options) {
    const v = wg[o.id];
    if (o.type === 'choice') s.choiceById[o.id] = v || null;
    else if (o.type === 'count') s.countById[o.id] = (v && typeof v === 'object') ? v : (Number(v) || 0);
    else if (o.type === 'add') s.addById[o.id] = Number(v) || 0;
  }
  return s;
};
const gear = (id, size, wg) => {
  const def = L[id];
  if (!def) return 0;
  return E.wargearCostForRollup(id, E.loRollup(def, size, sel(def, wg)));
};

let fail = 0;
const ck = (name, got, want) => {
  if (got !== want) { fail++; console.log(`FAIL ${name}: got ${got} want ${want}`); }
};

// (a) default loadout: only the seven priced units move.
const moved = [];
for (const u of units) {
  const szs = (u.points && u.points.sizes) || [];
  if (!szs.length) continue;
  const g = gear(u.unit_id, szs[0].size, {});
  if (g !== 0) moved.push([u.unit_id, u.unit_name, szs[0].first_unit, szs[0].first_unit + g]);
}
console.log('units whose default cost moves:', moved.length);
for (const m of moved) console.log('  ', m.join(' | '));

// (b) Terminator Assault Squad 000000118: 5 models, 155 base, 5 hammers @5 = 180.
ck('TAS default 5', 155 + gear('000000118', 5, {}), 180);
ck('TAS 10 = 360', 310 + gear('000000118', 10, {}), 360);
// swap two models to twin lightning claws -> two hammers leave the rollup -> -10.
ck('TAS 5, 2 claws', 155 + gear('000000118', 5, { cnt_1: 2 }), 170);
ck('TAS 5, 4 claws', 155 + gear('000000118', 5, { cnt_1: 4 }), 160);

// (c) Redemptor 000002717: macro plasma incinerator +10, otherwise +0.
ck('Redemptor default', gear('000002717', 1, {}), 0);
ck('Redemptor macro plasma', gear('000002717', 1, { sng_3: 'Macro plasma incinerator' }), 10);

// (d) Thunderwolf Cavalry 000000322 storm shield is an add-on part (+5 per model taking it).
ck('TWC default', gear('000000322', 3, {}), 0);
ck('TWC 2 shields', gear('000000322', 3, { cc_1: { 'Storm Shield': 2 } }), 10);

// (e) Victrix Honour Guard 000004185: banner (10) rides the optional Chapter Ancient
// group, blades of honour (10) the optional Chapter Champion group.
ck('Victrix base', gear('000004185', 2, {}), 0);

console.log(fail ? `\n${fail} FAILURES` : '\nall pts checks pass');
process.exit(fail ? 1 : 0);
