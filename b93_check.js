// b93_check.js — B93 turn 2. Loads the REAL bearerNorm / bearerTermSet /
// bearerAbilitySet / enhancementBearerRestriction / enhancementBearerEligible
// out of index.html, together with the real E23/B128 tank_ace block and the real
// E29/B126 mark block they depend on, and drives them against the shipped
// detachments.json and units.json.
//
// The resolver replaced an 11-row hand-curated table (B113's seven, B126's four).
// Curation could be eyeballed; 641 records cannot, so the checks below are all
// re-derivations from source rather than restatements of a scope document:
//
//   1. Structure. Every enhancement record's bearer_restriction is well-formed —
//      non-empty alternatives, each a non-empty term list; scope drawn from the
//      three known values; resolution from the two known values. And index.html
//      no longer carries a curated bearer table, so the rule has exactly one
//      implementation.
//   2. Term matching. bearerNorm folds case and both apostrophe spellings;
//      bearerTermSet reads all three keyword fields, the datasheet name and the
//      entry's effective Mark of Chaos.
//   3. Alternatives are OR-of-AND, exclusions refuse, and the ability qualifier
//      is enforced against rule_names.
//   4. D199's permissive fall-through, in all three places it lives: an entry
//      whose datasheet is not in the pool, a unit with no keywords at all, and a
//      unit with no ability data facing an ability-qualified clause. Each must
//      ADMIT. This is the check most likely to be "tidied" into a refusal.
//   5. The eleven records the curated table used to cover resolve to the same
//      bearers it named — except Bray Lord, whose curated row was narrower than
//      its own clause (SORCERER is a keyword, and Sorcerer In Terminator Armour
//      carries it). Pinned as the corrected set, not the old one.
//   6. The Mark of Chaos records, moved here from b126_check: right mark
//      admitted, wrong mark and unmade choice refused, innate mark admitted.
//   7. D335, not D334: the Characters-only default is NOT demoted. A Vehicle is
//      refused a Vehicle-only enhancement until Tank Ace confers CHARACTER on it,
//      and then admitted — the case D334 got backwards.
//   8. Whole-army census over every built faction: the zero-admit and one-admit
//      populations are pinned by cause, so a resolver regression that strands an
//      enhancement fails here rather than in someone's list.
//   9. The exclusion reader's standing assumption: no unit in units.json carries
//      an exclusion keyword on some model groups but not others, which is what
//      makes a whole-unit exclusion reading equivalent to a per-group one.
//
// Build-time only; not part of the served app.
// Usage: node b93_check.js index.html detachments.json units.json faction_taxonomy.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function load(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const e23 = slice(lines, '// ── E23/B128: tank_ace capped Character selection', '// ── E23/B128 block end');
  const e29 = slice(lines, '// ── E29/B126: Marks of Chaos', '// ── E29/B126 block end');
  const b93 = slice(lines, '// ── B93: enhancement bearer restrictions', '// ── B93 block end');
  // enhancementRecord sits with the rest of the E4b read path; the resolver
  // calls it, so the real one is sliced rather than stubbed.
  const recSrc = slice(lines, '  function enhancementRecord(name, detachmentKey) {',
                              '  // An unresolved assignment contributes 0 points');
  // The chapter-keyword restoration the resolver depends on (B132): without it
  // Dark Angels' Deathwing clauses regress to zero bearers, which is check 8's
  // job to notice. The real function is used, not a copy.
  const chapSrc = slice(lines, '  function applyChapterKeywordAdditions(units, armyName) {',
                               '  // Resolve the unit set for a faction record');

  const prelude = `
    let armyList = [];
    let rawUnits = [];
    let detachmentDefs = {};
    let detachmentEffects = {};
    let selectedDetachments = [];
    function renderAll() {}
    function flashBanner() {}
    function setState({ raw, defs, effects, keys, list }) {
      if (raw !== undefined)     rawUnits = raw;
      if (defs !== undefined)    detachmentDefs = defs;
      if (effects !== undefined) detachmentEffects = effects;
      if (keys !== undefined)    selectedDetachments = keys;
      if (list !== undefined)    armyList = list;
    }
  `;

  return new Function(
    prelude + '\n' + chapSrc + '\n' + e23 + '\n' + e29 + '\n' + recSrc + '\n' + b93 + '\n' +
    'return { setState, bearerNorm, bearerTermSet, bearerAbilitySet,' +
    ' enhancementBearerRestriction, enhancementBearerEligible,' +
    ' entryEffectiveType, entryEffectiveMark, applyChapterKeywordAdditions,' +
    ' markKeywordSet };'
  )();
}

