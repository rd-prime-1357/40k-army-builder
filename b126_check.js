// b126_check.js — B126 (D346). Loads the real markEffect / markKeywordSet /
// unitInnateMark / unitNeedsMark / markOptionsForUnit / entryEffectiveMark /
// entryMarkStale / entryMarkMissing / markAttachBlock / canSetMark / setMark and
// the real enhancementBearerEligible out of index.html, and proves the Marks of
// Chaos rule behaves as ruled rather than as described in prose (D107):
//
//   1. Pool membership. HERETIC ASTARTES in EITHER keyword_names or
//      faction_keyword_names puts a unit in the pool; EPIC HERO and each of the
//      five mark keywords take it back out. The three-field keyword reader is
//      tested directly, including the model_keyword_names-only case that would
//      otherwise put Masters of the Maelstrom in the pool.
//   2. Detachment scoping. With Pactbound Zealots deselected there is no effect,
//      no pool, no attach restriction and no offered options.
//   3. The Psyker/Khorne exclusion, on a unit-wide Psyker AND on a model-level
//      Psyker (D346: any model with the keyword makes it a PSYKER unit).
//   4. Innate marks. A datasheet that already carries one is out of the pool and
//      still reports that mark as its effective mark.
//   5. The attach restriction. A genuine mismatch is refused; a match is allowed;
//      a missing mark on EITHER side falls through permissive (D199).
//   6. D346's asymmetry, the thing most likely to be "fixed" back by mistake:
//      the ATTACH is refused, but a mark CHANGE that leaves an existing pair
//      mismatched is ALLOWED and surfaces through entryMarkPairError instead.
//   7. Staleness and the outstanding-choice flag: a pick survives its detachment
//      being deselected (S139) but reads stale, and an unmade choice reads missing.
//   8. The four mark-restricted Pactbound Zealots enhancements resolve through
//      entryEffectiveMark — right mark allowed, wrong mark and no mark refused.
//   9. Round-trip against the real detachment_effects.json and units.json: the
//      shipped row is enforced, its vocabulary is the five marks, and the pool it
//      describes is exactly the 45 Chaos Space Marines units re-derived from
//      units.json — not a number carried from a scope document.
//
// Build-time only; not part of the served app.
// Usage: node b126_check.js index.html detachment_effects.json units.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function load(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const markSrc = slice(lines, '── E29/B126: Marks of Chaos', '── E29/B126 block end');
  // enhancementBearerEligible lives in the E4b block; sliced from its own table
  // declaration so the four mark rows are the REAL ones, not a copy here.
  const bearerSrc = slice(lines, 'const ENHANCEMENT_BEARER_RESTRICTIONS = {', '// ── B99 BEGIN');
  // entryMarkPairError sits with entryHasError, outside the E29 block.
  const pairSrc = slice(lines, '  function entryMarkPairError(entry, keys) {', '  function getAttachedLeaders(');

  const prelude = `
    let armyList = [];
    let detachmentEffects = {};
    let rawUnits = [];
    let selectedDetachments = [];
    function flashBanner(msg) { flashBanner.lastMsg = msg; }
    function renderAll() { renderAll.calls = (renderAll.calls || 0) + 1; }
    function escHtml(s) { return String(s == null ? '' : s); }
    function setState({ list, effects, raw, keys }) {
      armyList = list; detachmentEffects = effects; rawUnits = raw; selectedDetachments = keys;
    }
  `;

  return new Function(
    prelude + '\n' + markSrc + '\n' + pairSrc + '\n' + bearerSrc + '\n' +
    'return { setState, flashBanner,' +
    ' markEffect, markKeywordSet, unitInnateMark, unitNeedsMark, markOptionsForUnit,' +
    ' entryEffectiveMark, entryMarkStale, entryMarkMissing, entryMarkPairError,' +
    ' markAttachBlock, canSetMark, setMark, renderMarkSectionHtml,' +
    ' enhancementBearerRestriction, enhancementBearerEligible,' +
    ' getArmyList: () => armyList };'
  )();
}

