// e21c_check.js — E21c / E22b (D204 rulings 1 & 3, D208, D209). Loads the real
// forbid / unlock / warlord block out of index.html and drives it against the
// real detachment_effects.json table and the real units.json pool.
//
// Three effect kinds, all landing on the ADD path or the Warlord pick, all
// governed by D0 — an illegal state is made unreachable, not reached-then-flagged:
//
//   forbid  (Chaos Daemons | SHADOW LEGION) — the set resolves to the two named
//           Daemon Princes (unit_type Character, so a type rule alone would miss
//           them) plus every Epic Hero EXCEPT Be'Lakor. Forbidden units are not
//           offered, the add refuses them with a reason, and selecting the
//           detachment while a forbidden unit is already in the list is refused.
//   unlock  (Death Guard | TALLYBAND SUMMONERS) — the six Plague Legions units
//           are offered ONLY while the detachment is selected (the live D0 leak
//           D204 found) and only up to a points sub-cap keyed by battle size.
//   warlord (Death Guard | TALLYBAND SUMMONERS) — no Plague Legions model is
//           Warlord-eligible while the detachment is selected.
//
// The behaviours worth the harness are the already-in-list forbid case and the
// sub-cap arithmetic at BOTH battle sizes: each would pass an on-state test and
// fail only after a detachment or battle-size change — the shape of bug that
// ships. enforced:false and mode filtering are checked with two tiny synthetic
// tables, because no built row exercises them and a silent regression there
// would apply a rule the data says to hold back.
//
// Build-time only; not part of the served app.
// Usage: node e21c_check.js index.html detachment_effects.json units.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const body = slice(lines, '// ── E21c / E22b: forbid, unlock', '// ── E21c / E22b block end');
  // These globals are read by the block; the harness owns them so it can drive
  // the current selection, battle size, list and pool per scenario.
  const prelude =
    'let armyList = []; let allUnits = []; let selectedDetachments = []; ' +
    'let POINTS_CAP = 2000; let detachmentEffects = {};\n';
  const exports =
    '\nreturn { forbiddenUnitNames, unlockedAlliedGroups, alliedPointsCap, ' +
    'alliedSubtotal, canAddUnitToList, addRefusalText, offerableUnits, ' +
    'detachmentForbidConflicts, warlordBannedByDetachment, entryAlliedError, ' +
    'setEffects: (e) => { detachmentEffects = e; }, ' +
    'setList: (l) => { armyList = l; }, setPool: (u) => { allUnits = u; }, ' +
    'select: (k) => { selectedDetachments = k; }, setCap: (p) => { POINTS_CAP = p; } };';
  return new Function(prelude + body + exports)();
}

const idxPath = process.argv[2] || 'index.html';
const effPath = process.argv[3] || 'detachment_effects.json';
const uniPath = process.argv[4] || 'units.json';

const EFF = JSON.parse(fs.readFileSync(effPath, 'utf8')).effects;
const U   = JSON.parse(fs.readFileSync(uniPath, 'utf8'));
const E   = loadEngine(idxPath);
E.setEffects(EFF);

const blocks = {};
U.forEach(b => { blocks[b.army] = b.units; });
// The lightweight view the app builds in setActiveUnits — the only fields the
// E21c block reads off a unit.
function view(army, name) {
  const u = (blocks[army] || []).find(x => x.unit_name === name);
  if (!u) throw new Error(`fixture missing: ${army} / ${name}`);
  return { unit_name: u.unit_name, unit_type: u.unit_type, alliedGroup: u.allied_group || null };
}
function poolFor(army) {
  return (blocks[army] || []).map(u => ({ unit_name: u.unit_name, unit_type: u.unit_type, alliedGroup: u.allied_group || null }));
}

const SHADOW = 'Chaos Daemons|SHADOW LEGION';
const TALLY  = 'Death Guard|TALLYBAND SUMMONERS';

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

