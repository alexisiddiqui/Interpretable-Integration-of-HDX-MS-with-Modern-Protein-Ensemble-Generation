/* Peptide-frame maps. Rendering only: scientific values are computed upstream. */
(function () {
 'use strict';
 const NS = 'http://www.w3.org/2000/svg';
 const instances = new Map();
 const channels = [
  {key:'shape', label:'Shape / height', short:'Height', unit:'Å', range:[-10,10], ends:['−10 Å','+10 Å'], colors:['#356c9b','#e8e4dc','#bb683f'], description:'Outward height relative to the mutation-site centre', field:'z'},
  {key:'electrostatics', label:'Electrostatics', short:'APBS', unit:'kT/e', range:[-5,5], ends:['−5 kT/e','+5 kT/e'], colors:['#c44348','#f0e9e3','#3d74ba'], description:'Partner-only potential · negative ← → positive', field:'potential'},
  {key:'hydrophobicity', label:'Hydrophobicity', short:'KD index', unit:'KD', range:[-4.5,4.5], ends:['−4.5','+4.5'], colors:['#3b7fa0','#e7e7dc','#d59b2d'], description:'Hydrophilic ← Kyte–Doolittle → hydrophobic', field:'hydrophobicity'},
  {key:'size', label:'Side-chain size', short:'vdW volume', unit:'Å³', range:[0,200], ends:['0 Å³','200 Å³'], colors:['#d5e6df','#568e81','#174f50'], description:'Modeled side-chain van der Waals union volume', field:'sidechain_volume'}
 ];
 function data() {
  if (window.OPIG_RADIAL_DATA) return window.OPIG_RADIAL_DATA;
  const script = document.getElementById('radial-data');
  if (!script) return {records:{}};
  try { window.OPIG_RADIAL_DATA = JSON.parse(script.textContent); }
  catch (error) { console.error('Could not read radial-map data:', error); return {records:{}}; }
  return window.OPIG_RADIAL_DATA;
 }
 function element(tag, attrs, content) {
  const node = document.createElementNS(NS, tag);
  for (const [key,value] of Object.entries(attrs || {})) if(value !== null && value !== undefined) node.setAttribute(key,String(value));
  if (content !== undefined) node.textContent = content;
  return node;
 }
 function html(tag, className, content) {
  const node = document.createElement(tag); if(className) node.className = className;
  if(content !== undefined) node.textContent = content; return node;
 }
 function finite(value) { return typeof value === 'number' && Number.isFinite(value); }
 function fmt(value, digits) { return finite(value) ? value.toFixed(digits === undefined ? 1 : digits) : '—'; }
 function palette(root) {
  const style = getComputedStyle(root);
  const read = (name, fallback) => style.getPropertyValue(name).trim() || fallback;
  return {bg:read('--bg','#f4f2ee'),panel:read('--panel','#ffffff'),grid:read('--grid','#e6e3dc'),line:read('--line','#d8d4cb'),ink:read('--ink','#1d2127'),muted:read('--muted','#727986'),peptide:read('--peptide','#0f7a7f'),mutation:read('--mutation','#c2185b'),fragment:read('--fragment','#e0a100'),missing:read('--hla','#9ba7b4')};
 }
 function rgb(hex) { const value = hex.replace('#',''); return [0,2,4].map(n=>parseInt(value.slice(n,n+2),16)); }
 function color(value, channel, missing) {
  if(!finite(value)) return missing;
  const t = Math.max(0,Math.min(1,(value-channel.range[0])/(channel.range[1]-channel.range[0])));
  const half = t < 0.5 ? 0 : 1; const f = t < 0.5 ? 2*t : 2*t-1;
  const a = rgb(channel.colors[half]); const b = rgb(channel.colors[half+1]);
  return `rgb(${a.map((v,i)=>Math.round(v+(b[i]-v)*f)).join(',')})`;
 }
 function residueLabel(residue) { return `${residue.chain || '?'}:${residue.name || residue.aa || '?'}${residue.resi === undefined ? '' : residue.resi}${residue.icode || ''}`; }
 function observedPeptide(record) {return Boolean(record && (record.peptide || []).some(p=>p.observed===true));}
 function centerPosition(record) {if(record?.center?.unrelated_control)return null;return record && record.center && finite(record.center.peptide_position)?record.center.peptide_position:6;}
 function siteLabel(record){const p=centerPosition(record);return p==null?'Reference site':'P'+p;}
 function centerText(record) {return record && record.center && record.center.label || `P${centerPosition(record)} mutation-site centre`;}
 function labelLayout(residues,peptide,mapX,mapY,cx,cy,edge) {
  // Greedy, deterministic placement shared by every property map. Footprints
  // remain at their physical positions; only text may move, with leader lines.
  const boxes=[[cx-9,cy-9,18,18]], positions=new Map(),multipleChains=new Set(residues.map(r=>r.chain)).size>1;
  peptide.forEach(r=>{const text=`${r.aa || ''}${r.position}`,w=text.length*6.1+5;boxes.push([mapX(r.x)-w/2,mapY(r.y)+5,w,13]);});
  const offsets=[[0,-9],[0,16],[15,-9],[-15,-9],[18,16],[-18,16],[0,-24],[0,30],[30,-9],[-30,-9],[30,24],[-30,24]];
  const overlap=(a,b)=>Math.max(0,Math.min(a[0]+a[2],b[0]+b[2])-Math.max(a[0],b[0]))*Math.max(0,Math.min(a[1]+a[3],b[1]+b[3])-Math.max(a[1],b[1]));
  residues.filter(r=>finite(r.x)&&finite(r.y)).slice().sort((a,b)=>a.y-b.y || a.x-b.x || String(a.key).localeCompare(String(b.key))).forEach(r=>{
   const text=`${multipleChains?r.chain+':':''}${r.aa || r.name || ''}${r.resi}${r.icode || ''}`,w=text.length*6.6+5,px=mapX(r.x),py=mapY(r.y);
   let best=null;
   offsets.forEach(([dx,dy])=>{
    const x=px+dx,y=py+dy,box=[x-w/2,y-10,w,14];
    const outside=Math.max(0,...[[-w/2,-10],[w/2,-10],[-w/2,4],[w/2,4]].map(([a,b])=>Math.hypot(x+a-cx,y+b-cy)-edge+2));
    const score=boxes.reduce((sum,prior)=>sum+overlap(box,prior),0)*10+outside*200+(dx*dx+dy*dy)*.06;
    if(!best || score<best.score)best={x,y,text,box,score,leader:Math.hypot(dx,dy)>13};
   });
   boxes.push(best.box);positions.set(r.key,best);
  });
  return positions;
 }
 function contactResidues(state) {
  const residues = state.record && state.record.residues || [];
  return residues.filter(r=>finite(r.min_target_distance) && r.min_target_distance<=4.5 && (state.scope!=='peptide' || finite(r.min_peptide_distance) && r.min_peptide_distance<=4.5));
 }
 function visibleResidues(state) {
  return contactResidues(state).filter(r=>{
   const points = r.footprint && r.footprint.length ? r.footprint : [[r.x,r.y]];
   return points.some(p=>finite(p[0]) && finite(p[1]) && Math.hypot(p[0],p[1])<=state.radius);
  });
 }
 function init(id) {
  if(instances.has(id)) return instances.get(id);
  const root = document.getElementById(`radial-${id}`); if(!root) return null;
  const dom = {}; root.querySelectorAll('[data-radial]').forEach(node=>{dom[node.dataset.radial]=node;});
  const state = {id,root,dom,key:null,record:null,channel:'all',scope:'target',radius:25,labels:true,patch:true,selected:null,callback:null};
  instances.set(id,state);
  ['channel','scope','radius','labels','patch'].forEach(key=>{
   dom[key].addEventListener('change',()=>{
    state[key] = key==='radius' ? Number(dom[key].value) : ['labels','patch'].includes(key) ? dom[key].checked : dom[key].value;
    if(['scope','radius'].includes(key) && !visibleResidues(state).some(r=>r.key===state.selected)) state.selected=null;
    render(state);
   });
  });
  dom.residue.addEventListener('change',()=>selectResidue(state,dom.residue.value,true));
  root.querySelectorAll('[data-radial-export]').forEach(button=>button.addEventListener('click',()=>exportMap(state,button.dataset.radialExport)));
  return state;
 }
 function setContext(state) {
  const {dom,record} = state; dom.context.replaceChildren();
  if(!record) {dom.context.textContent='Select a structure to inspect its partner interface.';return;}
  dom.context.appendChild(html('strong','',record.label || record.id || state.key));
  const center = record.center || {};
  dom.context.appendChild(document.createTextNode(' · '));
  if(!record.center){dom.context.appendChild(document.createTextNode('Projection not computed'));dom.provenance.textContent='';return;}
  if(center.kind==='transferred') dom.context.appendChild(html('span','radial-transfer',`${center.label || 'Mutation-site centre'} · transferred${observedPeptide(record)?'':' · peptide absent'}`));
  else dom.context.appendChild(document.createTextNode(center.label || `Observed P${centerPosition(record)} Cα centre`));
  if(record.target_covalent_ligands?.length)dom.context.appendChild(document.createTextNode(' · covalent target ligand included: '+record.target_covalent_ligands.map(r=>r.name+' '+r.chain+':'+r.resi+(r.icode||'')).join(', ')));
  const frame = record.frame || {};
  if(finite(frame.alignment_rmsd)) dom.context.appendChild(document.createTextNode(` · frame alignment ${fmt(frame.alignment_rmsd,2)} Å RMSD (${frame.aligned_residues || '—'} residues)`));
  dom.provenance.textContent = [frame.reference ? `Frame: ${frame.reference}` : '', center.kind==='transferred' && center.source ? `Transferred from ${center.source}` : ''].filter(Boolean).join(' · ');
 }
 function render(state) {
  const {dom,record} = state; setContext(state);
  dom.maps.replaceChildren(); dom.facts.replaceChildren();
  const ok = Boolean(record && record.status==='ok');
  dom.empty.hidden = ok; dom.key.hidden = !ok; dom.inspector.hidden = !ok;
  state.root.querySelectorAll('[data-radial-export]').forEach(button=>{button.disabled=!ok;});
  dom['patch-control'].hidden = state.id!=='prediction'; dom['patch-key'].hidden=state.id!=='prediction' || !state.patch;
  dom['peptide-key'].textContent=observedPeptide(record)?'Peptide Cα · dashed = transferred guide':'Transferred peptide trace · guide only';
  dom['center-key'].textContent=centerText(record);
  if(!ok) {
   const headings = {no_partner:'No binding partner in this structure',unavailable:'Interface map unavailable',error:'Interface-map calculation failed'};
   dom.empty.replaceChildren(html('strong','',headings[record && record.status] || 'Select a structure'));
   dom.empty.appendChild(document.createTextNode(record && record.reason || 'Choose an experimental complex or a passing pilot pose to display its interface.'));
   dom.status.textContent='No partner-residue surface is inferred for this entry.'; return;
  }
  const residues = visibleResidues(state); const total = contactResidues(state).length;
  const buried = record.summary && record.summary.partner_buried_sasa;
  dom.status.textContent = `${residues.length} / ${total} contact residues in the ${state.radius} Å window${finite(buried) ? ` · whole-target buried area ${fmt(buried,0)} Å²` : ''}${record.center && record.center.kind==='transferred' ? observedPeptide(record)?' · mutation-site centre transferred':' · transferred frame; peptide and mutation-site contacts absent' : ''}`;
  if(!residues.length) {
   dom.empty.hidden=false; dom.empty.replaceChildren(html('strong','','No residues in this contact view'));
   dom.empty.appendChild(document.createTextNode(state.scope==='peptide' ? 'There are no observed partner–peptide contacts in this pose. Choose whole-target contacts to inspect the HLA interface.' : 'Increase the map radius to inspect contacts farther from P6.'));
  }
  dom.maps.classList.toggle('radial-single',state.channel!=='all');
  const shown = state.channel==='all' ? channels : channels.filter(c=>c.key===state.channel);
  shown.forEach(channel=>dom.maps.appendChild(drawCard(state,channel,residues)));
  dom.residue.replaceChildren(new Option('Choose a residue…',''));
  residues.slice().sort((a,b)=>String(a.chain).localeCompare(String(b.chain)) || Number(a.resi)-Number(b.resi) || String(a.icode || '').localeCompare(String(b.icode || ''))).forEach(r=>{
   dom.residue.appendChild(new Option(`${residueLabel(r)} · ${fmt(r.min_target_distance)} Å target`,r.key));
  });
  if(state.selected && residues.some(r=>r.key===state.selected)) selectResidue(state,state.selected,false);
  else {state.selected=null; dom['residue-title'].textContent='Choose a residue';dom.residue.value='';}
 }
 function drawCard(state,channel,residues) {
  const card=html('figure','radial-map-card'); card.dataset.channel=channel.key;
  const cap=html('figcaption'); cap.appendChild(html('h4','',channel.label));cap.appendChild(html('span','',channel.short+' · '+channel.unit));card.appendChild(cap);
  const p=palette(state.root), radius=state.radius, cx=230, cy=218, edge=174, scale=edge/radius;
  const mapX=x=>cx+x*scale, mapY=y=>cy-y*scale;
  const svg=element('svg',{class:'radial-map',viewBox:'0 0 460 450',role:'group','aria-label':`${channel.label}, ${radius} Å radius, ${residues.length} partner residues`,xmlns:NS});
  svg.dataset.channel=channel.key; svg.appendChild(element('title',{},`${state.record.label || state.key}: ${channel.label}`));
  svg.appendChild(element('desc',{},`Orthographic peptide-groove projection, ${centerText(state.record)}. N to C runs left to right. Select a residue for its properties. ${channel.description}.`));
  const defs=element('defs'); const clipId=`radial-${state.id}-${channel.key}-clip`;
  const clip=element('clipPath',{id:clipId});clip.appendChild(element('circle',{cx,cy,r:edge}));defs.appendChild(clip);svg.appendChild(defs);
  svg.appendChild(element('circle',{cx,cy,r:edge,fill:p.panel,stroke:p.line,'stroke-width':1}));
  const ringStep=radius===40 ? 10 : 5;
  for(let ring=ringStep;ring<=radius;ring+=ringStep) {
   svg.appendChild(element('circle',{cx,cy,r:ring*scale,fill:'none',stroke:p.grid,'stroke-width':1}));
   svg.appendChild(element('text',{x:cx+ring*scale*.71+3,y:cy-ring*scale*.71-2,fill:p.muted,'font-size':10,'font-family':'IBM Plex Mono,monospace'},`${ring} Å`));
  }
  svg.appendChild(element('path',{d:`M${cx-edge},${cy}H${cx+edge} M${cx},${cy-edge}V${cy+edge}`,stroke:p.line,'stroke-width':1,'stroke-dasharray':'3 5',fill:'none'}));
  const surface=element('g',{'clip-path':`url(#${clipId})`});
  const peptide=(state.record.peptide || []).filter(r=>finite(r.x) && finite(r.y));
  const labels=state.labels?labelLayout(residues,peptide,mapX,mapY,cx,cy,edge):new Map();
  residues.slice().sort((a,b)=>(a.z || 0)-(b.z || 0)).forEach(residue=>{
   const group=element('g',{class:'radial-residue',tabindex:0,role:'button','data-residue-key':residue.key,'aria-label':`${residueLabel(residue)}, ${channel.label} ${fmt(residue[channel.field])} ${channel.unit}. ${fmt(residue.min_target_distance)} Å from target.`});
   const value=channel.key==='electrostatics' && state.record.electrostatics && state.record.electrostatics.status!=='ok' ? null : residue[channel.field];
   const fill=color(value,channel,p.missing), outline=state.patch && state.id==='prediction' && residue.native_patch ? p.fragment : p.line;
   const points=(residue.footprint || []).filter(point=>finite(point[0]) && finite(point[1]));
   let footprint;
   if(points.length>=3) footprint=element('polygon',{points:points.map(point=>`${mapX(point[0]).toFixed(2)},${mapY(point[1]).toFixed(2)}`).join(' ')});
   else footprint=element('circle',{cx:mapX(residue.x),cy:mapY(residue.y),r:2.4});
   footprint.setAttribute('class','radial-footprint');footprint.setAttribute('fill',fill);footprint.setAttribute('fill-opacity','.76');footprint.setAttribute('stroke',outline);footprint.setAttribute('stroke-width',outline===p.fragment ? '1.6' : '.5');
   group.appendChild(footprint);
   const samples=['shape','electrostatics'].includes(channel.key)?(residue.surface || []):[];
   const stride=Math.max(1,Math.ceil(samples.length/64));
   samples.forEach((point,index)=>{
    if(index%stride || !finite(point[0]) || !finite(point[1])) return;
    let sampleValue=value; if(channel.key==='shape') sampleValue=point[2];
    if(channel.key==='electrostatics') sampleValue=state.record.electrostatics && state.record.electrostatics.status==='ok' ? point[3] : null;
    group.appendChild(element('circle',{cx:mapX(point[0]),cy:mapY(point[1]),r:1.15,fill:color(sampleValue,channel,p.missing),'fill-opacity':'.72','pointer-events':'none'}));
   });
   group.appendChild(element('title',{},`${residueLabel(residue)} · ${channel.label}: ${fmt(value)} ${channel.unit}\nTarget ${fmt(residue.min_target_distance)} Å · peptide ${fmt(residue.min_peptide_distance)} Å · ${siteLabel(state.record)} ${fmt(residue.min_p6_distance)} Å`));
   const label=labels.get(residue.key);
   if(label) {
    if(label.leader)group.appendChild(element('path',{d:`M${mapX(residue.x)},${mapY(residue.y)}L${label.x},${label.y-4}`,fill:'none',stroke:p.ink,'stroke-width':.6,opacity:.45,'pointer-events':'none'}));
    group.appendChild(element('text',{x:label.x,y:label.y,'text-anchor':'middle',class:'radial-residue-label','font-size':11,'font-family':'IBM Plex Mono,monospace',fill:p.ink,style:`paint-order:stroke;stroke:${p.bg};stroke-width:2.2px;stroke-linejoin:round`},label.text));
   }
   group.addEventListener('click',()=>selectResidue(state,residue.key,true));
   group.addEventListener('keydown',event=>{if(event.key==='Enter' || event.key===' '){event.preventDefault();selectResidue(state,residue.key,true);}});
   group.addEventListener('mouseenter',()=>inspect(state,residue));
   group.addEventListener('mouseleave',()=>{const selected=residues.find(r=>r.key===state.selected);if(selected)inspect(state,selected);});
   group.addEventListener('focus',()=>inspect(state,residue)); surface.appendChild(group);
  });
  if(peptide.length) {
   peptide.forEach((r,index)=>{
    const next=peptide[index+1];if(!next || next.position!==r.position+1)return;
    const guide=r.observed!==true || next.observed!==true;
    surface.appendChild(element('path',{d:`M${mapX(r.x)},${mapY(r.y)}L${mapX(next.x)},${mapY(next.y)}`,fill:'none',stroke:p.peptide,'stroke-width':2,'stroke-linejoin':'round','stroke-dasharray':guide?'4 4':null,opacity:guide?'.35':'.85','pointer-events':'none'}));
   });
   peptide.forEach(r=>{
    const mutation=r.position===centerPosition(state.record) && r.observed===true;
    surface.appendChild(element('circle',{cx:mapX(r.x),cy:mapY(r.y),r:mutation?3.4:2.1,fill:mutation?p.mutation:p.peptide,opacity:r.observed===true?'1':'.4','pointer-events':'none'}));
    surface.appendChild(element('text',{x:mapX(r.x),y:mapY(r.y)+13,'text-anchor':'middle','font-size':10,'font-family':'IBM Plex Mono,monospace',fill:p.peptide,style:`paint-order:stroke;stroke:${p.bg};stroke-width:2.5px;stroke-linejoin:round`,'pointer-events':'none'},`${r.aa || ''}${r.position}`));
   });
  }
  surface.appendChild(element('path',{d:`M${cx},${cy-5}l5,5 -5,5 -5,-5Z`,fill:p.mutation,stroke:p.panel,'stroke-width':1,'pointer-events':'none'}));
  svg.appendChild(surface);
  svg.appendChild(element('text',{x:cx,y:34,'text-anchor':'middle',fill:p.muted,'font-size':10,'font-family':'IBM Plex Mono,monospace'},'+ across groove'));
  svg.appendChild(element('path',{d:'M181,426H279m-5,-4 5,4 -5,4',stroke:p.muted,fill:'none','stroke-width':1}));
  svg.appendChild(element('text',{x:173,y:429,'text-anchor':'end',fill:p.muted,'font-size':11,'font-family':'IBM Plex Mono,monospace'},'N'));
  svg.appendChild(element('text',{x:287,y:429,fill:p.muted,'font-size':11,'font-family':'IBM Plex Mono,monospace'},'C'));
  card.appendChild(svg);
  const bar=html('div','radial-scale');bar.appendChild(html('span','',channel.ends[0]));
  const gradient=html('span','radial-scale-bar');gradient.style.background=`linear-gradient(90deg,${channel.colors.join(',')})`;bar.appendChild(gradient);bar.appendChild(html('span','',channel.ends[1]));card.appendChild(bar);
  card.appendChild(html('p','radial-scale-caption',channel.description));
  if(channel.key==='electrostatics' && (!state.record.electrostatics || state.record.electrostatics.status!=='ok')) card.appendChild(html('p','radial-map-unavailable',state.record.electrostatics && state.record.electrostatics.reason || 'APBS surface potential unavailable; footprints shown in grey.'));
  return card;
 }
 function inspect(state,residue) {
  const {dom}=state;dom['residue-title'].textContent=residueLabel(residue);dom.facts.replaceChildren();
  const facts=[['Target distance',`${fmt(residue.min_target_distance)} Å`],['Peptide distance',finite(residue.min_peptide_distance)?`${fmt(residue.min_peptide_distance)} Å`:'Not observed / N/A'],[`${siteLabel(state.record)} distance`,finite(residue.min_p6_distance)?`${fmt(residue.min_p6_distance)} Å`:'Not observed / N/A'],['Buried SASA',`${fmt(residue.buried_sasa)} Å²`],['Height from site centre',`${fmt(residue.z)} Å`],['Mean APBS potential',state.record.electrostatics && state.record.electrostatics.status==='ok' && finite(residue.potential)?`${fmt(residue.potential,2)} kT/e`:'Unavailable'],['Kyte–Doolittle',fmt(residue.hydrophobicity,1)],['Side-chain volume',`${fmt(residue.sidechain_volume)} Å³`],['In-plane position',`${fmt(residue.x)}, ${fmt(residue.y)} Å`],['Radial distance',finite(residue.x)&&finite(residue.y)?`${fmt(Math.hypot(residue.x,residue.y))} Å`:'—'],['Residue confidence',finite(residue.confidence)?fmt(residue.confidence,1):'N/A · experimental'],['Original GQT patch',state.id==='prediction' ? residue.native_patch ? 'Yes' : 'No' : 'N/A · experimental']];
  facts.forEach(([label,value])=>{const group=html('div');group.appendChild(html('dt','',label));group.appendChild(html('dd','',value));dom.facts.appendChild(group);});
 }
 function selectResidue(state,key,notify) {
  const residue=visibleResidues(state).find(r=>r.key===key);if(!residue)return;
  state.selected=key;state.dom.residue.value=key;
  state.dom.maps.querySelectorAll('[data-residue-key]').forEach(node=>{
   const on=node.dataset.residueKey===key;node.classList.toggle('is-selected',on);node.setAttribute('aria-pressed',String(on));
   const footprint=node.querySelector('.radial-footprint');
   if(footprint){const original=state.patch && state.id==='prediction' && (state.record.residues.find(r=>r.key===node.dataset.residueKey) || {}).native_patch;const p=palette(state.root);footprint.setAttribute('stroke',on?p.ink:original?p.fragment:p.line);footprint.setAttribute('stroke-width',on?'2.2':original?'1.6':'.5');}
  });
  inspect(state,residue);if(notify && typeof state.callback==='function')state.callback(residue);
 }
 function save(blob,name) {
  const url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=name;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 }
 function exportMap(state,format) {
  if(!state.record || state.record.status!=='ok')return;
  const stem=`interface-${state.key.replace(/[^a-z0-9_-]+/gi,'-')}-${state.scope}-${state.radius}A`;
  const rows=visibleResidues(state);
  if(format==='json') {save(new Blob([JSON.stringify({record:state.record,display:{channel:state.channel,scope:state.scope,radius:state.radius,visible_residue_keys:rows.map(r=>r.key)},method:data().method || {}},null,2)],{type:'application/json'}),stem+'.json');return;}
  if(format==='csv') {
   const columns=['key','chain','resi','icode','name','aa','x','y','z','min_target_distance','min_peptide_distance','min_p6_distance','buried_sasa','potential','hydrophobicity','sidechain_volume','confidence','native_patch'];
   const quote=value=>value===null || value===undefined?'':`"${String(value).replace(/"/g,'""')}"`;
   const csv=[columns.join(','),...rows.map(r=>columns.map(c=>quote(r[c])).join(','))].join('\r\n');save(new Blob([csv],{type:'text/csv;charset=utf-8'}),stem+'.csv');return;
  }
  const cards=Array.from(state.dom.maps.querySelectorAll('.radial-map-card'));const cols=cards.length>1?2:1, cardW=500,cardH=540,top=83;
  const p=palette(state.root),out=element('svg',{xmlns:NS,width:cols*cardW,height:top+Math.ceil(cards.length/cols)*cardH+50,viewBox:`0 0 ${cols*cardW} ${top+Math.ceil(cards.length/cols)*cardH+50}`});
  out.appendChild(element('rect',{width:'100%',height:'100%',fill:p.bg}));
  out.appendChild(element('desc',{},JSON.stringify({key:state.key,center:state.record.center,frame:state.record.frame,target_covalent_ligands:state.record.target_covalent_ligands||[],method:data().method})));
  out.appendChild(element('text',{x:22,y:29,fill:p.ink,'font-family':'Chivo,Arial,sans-serif','font-size':19,'font-weight':700},state.record.label || state.key));
  out.appendChild(element('text',{x:22,y:50,fill:p.muted,'font-family':'IBM Plex Mono,monospace','font-size':10},`Mutation-site peptide-frame projection · ${state.scope} contacts ≤4.5 Å · ${state.radius} Å radius`));
  if(state.record.center && state.record.center.kind==='transferred')out.appendChild(element('text',{x:22,y:69,fill:p.mutation,'font-family':'IBM Plex Mono,monospace','font-size':10},observedPeptide(state.record)?'Mutation-site centre transferred; observed peptide retained.':'Transferred peptide frame; peptide and mutation-site contacts absent.'));
  cards.forEach((card,index)=>{
   const channel=channels.find(c=>c.key===card.dataset.channel),x=(index%cols)*cardW,y=top+Math.floor(index/cols)*cardH;
   out.appendChild(element('text',{x:x+22,y:y+20,fill:p.ink,'font-family':'Chivo,Arial,sans-serif','font-size':17,'font-weight':700},channel.label));
   const svg=card.querySelector('svg').cloneNode(true);svg.setAttribute('x',x+20);svg.setAttribute('y',y+25);svg.setAttribute('width',460);svg.setAttribute('height',450);svg.querySelectorAll('[tabindex]').forEach(n=>n.removeAttribute('tabindex'));out.appendChild(svg);
   const defs=element('defs'),gradient=element('linearGradient',{id:`${state.id}-export-${channel.key}`});channel.colors.forEach((c,i)=>gradient.appendChild(element('stop',{offset:`${i*50}%`,'stop-color':c})));defs.appendChild(gradient);out.appendChild(defs);
   out.appendChild(element('rect',{x:x+177,y:y+485,width:146,height:7,fill:`url(#${state.id}-export-${channel.key})`}));
   out.appendChild(element('text',{x:x+167,y:y+493,'text-anchor':'end',fill:p.muted,'font-family':'IBM Plex Mono,monospace','font-size':10},channel.ends[0]));
   out.appendChild(element('text',{x:x+333,y:y+493,fill:p.muted,'font-family':'IBM Plex Mono,monospace','font-size':10},channel.ends[1]));
   out.appendChild(element('text',{x:x+250,y:y+516,'text-anchor':'middle',fill:p.muted,'font-family':'Source Sans 3,Arial,sans-serif','font-size':11},channel.description));
  });
  const bottom=top+Math.ceil(cards.length/cols)*cardH;
  out.appendChild(element('text',{x:22,y:bottom+20,fill:p.muted,'font-family':'IBM Plex Mono,monospace','font-size':9},`${observedPeptide(state.record)?'Peptide Cα trace':'Transferred peptide guide'}: teal · mutation site: pink${state.id==='prediction' && state.patch?' · original patch: gold outline':''} · grey: unavailable`));
  out.appendChild(element('text',{x:22,y:bottom+37,fill:p.muted,'font-family':'IBM Plex Mono,monospace','font-size':9},'Orthographic projection, not a geodesic surface map. Fixed colour scales saturate at their limits.'));
  save(new Blob(['<?xml version="1.0" encoding="UTF-8"?>\n'+new XMLSerializer().serializeToString(out)],{type:'image/svg+xml'}),stem+'.svg');
 }
 window.opigRadialMaps={
  show:function(id,key,options){
   const state=init(id);if(!state)return false;
   state.key=key;state.record=data().records && data().records[key] || {id:key,status:'unavailable',reason:key && key.startsWith('prediction:')?'Maps are available for the three model-gate passing candidates and their matched contexts. This source is outside that computed subset.':'No precomputed interface map is available for this entry.'};
   state.callback=options && options.onSelect || null;state.selected=null;render(state);return state.record.status==='ok';
  },
  refreshTheme:function(){instances.forEach(state=>{if(state.record)render(state);});},
  getCurrent:function(id){const state=instances.get(id);return state?{key:state.key,record:state.record,scope:state.scope,radius:state.radius,channel:state.channel,selected:state.selected}:null;}
 };
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('[data-radial-instance]').forEach(node=>init(node.dataset.radialInstance));},{once:true});
 else document.querySelectorAll('[data-radial-instance]').forEach(node=>init(node.dataset.radialInstance));
})();
