// b31_check.js — B31 (Wulfen Dreadnought `000004133`).
//
// The datasheet's two option lines cannot be expressed as loadout swaps:
//
//   1. "This model's Fenrisian greataxe or great wolf claw and storm bolter can be
//       replaced with 1 blizzard shield and 1 heavy flamer."   -> OR_SOURCE_UNSUPPORTED
//   2. "If this model is not equipped with a storm bolter, its heavy flamer can be
//       replaced with 1 storm bolter."                          -> UNMATCHED
//
// Both are represented instead as a single 5-endpoint `owns` bundle. This harness
// loads the real engine out of index.html and asserts, against the committed
// units.json / unit_loadouts.json:
//
//   * the bundle exists with exactly the five legal endpoints and one default;
//   * each endpoint rolls up to the exact legal weapon set (the point of the ticket —
//     in particular the storm bolter IS consumed by the shield-and-flamer builds and
//     IS retained by the shield-and-bolter builds);
//   * the Blizzard Shield 4+ invulnerable save is conferred on every non-default
//     endpoint and on none of the default;
//   * the stale loadout option `sng_1` is suppressed by the bundle, so the unit
//     renders one control and the truncated swap can never be picked.
//
// Usage: node b31_check.js index.html units.json unit_loadouts.json datasheet_wargear_abilities.json

const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  if (s === -1) throw new Error(`slice start not found: ${startNeedle}`);
  const e = lines.findIndex((l, i) => i > s && l.includes(endNeedle));
  if (e === -1) throw new Error(`slice end not found: ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const body = [
    slice(lines, 'const PROFILE_SEP', 'function groupByType'),
    slice(lines, 'function bundleChosenEndpoint', 'function statOverrideFromText'),
    slice(lines, 'function statOverrideFromText', 'function activeWeaponStatOverrides'),
    slice(lines, 'const _condMarker', 'function unitMaxModels'),
    slice(lines, 'function isSingleModelGroup', '// ── B15 / D105'),
    slice(lines, 'function wargearAbilityDesc', 'function loDefNamesItem'),
    slice(lines, 'function loDefNamesItem', 'function statGroupScopes'),
    slice(lines, 'function statGroupScopes', 'function wargearCarrierState'),
    slice(lines, 'function wargearCarrierState', 'function allWargearAbilityNames'),
    slice(lines, 'function wargearCarrierStateUnit', '// B46 / D112'),
    slice(lines, 'function wargearAbilityMode', 'function conferredStats'),
    slice(lines, 'function conferredStats', '// Weapon add/remove from the chosen'),
    slice(lines, 'function activeBundleWeaponDelta', 'function bundleSuppressesLoadout'),
    slice(lines, 'function bundleSuppressesLoadout', 'function buildWargearHtml'),
    slice(lines, 'function loMaxCount', 'function loadoutSize'),
    slice(lines, 'function loadoutSize', 'function buildLoadoutHtml'),
  ].join('\n');

  const prelude = `
    let allUnits = [], armyData = [], loadoutDefs = {},
        dsWargearAbilities = {}, weaponAbilitiesLookup = {}, wargearPts = {};
    function glossaryDesc(n) { return weaponAbilitiesLookup[n] || ''; }
  `;
  return new Function(prelude + body + `
    return {
      setLoadoutDefs: (d) => { loadoutDefs = d; },
      setArmyData:    (d) => { armyData = d; },
      setAllUnits:    (u) => { allUnits = u; },
      setDsWargear:   (d) => { dsWargearAbilities = d; },
      weaponBase, loRollup, loadoutSelections, loadoutSize, loOptCounts,
      loGroupCounts, loWeaponParts, conferredStats, activeStatOverrides,
      activeBundleGrants, activeBundleWeaponDelta, bundleManagedFamilies,
      bundleSuppressesLoadout, bundleChosenEndpoint, bundleDuplicateSwaps,
      wargearAbilityMode,
    };
  `)();
}

const E = loadEngine(process.argv[2] || 'index.html');

const unitsDoc  = JSON.parse(fs.readFileSync(process.argv[3] || 'units.json', 'utf8'));
const loadouts  = JSON.parse(fs.readFileSync(process.argv[4] || 'unit_loadouts.json', 'utf8'));
const dsWargear = JSON.parse(fs.readFileSync(process.argv[5] || 'datasheet_wargear_abilities.json', 'utf8'));

E.setArmyData(unitsDoc);
E.setLoadoutDefs(loadouts);
E.setDsWargear(dsWargear);

const UID = '000004133';
let RAW = null;
for (const blk of unitsDoc)
  for (const u of blk.units)
    if (u.unit_id === UID) RAW = u;

E.setAllUnits([{ unit_name: RAW.unit_name, sizes: [{ size: 1 }] }]);

const DEF = loadouts[UID];

let fail = 0;
function ck(label, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) fail++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${label}` + (ok ? '' : `: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`));
}
function ckTrue(label, cond) { ck(label, !!cond, true); }