const idxPath  = process.argv[2] || 'index.html';
const dePath   = process.argv[3] || 'detachment_effects.json';
const unitPath = process.argv[4] || 'units.json';

const M  = load(idxPath);
const DE = JSON.parse(fs.readFileSync(dePath, 'utf8'));
const UJ = JSON.parse(fs.readFileSync(unitPath, 'utf8'));

let failures = 0;
function check(cond, msg) {
  if (!cond) { console.log('  FAIL ' + msg); failures++; }
}

const PZ_KEY = 'Chaos Space Marines|PACTBOUND ZEALOTS';

// The effect table used for the behavioural tests is the REAL shipped row, not a
// fixture — a change to the data that broke the engine's reading of it would
// otherwise pass here and fail only in the browser.
const effects = { [PZ_KEY]: DE.effects[PZ_KEY] };
if (!effects[PZ_KEY]) {
  console.log(`FAIL b126_check    ${PZ_KEY} has no row in ${dePath}`);
  process.exitCode = 1;
  process.exit();
}

// ── raw unit fixtures ─────────────────────────────────────────────────────────
// Each isolates one arm of the keyword reader, because the three fields are read
// for different real reasons and a regression in any one of them is silent.
function raw(name, unit_type, mg) {
  return { unit_name: name, unit_type, model_groups: Array.isArray(mg) ? mg : [mg] };
}
const R = {
  // HERETIC ASTARTES in faction_keyword_names — how all 58 real CSM units carry it
  legionaries: raw('Legionaries', 'Battleline',
    { keyword_names: ['Chaos', 'Infantry'], faction_keyword_names: ['Heretic Astartes'], model_keyword_names: [] }),
  chaosLord: raw('Chaos Lord', 'Character',
    { keyword_names: ['Chaos', 'Character', 'Infantry'], faction_keyword_names: ['Heretic Astartes'], model_keyword_names: [] }),
  chosen: raw('Chosen', 'Infantry',
    { keyword_names: ['Chaos', 'Infantry'], faction_keyword_names: ['Heretic Astartes'], model_keyword_names: [] }),
  // HERETIC ASTARTES in keyword_names — how the Shadow Legion Thralls carry it
  thrall: raw('Thrall Legionaries', 'Battleline',
    { keyword_names: ['Chaos', 'Infantry', 'Heretic Astartes'], faction_keyword_names: [], model_keyword_names: [] }),
  // unit-wide Psyker
  sorcerer: raw('Sorcerer', 'Character',
    { keyword_names: ['Chaos', 'Character', 'Infantry', 'Psyker'], faction_keyword_names: ['Heretic Astartes'], model_keyword_names: [] }),
  // model-level Psyker only (Dark Commune's Mindwitch) — D346's case
  darkCommune: raw('Dark Commune', 'Character',
    { keyword_names: ['Chaos', 'Damned', 'Infantry'], faction_keyword_names: ['Heretic Astartes'],
      model_keyword_names: [{ model: 'MINDWITCH ONLY', keywords: ['Psyker'] }] }),
  // Epic Hero, out of the pool
  abaddon: raw('Abaddon The Despoiler', 'Epic Hero',
    { keyword_names: ['Chaos', 'Character', 'Epic Hero', 'Chaos Undivided'], faction_keyword_names: ['Heretic Astartes'], model_keyword_names: [] }),
  // innate mark, out of the pool
  berzerkers: raw('Khorne Berzerkers', 'Battleline',
    { keyword_names: ['Chaos', 'Infantry', 'Khorne'], faction_keyword_names: ['Heretic Astartes'], model_keyword_names: [] }),
  // EMPTY keyword_names, everything at model level — Masters of the Maelstrom
  masters: raw('Masters of the Maelstrom', 'Other',
    { keyword_names: [], faction_keyword_names: [],
      model_keyword_names: [{ model: 'OTHER MODELS', keywords: ['Chaos', 'Chaos Undivided', 'Epic Hero', 'Heretic Astartes'] },
                            { model: 'GARLON SOULEATER', keywords: ['Psyker'] }] }),
  // not Heretic Astartes at all
  bloodletters: raw('Bloodletters', 'Infantry',
    { keyword_names: ['Chaos', 'Daemon', 'Khorne'], faction_keyword_names: [], model_keyword_names: [] }),
};
const RAWS = Object.values(R);

