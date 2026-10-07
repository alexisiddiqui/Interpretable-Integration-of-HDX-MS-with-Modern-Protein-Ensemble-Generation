/* Isolated DOM tests: no connection to a user's browser or external resources. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM, VirtualConsole } = require('jsdom');
const repo = path.resolve(__dirname, '../../..');
const examples = process.env.THESIS_MAP_EXAMPLES || path.join(repo, 'examples');

async function check(name) {
  const directory = process.env.THESIS_MAP_EXAMPLES ? path.join(examples, `thesis-map-${name}-check`) : path.join(examples, `${name}-map`);
  const data = JSON.parse(fs.readFileSync(path.join(directory, 'thesis.json'), 'utf8'));
  const html = fs.readFileSync(path.join(directory, 'map.html'), 'utf8');
  assert(!/<(?:script|link)[^>]+(?:src|href)=["']https?:/i.test(html), 'HTML requires external assets');
  const errors = [];
  const console = new VirtualConsole();
  console.on('jsdomError', error => errors.push(error.message));
  const dom = new JSDOM(html, {
    url: `file://${directory}/map.html`, runScripts: 'dangerously', pretendToBeVisual: true,
    virtualConsole: console,
    beforeParse(window) {
      window.matchMedia = query => ({ matches: query.includes('reduced-motion'), addEventListener() {}, removeEventListener() {} });
      window.ResizeObserver = class { observe() {} disconnect() {} };
      window.scrollTo = () => {};
      window.HTMLElement.prototype.scrollIntoView = () => {};
    },
  });
  const { window } = dom;
  await new Promise(resolve => window.addEventListener('load', resolve, { once: true }));
  const doc = window.document;
  function click(selector) {
    const element = doc.querySelector(selector);
    assert(element, `Missing control ${selector}`);
    element.click();
  }
  function search(text) {
    const input = doc.querySelector('#q');
    input.value = text;
    input.dispatchEvent(new window.Event('input', { bubbles: true }));
    const result = doc.querySelector('#results button');
    assert(result, `No search result for ${text}`);
    result.click();
  }
  assert.equal(doc.querySelector('#ttl').textContent, data.meta.title);
  assert.equal(doc.querySelectorAll('#v-journey [data-stage]').length, data.journey.stages.length);
  assert(!doc.body.textContent.includes('undefined'), 'Undefined metadata appears in interface');
  for (const stage of data.journey.stages) {
    click(`[data-stage="${stage.id}"]`);
    assert(doc.querySelector('#panel').textContent.includes(stage.title));
  }
  click('#tab-structure');
  [...doc.querySelectorAll('#v-structure button')].find(b => b.textContent === 'Expand all').click();
  assert.equal(doc.querySelectorAll('#tree .row').length, Object.keys(data.structure.nodes).length);
  const leaves = doc.querySelector('#leaves');
  leaves.checked = false;
  leaves.dispatchEvent(new window.Event('change', { bubbles: true }));
  assert.equal(doc.querySelectorAll('#tree .leafrow').length, 0);
  leaves.checked = true;
  leaves.dispatchEvent(new window.Event('change', { bubbles: true }));
  const figure = Object.values(data.structure.nodes).find(n => n.kind === 'figure');
  click(`#tree [data-node="${figure.id}"]`);
  assert(doc.querySelector('#panel').textContent.includes(figure.summary));
  if (name === 'carlos') {
    click('#tree [data-node="fig.J1"]');
    assert(doc.querySelector('#panel').textContent.includes('Chem. Sci.'));
  }
  click('#tab-links');
  assert(doc.querySelector('#graph svg'));
  const chapters = Object.values(data.structure.nodes).filter(n => ['chapter', 'appendix'].includes(n.kind));
  for (const chapter of chapters) assert(doc.querySelector(`[data-gid="${chapter.id}"]`), `Missing graph chapter ${chapter.id}`);
  click('#t-leaf');
  assert.equal(doc.querySelectorAll('.gnode.leaf').length, Object.values(data.structure.nodes).filter(n => ['figure', 'table'].includes(n.kind)).length);
  click('#t-ent');
  assert(doc.querySelectorAll('.gnode.entity').length > 0);
  for (const category of new Set(data.links.entities.map(e => e.category))) assert(doc.querySelector(`[data-cat="${category}"]`));
  const edge = doc.querySelector('#edgetbl tbody tr td:last-child button');
  assert(edge);
  edge.click();
  assert(doc.querySelector('#panel').textContent.includes('Reason'));
  search(data.links.entities[0].name);
  assert(doc.querySelector('#panel').textContent.includes(data.links.entities[0].description));
  search(data.links.claims[0].text);
  assert(doc.querySelector('#panel').textContent.includes(data.links.claims[0].text));
  if (data.quality.observations.length) {
    search(data.quality.observations[0].text);
    assert(doc.querySelector('#panel').textContent.includes(data.quality.observations[0].text));
  }
  click('#theme');
  assert(doc.documentElement.hasAttribute('data-theme'));
  // Every exposed selectable record must render a detail panel, even if it lacks a summary/quote.
  for (const node of Object.values(data.structure.nodes)) window.__thesisMap.select({ kind: 'node', id: node.id }, { scroll: false });
  for (const claim of data.links.claims) window.__thesisMap.select({ kind: 'claim', id: claim.id }, { scroll: false });
  for (const entity of data.links.entities) window.__thesisMap.select({ kind: 'entity', id: entity.id }, { scroll: false });
  for (const edge of data.links.edges) window.__thesisMap.select({ kind: 'edge', id: edge.id }, { scroll: false });
  assert(!doc.querySelector('#panel').textContent.includes('undefined'));
  assert.equal(errors.length, 0, errors.join('\n'));
  dom.window.close();
  process.stdout.write(`${name}: all views, records, filters, search and source observations passed\n`);
}
(async () => { for (const name of ['crook', 'carlos', 'vost']) await check(name); })().catch(error => { console.error(error); process.exitCode = 1; });