const cdPool = poolFor('Chaos Daemons');
const dgPool = poolFor('Death Guard');
const cdEpicHeroes = cdPool.filter(u => u.unit_type === 'Epic Hero').map(u => u.unit_name);

// ── Section 1: forbid resolves to the right set ──────────────────────────────
{
  const set = E.forbiddenUnitNames([SHADOW], cdPool);
  ok(set.has('Daemon Prince of Chaos'), 'S1: named Daemon Prince (type Character) is forbidden');
  ok(set.has('Daemon Prince of Chaos with Wings'), 'S1: named winged Daemon Prince is forbidden');
  ok(!set.has("Be'Lakor"), "S1: Be'Lakor is exempt despite being an Epic Hero");
  const otherEH = cdEpicHeroes.filter(n => n !== "Be'Lakor");
  ok(otherEH.length === 12, 'S1: fixture has 12 non-Be\'Lakor Epic Heroes (guards D209 arithmetic)');
  ok(otherEH.every(n => set.has(n)), 'S1: every other Epic Hero is caught by type');
  // 2 named Characters + 12 Epic Heroes = 14
  ok(set.size === 14, `S1: forbidden set is exactly 14 (got ${set.size})`);
  ok(!set.has('Bloodthirster'), 'S1: a non-forbidden Daemon unit is not in the set');
  const none = E.forbiddenUnitNames([], cdPool);
  ok(none.size === 0, 'S1: nothing forbidden with no detachment selected (negative control)');
}

// ── Section 2: forbid gates the offer and the add ────────────────────────────
{
  E.select([SHADOW]); E.setPool(cdPool); E.setList([]);
  const dp = view('Chaos Daemons', 'Daemon Prince of Chaos');
  const bl = view('Chaos Daemons', "Be'Lakor");
  const other = view('Chaos Daemons', 'Bloodthirster');

  const g = E.canAddUnitToList(dp, 210);
  ok(g.ok === false && g.reason === 'forbidden', 'S2: add of a forbidden unit is refused (reason forbidden)');
  ok(E.addRefusalText(g).length > 0, 'S2: the refusal carries a reason string (no mute refusal)');
  ok(E.canAddUnitToList(bl, 325).ok === true, "S2: Be'Lakor still adds under Shadow Legion");
  ok(E.canAddUnitToList(other, 300).ok === true, 'S2: a non-forbidden unit still adds');

  E.select([]);
  ok(E.canAddUnitToList(dp, 210).ok === true, 'S2: same Daemon Prince adds once the detachment is deselected');

  const offered = new Set(E.offerableUnits(cdPool, [SHADOW]).map(u => u.unit_name));
  ok(!offered.has('Daemon Prince of Chaos'), 'S2: forbidden unit is not offered in the roster');
  ok(offered.has("Be'Lakor"), "S2: Be'Lakor is still offered");
  ok(offered.has('Bloodthirster'), 'S2: a non-forbidden unit is still offered');
  const offeredNone = new Set(E.offerableUnits(cdPool, []).map(u => u.unit_name));
  ok(offeredNone.has('Daemon Prince of Chaos'), 'S2: with no detachment, the Daemon Prince is offered again');
}

// ── Section 3: forbid covers the unit already in the list ────────────────────
{
  E.setPool(cdPool);
  E.setList([
    { listId: 1, unit_name: 'Daemon Prince of Chaos', unit_type: 'Character', points: 210 },
    { listId: 2, unit_name: 'Bloodthirster', unit_type: 'Monster', points: 300 },
  ]);
  const c = E.detachmentForbidConflicts(SHADOW);
  ok(c.length === 1 && c[0] === 'Daemon Prince of Chaos', 'S3: selecting Shadow Legion conflicts with the present Daemon Prince');

  E.setList([
    { listId: 1, unit_name: "Be'Lakor", unit_type: 'Epic Hero', points: 325 },
    { listId: 2, unit_name: 'Bloodthirster', unit_type: 'Monster', points: 300 },
  ]);
  ok(E.detachmentForbidConflicts(SHADOW).length === 0, "S3: no conflict when only Be'Lakor and non-forbidden units are present");

  // A ghost (unresolved) entry never counts against a forbid conflict.
  E.setList([{ listId: 1, unit_name: 'Daemon Prince of Chaos', unresolved: true, points: 210 }]);
  ok(E.detachmentForbidConflicts(SHADOW).length === 0, 'S3: a ghost entry does not create a conflict');
}