function entry(id, name, unit_type, mark, attachedTo) {
  return { listId: id, unit_name: name, unit_type, mark: mark || null,
           attachedToListId: attachedTo == null ? null : attachedTo, unresolved: false };
}
function set(list, keys) { M.setState({ list: list || [], effects, raw: RAWS, keys: keys || [PZ_KEY] }); }

// ── 1. pool membership and the three-field keyword reader ────────────────────
console.log('B126 — pool membership');
{
  set([], [PZ_KEY]);
  const eff = M.markEffect([PZ_KEY]);
  check(!!eff, 'the shipped Pactbound Zealots row should produce an active effect');
  check(M.unitNeedsMark(R.legionaries, eff) === true, 'faction_keyword_names Heretic Astartes puts a unit in the pool');
  check(M.unitNeedsMark(R.thrall, eff) === true, 'keyword_names Heretic Astartes puts a unit in the pool');
  check(M.unitNeedsMark(R.abaddon, eff) === false, 'an EPIC HERO is out of the pool');
  check(M.unitNeedsMark(R.berzerkers, eff) === false, 'a unit already carrying a mark is out of the pool');
  check(M.unitNeedsMark(R.masters, eff) === false,
        'model_keyword_names alone must be read — Masters of the Maelstrom is Epic Hero + Chaos Undivided there and must NOT be asked for a mark');
  check(M.unitNeedsMark(R.bloodletters, eff) === false, 'a non-Heretic-Astartes unit is never in the pool');
  const kws = M.markKeywordSet(R.masters);
  check(kws.has('epic hero') && kws.has('chaos undivided') && kws.has('psyker'),
        'markKeywordSet reads model_keyword_names');
  check(M.markKeywordSet(R.legionaries).has('heretic astartes'),
        'markKeywordSet reads faction_keyword_names');
}

// ── 2. detachment scoping ────────────────────────────────────────────────────
console.log('B126 — the rule exists only while Pactbound Zealots is selected');
{
  check(M.markEffect([]) === null, 'no selected detachment means no effect');
  check(M.markEffect(['Chaos Space Marines|RENEGADE RAIDERS']) === null,
        'a non-granting selected detachment must not open the rule');
  check(M.unitNeedsMark(R.legionaries, M.markEffect([])) === false, 'no effect means no pool');
  set([entry(1, 'Legionaries', 'Battleline', null)], []);
  check(M.entryMarkMissing(M.getArmyList()[0], []) === false,
        'with the detachment deselected nothing is asked for, so nothing is missing');
  check(M.markAttachBlock(entry(1, 'Chaos Lord', 'Character', 'Khorne'),
                          entry(2, 'Legionaries', 'Battleline', 'Nurgle'), []) === null,
        'the attach restriction does not apply while the detachment is deselected');
}

// ── 3. the Psyker / Khorne exclusion ─────────────────────────────────────────
console.log('B126 — KHORNE is never offered to a PSYKER unit');
{
  set([], [PZ_KEY]);
  const eff = M.markEffect([PZ_KEY]);
  const all = M.markOptionsForUnit(R.legionaries, eff);
  check(all.length === 5 && all.indexOf('Khorne') === 0 && all.indexOf('Chaos Undivided') === 4,
        'a non-Psyker unit is offered all five marks in source order');
  const sorc = M.markOptionsForUnit(R.sorcerer, eff);
  check(sorc.length === 4 && sorc.indexOf('Khorne') < 0, 'a unit-wide Psyker is not offered Khorne');
  const dc = M.markOptionsForUnit(R.darkCommune, eff);
  check(dc.length === 4 && dc.indexOf('Khorne') < 0,
        'D346: a model-level Psyker (Dark Commune / Mindwitch) is not offered Khorne either');
  set([entry(1, 'Dark Commune', 'Character', null)], [PZ_KEY]);
  const g = M.canSetMark(M.getArmyList()[0], 'Khorne', [PZ_KEY]);
  check(g.ok === false && g.reason === 'not_an_option', 'Khorne on Dark Commune is refused at the gate, not just hidden');
  M.setMark(1, 'Khorne');
  check(M.getArmyList()[0].mark === null, 'a refused pick leaves no trace on the entry');
  M.setMark(1, 'Nurgle');
  check(M.getArmyList()[0].mark === 'Nurgle', 'an offered pick is accepted');
}

