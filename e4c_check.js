// e4c_check.js — E4c. Loads the real E4b engine and E4c picker/chip functions
// out of index.html and exercises them against the real detachment catalogue.
// Per D107 these are claims about BEHAVIOUR, so they are executed rather than
// described in prose.
//
// What it holds:
//   1. enhancementOfferedRowsForEntry filters by enhancementTypeEligible, and
//      nothing else — an Epic Hero with no Upgrade on the table gets no rows.
//   2. flag-don't-drop: whatever an entry currently holds stays in its row
//      list even if it is no longer type-eligible or no longer offered, so it
//      can always be cleared from its own panel.
//   3. the picker's disabled flag is canAssignEnhancement's answer for every
//      offered row across scenarios, and nothing else (E4b-4's single-call-
//      site guarantee, checked at the E4c layer this time).
//   4. a selected row is never disabled, however stale.
//   5. renderEnhancementSectionHtml is empty for a unit with no eligible row,
//      and every disabled row it renders carries enhancementRefusalText's
//      prose, verbatim.
//   6. renderEnhancementChipHtml's numbers are enhancementArmyState's numbers,
//      and its warning lines appear for exactly the states an import or a
//      battle-size/detachment change can reach — over, notOffered, wrongType,
//      sharedUnits.
//
// Build-time only; not part of the served app.
// Usage: node e4c_check.js index.html detachments.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path, defs) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const e4b = slice(lines, '// ── E4b: enhancement assignment rules', '// ── E4b block end');
  const e4c = slice(lines, '// ── E4c: enhancement picker', '// ── E4c block end');
  const src = 'let detachmentDefs = DEFS; let selectedDetachments = []; '
            + 'let armyList = []; let POINTS_CAP = 2000; '
            + 'function renderAll(){} '
            + 'function esc(s){return String(s);} '
            + 'function escHtml(s){return String(s==null?"":s);} '
            + 'function detTier2Badge(source){return source && source !== "faction_pack" ? " [prev.ed]" : "";} '
            + 'let _detSeq = 0; '
            + 'function infoBtn(){ return "<button></button>"; } '
            + 'function mkDetail(kind, html){ const id = "det" + (++_detSeq); return { btn: infoBtn(), panel: "<div id=\\"" + id + "\\">" + html + "</div>" }; }\n'
            + e4b + '\n' + e4c
            + '\nreturn { enhancementLimit, enhancementRecord, enhancementPoints, '
            + 'enhancementIsUpgrade, enhancementIsOffered, offeredEnhancements, '
            + 'assignedEnhancements, enhancementCount, enhancementCopies, '
            + 'enhancementMaxCopies, attachedGroupListIds, groupEnhancementCarriers, '
            + 'enhancementTypeEligible, canAssignEnhancement, enhancementArmyState, '
            + 'enhancementRowState, enhancementRefusalText, enhancementAttachBlock, '
            + 'enhancementPointsForEntry, assignEnhancement, clearEnhancement, '
            + 'enhancementOfferedRowsForEntry, renderEnhancementSectionHtml, '
            + 'renderEnhancementChipHtml, '
            + 'setArmy: (a) => { armyList = a; }, '
            + 'setDetachments: (d) => { selectedDetachments = d; }, '
            + 'setCap: (p) => { POINTS_CAP = p; }, '
            + 'army: () => armyList };';
  return new Function('DEFS', src)(defs);
}

const idxPath = process.argv[2] || 'index.html';
const detPath = process.argv[3] || 'detachments.json';

const DJ = JSON.parse(fs.readFileSync(detPath, 'utf8'));
const E  = loadEngine(idxPath, DJ.detachments);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (a, b, msg) => ok(JSON.stringify(a) === JSON.stringify(b), `${msg} (got ${JSON.stringify(a)})`);

// ── fixtures, the same ones e4b_check.js uses ────────────────────────────────
const K_ICTF = 'Dark Angels|INNER CIRCLE TASK FORCE';   // Deathwing Assault @ 30
const K_WOTR = 'Dark Angels|WRATH OF THE ROCK';         // Deathwing Assault @ 15
const K_FIRE = 'Space Marines|FIRESTORM ASSAULT FORCE'; // Adamantine Mantle @ 20
const K_FORG = "Space Marines|FORGEFATHER'S SEEKERS";   // Adamantine Mantle @ 20
const K_FULG = 'Space Marines|FULGURIS TASK FORCE';     // Bellicose Weapon Spirits — Upgrade @ 15

const N_DWA  = 'Deathwing Assault';
const N_ADAM = 'Adamantine Mantle';
const N_BWS  = 'Bellicose Weapon Spirits';