// ── Section 4: unlock offer filter (the live D0 leak) ────────────────────────
{
  const alliedNames = dgPool.filter(u => u.alliedGroup === 'Plague Legions').map(u => u.unit_name);
  ok(alliedNames.length === 6, `S4: fixture has the six Plague Legions units (got ${alliedNames.length})`);

  const without = new Set(E.offerableUnits(dgPool, []).map(u => u.unit_name));
  ok(alliedNames.every(n => !without.has(n)), 'S4: NONE of the six is offered without Tallyband Summoners (D0 leak closed)');
  ok(without.has('Plague Marines'), 'S4: a native Death Guard unit is still offered');

  const withT = new Set(E.offerableUnits(dgPool, [TALLY]).map(u => u.unit_name));
  ok(alliedNames.every(n => withT.has(n)), 'S4: all six are offered once Tallyband Summoners is selected');

  E.select([]); E.setPool(dgPool); E.setList([]);
  const pb = view('Death Guard', 'Plaguebearers');
  const gate = E.canAddUnitToList(pb, 100);
  ok(gate.ok === false && gate.reason === 'not_unlocked', 'S4: adding an allied unit with no unlock is refused (not_unlocked)');
  ok(E.addRefusalText(gate).length > 0, 'S4: the not_unlocked refusal carries a reason string');

  // B114 (S231): Shadow Legion's unlock was re-shaped from a dead enforced:false/keyword
  // stub onto the real allied_group mechanism (Shadow Legion Thralls, 21 units, sourced
  // from Chaos Space Marines). Same D0 leak shape as Plague Legions above, now with a
  // live built row to test rather than a synthetic one.
  const thrallNames = cdPool.filter(u => u.alliedGroup === 'Shadow Legion Thralls').map(u => u.unit_name);
  ok(thrallNames.length === 21, `S4: fixture has the 21 Shadow Legion Thralls units (got ${thrallNames.length})`);

  const cdWithout = new Set(E.offerableUnits(cdPool, []).map(u => u.unit_name));
  ok(thrallNames.every(n => !cdWithout.has(n)), 'S4: NONE of the 21 Thralls units is offered without Shadow Legion');
  ok(cdWithout.has('Bloodthirster'), 'S4: a native Chaos Daemons unit is still offered');

  const cdWithSL = new Set(E.offerableUnits(cdPool, [SHADOW]).map(u => u.unit_name));
  ok(thrallNames.every(n => cdWithSL.has(n)), 'S4: all 21 Thralls units are offered once Shadow Legion is selected');

  E.select([]); E.setPool(cdPool); E.setList([]);
  const cl = view('Chaos Daemons', 'Chaos Lord');
  const slGate = E.canAddUnitToList(cl, 90);
  ok(slGate.ok === false && slGate.reason === 'not_unlocked', 'S4: adding a Thralls unit with no unlock is refused (not_unlocked)');
  ok(E.addRefusalText(slGate).length > 0, 'S4: the Thralls not_unlocked refusal carries a reason string');
}