// ── 4. innate marks ──────────────────────────────────────────────────────────
console.log('B126 — a datasheet that already carries a mark keeps it and is never asked');
{
  set([entry(1, 'Khorne Berzerkers', 'Battleline', null), entry(2, 'Abaddon The Despoiler', 'Epic Hero', null)], [PZ_KEY]);
  const [bz, ab] = M.getArmyList();
  check(M.entryEffectiveMark(bz, [PZ_KEY]) === 'Khorne', 'Khorne Berzerkers report Khorne with no pick made');
  check(M.entryEffectiveMark(ab, [PZ_KEY]) === 'Chaos Undivided', 'Abaddon reports his innate Chaos Undivided');
  check(M.entryMarkMissing(bz, [PZ_KEY]) === false, 'a unit with an innate mark is never flagged as missing one');
  check(M.entryMarkMissing(ab, [PZ_KEY]) === false, 'an Epic Hero is never flagged as missing one');
  check(M.renderMarkSectionHtml(bz) === '', 'no selector is rendered for a unit with an innate mark');
}

// ── 5. the attach restriction ────────────────────────────────────────────────
console.log('B126 — a Character can only attach to a unit sharing its mark');
{
  set([], [PZ_KEY]);
  const kh = entry(1, 'Chaos Lord', 'Character', 'Khorne');
  const nu = entry(2, 'Chaos Lord', 'Character', 'Nurgle');
  const bgKh = entry(3, 'Legionaries', 'Battleline', 'Khorne');
  const bgNu = entry(4, 'Legionaries', 'Battleline', 'Nurgle');
  const none = entry(5, 'Legionaries', 'Battleline', null);
  const noneChar = entry(6, 'Chaos Lord', 'Character', null);
  check(M.markAttachBlock(kh, bgKh, [PZ_KEY]) === null, 'matching marks attach');
  const blk = M.markAttachBlock(kh, bgNu, [PZ_KEY]);
  check(blk && blk.leaderMark === 'Khorne' && blk.bodyguardMark === 'Nurgle',
        'mismatching marks are refused and name both marks');
  check(M.markAttachBlock(nu, bgNu, [PZ_KEY]) === null, 'the other matching pair also attaches');
  check(M.markAttachBlock(kh, none, [PZ_KEY]) === null,
        'D199: an unmade choice on the bodyguard falls through permissive, it does not refuse');
  check(M.markAttachBlock(noneChar, bgKh, [PZ_KEY]) === null,
        'D199: an unmade choice on the leader falls through permissive too');
  // an innate mark is a real mark for this test, on both sides
  check(M.markAttachBlock(nu, entry(7, 'Khorne Berzerkers', 'Battleline', null), [PZ_KEY]) !== null,
        'an innate Khorne bodyguard refuses a Nurgle leader');
  check(M.markAttachBlock(kh, entry(8, 'Khorne Berzerkers', 'Battleline', null), [PZ_KEY]) === null,
        'an innate Khorne bodyguard accepts a Khorne leader');
}

