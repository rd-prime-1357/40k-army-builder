// stat_check.js — B15 / D105. Loads the real conferredStats + loRollup out of
// index.html and proves the three-way carrier-count rule on real units.
// Usage: node stat_check.js index.html unit_loadouts.json units.json datasheet_wargear_abilities.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  let rollup    = slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.');
  rollup = rollup.replace('function loadoutSize(entry, def) {', 'var loadoutSize = function(entry, def) {')
                 .replace('function loadoutSelections(entry, def) {', 'var loadoutSelections = function(entry, def) {');
  const conferred = slice(lines, 'function statOverrideFromText', '// Weapon add/remove from the chosen bundle endpoints.');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
function baseAbilityName(n){return String(n||'');}
let dsWargearAbilities={}, loadoutDefs={}, allUnits=[], armyData=[];
let rulesLookup={}, abilitiesLookup={}, weaponAbilitiesLookup={}, coreGlossaryLookup={};
function glossaryDesc(n){return rulesLookup[n]||abilitiesLookup[n]||weaponAbilitiesLookup[n]||coreGlossaryLookup[n]||'';}
function activeBundleGrants(){return [];}
`;
  return new Function(prelude + rollup + '\n' + conferred + `
loadoutSize = (entry, def) => entry.__size;
loadoutSelections = (entry, def) => entry.__sel;
return {
  conferredStats, wargearCarrierState, loRollup, loGroupCounts,
  allWargearAbilityNames, wargearAbilityMode,
  set: (o) => { dsWargearAbilities=o.ds; loadoutDefs=o.defs; allUnits=o.units;
                weaponAbilitiesLookup=o.wa; }
};`)();
}

const E   = loadEngine(process.argv[2]);
const L   = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const U   = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
const DS  = JSON.parse(fs.readFileSync(process.argv[5], 'utf8'));
const WA  = JSON.parse(fs.readFileSync('weapon_abilities.json', 'utf8'));

const units = [];
for (const blk of U) for (const u of (blk.units || [])) units.push(u);
const defs = {}; for (const k of Object.keys(L)) if (k[0] !== '_') defs[k] = L[k];
const ds   = {}; for (const k of Object.keys(DS)) if (k[0] !== '_') ds[k] = DS[k];
const wa   = {}; for (const e of WA) wa[e.weapon_ability_name] = e.weapon_ability_description;
E.set({ ds, defs, units, wa });

const byId = {}; for (const u of units) byId[u.unit_id] = u;

let fails = 0;
function check(label, got, want) {
  const g = JSON.stringify(got), w = JSON.stringify(want);
  if (g !== w) { fails++; console.log(`FAIL  ${label}\n        got  ${g}\n        want ${w}`); }
}

// entry stub: size + raw selections, exactly what loadoutSize/loadoutSelections read.
function entryOf(uid, size, sel, otherOptions) {
  return { __size: size, __sel: Object.assign({ choiceById: {}, countById: {}, addById: {} }, sel || {}),
           otherOptions: otherOptions || {}, wargear: {} };
}

// ── 1. Terminator Assault Squad 000000118 — Storm Shield = W4 on THIS datasheet.
//      Default: all 5 models carry a shield -> W override reaches the statline.
{
  // B18/D116: 'Any number of models' fans out — cnt_1 is the SERGEANT group (1 model),
  // cnt_2 is the body (size - 1). Together they can reach EVERY model.
  const raw = byId['000000118'], mg = raw.model_groups[0];
  check('118 default (5) -> W4', E.conferredStats(raw, mg, entryOf('000000118', 5)).ov, { W: '4' });
  // swap 2 of 5 to twin lightning claws -> 3 shields / 5 models -> asterisk, no override
  const some = E.conferredStats(raw, mg, entryOf('000000118', 5, { countById: { cnt_2: 2 } }));
  check('118 2 swapped -> no override', some.ov, {});
  check('118 2 swapped -> W asterisk',  some.flags, { W: true });
  // body fully swapped, Sergeant still holds his shield -> 1 of 5 carries -> still 'some'.
  const most = E.conferredStats(raw, mg, entryOf('000000118', 5, { countById: { cnt_2: 4 } }));
  check('118 body all swapped -> no override', most.ov, {});
  check('118 body all swapped -> W asterisk',  most.flags, { W: true });
  check('118 body all swapped -> not inert',   [...most.inert], []);
  // THE NEGATIVE CASE (D112). B18 lets the Sergeant drop his shield too. At zero
  // carriers the conferred W4 must vanish entirely: no override, no asterisk, inert.
  const none = E.conferredStats(raw, mg, entryOf('000000118', 5, { countById: { cnt_1: 1, cnt_2: 4 } }));
  check('118 zero carriers -> no override', none.ov, {});
  check('118 zero carriers -> no asterisk', none.flags, {});
  check('118 zero carriers -> inert',       [...none.inert], ['Storm Shield']);
}

// ── 2. Wolf Guard Battle Leader 000004130 — Storm Shield = W6 on THIS datasheet.
//      Printed W is 5. The flat glossary would say W4 and regress him. It must not.
{
  const raw = byId['000004130'], mg = raw.model_groups[0];
  check('4130 printed W', mg.W, 5);
  check('4130 default -> W6', E.conferredStats(raw, mg, entryOf('000004130', 1)).ov, { W: '6' });
  // cho_2 replaces the Storm Shield with a pistol -> no shield -> inert, W stays 5
  const gone = E.conferredStats(raw, mg, entryOf('000004130', 1, { choiceById: { cho_2: 'Plasma pistol' } }));
  check('4130 shield traded -> no override', gone.ov, {});
  check('4130 shield traded -> inert',       [...gone.inert], ['Storm Shield']);
}

// ── 3. Wolf Guard Terminators 000000318 — Storm Shield = W4, and it is an OPTION
//      the pack leader cannot take, so it can never reach every model.
{
  const raw = byId['000000318'], mg = raw.model_groups[0];
  const zero = E.conferredStats(raw, mg, entryOf('000000318', 5));
  check('318 default (no shields) -> no override', zero.ov, {});
  check('318 default -> inert',                    [...zero.inert], ['Storm Shield']);
  const two = E.conferredStats(raw, mg, entryOf('000000318', 5, { countById: { cnt_1: 2 } }));
  check('318 2 shields -> no override', two.ov, {});
  check('318 2 shields -> W asterisk',  two.flags, { W: true });
}

// ── 4. The name-keyed lookup is provably wrong: same name, three texts.
{
  const t = n => (ds[n] || {})['Storm Shield'];
  check('118 text',  t('000000118'), 'The bearer has a Wounds characteristic of 4.');
  check('4130 text', t('000004130'), 'The bearer has a Wounds characteristic of 6.');
  check('147 text',  t('000000147'), 'The bearer has a 4+ invulnerable save.');
  check('flat glossary is the 118 text', wa['Storm Shield'], 'The bearer has a Wounds characteristic of 4.');
}

// ── 5. Sweep: no unit gets a characteristic override that LOWERS a printed stat.
//      (D105 says apply literally, but a lowered stat is the exact symptom of a
//      name-keyed misread, so it is worth a tripwire.)
{
  for (const u of units) {
    const def = defs[u.unit_id];
    const size = def && def.size_brackets ? def.size_brackets[0] : 0;
    for (const mg of (u.model_groups || [])) {
      const ov = E.conferredStats(u, mg, def ? entryOf(u.unit_id, size) : null).ov;
      for (const k of ['W']) {
        if (ov[k] == null || mg[k] == null) continue;
        if (Number(ov[k]) < Number(mg[k]))
          check(`${u.unit_id} ${u.unit_name} ${k} lowered ${mg[k]}->${ov[k]}`, 'lowered', 'not lowered');
      }
    }
  }
}

// ── 6. B46. Option-granted wargear abilities reach the popup.
//      (a) The name source is the unit's own datasheet, so nothing in
//      datasheet_wargear_abilities.json is unreachable — this is B46-2 at zero.
{
  let unreachable = 0;
  for (const u of units) {
    const reachable = new Set(E.allWargearAbilityNames(u));
    for (const n of Object.keys(ds[u.unit_id] || {})) if (!reachable.has(n)) unreachable++;
  }
  check('B46: wargear abilities the popup cannot list', unreachable, 0);
}

// (b) Reiver Squad 000002718 — grav-chute and grapnel launcher are OPTION-granted
//     (loadout adds, one per model). The three-way rule runs on the carrier count.
{
  const raw = byId['000002718'];
  check('2718 browse lists both option items',
        E.allWargearAbilityNames(raw).slice().sort(),
        ['Grapnel Launcher', 'Reiver Grav-chute']);
  const none = entryOf('000002718', 5);
  check('2718 no chutes -> none', E.wargearAbilityMode(raw, none, 'Reiver Grav-chute'), 'none');
  const one  = entryOf('000002718', 5, { addById: { add_4: 1 } });
  check('2718 sergeant only -> some', E.wargearAbilityMode(raw, one, 'Reiver Grav-chute'), 'some');
  const all  = entryOf('000002718', 5, { addById: { add_4: 1, add_5: 4 } });
  check('2718 every model -> all', E.wargearAbilityMode(raw, all, 'Reiver Grav-chute'), 'all');
  check('2718 grapnel still none', E.wargearAbilityMode(raw, all, 'Grapnel Launcher'), 'none');
}

// (c) Infiltrator Squad 000000128 — the Helix Gauntlet is a B14 other-option, not a
//     loadout add, and its text is a unit-wide aura from ONE bearer, so a single
//     checked carrier reads as 'all', never an asterisk.
{
  const raw = byId['000000128'];
  const off = entryOf('000000128', 5);
  const on  = entryOf('000000128', 5, {}, { 'Helix Gauntlet': true });
  check('128 gauntlet unchecked -> none', E.wargearAbilityMode(raw, off, 'Helix Gauntlet'), 'none');
  check('128 gauntlet checked -> all',    E.wargearAbilityMode(raw, on,  'Helix Gauntlet'), 'all');
  check('128 comms array unchecked -> none',
        E.wargearAbilityMode(raw, on, 'Infiltrator Comms Array'), 'none');
}

// (d) Default-issue gear is unchanged by B46: the Terminator Assault Squad's storm
//     shield still reads all / some / none off the same carrier count.
{
  const raw = byId['000000118'];
  check('118 default shields -> all',
        E.wargearAbilityMode(raw, entryOf('000000118', 5), 'Storm Shield'), 'all');
  check('118 two traded -> some',
        E.wargearAbilityMode(raw, entryOf('000000118', 5, { countById: { cnt_2: 2 } }), 'Storm Shield'), 'some');
  check('118 all traded -> none',
        E.wargearAbilityMode(raw, entryOf('000000118', 5, { countById: { cnt_1: 1, cnt_2: 4 } }), 'Storm Shield'), 'none');
}

console.log(fails ? `\n${fails} stat check(s) FAILED` : '\nall stat checks pass');
process.exit(fails ? 1 : 0);
