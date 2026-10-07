/* Automated offline tests in a disposable headless browser, never a user's profile. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('@playwright/test');
const repo = path.resolve(__dirname, '../../..');
const examples = process.env.THESIS_MAP_EXAMPLES || path.join(repo, 'examples');
const screenshots = process.env.THESIS_MAP_SCREENSHOTS || path.join(__dirname, 'test-results');

(async () => {
  fs.mkdirSync(screenshots, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    for (const name of ['crook', 'carlos', 'vost']) {
      const directory = process.env.THESIS_MAP_EXAMPLES ? path.join(examples, `thesis-map-${name}-check`) : path.join(examples, `${name}-map`);
      const data = JSON.parse(fs.readFileSync(path.join(directory, 'thesis.json'), 'utf8'));
      for (const [label, viewport] of [['desktop', { width: 1280, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
        const context = await browser.newContext({ viewport, offline: true, reducedMotion: 'reduce', colorScheme: 'light' });
        const page = await context.newPage();
        const errors = [], remote = [];
        page.on('pageerror', e => errors.push(e.message));
        page.on('request', request => { if (/^https?:/.test(request.url())) remote.push(request.url()); });
        await page.goto(pathToFileURL(path.join(directory, 'map.html')).href);
        assert.equal(await page.locator('#ttl').textContent(), data.meta.title);
        assert.equal(await page.locator('#v-journey [data-stage]').count(), data.journey.stages.length);
        for (const tab of ['journey', 'structure', 'links']) {
          await page.locator(`#tab-${tab}`).click();
          if (tab === 'structure') await page.getByRole('button', { name: 'Expand all', exact: true }).click();
          await page.evaluate(() => window.scrollTo(0, 0));
          assert(await page.locator(`#v-${tab}`).isVisible());
          const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
          if(overflow){console.log(await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,elements:[...document.querySelectorAll('body *')].map(e=>({tag:e.tagName,cls:e.className?.baseVal||e.className,x:e.getBoundingClientRect().x,width:e.getBoundingClientRect().width,text:e.textContent.slice(0,100)})).filter(r=>r.x+r.width>innerWidth+1).slice(0,20)})));await page.screenshot({path:path.join(screenshots,`${name}-${label}-${tab}-overflow.png`)});}
          assert(!overflow, `${name}/${label}/${tab}: page overflows horizontally`);
          await page.screenshot({ path: path.join(screenshots, `${name}-${label}-${tab}.png`) });
        }
        await page.locator('#tab-journey').click();
        await page.locator('#v-journey [data-stage]').first().click();
        assert((await page.locator('#panel').textContent()).includes(data.journey.stages[0].title));
        await page.screenshot({ path: path.join(screenshots, `${name}-${label}-selection.png`) });
        await page.locator('#panel').getByRole('button', { name: 'Close', exact: true }).click();
        await page.locator('#tab-structure').click();
        assert.equal(await page.locator('#tree .row').count(), Object.keys(data.structure.nodes).length);
        await page.locator('#leaves').uncheck();
        assert.equal(await page.locator('#tree .leafrow').count(), 0);
        await page.locator('#leaves').check();
        await page.locator('#tab-links').click();
        await page.locator('#t-ent').click();
        assert((await page.locator('.gnode.entity').count()) > 0);
        await page.locator('#t-leaf').click();
        assert.equal(await page.locator('.gnode.leaf').count(), Object.values(data.structure.nodes).filter(n => ['figure', 'table'].includes(n.kind)).length);
        const search = page.locator('#q');
        await search.fill(data.links.claims[0].text);
        await page.locator('#results button').first().click();
        assert((await page.locator('#panel').textContent()).includes(data.links.claims[0].text));
        const saved = page.url();
        await page.reload();
        assert.equal(page.url(), saved);
        assert((await page.locator('#panel').textContent()).includes(data.links.claims[0].text));
        assert.deepEqual(errors, [], `${name}/${label}: runtime errors`);
        assert.deepEqual(remote, [], `${name}/${label}: attempted network access`);
        await context.close();
        process.stdout.write(`${name}/${label}: offline views, selection, filters, search and deep links passed\n`);
      }
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