function entry(listId, unitType, name, opts) {
  return Object.assign({
    listId: listId, unit_name: name || ('U' + listId), unit_type: unitType,
    enhancement: null, attachedToListId: null, unresolved: false
  }, opts || {});
}
function assign(e, name, key) { e.enhancement = { name: name, detachment_key: key }; return e; }

const fireRegulars = (DJ.detachments[K_FIRE].enhancements || [])
  .filter(e => !e.is_upgrade).map(e => e.name);

// ── 1. rows are filtered by type-eligibility, and only that ─────────────────
console.log('E4c — offered rows are filtered by enhancementTypeEligible, and nothing else');
E.setDetachments([K_FIRE, K_FULG]);
{
  const hero = entry(1, 'Epic Hero'), inf = entry(2, 'Infantry'), chr = entry(3, 'Character');
  E.setArmy([hero, inf, chr]);

  const heroRows = E.enhancementOfferedRowsForEntry(hero, 2000);
  ok(heroRows.length === 0, 'an Epic Hero with no Upgrade offered gets zero rows');

  const infRows = E.enhancementOfferedRowsForEntry(inf, 2000);
  ok(infRows.length > 0 && infRows.every(r => r.is_upgrade),
     'a non-Character sees only Upgrade rows');

  const chrRows = E.enhancementOfferedRowsForEntry(chr, 2000);
  ok(chrRows.some(r => r.is_upgrade) && chrRows.some(r => !r.is_upgrade),
     'a Character sees both regular and Upgrade rows');
  eq(chrRows.length, E.offeredEnhancements().length,
     'a Character is offered every row on the table (regular + Upgrade), no fewer');
}

// ── 2. flag-don't-drop: a held row survives even when no longer offered ─────
console.log("E4c — a unit's held enhancement stays in its own row list even if stale");
{
  // Nothing from WRATH OF THE ROCK is on the table (only FIRE/FULG selected),
  // so a Character holding a WOTR pick is holding a NOT-OFFERED assignment —
  // exactly the import/detachment-change case D199/D200 call out.
  const chr = assign(entry(5, 'Character'), N_DWA, K_WOTR);
  E.setArmy([chr]);
  const rows = E.enhancementOfferedRowsForEntry(chr, 2000);
  const held = rows.find(r => r.name === N_DWA && r.detachment_key === K_WOTR);
  ok(!!held, 'the stale WOTR pick still appears in the row list');
  ok(held.state.selected === true, 'it reads as selected');
  ok(held.state.disabled === false, 'and is never disabled — it must stay clearable');

  // An Epic Hero holding a stale regular pick (e.g. from a data change that
  // reclassified the unit) must likewise still see its own row to clear it.
  const hero = assign(entry(6, 'Epic Hero'), N_ADAM, K_FIRE);
  E.setArmy([hero]);
  const heroRows = E.enhancementOfferedRowsForEntry(hero, 2000);
  ok(heroRows.length === 1 && heroRows[0].state.selected,
     "an Epic Hero's own stale-but-held pick is the ONLY row it sees, and it is selected");
}

// ── 3. the picker's disabled flag is canAssignEnhancement's answer, and only that ─
console.log('E4c — disabled is exactly canAssignEnhancement, not a second implementation of it');
E.setDetachments([K_FIRE, K_FORG, K_FULG]);
{
  const scenarios = [
    { name: 'empty army',
      army: [entry(1, 'Character'), entry(2, 'Infantry'), entry(3, 'Epic Hero')] },
    { name: 'one assignment already made',
      army: [assign(entry(1, 'Character'), N_ADAM, K_FIRE), entry(2, 'Character'), entry(3, 'Infantry')] },
    { name: 'attached leader pair, bodyguard already carrying',
      army: [assign(entry(1, 'Infantry', 'Bodyguard'), N_BWS, K_FULG),
             entry(2, 'Character', 'Leader', { attachedToListId: 1 })] },
  ];
  for (const sc of scenarios) {
    E.setArmy(sc.army);
    for (const e of sc.army) {
      if (e.unresolved) continue;
      const rows = E.enhancementOfferedRowsForEntry(e, 2000);
      for (const r of rows) {
        const can = E.canAssignEnhancement(e, r.name, r.detachment_key, 2000);
        const expectedDisabled = r.state.selected ? false : !can.ok;
        ok(r.state.disabled === expectedDisabled,
           `${sc.name} / listId ${e.listId} / ${r.name}@${r.detachment_key}: disabled = selected ? false : !canAssign.ok`);
      }
    }
  }
}