// ── 6. D346's asymmetry — attach refused, later change allowed ───────────────
console.log('B126 — the attach is gated, a later mark change is not (D346)');
{
  const ldr = entry(1, 'Chaos Lord', 'Character', 'Khorne', 2);
  const bg  = entry(2, 'Legionaries', 'Battleline', 'Khorne');
  set([ldr, bg], [PZ_KEY]);
  check(M.entryMarkPairError(M.getArmyList()[0], [PZ_KEY]) === false, 'a matching attached pair is not an error');
  const gate = M.canSetMark(M.getArmyList()[1], 'Nurgle', [PZ_KEY]);
  check(gate.ok === true, 'changing the bodyguard mark under an attached leader is ALLOWED, not refused');
  M.setMark(2, 'Nurgle');
  check(M.getArmyList()[1].mark === 'Nurgle', 'and the change actually lands');
  check(M.entryMarkPairError(M.getArmyList()[0], [PZ_KEY]) === true, 'the now-mismatched pair flags on the leader');
  check(M.entryMarkPairError(M.getArmyList()[1], [PZ_KEY]) === true, 'and on the bodyguard — the flag reads both directions');
  M.setMark(1, 'Nurgle');
  check(M.entryMarkPairError(M.getArmyList()[0], [PZ_KEY]) === false,
        'completing the two-step edit clears the flag without any detach');
  check(M.entryMarkPairError(M.getArmyList()[1], [PZ_KEY]) === false, 'on both halves');
}

// ── 7. staleness and the outstanding choice ──────────────────────────────────
console.log('B126 — an unmade choice is flagged; a made one survives deselection');
{
  set([entry(1, 'Legionaries', 'Battleline', null)], [PZ_KEY]);
  check(M.entryMarkMissing(M.getArmyList()[0], [PZ_KEY]) === true, 'a pool unit with no pick is flagged missing');
  M.setMark(1, 'Slaanesh');
  check(M.entryMarkMissing(M.getArmyList()[0], [PZ_KEY]) === false, 'and stops being flagged once picked');
  check(M.entryMarkStale(M.getArmyList()[0], [PZ_KEY]) === false, 'a live pick is not stale');
  // deselect the detachment: S139 — the pick is kept, but reads stale and inert
  set(M.getArmyList(), []);
  check(M.getArmyList()[0].mark === 'Slaanesh', 'S139: deselecting the detachment does not discard the pick');
  check(M.entryMarkStale(M.getArmyList()[0], []) === true, 'but it reads stale');
  check(M.entryEffectiveMark(M.getArmyList()[0], []) === null, 'and confers nothing while stale');
  // reselect: it comes back with no re-click
  set(M.getArmyList(), [PZ_KEY]);
  check(M.entryMarkStale(M.getArmyList()[0], [PZ_KEY]) === false, 'reselecting the detachment revives it with no re-click');
  check(M.entryEffectiveMark(M.getArmyList()[0], [PZ_KEY]) === 'Slaanesh', 'and it confers again');
}

// ── 8. the four mark-restricted enhancements ─────────────────────────────────
console.log('B126 — the four Pactbound Zealots mark enhancements resolve through the mark');
{
  const EXPECT = { 'Eye of Tzeentch': 'Tzeentch', 'Intoxicating Elixir': 'Slaanesh',
                   'Orbs of Unlife': 'Nurgle', 'Talisman of Burning Blood': 'Khorne' };
  for (const [name, mark] of Object.entries(EXPECT)) {
    const rule = M.enhancementBearerRestriction(name, PZ_KEY);
    check(rule && rule.kind === 'mark' && rule.mark === mark, `${name} carries a mark rule for ${mark}`);
  }
  const other = Object.keys(EXPECT).find(n => EXPECT[n] !== 'Nurgle');
  set([entry(1, 'Chaos Lord', 'Character', 'Nurgle')], [PZ_KEY]);
  const e = M.getArmyList()[0];
  check(M.enhancementBearerEligible(e, 'Orbs of Unlife', PZ_KEY) === true,
        'a Nurgle Chaos Lord may take Orbs of Unlife');
  check(M.enhancementBearerEligible(e, other, PZ_KEY) === false,
        `a Nurgle Chaos Lord may not take ${other}`);
  set([entry(1, 'Chaos Lord', 'Character', null)], [PZ_KEY]);
  check(M.enhancementBearerEligible(M.getArmyList()[0], 'Orbs of Unlife', PZ_KEY) === false,
        'a Chaos Lord with no mark chosen yet may not take a mark-restricted enhancement');
  set([entry(1, 'Khorne Berzerkers', 'Battleline', null)], [PZ_KEY]);
  check(M.enhancementBearerEligible(M.getArmyList()[0], 'Talisman of Burning Blood', PZ_KEY) === true,
        'an innate Khorne unit satisfies the Khorne enhancement restriction');
}

