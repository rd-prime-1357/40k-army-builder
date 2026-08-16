// b128_check.js — B128 (D345). Loads the real unitInTankAcePool / entryTankAceActive /
// entryEffectiveType / canSetTankAce / setTankAce / enhancementTypeEligible out of
// index.html and proves the Headhunter Task Force cap is a real, D0-safe capped pick:
//
//   1. A qualifying Vehicle (base_keyword match, no except) is in the pool; a Fly/
//      Walker/Drop Pod/Fortification unit is not, even when it carries the base
//      keyword — both except arms tested separately.
//   2. The pool is empty when the granting detachment is not in `selectedDetachments`
//      (deriving nothing without the key, not just filtering an offer list).
//   3. canSetTankAce refuses a 4th check once 3 are active — the cap is enforced at
//      the gate, not after the fact — and never refuses an uncheck.
//   4. entryTankAceActive requires BOTH entry.tankAce and current pool membership: a
//      checked entry whose detachment gets deselected goes inactive, not silently true.
//   5. entryEffectiveType flips to 'Character' only while active, and
//      enhancementTypeEligible/the Warlord filter follow that flip — an Epic Hero
//      exclusion elsewhere is untouched (E23 doesn't grant Epic Hero anything).
//   6. tankAceActiveCount only counts active picks — a stale checked box doesn't
//      occupy a cap slot, matching point 4's staleness reading.
//   7. Round-trip through the real detachment_effects.json: the six shipped
//      Headhunter rows are enforced:true and cap:3 (the flip this session made).
//
// Build-time only; not part of the served app.
// Usage: node b128_check.js index.html detachment_effects.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function load(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const tankAceSrc = slice(lines, '── E23/B128: tank_ace capped Character selection', '── E23/B128 block end');
  const enhTypeSrc = slice(lines, 'function enhancementTypeEligible', 'function canAssignEnhancement');

  const prelude = `
    let armyList = [];
    let detachmentEffects = {};
    let rawUnits = [];
    let selectedDetachments = [];
    function flashBanner(msg) { flashBanner.lastMsg = msg; }
    function renderAll() { renderAll.calls = (renderAll.calls || 0) + 1; }
    function setState({ list, effects, raw, keys }) {
      armyList = list; detachmentEffects = effects; rawUnits = raw; selectedDetachments = keys;
    }
  `;

  return new Function(
    prelude + '\n' + tankAceSrc + '\n' + enhTypeSrc + '\n' +
    'return { setState, flashBanner, renderAll,' +
    ' unitInTankAcePool, entryTankAceActive, entryEffectiveType, tankAceActiveCount,' +
    ' canSetTankAce, setTankAce, enhancementTypeEligible, TANK_ACE_CAP,' +
    ' getArmyList: () => armyList };'
  )();
}

function fail(msg) { console.log('FAIL b128_check    ' + msg); process.exitCode = 1; }

const idxPath = process.argv[2] || 'index.html';
const dePath  = process.argv[3] || 'detachment_effects.json';
const M = load(idxPath);

let failures = 0;
function check(cond, msg) {
  if (!cond) { fail(msg); failures++; }
}

const HH_KEY = 'Space Marines|HEADHUNTER TASK FORCE';
const effects = {
  [HH_KEY]: {
    army: 'Space Marines', detachment: 'Headhunter Task Force',
    effects: [{
      kind: 'tank_ace',
      target: { base_keyword: 'Vehicle', except_keywords: ['Fly', 'Walker', 'Drop Pod'], except_unit_types: ['Fortification'] },
      cap: 3, enforced: true
    }]
  }
};

function rawUnit(name, unit_type, keywords) {
  return { unit_name: name, unit_type, model_groups: [{ keyword_names: keywords }] };
}

const raws = [
  rawUnit('Repulsor Executioner A', 'Vehicle', ['Vehicle', 'Transport']),
  rawUnit('Repulsor Executioner B', 'Vehicle', ['Vehicle', 'Transport']),
  rawUnit('Repulsor Executioner C', 'Vehicle', ['Vehicle', 'Transport']),
  rawUnit('Repulsor Executioner D', 'Vehicle', ['Vehicle', 'Transport']),
  rawUnit('Stormtalon Gunship', 'Vehicle', ['Vehicle', 'Fly', 'Aircraft']),        // except_keywords
  rawUnit('Dreadnought', 'Vehicle', ['Vehicle', 'Walker']),                        // except_keywords
  rawUnit('Hammerfall Bunker', 'Fortification', ['Vehicle']),                      // except_unit_types
  rawUnit('Intercessor Squad', 'Infantry', ['Infantry']),                          // no base_keyword at all
];

function entry(id, name, checked) {
  return { listId: id, unit_name: name, unit_type: 'Vehicle', unresolved: false, tankAce: !!checked };
}