const idxPath  = process.argv[2] || 'index.html';
const detPath  = process.argv[3] || 'detachments.json';
const unitPath = process.argv[4] || 'units.json';
const taxPath  = process.argv[5] || 'faction_taxonomy.json';

const E   = load(idxPath);
const DJ  = JSON.parse(fs.readFileSync(detPath, 'utf8'));
const UJ  = JSON.parse(fs.readFileSync(unitPath, 'utf8'));
const TAX = JSON.parse(fs.readFileSync(taxPath, 'utf8'));
const IDX = fs.readFileSync(idxPath, 'utf8');

const byArmy = {};
for (const b of UJ) byArmy[b.army] = b.units;

let failures = 0;
function check(cond, msg) {
  if (!cond) { console.log('  FAIL ' + msg); failures++; }
}

// Every (detachment key, enhancement record) pair in the shipped data.
const RECORDS = [];
for (const [k, d] of Object.entries(DJ.detachments))
  for (const e of (d.enhancements || [])) RECORDS.push([k, e]);

function entry(listId, unitName, unitType, mark) {
  return { listId, unit_name: unitName, unit_type: unitType, mark: mark || null };
}

// ── 1. structure, and single implementation ──────────────────────────────────
console.log('B93 — the shipped bearer_restriction field is well-formed, and the curated table is gone');
{
  const SCOPES = new Set(['model', 'unit', 'bare_name']);
  const RES    = new Set(['parsed', 'curated']);
  let withRule = 0, bad = 0, firstBad = '';
  for (const [k, e] of RECORDS) {
    const br = e.bearer_restriction;
    if (!br) continue;
    withRule++;
    const ok = Array.isArray(br.alternatives) && br.alternatives.length > 0 &&
               br.alternatives.every(a => Array.isArray(a) && a.length > 0 &&
                                          a.every(t => typeof t === 'string' && t.trim())) &&
               Array.isArray(br.exclusions) &&
               br.exclusions.every(x => Array.isArray(x) && x.length > 0) &&
               SCOPES.has(br.scope) && RES.has(br.resolution) &&
               typeof br.clause === 'string' && br.clause.trim().length > 0;
    if (!ok) { bad++; if (!firstBad) firstBad = `${k} / ${e.name}`; }
  }
  check(bad === 0, `${bad} malformed bearer_restriction record(s), first: ${firstBad}`);
  check(withRule === 641, `expected 641 records carrying a bearer_restriction, got ${withRule}`);
  check(RECORDS.length === 739, `expected 739 enhancement records, got ${RECORDS.length}`);

  check(!/ENHANCEMENT_BEARER_RESTRICTIONS/.test(IDX),
        'index.html still declares ENHANCEMENT_BEARER_RESTRICTIONS — the curated table must not survive alongside the resolver');
  // The resolver must read the data, not a literal: a clause string hard-coded
  // in index.html would mean a second copy of the vocabulary.
  check(!/model only/i.test(IDX.split('── B93: enhancement bearer restrictions')[1].split('── B93 block end')[0]
                             .replace(/\/\/[^\n]*/g, '')),
        'the B93 block carries clause text outside its comments — the vocabulary belongs in detachments.json');
}

