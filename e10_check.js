// e10_check.js — E10 (D148). Loads the real duplicateUnit + its dependency chain
// (getAttachedLeaders, ptsForEntry, unitLimit family) out of index.html and drives
// it against synthetic armyList scenarios: a plain unit, a unit with one non-Epic-Hero
// leader attached, a unit with an Epic Hero leader attached, and a unit already at its
// instance limit. wargearCostForEntry is stubbed to 0 (points-tier math is not what
// this checks — structural duplication + Epic Hero exclusion + limit enforcement are).
//
// E4b: the real enhancement block is loaded too, not stubbed, so the claim that a
// duplicate does NOT inherit its original's enhancement is executed against the real
// code. Carrying it over would put the copy in an illegal state the instant it
// appeared (25.04 allows one of each enhancement in an army), which is the failure
// mode B41 exists to prevent for unit counts.
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s === -1 || e === -1) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const body = [
    slice(lines, 'function battleSizeUnitLimit', 'function limitState'),
    slice(lines, 'function limitState', 'function canAddUnit'),
    slice(lines, 'function canAddUnit', '// State'),
    slice(lines, 'function ptsForEntry', 'function refreshPoints'),
    slice(lines, 'function getAttachedLeaders', 'function addUnitFromRoster'),
    slice(lines, 'function duplicateUnit', '// ── Edit operations'),
    slice(lines, 'function permitsCoLeader', 'function renderAll'),
    slice(lines, '// ── E4b: enhancement assignment rules', '// ── E4b block end'),
  ].join('\n');

  const prelude = `
    let armyList = [];
    let allUnits = [];
    let nextId = 1;
    let selectedListId = null;
    let POINTS_CAP = 2000;
    let detachmentDefs = {};
    let selectedDetachments = [];
    function wargearCostForEntry() { return 0; }
    function flashBanner(msg) { flashed.push(msg); }
    let flashed = [];
    function renderAll() { /* no-op for test */ }
  `;
  return new Function(prelude + body + `
    return {
      setArmyList: (l) => { armyList = l; },
      getArmyList: () => armyList,
      setAllUnits: (u) => { allUnits = u; },
      setNextId: (n) => { nextId = n; },
      duplicateUnit,
      canAttachLeader,
      getFlashed: () => flashed,
      setDetachmentDefs: (d) => { detachmentDefs = d; },
      setSelectedDetachments: (k) => { selectedDetachments = k; },
    };
  `)();
}

const E = loadEngine(process.argv[2] || 'index.html');

let failures = 0;
function check(label, cond) {
  console.log(`  ${cond ? 'ok  ' : 'FAIL'} ${label}`);
  if (!cond) failures++;
}

// unit_type limits: default 3 at 2000pts, Epic Hero always 1
function unit(name, type) { return { unit_name: name, unit_type: type, sizes: [{ size: 5, first_unit: 100, second_unit: 90, third_plus: 80 }] }; }

// ── Scenario 1: plain unit, no leaders ──────────────────────────────────────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry')]);
  E.setNextId(10);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: { a: 'x' }, otherOptions: {}, attachedToListId: null },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 1: two entries after duplicate', list.length === 2);
  const copy = list.find(e => e.listId !== 1);
  check('scenario 1: copy has new listId', copy && copy.listId === 10);
  check('scenario 1: copy inherits wargear (deep, not same ref)', copy.wargear.a === 'x' && copy.wargear !== list[0].wargear);
  check('scenario 1: copy priced as second copy (90)', copy.points === 90);
  check('scenario 1: copy not attached', copy.attachedToListId === null);
}

// ── Scenario 2: unit with one non-Epic-Hero leader attached ────────────────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Tallyman', 'Character')]);
  E.setNextId(20);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Tallyman', unit_type: 'Character', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: 1 },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 2: four entries after duplicate (body+leader x2)', list.length === 4);
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  const leaderCopy = list.find(e => e.unit_name === 'Tallyman' && e.listId !== 2);
  check('scenario 2: leader duplicated', !!leaderCopy);
  check('scenario 2: leader copy attached to body copy', leaderCopy && bodyCopy && leaderCopy.attachedToListId === bodyCopy.listId);
}

// ── Scenario 3: unit with an Epic Hero leader attached — NOT duplicated ────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Typhus', 'Epic Hero')]);
  E.setNextId(30);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Typhus', unit_type: 'Epic Hero', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: 1 },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 3: only three entries (Epic Hero not duplicated)', list.length === 3);
  const epicCopies = list.filter(e => e.unit_name === 'Typhus');
  check('scenario 3: still exactly one Typhus', epicCopies.length === 1);
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  check('scenario 3: body copy has no leader attached to it', !list.some(e => e.attachedToListId === bodyCopy.listId));
}

// ── Scenario 4: unit already at its instance limit — duplicate refused ─────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry')]);
  E.setNextId(40);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 90, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 3, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 80, wargear: {}, otherOptions: {}, attachedToListId: null },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 4: refused at limit (still 3 entries)', list.length === 3);
  check('scenario 4: banner shown', E.getFlashed().length === 1 && E.getFlashed()[0].includes('Limit reached'));
}

