const fs=require('fs');
const src=fs.readFileSync(process.argv[2]||'index.html','utf8');
const lines=src.split('\n');
// slice from 'function loMaxCount' to end of loRollup
const start=lines.findIndex(l=>l.includes('function loMaxCount'));
const end=lines.findIndex(l=>l.includes('// Unit Options UI for loadout-defined units.'));
const body=lines.slice(start,end).join('\n');
const prelude=`
const PROFILE_SEP=' \\u2013 ';
function stripProfile(name){return String(name||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(name){return stripProfile(name).toLowerCase();}
`;
const mod=new Function(prelude+body+'\nreturn {loRollup,loMaxCount,loGroupCounts,loCarriers};')();
const L=JSON.parse(fs.readFileSync('unit_loadouts.json','utf8'));
function roll(uid,size,wargear){
  const def=L[uid];
  const sel={choiceById:{},countById:{},addById:{}};
  for(const o of def.options){const v=wargear[o.id];
    if(o.type==='choice') sel.choiceById[o.id]=v||null;
    else if(o.type==='count') sel.countById[o.id]=(v&&typeof v==='object')?v:(Number(v)||0);
    else if(o.type==='add') sel.addById[o.id]=Number(v)||0;}
  const r=mod.loRollup(def,size,sel);
  return {weapons:Object.fromEntries(r.weapons), equipment:Object.fromEntries(r.equipment), over:r.overAllocated};
}
module.exports={roll,L};
if(require.main===module){
  const cases=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
  for(const c of cases){
    const r=roll(c.uid,c.size,c.wargear||{});
    console.log('---',c.label);
    console.log('  weapons:',JSON.stringify(r.weapons));
    if(Object.keys(r.equipment).length) console.log('  equip:',JSON.stringify(r.equipment));
    if(r.over) console.log('  OVERALLOCATED');
  }
}