// ── 2. normalisation and the term namespaces ─────────────────────────────────
console.log('B93 — bearerNorm folds case and apostrophes; bearerTermSet reads all four namespaces');
{
  check(E.bearerNorm('ADEPTUS ASTARTES') === 'adeptus astartes', 'bearerNorm folds case');
  check(E.bearerNorm("Emperor\u2019s Children") === E.bearerNorm("Emperor's Children"),
        'bearerNorm folds the curly and straight apostrophe spellings together');
  check(E.bearerNorm('  Jump   Pack ') === 'jump pack', 'bearerNorm collapses whitespace');

  const raw = {
    unit_name: 'Test Lord', unit_type: 'Character',
    model_groups: [{ keyword_names: ['Character', 'Infantry'],
                     faction_keyword_names: ['Heretic Astartes'],
                     model_keyword_names: [{ keywords: ['Chaos Undivided'] }],
                     rule_names: ['Deep Strike'] }]
  };
  E.setState({ raw: [raw], effects: {}, keys: [] });
  const t = E.bearerTermSet(entry(1, 'Test Lord', 'Character'), []);
  check(t.has('character'),        'keyword_names is read');
  check(t.has('heretic astartes'), 'faction_keyword_names is read');
  check(t.has('chaos undivided'),  'model_keyword_names is read');
  check(t.has('test lord'),        'the datasheet name is a term');

  const ab = E.bearerAbilitySet(raw);
  check(ab.has('deep strike'), 'rule_names feeds the ability set');
}

// ── 3. alternatives, exclusions, ability qualifier ───────────────────────────
console.log('B93 — OR-of-AND alternatives, refusing exclusions, and the ability qualifier');
{
  const raw = [
    { unit_name: 'Termie Captain', unit_type: 'Character',
      model_groups: [{ keyword_names: ['Adeptus Astartes', 'Captain', 'Character', 'Terminator'],
                       faction_keyword_names: [], model_keyword_names: [], rule_names: ['Deep Strike'] }] },
    { unit_name: 'Gravis Captain', unit_type: 'Character',
      model_groups: [{ keyword_names: ['Adeptus Astartes', 'Captain', 'Character', 'Gravis'],
                       faction_keyword_names: [], model_keyword_names: [], rule_names: ['Leader'] }] },
    { unit_name: 'Plain Captain', unit_type: 'Character',
      model_groups: [{ keyword_names: ['Adeptus Astartes', 'Captain', 'Character'],
                       faction_keyword_names: [], model_keyword_names: [], rule_names: [] }] },
  ];
  const defs = { 'T|D': { enhancements: [
    { name: 'TwoAlts', bearer_restriction: { clause: 'x', scope: 'model', resolution: 'parsed',
        alternatives: [['Adeptus Astartes', 'Terminator'], ['Gravis']], exclusions: [], ability: null } },
    { name: 'Excluded', bearer_restriction: { clause: 'x', scope: 'model', resolution: 'parsed',
        alternatives: [['Adeptus Astartes']], exclusions: [['Terminator']], ability: null } },
    { name: 'NeedsDS', bearer_restriction: { clause: 'x', scope: 'model', resolution: 'parsed',
        alternatives: [['Captain']], exclusions: [], ability: 'Deep Strike' } },
    { name: 'NoRule', bearer_restriction: null },
  ] } };
  E.setState({ raw, defs, effects: {}, keys: ['T|D'] });
  const T = entry(1, 'Termie Captain', 'Character');
  const G = entry(2, 'Gravis Captain', 'Character');
  const P = entry(3, 'Plain Captain', 'Character');

  check(E.enhancementBearerEligible(T, 'TwoAlts', 'T|D') === true,  'first alternative satisfied');
  check(E.enhancementBearerEligible(G, 'TwoAlts', 'T|D') === true,  'second alternative satisfied');
  check(E.enhancementBearerEligible(P, 'TwoAlts', 'T|D') === false, 'neither alternative satisfied is a refusal');

  check(E.enhancementBearerEligible(P, 'Excluded', 'T|D') === true,  'an unexcluded match is admitted');
  check(E.enhancementBearerEligible(T, 'Excluded', 'T|D') === false, 'an exclusion refuses an otherwise-matching unit');

  check(E.enhancementBearerEligible(T, 'NeedsDS', 'T|D') === true,  'the ability qualifier admits a unit that has it');
  check(E.enhancementBearerEligible(G, 'NeedsDS', 'T|D') === false, 'the ability qualifier refuses a unit that lacks it');

  check(E.enhancementBearerRestriction('NoRule', 'T|D') === null, 'a record with no clause carries no rule');
  check(E.enhancementBearerEligible(P, 'NoRule', 'T|D') === true, 'and is admitted to everyone');
}