// ── Scenario 5: Epic Hero leader already at its own limit (1) elsewhere ────
// duplicating the SECOND copy of a bodyguard whose leader is a non-Epic-Hero already
// at that leader's own instance limit — leader copy silently skipped, body still copies.
{
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Foul Blightspawn', 'Character')]);
  E.setNextId(50);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: 1 },
    { listId: 3, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 4, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: null },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  check('scenario 5: body still copies despite leader being at its own limit', !!bodyCopy);
  check('scenario 5: leader copy silently skipped (still only 3 Foul Blightspawn)', list.filter(e => e.unit_name === 'Foul Blightspawn').length === 3);
  check('scenario 5: body copy left with no leader attached', !list.some(e => e.attachedToListId === bodyCopy.listId));
}

// ── Scenario 6: 2-leader stack duplicate (B7a) — both leaders copy if under
// their own limits, and the duplicated body refuses a 3rd leader (D157 cap),
// independent of pairwise permits which would otherwise allow it.
{
  function leaderUnit(name, coLeaderWith) {
    return {
      unit_name: name, unit_type: 'Character', sizes: [{ size: 1, first_unit: 60, second_unit: 60, third_plus: 60 }],
      leaderEligible: ['Plague Marines'], coLeaderWith, coLeaderAny: false,
    };
  }
  E.setAllUnits([
    unit('Plague Marines', 'Infantry'),
    leaderUnit('Tallyman', ['Foul Blightspawn', 'Biologus Putrifier']),
    leaderUnit('Foul Blightspawn', ['Tallyman']),
    leaderUnit('Biologus Putrifier', ['Tallyman']),
  ]);
  E.setNextId(60);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Tallyman', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: 1 },
    { listId: 3, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: 1 },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 6: six entries after duplicate (body+2 leaders x2)', list.length === 6);
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  const attachedToCopy = list.filter(e => e.attachedToListId === bodyCopy.listId);
  check('scenario 6: both leaders duplicated onto the body copy', attachedToCopy.length === 2);
  check('scenario 6: leader copies are Tallyman + Foul Blightspawn',
    attachedToCopy.map(e => e.unit_name).sort().join(',') === 'Foul Blightspawn,Tallyman');

  // B7a: the duplicated body already carries 2 leaders — a 3rd must refuse even
  // though Biologus Putrifier's pairwise permits (coLeaderWith Tallyman) would allow it.
  const refused = E.canAttachLeader('Biologus Putrifier', bodyCopy);
  check('scenario 6: 3rd leader refused on the 2-leader-stacked body copy (B7a cap)', refused === false);

  // Sanity: a fresh, unattached body (only 0 existing leaders) still accepts a leader.
  const fresh = { listId: 999, unit_name: 'Plague Marines' };
  const allowed = E.canAttachLeader('Tallyman', fresh);
  check('scenario 6: leader still attaches to an unstacked body (cap did not overreach)', allowed === true);
}


// ── Scenario 7 (E4b): the enhancement is not inherited by a duplicate ────────
// Both the copied unit and any copied leader start clean. 25.04 allows one of each
// enhancement in an army, so inheriting would create an illegal state at the moment
// of the copy — refused up front, in the B41/D0 spirit, rather than flagged after.
{
  const DETS = { 'X|D1': { name: 'D1', enhancements: [
    { name: 'Test Relic', points: 20, is_upgrade: false },
    { name: 'Test Upgrade', points: 15, is_upgrade: true } ] } };
  E.setDetachmentDefs(DETS);
  E.setSelectedDetachments(['X|D1']);
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Tallyman', 'Character')]);
  E.setNextId(40);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100,
      wargear: {}, otherOptions: {}, enhancement: { name: 'Test Upgrade', detachment_key: 'X|D1' }, attachedToListId: null },
    { listId: 2, unit_name: 'Tallyman', unit_type: 'Character', sizeIdx: 0, god: null, points: 60,
      wargear: {}, otherOptions: {}, enhancement: { name: 'Test Relic', detachment_key: 'X|D1' }, attachedToListId: 1 },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  const bodyCopy   = list.find(e => e.listId === 40);
  const leaderCopy = list.find(e => e.listId === 41);
  check('scenario 7: body copy carries no enhancement', bodyCopy && bodyCopy.enhancement === null);
  check('scenario 7: leader copy carries no enhancement', leaderCopy && leaderCopy.enhancement === null);
  check('scenario 7: the originals keep theirs',
        list.find(e => e.listId === 1).enhancement.name === 'Test Upgrade' &&
        list.find(e => e.listId === 2).enhancement.name === 'Test Relic');
  // Second copy of the datasheet, so second_unit pricing (90) with no enhancement
  // added on top — 110 would mean the Upgrade had been inherited and priced.
  check('scenario 7: the copy is priced without an enhancement', bodyCopy.points === 90);
}

console.log(failures === 0 ? '\nall E10 checks pass' : `\n${failures} E10 check(s) FAILED`);
process.exit(failures === 0 ? 0 : 1);
