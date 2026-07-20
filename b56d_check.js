// b56d_check.js — B56d. Loads the real resolveUnits / applyChapterPointOverrides
// out of index.html and proves: chapter-scoped overrides apply only under the
// chapters that carry them, never leak into a different chapter's view, never
// mutate the shared generic unit object, and the generic Adeptus Astartes view
// always sees the base price.
// Usage: node b56d_check.js index.html units.json faction_taxonomy.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}
function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const block = slice(lines, 'function applyChapterPointOverrides', 'function setActiveUnits');
  return new Function('unitsByArmy', block + '\nreturn {applyChapterPointOverrides, resolveUnits};')({});
}

const units = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const taxonomy = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));

// Rebuild unitsByArmy the same way index.html does.
const unitsByArmy = {};
units.forEach(b => { unitsByArmy[b.army] = b.units; });

const lines = fs.readFileSync(process.argv[2], 'utf8').split('\n');
const block = slice(lines, 'function applyChapterPointOverrides', 'function setActiveUnits');
const fn = new Function('unitsByArmy', block + '\nreturn {applyChapterPointOverrides, resolveUnits};')(unitsByArmy);

function findFaction(name) {
  for (const g of taxonomy.groups) {
    const f = g.factions.find(x => x.name === name);
    if (f) return f;
  }
  return null;
}

let pass = 0, fail = 0;
function ok(label, cond) {
  if (cond) { pass++; console.log('  ok   ' + label); }
  else { fail++; console.log('  FAIL ' + label); }
}

const repulsorId = '000002722';
const genericRepulsor = unitsByArmy['Adeptus Astartes'].find(u => u.unit_id === repulsorId);
ok('generic Repulsor Executioner base price 240/260',
   genericRepulsor.points.sizes[0].first_unit === 240 && genericRepulsor.points.sizes[0].third_plus === 260);

// Overridden chapters: Space Wolves, Blood Angels, Dark Angels, Deathwatch -> 230/250
for (const chName of ['Space Wolves', 'Blood Angels', 'Dark Angels', 'Deathwatch']) {
  const fac = findFaction(chName);
  const resolved = fn.resolveUnits(fac);
  const u = resolved.find(x => x.unit_id === repulsorId);
  ok(`Repulsor Executioner reads 230 under ${chName}`, u.points.sizes[0].first_unit === 230);
  ok(`Repulsor Executioner reads 250 (third+) under ${chName}`, u.points.sizes[0].third_plus === 250);
}

// Non-overridden chapter or generic view keeps 240/250 (base). Try Ultramarines
// (a chapter without an override) and the generic Adeptus Astartes faction.
const facUM = findFaction('Ultramarines');
if (facUM) {
  const resolvedUM = fn.resolveUnits(facUM);
  const uUM = resolvedUM.find(x => x.unit_id === repulsorId);
  ok('Repulsor Executioner reads 240 (base) under Ultramarines (no override)',
     uUM.points.sizes[0].first_unit === 240);
}
const facGeneric = findFaction('Adeptus Astartes') || findFaction('Space Marines');
if (facGeneric) {
  const resolvedGeneric = fn.resolveUnits(facGeneric);
  const uGeneric = resolvedGeneric.find(x => x.unit_id === repulsorId);
  ok('Repulsor Executioner reads 240 (base) under the generic view',
     uGeneric.points.sizes[0].first_unit === 240);
}

// Blood-Angels-only override: Assault Intercessor Squad 80/150 under BA,
// stays 75/150 under Dark Angels (a different chapter's view, no leak).
const aisId = '000001606';
const facBA = findFaction('Blood Angels');
const facDA = findFaction('Dark Angels');
const resolvedBA = fn.resolveUnits(facBA);
const resolvedDA = fn.resolveUnits(facDA);
const uAIS_BA = resolvedBA.find(x => x.unit_id === aisId);
const uAIS_DA = resolvedDA.find(x => x.unit_id === aisId);
ok('Assault Intercessor Squad reads 80 under Blood Angels', uAIS_BA.points.sizes[0].first_unit === 80);
ok('Assault Intercessor Squad stays 75 under Dark Angels (no leak)', uAIS_DA.points.sizes[0].first_unit === 75);

// Object identity: the shared generic unit object itself must be untouched
// after resolving Blood Angels (no in-place mutation of unitsByArmy).
ok('generic unitsByArmy object for Repulsor Executioner still reads 240 after BA resolve',
   genericRepulsor.points.sizes[0].first_unit === 240);
ok('generic unitsByArmy object for Assault Intercessor Squad still reads 75 after BA resolve',
   unitsByArmy['Adeptus Astartes'].find(u => u.unit_id === aisId).points.sizes[0].first_unit === 75);

console.log('');
if (fail) { console.log(fail + ' B56d check(s) FAILED'); process.exit(1); }
console.log('all B56d checks pass');