// An entry with the bundle radio set to `epId` (unset = default endpoint).
function entryFor(epId) {
  const wargear = {};
  if (epId) wargear['bundle_0'] = epId;
  return { unit_id: UID, unit_name: RAW.unit_name, size: 1, wargear, otherOptions: {} };
}

// The unit's final weapon families for a chosen endpoint: loadout rollup + bundle delta,
// exactly as loadoutWeaponHtml composes them for display.
function weaponsFor(epId) {
  const entry = entryFor(epId);
  const size  = E.loadoutSize(entry, DEF);
  const roll  = E.loRollup(DEF, size, E.loadoutSelections(entry, DEF), E.loOptCounts(DEF, entry));
  const cmap  = {};
  for (const [k, v] of roll.weapons.entries()) cmap[k.toLowerCase()] = v;
  const bd = E.activeBundleWeaponDelta(entry, RAW);
  for (const r of bd.removes) delete cmap[E.weaponBase(r)];
  for (const a of bd.adds) cmap[E.weaponBase(a)] = (cmap[E.weaponBase(a)] || 0) + 1;
  return Object.keys(cmap).filter(k => cmap[k] > 0).sort();
}

function invFor(epId) {
  const entry = entryFor(epId);
  const mg = RAW.model_groups[0];
  const cs = E.conferredStats(RAW, mg, entry);
  const ov = Object.assign({}, cs.ov, E.activeStatOverrides(entry, RAW));
  return ov.INV || null;
}

// ── 1. Bundle shape ────────────────────────────────────────────────────────
console.log('B31 — bundle shape');
const bundles = RAW.bundled_swaps || [];
ck('exactly one bundle group', bundles.length, 1);
const B = bundles[0] || { endpoints: [] };
ck('bundle owns the loadout slots', B.loadout_relation || 'owns', 'owns');
ck('five endpoints', (B.endpoints || []).length, 5);
ck('exactly one default endpoint', (B.endpoints || []).filter(e => e.is_default).length, 1);
ck('endpoint ids', (B.endpoints || []).map(e => e.id), [
  'wulfen-base',
  'wulfen-shield-flamer-keep-claw',
  'wulfen-shield-flamer-keep-axe',
  'wulfen-shield-bolter-keep-claw',
  'wulfen-shield-bolter-keep-axe',
]);
ckTrue('every non-default endpoint grants Blizzard Shield',
  (B.endpoints || []).filter(e => !e.is_default)
    .every(e => (e.grants || []).some(g => g.ability_name === 'Blizzard Shield')));
ckTrue('the default endpoint grants nothing', (() => {
  const d = (B.endpoints || []).find(e => e.is_default);
  return !!d && (d.grants || []).length === 0;
})());

// ── 2. Legal weapon set per endpoint ───────────────────────────────────────
// Datasheet default: storm bolter; Fenrisian greataxe; great wolf claw.
console.log('\nB31 — weapon rollup per endpoint');
ck('default: storm bolter + both melee weapons', weaponsFor(null),
   ['fenrisian greataxe', 'great wolf claw', 'storm bolter']);

// Line 1 consumes ONE melee weapon AND the storm bolter. The storm bolter going
// away is the whole point of the "or ... and" source the parser could not express.
ck('shield+flamer, keep claw: greataxe AND storm bolter consumed',
   weaponsFor('wulfen-shield-flamer-keep-claw'),
   ['great wolf claw', 'heavy flamer']);
ck('shield+flamer, keep axe: wolf claw AND storm bolter consumed',
   weaponsFor('wulfen-shield-flamer-keep-axe'),
   ['fenrisian greataxe', 'heavy flamer']);