// ── Section 5: unlock points sub-cap, keyed by battle size ───────────────────
{
  E.setPool(dgPool); E.select([TALLY]);
  const pb = view('Death Guard', 'Plaguebearers');

  ok(E.alliedPointsCap([TALLY], 'Plague Legions', 1000) === 500, 'S5: cap is 500 at Incursion (1000 pts)');
  ok(E.alliedPointsCap([TALLY], 'Plague Legions', 2000) === 1000, 'S5: cap is 1000 at Strike Force (2000 pts)');
  ok(E.alliedPointsCap([TALLY], 'Plague Legions', 3000) === 1500, 'S5: cap is 1500 at Onslaught (3000 pts)');
  ok(E.alliedPointsCap([], 'Plague Legions', 2000) === null, 'S5: cap is null when the group is not unlocked');

  // 450 of allied points already in the list; a native unit alongside does not count.
  E.setList([
    { listId: 1, unit_name: 'Plaguebearers', unit_type: 'Battleline', points: 300 },
    { listId: 2, unit_name: 'Nurglings',     unit_type: 'Other',      points: 150 },
    { listId: 3, unit_name: 'Plague Marines', unit_type: 'Battleline', points: 400 },
  ]);
  ok(E.alliedSubtotal('Plague Legions') === 450, 'S5: subtotal counts only allied units (native Plague Marines excluded)');

  E.setCap(1000);   // cap 500 at Incursion
  ok(E.canAddUnitToList(pb, 40).ok === true, 'S5: at cap 500, 450 + 40 fits');
  const over = E.canAddUnitToList(pb, 60);
  ok(over.ok === false && over.reason === 'allied_cap' && over.cap === 500, 'S5: at cap 500, 450 + 60 is refused (allied_cap)');
  ok(E.addRefusalText(over).length > 0, 'S5: the allied_cap refusal carries a reason string');

  E.setCap(2000);   // cap 1000 at Strike Force — the same add now fits
  ok(E.canAddUnitToList(pb, 60).ok === true, 'S5: the same 60-pt add fits at cap 1000 (cap is battle-size-keyed)');
}

// ── Section 6: warlord cannot_be, detachment-scoped ──────────────────────────
{
  const pb = view('Death Guard', 'Plaguebearers');
  const rot = view('Death Guard', 'Rotigus');            // allied Epic Hero
  const native = view('Death Guard', 'Daemon Prince of Nurgle'); // native character, not allied

  ok(E.warlordBannedByDetachment(pb, [TALLY]) === true, 'S6: a Plague Legions unit cannot be Warlord under Tallyband Summoners');
  ok(E.warlordBannedByDetachment(rot, [TALLY]) === true, 'S6: the ban is by allied_group, so it catches Rotigus too');
  ok(E.warlordBannedByDetachment(pb, []) === false, 'S6: no ban when the detachment is not selected');
  ok(E.warlordBannedByDetachment(native, [TALLY]) === false, 'S6: a native Death Guard character is unaffected');
}

// ── Section 7: mode and enforced filtering (synthetic — no built row exercises it) ──
{
  const syn = {
    // must_be_if_present must NOT act as a cannot_be ban.
    'X|MUSTBE': { effects: [{ kind: 'warlord', mode: 'must_be_if_present', enforced: true, target: { allied_group: 'G' } }] },
    // an enforced:false cannot_be ban must not apply.
    'X|OFF':    { effects: [{ kind: 'warlord', mode: 'cannot_be', enforced: false, target: { allied_group: 'G' } }] },
    // an enforced:false unlock must unlock nothing.
    'X|UNLOFF': { effects: [{ kind: 'unlock', enforced: false, target: { allied_group: 'G' }, points_cap: { '2000': 500 } }] },
    // an enforced:false forbid must forbid nothing.
    'X|FORBOFF':{ effects: [{ kind: 'forbid', enforced: false, target: { units: ['Zzz'] } }] },
  };
  E.setEffects(syn);
  const g = { unit_name: 'G-unit', unit_type: 'Character', alliedGroup: 'G' };
  ok(E.warlordBannedByDetachment(g, ['X|MUSTBE']) === false, 'S7: must_be_if_present does not ban a unit from being Warlord');
  ok(E.warlordBannedByDetachment(g, ['X|OFF']) === false, 'S7: an enforced:false cannot_be ban does not apply');
  ok(E.unlockedAlliedGroups(['X|UNLOFF']).size === 0, 'S7: an enforced:false unlock unlocks nothing');
  ok(E.forbiddenUnitNames(['X|FORBOFF'], [{ unit_name: 'Zzz', unit_type: 'Character' }]).size === 0, 'S7: an enforced:false forbid forbids nothing');
  E.setEffects(EFF);
}