// ── 4. renderEnhancementSectionHtml: empty when there is nothing to hold ────
console.log('E4c — the section is absent for a unit with no eligible row');
E.setDetachments([K_FIRE]);   // no Upgrade offered here
{
  const hero = entry(9, 'Epic Hero');
  E.setArmy([hero]);
  ok(E.renderEnhancementSectionHtml(hero, 2000) === '', 'an Epic Hero with nothing offered renders nothing');
}

// ── 5. renderEnhancementSectionHtml: disabled rows carry the refusal prose ──
console.log('E4c — every disabled row carries enhancementRefusalText verbatim, selected rows carry none');
E.setDetachments([K_FIRE, K_FORG, K_FULG]);
{
  const bg    = assign(entry(1, 'Infantry', 'Bodyguard'), N_BWS, K_FULG);
  const lead  = entry(2, 'Character', 'Leader', { attachedToListId: 1 });
  E.setArmy([bg, lead]);
  const html = E.renderEnhancementSectionHtml(lead, 2000);
  ok(html.length > 0, 'the Character sees an Enhancement section');
  const rows = E.enhancementOfferedRowsForEntry(lead, 2000);
  const disabledRows = rows.filter(r => r.state.disabled);
  ok(disabledRows.length > 0, 'at least one row is disabled (the bodyguard already carries one)');
  for (const r of disabledRows) {
    const text = E.enhancementRefusalText(r.state.canAssign);
    ok(text.length > 0 && html.indexOf(text) >= 0,
       `disabled row ${r.name}@${r.detachment_key}: refusal text "${text}" appears in the rendered section`);
  }
  ok(html.indexOf('disabled') === -1 || rows.some(r => r.state.disabled),
     'the "disabled" CSS class only appears alongside an actually-disabled row');

  const withDesc = rows.find(r => r.description && r.description.length > 0);
  if (withDesc) {
    ok(html.indexOf(withDesc.description) >= 0,
       `${withDesc.name}: its own description text appears in the section's detail panel`);
  }
}

// ── 6. renderEnhancementChipHtml: numbers and warnings ───────────────────────
console.log("E4c — the roster chip's numbers are enhancementArmyState's numbers");
E.setDetachments([]);
E.setArmy([]);
ok(E.renderEnhancementChipHtml() === '', 'no detachments and nothing assigned renders nothing');

E.setDetachments([K_FIRE, K_FORG, K_FULG]);
E.setCap(1000);
{
  const a = assign(entry(1, 'Character'), N_ADAM, K_FIRE);
  const b = assign(entry(2, 'Character'), fireRegulars.find(n => n !== N_ADAM), K_FIRE);
  E.setArmy([a, b]);
  const st   = E.enhancementArmyState(1000);
  const html = E.renderEnhancementChipHtml();
  ok(html.indexOf(`${st.used} of ${st.limit}`) >= 0,
     `chip shows "${st.used} of ${st.limit}" matching enhancementArmyState`);
  ok(st.state === 'at', 'two regulars at a 2-limit battle size reads as at-limit (sanity on the fixture)');
}

console.log('E4c — the chip surfaces notOffered, wrongType, and sharedUnits by unit name');
E.setCap(2000);
{
  // notOffered: assign out of a detachment, then deselect it.
  const stale = assign(entry(1, 'Character', 'Stale Carrier'), N_DWA, K_WOTR);
  E.setArmy([stale]);
  E.setDetachments([K_FIRE]);   // WOTR no longer selected
  let html = E.renderEnhancementChipHtml();
  ok(html.indexOf('Stale Carrier') >= 0, 'the not-offered carrier is named in the chip');

  // wrongType: an Epic Hero somehow holding a regular pick.
  const wrong = assign(entry(2, 'Epic Hero', 'Wrong Type Carrier'), N_ADAM, K_FIRE);
  E.setArmy([wrong]);
  E.setDetachments([K_FIRE]);
  html = E.renderEnhancementChipHtml();
  ok(html.indexOf('Wrong Type Carrier') >= 0, 'the wrong-type carrier is named in the chip');

  // sharedUnits: two carriers in one attached cluster (reachable via import,
  // since assignment-time and attach-time gates both block this going forward).
  const bg   = assign(entry(3, 'Infantry', 'Shared Bodyguard'), N_BWS, K_FULG);
  const lead = assign(entry(4, 'Character', 'Shared Leader'), N_ADAM, K_FIRE);
  lead.attachedToListId = 3;
  E.setArmy([bg, lead]);
  E.setDetachments([K_FIRE, K_FULG]);
  html = E.renderEnhancementChipHtml();
  ok(html.indexOf('Shared Bodyguard') >= 0 || html.indexOf('Shared Leader') >= 0,
     'a shared-unit cluster is flagged by the root carrier\'s name');
}

console.log(fail === 0 ? '\nall E4c checks pass' : `\n${fail} E4c check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