// ── 4. D199 — every fall-through admits ──────────────────────────────────────
console.log('B93 — D199: an unevaluable restriction falls through to permissive, never to a refusal');
{
  const raw = [
    { unit_name: 'No Keywords', unit_type: 'Character',
      model_groups: [{ keyword_names: [], faction_keyword_names: [], model_keyword_names: [], rule_names: [] }] },
    { unit_name: 'No Abilities', unit_type: 'Character',
      model_groups: [{ keyword_names: ['Captain'], faction_keyword_names: [], model_keyword_names: [] }] },
  ];
  const defs = { 'T|D': { enhancements: [
    { name: 'Narrow', bearer_restriction: { clause: 'x', scope: 'model', resolution: 'parsed',
        alternatives: [['Deathwing']], exclusions: [], ability: null } },
    { name: 'NeedsDS', bearer_restriction: { clause: 'x', scope: 'model', resolution: 'parsed',
        alternatives: [['Captain']], exclusions: [], ability: 'Deep Strike' } },
  ] } };
  E.setState({ raw, defs, effects: {}, keys: ['T|D'] });

  // (a) the datasheet is not in the pool at all
  check(E.enhancementBearerEligible(entry(1, 'Not In Pool', 'Character'), 'Narrow', 'T|D') === true,
        'an entry whose datasheet is absent from rawUnits is ADMITTED, not refused');
  // NOTE: "No Keywords" still yields its own name as a term, so the empty-set
  // branch is reached through a nameless record — the shape a stripped or
  // partially-built roster produces.
  E.setState({ raw: [{ unit_name: '', unit_type: 'Character', model_groups: [{}] }] });
  check(E.enhancementBearerEligible(entry(1, '', 'Character'), 'Narrow', 'T|D') === true,
        'a unit with an empty term set is ADMITTED, not refused');
  // (c) no ability data at all, against an ability-qualified clause
  E.setState({ raw });
  check(E.enhancementBearerEligible(entry(2, 'No Abilities', 'Character'), 'NeedsDS', 'T|D') === true,
        'a unit carrying no ability data at all is ADMITTED against an ability qualifier');
  // and the negative control: keywords present, clause simply not met
  check(E.enhancementBearerEligible(entry(3, 'No Abilities', 'Character'), 'Narrow', 'T|D') === false,
        'a unit WITH keywords that do not match is still refused — the fall-through is not a blanket pass');
}

// ── real-data scaffolding, shared by checks 5–8 ──────────────────────────────
function resolveUnits(f) {
  if (!f.is_subfaction) return (byArmy[f.data_army] || byArmy['Adeptus Astartes'] || []).slice();
  const chapter = byArmy[f.data_army] || [];
  if (f.roster_mode === 'complete') return chapter.slice();
  const generic = byArmy['Adeptus Astartes'] || [];
  const names = new Set(chapter.map(u => u.unit_name));
  // Point overrides touch points only, never keywords, so only the keyword map
  // matters here — and it is the REAL one out of index.html.
  return E.applyChapterKeywordAdditions(
    generic.filter(u => !names.has(u.unit_name)).concat(chapter), f.data_army);
}
const FACTIONS = [].concat(...TAX.groups.map(g => g.factions)).filter(f => f.built);