// ── Section 8: entryAlliedError — the render-side over-state (E21d piece 3) ───
// The mirror of the add gate: a unit legal when added but stranded by a LATER
// change elsewhere reads as a roster error, never trimmed. Three branches, all
// on the real data: unlock removed, group over its sub-cap, and forbid-by-import.
{
  const pb     = view('Death Guard', 'Plaguebearers');       // allied
  const nurg   = view('Death Guard', 'Nurglings');           // allied
  const native = view('Death Guard', 'Plague Marines');      // native, no group

  // Branch A — unlock removed (the core piece-3 case).
  E.setPool(dgPool); E.setCap(2000);
  E.setList([{ listId: 1, unit_name: 'Plaguebearers', unit_type: 'Battleline', points: 300 }]);
  E.select([TALLY]);
  ok(E.entryAlliedError(pb) === false, 'S8: an allied unit is NOT flagged while its detachment unlocks it');
  E.select([]);
  ok(E.entryAlliedError(pb) === true, 'S8: the same unit IS flagged once Tallyband Summoners is deselected (stranded)');
  ok(E.entryAlliedError(native) === false, 'S8: a native unit is never flagged by the allied predicate');

  // Branch B — group over its sub-cap after a battle-size drop.
  E.select([TALLY]);
  E.setList([
    { listId: 1, unit_name: 'Plaguebearers', unit_type: 'Battleline', points: 300 },
    { listId: 2, unit_name: 'Nurglings',     unit_type: 'Other',      points: 300 },
    { listId: 3, unit_name: 'Plague Marines', unit_type: 'Battleline', points: 400 },
  ]);
  E.setCap(2000);   // cap 1000 — 600 of allied points is under
  ok(E.entryAlliedError(pb) === false, 'S8: allied unit under the sub-cap is not flagged (600 <= 1000)');
  E.setCap(1000);   // cap 500 — 600 of allied points is now over
  ok(E.entryAlliedError(pb) === true,  'S8: dropping to a battle size whose sub-cap is exceeded flags the group (600 > 500)');
  ok(E.entryAlliedError(nurg) === true, 'S8: every member of the over-cap group is flagged, not one arbitrary victim');
  ok(E.entryAlliedError(native) === false, 'S8: the native unit in the same list is unaffected by the sub-cap');

  // Branch C — forbid seated by import (toggleDetachment refuses it live; import can still seat it).
  E.setPool(cdPool); E.setCap(2000);
  const dp = view('Chaos Daemons', 'Daemon Prince of Chaos');
  const bl = view('Chaos Daemons', "Be'Lakor");
  E.setList([{ listId: 1, unit_name: 'Daemon Prince of Chaos', unit_type: 'Character', points: 210 }]);
  E.select([SHADOW]);
  ok(E.entryAlliedError(dp) === true,  'S8: a forbidden unit seated by import reads as a roster error');
  ok(E.entryAlliedError(bl) === false, "S8: Be'Lakor is exempt from the forbid, so not flagged");
  E.select([]);
  ok(E.entryAlliedError(dp) === false, 'S8: same unit is clean once the forbidding detachment is deselected');
}

console.log(fail === 0 ? '\nall E21c checks pass' : `\n${fail} E21c check(s) failed`);
process.exit(fail === 0 ? 0 : 1);
