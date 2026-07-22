// sweep.js — one dataset, two engines.
// Usage: node sweep.js old_index.html new_index.html unit_loadouts.json
// Compares loRollup output for every unit across singleton and pairwise option scenarios.
const fs = require('fs');
function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const s = lines.findIndex(l => l.includes('function loMaxCount'));
  const e = lines.findIndex(l => l.includes('// Unit Options UI for loadout-defined units.'));
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}`;
  return new Function(prelude + lines.slice(s, e).join('\n') + '\nreturn {loRollup};')();
}
const OLD = loadEngine(process.argv[2]);
const NEW = loadEngine(process.argv[3]);
const L = JSON.parse(fs.readFileSync(process.argv[4] || 'unit_loadouts.json', 'utf8'));

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
const dump = (M, def, size, wg) => {
  const x = M.loRollup(def, size, sel(def, wg));
  return JSON.stringify({ w: [...x.weapons].sort(), e: [...x.equipment].sort(), o: x.overAllocated });
};
function picks(o) {
  const out = [];
  if (o.type === 'choice' && o.choices) for (const c of o.choices) out.push({ [o.id]: c });
  else if (o.type === 'count' && o.replacement_choices) for (const c of o.replacement_choices) out.push({ [o.id]: { [c]: 2 } });
  else if (o.type === 'count') { out.push({ [o.id]: 1 }); out.push({ [o.id]: 2 }); }
  else if (o.type === 'add') out.push({ [o.id]: 1 });
  return out;
}
function scenarios(def) {
  const singles = [];
  for (const o of def.options) singles.push(...picks(o));
  const out = [{}, ...singles];
  // pairwise across distinct options (capped so big units don't explode)
  const byOpt = def.options.map(o => picks(o)).filter(p => p.length);
  for (let i = 0; i < byOpt.length; i++)
    for (let j = i + 1; j < byOpt.length; j++)
      for (const a of byOpt[i]) for (const b of byOpt[j])
        if (out.length < 4000) out.push(Object.assign({}, a, b));
  return out;
}
let cases = 0; const diffs = []; const units = new Set();
for (const uid of Object.keys(L)) {
  if (uid.startsWith('_')) continue;
  const def = L[uid];
  if (!def.model_groups || !def.options) continue;
  const sizes = def.size_brackets && def.size_brackets.length ? def.size_brackets : [1];
  const scen = scenarios(def);
  for (const s of sizes) for (const wg of scen) {
    cases++;
    let a, b;
    try { a = dump(OLD, def, s, wg); } catch (err) { a = 'ERR:' + err.message; }
    try { b = dump(NEW, def, s, wg); } catch (err) { b = 'ERR:' + err.message; }
    if (a !== b) { diffs.push({ uid, size: s, wg: JSON.stringify(wg), a, b }); units.add(uid); }
  }
}
console.log(`cases=${cases} diffs=${diffs.length} units=${units.size} [${[...units].join(',')}]`);
for (const d of diffs.slice(0, 60)) console.log(JSON.stringify(d));