// Bearers of one record within one faction's resolved pool, applying the same
// two gates canAssignEnhancement applies: the Characters-only default (D335,
// NOT demoted) and the unconditional Epic Hero refusal.
function bearers(f, detKey, rec) {
  const units = resolveUnits(f);
  E.setState({ raw: units, defs: DJ.detachments, effects: {}, keys: [detKey], list: [] });
  const out = [];
  for (const u of units) {
    if (u.unit_type === 'Epic Hero') continue;
    if (!rec.is_upgrade && u.unit_type !== 'Character') continue;
    if (E.enhancementBearerEligible(entry(1, u.unit_name, u.unit_type), rec.name, detKey)) out.push(u.unit_name);
  }
  return out.sort();
}
function faction(name) {
  const f = FACTIONS.find(x => x.name === name);
  if (!f) throw new Error(`faction ${name} not built`);
  return f;
}
function record(detKey, name) {
  const r = (DJ.detachments[detKey].enhancements || []).find(e => e.name === name);
  if (!r) throw new Error(`${detKey} / ${name} not found`);
  return r;
}

// ── 5. the eleven records the curated table used to cover ────────────────────
console.log('B93 — the records B113 and B126 curated resolve to the pinned bearer sets');
{
  const CASES = [
    ['Space Wolves',      'Space Wolves|SAGA OF THE BEASTSLAYER', 'Wolf-touched',
     ['Iron Priest', 'Wolf Guard Battle Leader', 'Wolf Priest']],
    ['Space Wolves',      'Space Wolves|SAGA OF THE GREAT WOLF',  "Grimnar's Mark",
     ['Captain In Terminator Armour']],
    ['Chaos Space Marines', 'Chaos Space Marines|NIGHTMARE HUNT', 'Sorrowscent Vulture',
     ['Chaos Lord with Jump Pack']],
    // CORRECTED, not carried over: B113's row named Sorcerer and Infernal Master
    // only. The clause is keyword-scoped ("model only"), SORCERER is a real
    // datasheet keyword, and Sorcerer In Terminator Armour carries it — so the
    // curated row refused a legal bearer. Checked against Datasheets_keywords
    // through units.json, not inferred from the datasheet list.
    ['Thousand Sons',     'Thousand Sons|WARPMELD PACT',          'Bray Lord',
     ['Infernal Master', 'Sorcerer', 'Sorcerer In Terminator Armour']],
    ["Emperor's Children", "Emperor's Children|COURT OF THE PHOENICIAN", 'Exalted Patron',
     ['Lord Exultant']],
    ['World Eaters',      'World Eaters|CULT OF BLOOD',           'Butcher Lord',
     ['Master of Executions', 'Slaughterbound']],
    ['World Eaters',      'World Eaters|KHORNE DAEMONKIN',        'Disciple of Khorne',
     ['Lord on Juggernaut']],
  ];
  for (const [fname, detKey, name, want] of CASES) {
    const got = bearers(faction(fname), detKey, record(detKey, name));
    check(JSON.stringify(got) === JSON.stringify(want.slice().sort()),
          `${name}: bearers ${JSON.stringify(got)} != pinned ${JSON.stringify(want.slice().sort())}`);
  }
  // Pact of Cursed Pinions still carries no bearer text anywhere in the sources
  // (B113_LEADER_RESTRICTION_SCOPE.md §4) and must stay unenforced — the data
  // turn must not have invented a clause for it.
  E.setState({ defs: DJ.detachments, keys: ['Chaos Space Marines|MURDERTALON RAIDERS'] });
  check(E.enhancementBearerRestriction('Pact of Cursed Pinions', 'Chaos Space Marines|MURDERTALON RAIDERS') === null,
        'Pact of Cursed Pinions carries no bearer restriction');
}