// ── 9. the shipped data, and the pool re-derived from units.json ─────────────
console.log('B126 — shipped data facts, and the real pool re-derived from units.json');
{
  const rec = DE.effects[PZ_KEY];
  const eff = (rec.effects || []).find(x => x.kind === 'mark_of_chaos');
  check(!!eff, `${PZ_KEY}: no mark_of_chaos effect found`);
  check(eff.enforced === true, 'the shipped row is enforced');
  check(JSON.stringify(eff.marks) === JSON.stringify(['Khorne', 'Tzeentch', 'Nurgle', 'Slaanesh', 'Chaos Undivided']),
        'the shipped vocabulary is the five marks in source order');
  check(eff.attach_restriction && eff.attach_restriction.must_match === true, 'the attach restriction is recorded');
  check(Array.isArray(eff.unmodelled_restrictions) && eff.unmodelled_restrictions.length === 1,
        'the embark restriction is recorded as unmodelled rather than silently dropped');
  // Pactbound Zealots must be a Chaos Space Marines detachment and nothing else's
  check(Object.keys(DE.effects).filter(k => k.includes('PACTBOUND ZEALOTS')).length === 1,
        'exactly one mark_of_chaos row exists');

  const csm = UJ.find(a => a.army === 'Chaos Space Marines');
  check(!!csm, 'units.json carries a Chaos Space Marines block');
  const inPool = (csm.units || []).filter(u => M.unitNeedsMark(u, eff));
  check(inPool.length === 45,
        `the real CSM pool should be 45 units, got ${inPool.length}`);
  const withInnate = (csm.units || []).filter(u => M.unitInnateMark(u, eff));
  check(withInnate.length === 11,
        `11 CSM units should carry an innate mark, got ${withInnate.length}`);
  // no unit may be both in the pool and already marked — the two sets partition
  check(inPool.every(u => !M.unitInnateMark(u, eff)),
        'no unit is both in the pool and already carrying a mark');
  // every pool member must have at least one offerable option, or the rule is unsatisfiable
  const starved = inPool.filter(u => M.markOptionsForUnit(u, eff).length === 0);
  check(starved.length === 0,
        `every pool unit must have at least one offerable mark; ${starved.length} have none`);
  // Re-derived S249, not carried from prose: Sorcerer, Sorcerer In Terminator
  // Armour, Master Of Possession, Nemesis Claw (all unit-wide PSYKER) and Dark
  // Commune (PSYKER on the MINDWITCH model only — the D346 case).
  const psykers = inPool.filter(u => M.markOptionsForUnit(u, eff).length === 4);
  check(psykers.length === 5,
        `5 CSM pool units should be Psyker units offered four marks, got ${psykers.length} (${psykers.map(u => u.unit_name).join(', ')})`);
  check(psykers.some(u => u.unit_name === 'Dark Commune'),
        'Dark Commune must be among them — the model-level PSYKER case D346 rules on');
}

if (failures === 0) {
  console.log('PASS b126_check    all B126 checks pass (three-field pool reader, detachment scoping, Psyker/Khorne exclusion incl. model-level, innate marks, attach gate with permissive fall-through, D346 change-allowed asymmetry, staleness, the four mark enhancements, shipped data and the real 45-unit pool)');
} else {
  console.log(`FAIL b126_check    ${failures} check(s) failed`);
  process.exitCode = 1;
}
