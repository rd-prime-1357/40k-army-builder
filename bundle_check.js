// bundle_check.js — B36. Loads the real buildLoadoutHtml out of index.html and asserts
// the bundle-vs-loadout suppression on the two units that carry both a bundled_swaps
// entry and a unit_loadouts.json def (Captain 000000073, Lieutenant 000001346).
// Usage: node bundle_check.js index.html unit_loadouts.json units.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const bundles = slice(lines, 'function bundleChosenEndpoint', 'function buildWargearHtml');
  const loadout = slice(lines, 'function loMaxCount', 'function loStepper');
  const rows    = slice(lines, 'function loStepper', 'function loadoutWeaponHtml');
  // B47: buildLoadoutHtml now references the inline-detail helpers (mkDetail,
  // itemDetailHtml, groupDetailHtml, …). Pull that block in too.
  const detail  = slice(lines, 'let _detSeq = 0;', 'function buildModalFull');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
function esc(s){return String(s);}
let dsWargearAbilities={};
function glossaryDesc(){return '';}
let lists=[], allUnits=[];
`;
  return new Function(prelude + bundles + '\n' + loadout + '\n' + rows + '\n' + detail + `
return { buildLoadoutHtml, setUnits: (u)=>{allUnits=u;} };`)();
}

const E = loadEngine(process.argv[2]);
const L = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const U = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));

const raws = {};
const flat = [];
for (const b of U) for (const u of b.units) { raws[u.unit_id] = u; flat.push(u); }
E.setUnits(flat);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

// Count how many distinct controls offer a given weapon name: bundle endpoint labels
// plus rendered loadout choice rows.
function neoCount(html, raw) {
  let n = 0;
  for (const b of (raw.bundled_swaps || []))
    for (const ep of (b.endpoints || []))
      if (/neo.?volkite/i.test(ep.label || '')) n++;
  n += (html.match(/[Nn]eo.?volkite/g) || []).length;
  return n;
}

function render(id, wargear) {
  const raw = raws[id], def = L[id];
  const entry = { listId: 1, size: 1, wargear: wargear || {} };
  return { html: E.buildLoadoutHtml(entry, def, raw), entry, raw, def };
}

console.log('Lieutenant 000001346 — bundle at default');
{
  const r = render('000001346', {});
  ok(!/Neo-volkite pistol \+ Master-crafted power weapon/i.test(r.html),
     'the atomic 3-for-3 swap is not re-offered by the loadout panel (bundle owns it)');
  ok(neoCount(r.html, r.raw) === 1, 'neo-volkite pistol is offered exactly once (bundle endpoint only)');
  ok(/Master-Crafted Bolter Options/.test(r.html), 'master-crafted bolter pane renders');
  ok(/Bolt Pistol Options/.test(r.html),           'bolt pistol pane renders');
  ok(/Close Combat Weapon Options/.test(r.html),   'close combat weapon pane renders');
  const keeps = (r.html.match(/Keep /g) || []).length;
  ok(keeps === 3, `three independent choice clusters, not one merged radio (found ${keeps} "Keep" rows)`);
}

console.log('Lieutenant 000001346 — acceptance (Ryan, corrected S54): master-crafted bolter KEPT + heavy bolt pistol + power fist');
{
  // The master-crafted bolter is left alone (cho_1 unset). sng_3 swaps the bolt pistol for a
  // heavy bolt pistol (Datasheets_options.csv 000001346 line 3). cho_4 swaps the close combat
  // weapon for a power fist (line 4). Nothing on this datasheet couples the three.
  const r = render('000001346', { sng_3: 'Heavy bolt pistol', cho_4: 'Power fist' });
  ok(r.entry.wargear.sng_3 === 'Heavy bolt pistol', 'heavy bolt pistol survives the render (not cleared)');
  ok(r.entry.wargear.cho_4 === 'Power fist',        'power fist survives alongside it');
  ok(r.entry.wargear.cho_1 == null,                 'the master-crafted bolter is kept');
  const roll = r.html;
  ok(/Keep Master-crafted bolter/i.test(roll),      'keeping the bolter is still an offered choice');
}

console.log('Lieutenant 000001346 — plasma pistol + power fist (also legal; costs the bolter)');
{
  const r = render('000001346', { cho_1: 'Plasma pistol', cho_4: 'Power fist' });
  ok(r.entry.wargear.cho_1 === 'Plasma pistol', 'plasma pistol survives the render (not cleared)');
  ok(r.entry.wargear.cho_4 === 'Power fist',    'power fist survives the render alongside it');
}

console.log('Lieutenant 000001346 — atomic bundle endpoint engaged');
{
  const raw = raws['000001346'], def = L['000001346'];
  const entry = { listId: 1, size: 1, wargear: { cho_1: 'Plasma pistol', bundle_0: 'lt-nvp-mcpw-shield' } };
  const html = E.buildLoadoutHtml(entry, def, raw);
  ok(!/Options/.test(html), 'every per-slot loadout pane is hidden while the atomic swap is chosen');
  ok(entry.wargear.cho_1 == null, 'a stale per-slot pick is cleared, so it cannot leak into the rollup');
}

console.log('Captain 000000073 — bundle owns the whole loadout');
{
  const r = render('000000073', {});
  ok(r.html.trim() === '', 'no loadout panes render; the bundle picker is the single control');
}

console.log(fail ? `\n${fail} bundle check(s) FAILED` : '\nall bundle checks pass');
process.exit(fail ? 1 : 0);