// ── 6. the Mark of Chaos records (moved from b126_check) ─────────────────────
console.log('B93 — the four Pactbound Zealots mark records resolve through entryEffectiveMark');
{
  const PZ = 'Chaos Space Marines|PACTBOUND ZEALOTS';
  const DE = JSON.parse(fs.readFileSync('detachment_effects.json', 'utf8'));
  const effects = { [PZ]: DE.effects[PZ] };
  const units = byArmy['Chaos Space Marines'];
  E.setState({ raw: units, defs: DJ.detachments, effects, keys: [PZ], list: [] });

  const EXPECT = { 'Eye of Tzeentch': 'Tzeentch', 'Intoxicating Elixir': 'Slaanesh',
                   'Orbs of Unlife': 'Nurgle', 'Talisman of Burning Blood': 'Khorne' };
  for (const [name, mark] of Object.entries(EXPECT)) {
    const r = E.enhancementBearerRestriction(name, PZ);
    check(!!r && r.alternatives.some(a => a.some(t => E.bearerNorm(t) === E.bearerNorm(mark))),
          `${name} carries a clause naming ${mark}`);
  }
  const lord = entry(1, 'Chaos Lord', 'Character', 'Nurgle');
  check(E.enhancementBearerEligible(lord, 'Orbs of Unlife', PZ) === true,
        'a Nurgle Chaos Lord may take Orbs of Unlife');
  check(E.enhancementBearerEligible(lord, 'Eye of Tzeentch', PZ) === false,
        'a Nurgle Chaos Lord may not take Eye of Tzeentch');
  check(E.enhancementBearerEligible(entry(2, 'Chaos Lord', 'Character', null), 'Orbs of Unlife', PZ) === false,
        'a Chaos Lord with the mark choice still outstanding is refused');
  // An innate mark needs no pick. Khorne Berzerkers are Battleline, so this is
  // asked of the resolver directly rather than through the Characters gate.
  check(E.enhancementBearerEligible(entry(3, 'Khorne Berzerkers', 'Battleline', null), 'Talisman of Burning Blood', PZ) === true,
        'an innate Khorne unit satisfies the Khorne clause with no pick');
}

// ── 7. D335, not D334 — the Characters-only default is not demoted ───────────
console.log('B93 — D335: a Vehicle reaches a Vehicle-only enhancement through Tank Ace, not by demoting the type gate');
{
  const HH = 'Space Marines|HEADHUNTER TASK FORCE';
  const DE = JSON.parse(fs.readFileSync('detachment_effects.json', 'utf8'));
  const effects = { [HH]: DE.effects[HH] };
  const units = byArmy['Adeptus Astartes'];
  E.setState({ raw: units, defs: DJ.detachments, effects, keys: [HH], list: [] });

  const rec = record(HH, 'Astartes Tank Ace');
  check(!!rec.bearer_restriction && /vehicle/i.test(rec.bearer_restriction.clause),
        'Astartes Tank Ace still carries a Vehicle clause');

  // A Vehicle that IS in the tank_ace pool: refused while unchecked (it is not a
  // Character), admitted once checked. Picked from the data rather than named.
  const veh = units.find(u => u.unit_type !== 'Character' && u.unit_type !== 'Epic Hero' &&
    (u.model_groups || []).some(g => (g.keyword_names || []).includes('Vehicle')) &&
    E.entryEffectiveType({ listId: 9, unit_name: u.unit_name, unit_type: u.unit_type, tankAce: true }, [HH]) === 'Character');
  check(!!veh, 'a Vehicle in the Headhunter Task Force tank_ace pool exists in the data');
  if (veh) {
    const off = { listId: 9, unit_name: veh.unit_name, unit_type: veh.unit_type, tankAce: false };
    const on  = { listId: 9, unit_name: veh.unit_name, unit_type: veh.unit_type, tankAce: true };
    E.setState({ list: [on] });
    check(E.entryEffectiveType(off, [HH]) !== 'Character',
          `${veh.unit_name} is not a Character until Tank Ace is picked`);
    check(E.entryEffectiveType(on, [HH]) === 'Character',
          `${veh.unit_name} becomes a Character when Tank Ace is picked`);
    check(E.enhancementBearerEligible(on, 'Astartes Tank Ace', HH) === true,
          `${veh.unit_name} satisfies the Vehicle clause`);
  }
  // The complement: a Character that is not a Vehicle is refused, which is the
  // half the engine got wrong before B93 (it offered these on any Character).
  const cap = units.find(u => u.unit_name === 'Captain');
  check(!!cap, 'Captain is present in the generic Adeptus Astartes pool');
  check(E.enhancementBearerEligible(entry(8, 'Captain', 'Character'), 'Astartes Tank Ace', HH) === false,
        'a plain Captain is now refused Astartes Tank Ace');
}

