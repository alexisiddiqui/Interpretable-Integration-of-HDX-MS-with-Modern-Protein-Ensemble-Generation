// Reuse the dashboard renderer unchanged; provide a small SVG-only DOM adapter.
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const dir=path.dirname(fileURLToPath(import.meta.url));
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
class Node {
 constructor(tag){this.tag=tag;this.attrs={};this.children=[];this.dataset={};this.style={};this.textContent='';}
 setAttribute(k,v){this.attrs[k]=String(v);}
 appendChild(n){this.children.push(n);return n;}
 addEventListener(){}
 toString(){return `<${this.tag} ${Object.entries(this.attrs).map(([k,v])=>`${k}="${escape(v)}"`).join(' ')}>${escape(this.textContent)}${this.children.join('')}</${this.tag}>`;}
}
const palette={'--bg':'#ffffff','--panel':'#ffffff','--grid':'#e6e6e6','--line':'#b9b9b9','--ink':'#20242c','--muted':'#666666'};
const context={window:{},document:{createElementNS:(_,tag)=>new Node(tag),createElement:tag=>new Node(tag),readyState:'loading',addEventListener(){}},getComputedStyle:()=>({getPropertyValue:key=>palette[key] || ''}),console};
vm.createContext(context);
const source=fs.readFileSync(path.join(dir,'dashboard-radial-maps.js'),'utf8');
const marker=' window.opigRadialMaps={';
if(!source.includes(marker))throw Error('Dashboard renderer API changed');
vm.runInContext(source.replace(marker,' window.thesisRender={drawCard,channels,visibleResidues};\n'+marker),context);
const {drawCard,channels,visibleResidues}=context.window.thesisRender;
const data=JSON.parse(fs.readFileSync(path.join(dir,'radial-data.json')));
const records=Object.entries(data.records);
const titles=['Reference TCR · G12D','Reference TCR · WT','Screened lead · G12D','Screened lead · WT'];
const subtitles=['7OW6 · crystal structure','7OW5 · crystal structure','ID_1457932 · predicted · iPTM 0.875','ID_1457932 · predicted · iPTM 0.761'];
const text=(x,y,size,s,extra='')=>`<text x="${x}" y="${y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="${size}" fill="#1d2127" ${extra}>${escape(s)}</text>`;
for(const channel of channels){
 let parts=[`<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1185" viewBox="0 0 1000 1185"><rect width="1000" height="1185" fill="#ffffff"/>`,text(30,35,24,channel.label,'font-weight="bold"')];
 parts.push(text(30,59,13,'KRAS pMHC · mutation-centred interface · 25 Å radius'));
 records.forEach(([key,record],index)=>{
  const state={id:key.startsWith('prediction')?'prediction':'atlas',root:{},record,key,scope:'target',radius:25,labels:true,patch:true};
  const card=drawCard(state,channel,visibleResidues(state));const svg=card.children.find(n=>n.tag==='svg');
  // Print styling: one sans-serif face and labels above all surface polygons.
  const labels=[];
  function restyle(node){
   if(node.attrs['font-family'])node.attrs['font-family']='DejaVu Sans,Arial,sans-serif';
   if(node.attrs.class==='radial-footprint')node.attrs['fill-opacity']='0.9';
   if(node.attrs.class==='radial-residue-label'){
    node.attrs['font-size']='10.5';node.attrs.style='paint-order:stroke;stroke:#ffffff;stroke-width:3px;stroke-linejoin:round';
   }
   for(const child of [...node.children]){
    if(child.attrs.class==='radial-residue-label' || (node.attrs.class==='radial-residue' && child.tag==='path')){
     labels.push(child);node.children=node.children.filter(n=>n!==child);
    }
    restyle(child);
   }
  }
  restyle(svg);
  svg.children=svg.children.filter(n=>n.textContent!=='+ across groove');
  const overlay=new Node('g');labels.forEach(n=>overlay.appendChild(n));svg.appendChild(overlay);
  // IDs must be unique when two atlas and two predicted maps share a page.
  let body=String(svg).replaceAll(`radial-${state.id}-${channel.key}-clip`,`map-${index}-${channel.key}-clip`);
  const x=(index%2)*500,y=86+Math.floor(index/2)*500;
  parts.push(`<g transform="translate(${x},${y})">`,text(28,20,19,String.fromCharCode(65+index)+'   '+titles[index],'font-weight="bold"'),text(28,42,12,subtitles[index]),`<g transform="translate(20,45)">${body.replace('<svg ','<svg width="460" height="450" ')}</g></g>`);
 });
 parts.push(`<defs><linearGradient id="scale">${channel.colors.map((c,i)=>`<stop offset="${i*50}%" stop-color="${c}"/>`).join('')}</linearGradient></defs><rect x="380" y="1103" width="240" height="10" fill="url(#scale)"/>`,text(367,1114,12,channel.ends[0],'text-anchor="end"'),text(633,1114,12,channel.ends[1]),text(500,1135,12,channel.description,'text-anchor="middle"'),`<path d="M160,1161h25" stroke="#0f7a7f" stroke-width="2"/>`,text(193,1165,12,'Peptide'),`<path d="M340,1156l5,5 -5,5 -5,-5Z" fill="#c2185b"/>`,text(354,1165,12,'Mutation site'),`<rect x="540" y="1156" width="16" height="10" fill="none" stroke="#e0a100" stroke-width="2"/>`,text(565,1165,12,'Original screened patch'),'</svg>');
 const stem=path.join(dir,channel.key);fs.writeFileSync(stem+'.svg',parts.join('\n'));
 execFileSync('rsvg-convert',['-f','pdf','-o',stem+'.pdf',stem+'.svg']);
 execFileSync('rsvg-convert',['-w','1300','-o',stem+'.png',stem+'.svg']);
}
const hashes={};for(const name of fs.readdirSync(dir)){if(/\.(svg|pdf|png|mjs|json|js)$/.test(name)&&name!=='provenance.json' && !name.startsWith('fig.'))hashes[name]=createHash('sha256').update(fs.readFileSync(path.join(dir,name))).digest('hex');}
fs.writeFileSync(path.join(dir,'provenance.json'),JSON.stringify({command:'node figures/jaxka-kras-pmhc-radial/make.mjs',scope:'target',radius_angstrom:25,renderer:'Dashboard geometry with white print palette, DejaVu Sans typography, foreground labels and shared-scale four-panel composition',hashes},null,2)+'\n');
console.log('Built four comparisons in SVG, PDF and PNG.');