// Line 2 swaps that heavy flamer back to a storm bolter. Net vs default: one melee
// weapon gone, shield gained, storm bolter retained — and never a flamer as well.
ck('shield+bolter, keep claw: storm bolter retained, no flamer',
   weaponsFor('wulfen-shield-bolter-keep-claw'),
   ['great wolf claw', 'storm bolter']);
ck('shield+bolter, keep axe: storm bolter retained, no flamer',
   weaponsFor('wulfen-shield-bolter-keep-axe'),
   ['fenrisian greataxe', 'storm bolter']);

// No endpoint may leave the model holding both melee weapons and the shield, and
// none may leave it holding both a heavy flamer and a storm bolter.
console.log('\nB31 — endpoint legality invariants');
for (const ep of (B.endpoints || [])) {
  const w = new Set(weaponsFor(ep.is_default ? null : ep.id));
  ckTrue(`${ep.id}: never both melee weapons alongside the shield`,
    ep.is_default || !(w.has('fenrisian greataxe') && w.has('great wolf claw')));
  ckTrue(`${ep.id}: never heavy flamer and storm bolter together`,
    !(w.has('heavy flamer') && w.has('storm bolter')));
  ckTrue(`${ep.id}: always at least one melee weapon`,
    w.has('fenrisian greataxe') || w.has('great wolf claw'));
}

// ── 3. Blizzard Shield invulnerable save ───────────────────────────────────
console.log('\nB31 — Blizzard Shield 4+ invulnerable');
ck('default build has no invulnerable save', invFor(null), null);
for (const ep of (B.endpoints || []).filter(e => !e.is_default))
  ck(`${ep.id}: INV 4+`, invFor(ep.id), '4');
ck('Blizzard Shield row hidden on the default build',
   E.wargearAbilityMode(RAW, entryFor(null), 'Blizzard Shield'), 'none');
ck('Blizzard Shield row shown on a shield build',
   E.wargearAbilityMode(RAW, entryFor('wulfen-shield-flamer-keep-axe'), 'Blizzard Shield'), 'all');

// ── 4. The stale loadout option is suppressed ──────────────────────────────
// `sng_1` is the truncated single-source swap the parser emitted before the bundle
// existed (Fenrisian greataxe -> Blizzard Shield + Heavy flamer, storm bolter never
// consumed, no wolf-claw alternative). The bundle owns that slot, so it must never
// render — otherwise the illegal build is still reachable.
console.log('\nB31 — stale loadout option suppressed');
const managed = E.bundleManagedFamilies(RAW);
ckTrue('bundle claims the Fenrisian greataxe slot', managed.has('fenrisian greataxe'));
ckTrue('bundle claims the great wolf claw slot',   managed.has('great wolf claw'));
ckTrue('bundle claims the storm bolter slot',      managed.has('storm bolter'));
ckTrue('bundle suppresses the loadout options', E.bundleSuppressesLoadout(entryFor(null), RAW));

const sng1 = (DEF.options || []).find(o => o.id === 'sng_1');
ckTrue('sng_1 still present in unit_loadouts.json (parser truth, unchanged)', !!sng1);
ckTrue('sng_1 is bundle-owned, so it is hidden',
  !!sng1 && E.loWeaponParts(sng1.replaces).some(p => managed.has(p)));

// Why suppression matters: sng_1's own rollup produces an illegal build. It keeps the
// storm bolter alongside the new heavy flamer (the "and storm bolter" half of the source
// the parser could not express) and offers no wolf-claw alternative. If the bundle ever
// stopped owning this slot, that build becomes reachable again.
{
  const entry = entryFor(null);
  entry.wargear['sng_1'] = (sng1.choices || [])[0];
  const size = E.loadoutSize(entry, DEF);
  const roll = E.loRollup(DEF, size, E.loadoutSelections(entry, DEF), E.loOptCounts(DEF, entry));
  const w = new Set([...roll.weapons.keys()].map(E.weaponBase));
  ckTrue('sng_1 alone would keep the storm bolter beside a heavy flamer (illegal)',
    w.has('storm bolter') && w.has('heavy flamer'));
  ckTrue('sng_1 alone offers no great-wolf-claw alternative',
    (sng1.choices || []).length === 1);
}

console.log(fail ? `\n${fail} B31 check(s) FAILED` : '\nall B31 checks pass');
process.exit(fail ? 1 : 0);