// ── 8. whole-army census, pinned by cause ────────────────────────────────────
console.log('B93 — whole-army census: the zero-admit and one-admit populations are pinned');
{
  let evaluated = 0;
  const zero = {};
  let one = 0;
  for (const f of FACTIONS) {
    const keys = DJ.armies[f.data_army] || [];
    for (const k of keys) {
      for (const e of (DJ.detachments[k].enhancements || [])) {
        if (!e.bearer_restriction) continue;
        evaluated++;
        const n = bearers(f, k, e).length;
        if (n === 0) zero[e.bearer_restriction.clause] = (zero[e.bearer_restriction.clause] || 0) + 1;
        else if (n === 1) one++;
      }
    }
  }
  check(evaluated === 1145, `expected 1145 army x record evaluations, got ${evaluated}`);

  // Every zero-admit clause must be one of the four KNOWN causes, each of which
  // is reachable by another mechanism or is an honestly-absent faction. A new
  // clause appearing here means the resolver stranded an enhancement.
  const EXPECT_ZERO = {
    // reachable through the Tank Ace checkbox (B128) — 12 armies x 4 records
    'Adeptus Astartes Vehicle model only': 48,
    // reachable once the player picks the mark (B126)
    'Heretic Astartes Khorne model only': 1,
    'Heretic Astartes Tzeentch model only': 1,
    'Heretic Astartes Nurgle model only': 1,
    'Heretic Astartes Slaanesh model only': 1,
    // Harlequins are not a built faction, so this genuinely has no bearer yet
    'Harlequins model only': 1,
  };
  const gotKeys = Object.keys(zero).sort();
  const wantKeys = Object.keys(EXPECT_ZERO).sort();
  check(JSON.stringify(gotKeys) === JSON.stringify(wantKeys),
        `zero-admit clauses ${JSON.stringify(gotKeys)} != pinned ${JSON.stringify(wantKeys)}`);
  for (const c of wantKeys)
    check(zero[c] === EXPECT_ZERO[c], `zero-admit count for ${c}: got ${zero[c]} want ${EXPECT_ZERO[c]}`);

  // The one-admit set is where a resolver bug turns into an unassignable
  // enhancement rather than a mildly wrong list, so its size is pinned too.
  check(one === 98, `expected 98 one-admit army x record cases, got ${one}`);
}

// ── 9. the exclusion reader's standing assumption ────────────────────────────
console.log('B93 — no unit splits an exclusion keyword across its model groups');
{
  const EX = new Set();
  for (const [, e] of RECORDS)
    for (const x of ((e.bearer_restriction || {}).exclusions || []))
      for (const t of x) EX.add(t);
  check(EX.size > 0, 'the shipped data carries at least one exclusion term');

  const split = [];
  for (const b of UJ) for (const u of b.units) {
    const gs = u.model_groups || [];
    if (gs.length < 2) continue;
    for (const t of EX) {
      const has = gs.map(g => (g.keyword_names || []).concat(g.faction_keyword_names || [])
                               .some(k => E.bearerNorm(k) === E.bearerNorm(t)));
      if (has.some(Boolean) && !has.every(Boolean)) split.push(`${b.army}/${u.unit_name}/${t}`);
    }
  }
  check(split.length === 0,
        `${split.length} unit(s) carry an exclusion keyword on some model groups but not others ` +
        `(${split.slice(0, 3).join(', ')}) — the whole-unit exclusion reading now over-refuses and must go per-group`);
}

if (failures) {
  console.log(`b93_check: ${failures} FAILED`);
  process.exitCode = 1;
} else {
  console.log('all B93 checks pass (structure, term namespaces, alternatives/exclusions/ability, ' +
              'D199 fall-through in all three places, the eleven formerly-curated records, ' +
              'the mark records, D335 via Tank Ace, the 1145-evaluation census and the exclusion assumption)');
}