// ── 1. Pool membership: base match, both except arms, no-match ─────────────
{
  M.setState({ list: [], effects, raw: raws, keys: [HH_KEY] });
  check(M.unitInTankAcePool(raws[0], [HH_KEY]) === true, 'qualifying Vehicle should be in the pool');
  check(M.unitInTankAcePool(raws[4], [HH_KEY]) === false, 'Fly Vehicle should be excluded (except_keywords)');
  check(M.unitInTankAcePool(raws[5], [HH_KEY]) === false, 'Walker Vehicle should be excluded (except_keywords)');
  check(M.unitInTankAcePool(raws[6], [HH_KEY]) === false, 'Fortification should be excluded (except_unit_types)');
  check(M.unitInTankAcePool(raws[7], [HH_KEY]) === false, 'non-Vehicle should never match base_keyword');
}

// ── 2. No selected detachment -> empty pool ─────────────────────────────────
{
  check(M.unitInTankAcePool(raws[0], []) === false, 'pool must be empty with no detachment selected');
  check(M.unitInTankAcePool(raws[0], ['Space Marines|SOME OTHER DETACHMENT']) === false,
        'a non-granting selected detachment must not open the pool');
}

// ── 3. Cap enforcement at the gate, both directions ─────────────────────────
{
  const list = [entry(1, 'Repulsor Executioner A', true), entry(2, 'Repulsor Executioner B', true),
                entry(3, 'Repulsor Executioner C', true), entry(4, 'Repulsor Executioner D', false)];
  M.setState({ list, effects, raw: raws, keys: [HH_KEY] });
  const gate4th = M.canSetTankAce(list[3], true, [HH_KEY]);
  check(gate4th.ok === false && gate4th.reason === 'cap', 'checking a 4th pick must be refused at the gate (cap)');
  const gateUncheck = M.canSetTankAce(list[0], false, [HH_KEY]);
  check(gateUncheck.ok === true, 'unchecking an already-checked entry must never be refused');
  // Re-checking the SAME already-checked entry (checked -> checked) must not
  // self-block against its own slot.
  const gateReCheck = M.canSetTankAce(list[0], true, [HH_KEY]);
  check(gateReCheck.ok === true, 're-affirming an already-checked entry must not self-block on the cap');
}

// ── 4/6. Staleness: checked but detachment deselected -> inactive, no cap slot ──
{
  const list = [entry(1, 'Repulsor Executioner A', true), entry(2, 'Repulsor Executioner B', true),
                entry(3, 'Repulsor Executioner C', true)];
  M.setState({ list, effects, raw: raws, keys: [] }); // detachment deselected
  check(M.entryTankAceActive(list[0], []) === false, 'a checked entry must go inactive when its detachment is deselected');
  check(M.tankAceActiveCount([]) === 0, 'a stale checked entry must not occupy a cap slot');
  // Re-selecting the detachment restores active status with no re-click needed —
  // the check itself was never cleared (S139 flag-don't-drop).
  check(M.entryTankAceActive(list[0], [HH_KEY]) === true, 'active status must be restored once the detachment is reselected');
}

// ── 5. Effective type flip drives enhancement + (by extension) Warlord eligibility ──
{
  const list = [entry(1, 'Repulsor Executioner A', true), entry(2, 'Repulsor Executioner B', false)];
  M.setState({ list, effects, raw: raws, keys: [HH_KEY] });
  check(M.entryEffectiveType(list[0], [HH_KEY]) === 'Character', 'an active Tank Ace pick must present as Character');
  check(M.entryEffectiveType(list[1], [HH_KEY]) === 'Vehicle', 'an unchecked entry must keep its own unit_type');
  check(M.enhancementTypeEligible(M.entryEffectiveType(list[0], [HH_KEY]), false) === true,
        'an active Tank Ace entry must be enhancement-eligible for a non-Upgrade row');
  check(M.enhancementTypeEligible(M.entryEffectiveType(list[1], [HH_KEY]), false) === false,
        'an inactive Vehicle entry must stay enhancement-ineligible for a non-Upgrade row');
}

// ── 7. Shipped data: the six Headhunter rows are enforced:true, cap:3 ──────
{
  const de = JSON.parse(fs.readFileSync(dePath, 'utf8'));
  const hhKeys = Object.keys(de.effects).filter(k => k.includes('HEADHUNTER TASK FORCE'));
  check(hhKeys.length === 6, `expected 6 Headhunter Task Force rows in ${dePath}, found ${hhKeys.length}`);
  for (const k of hhKeys) {
    const eff = (de.effects[k].effects || []).find(e => e.kind === 'tank_ace');
    check(!!eff, `${k}: no tank_ace effect found`);
    if (eff) {
      check(eff.enforced === true, `${k}: expected enforced:true, got ${eff.enforced}`);
      check(eff.cap === 3, `${k}: expected cap:3, got ${eff.cap}`);
      check(!('unenforced_reason' in eff), `${k}: unenforced_reason should be removed once enforced:true`);
    }
  }
}

if (failures === 0) {
  console.log('PASS b128_check    all B128 checks pass (pool exclusions, empty-pool-without-key, cap gate both directions, staleness, effective-type flip, shipped data enforced)');
} else {
  console.log(`FAIL b128_check    ${failures} check(s) failed`);
  process.exitCode = 1;
}
