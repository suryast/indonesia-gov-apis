// Read-only browser regression; never invokes monitors or rewrites datasets.
// PLAYWRIGHT_MODULE=/path/to/playwright CHROMIUM_PATH=/path/to/chromium node scripts/test_status_layout.cjs
// Optional STATUS_HTML and STATUS_LAYOUT_OUTPUT select a baseline and evidence directory.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../status');
const out = process.env.STATUS_LAYOUT_OUTPUT;
if (out) fs.mkdirSync(out, { recursive: true });
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  const reports = [];
  const failures = [];
  try {
    for (const width of [390, 768, 980, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 1000 } });
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.origin !== 'http://status.test') return route.fulfill({ status: 200, contentType: 'text/css', body: '' });
        const file = url.pathname === '/' ? (process.env.STATUS_HTML || path.join(root, 'index.html')) : path.resolve(root, '.' + url.pathname);
        if (url.pathname !== '/' && !file.startsWith(root + path.sep)) return route.abort();
        if (!fs.existsSync(file)) return route.fulfill({ status: 404, body: '' });
        return route.fulfill({ status: 200, contentType: url.pathname === '/' ? 'text/html' : file.endsWith('.json') ? 'application/json' : 'application/octet-stream', body: fs.readFileSync(file) });
      });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      await page.goto('http://status.test/');
      await page.waitForSelector('.portal-row');
      await page.evaluate(() => document.fonts.ready);
      const state = await page.evaluate(() => {
        const rect = e => { const r = e.getBoundingClientRect(); return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width }; };
        return {
          width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
          overflowElements: [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > innerWidth).map(e => ({ tag: e.tagName, class: e.className, text: e.textContent.slice(0, 120), rect: rect(e) })),
          subtitle: document.querySelector('header p').textContent,
          description: document.querySelector('meta[name="description"]').content,
          ogDescription: document.querySelector('meta[property="og:description"]').content,
          legend: document.querySelector('.legend').textContent,
          maxDays: MAX_DAYS,
          summary: document.querySelector('#summary').innerText,
          checkedAt: document.querySelector('#last-check').textContent,
          body: document.body.outerHTML,
          rows: [...document.querySelectorAll('.portal-row')].map(row => ({
            name: row.querySelector('.portal-name').textContent,
            row: rect(row), spark: rect(row.querySelector('.spark')),
            sparkDisplay: getComputedStyle(row.querySelector('.spark')).display,
            badge: rect(row.querySelector('.badge')),
            bars: [...row.querySelectorAll('.spark-bar')].map(rect),
            tooltips: [...row.querySelectorAll('.tooltip')].map(rect),
            grid: getComputedStyle(row).gridTemplateColumns,
            gap: getComputedStyle(row.querySelector('.spark')).gap,
            barMinWidth: getComputedStyle(row.querySelector('.spark-bar')).minWidth
          }))
        };
      });
      const history = JSON.parse(fs.readFileSync(path.join(root, 'data/history.json')));
      const dates = Object.keys(history).sort();
      try {
        assert.equal(state.rows.length, Object.keys(history[dates.at(-1)].portals).length);
        for (const text of [state.subtitle, state.description, state.ogDescription]) {
          assert.ok(text.includes(`monitoring of ${state.rows.length} Indonesian`), `count mismatch: ${text}`);
        }
        assert.ok(state.legend.includes(`Last ${state.maxDays} days, one bar per day`), 'history legend matches renderer window');
        assert.equal(state.scrollWidth, width, 'document overflow');
        assert.deepEqual(errors, []);
        for (const r of state.rows) {
          assert.equal(r.bars.length, Math.max(7, Math.min(90, dates.length)));
          assert.ok(r.badge.left >= r.row.left && r.badge.right <= r.row.right + 0.1, `${r.name}: badge outside row`);
          if (width <= 480) { assert.equal(r.sparkDisplay, 'none'); continue; }
          assert.ok(r.spark.right <= r.badge.left, `${r.name}: history container overlaps status`);
          for (const tip of r.tooltips) {
            assert.ok(tip.left >= 0 && tip.right <= width, `${r.name}: tooltip outside viewport`);
          }
          for (const bar of r.bars) {
            assert.ok(bar.width > 0, `${r.name}: invisible bar`);
            assert.ok(bar.left >= r.spark.left - 0.1 && bar.right <= r.spark.right + 0.1, `${r.name}: bar exceeds history container (${bar.right} > ${r.spark.right})`);
            assert.ok(bar.right <= r.badge.left, `${r.name}: bar overlaps status`);
            assert.ok(bar.right <= r.row.right + 0.1, `${r.name}: bar outside row`);
          }
        }
      } catch (e) { failures.push(`${width}: ${e.message}`); }
      if (out) {
        await page.screenshot({ path: path.join(out, `${width}.png`), fullPage: true, animations: 'disabled' });
        await page.screenshot({ path: path.join(out, `${width}-viewport.png`), animations: 'disabled' });
      }
      if (width > 480) {
        // Tablet bars are subpixel-wide; target the history strip and verify the actual hovered bar.
        const spark = await page.locator('.spark').first().boundingBox();
        await page.mouse.move(spark.x + spark.width - 2, spark.y + spark.height / 2);
        await page.waitForTimeout(200);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), width, 'hover overflow');
        assert.equal(await page.locator('.spark-bar:hover .tooltip').evaluate(e => getComputedStyle(e).opacity), '1');
        if (out) await page.screenshot({ path: path.join(out, `${width}-hover.png`), animations: 'disabled' });
      }
      reports.push({ ...state, errors });
      await context.close();
    }
    if (out) fs.writeFileSync(path.join(out, 'geometry.json'), JSON.stringify({ reports, failures }, null, 2));
    assert.deepEqual(failures, []);
    // A changed in-memory snapshot proves counts are derived, not pinned to 57.
    const context = await browser.newContext();
    const history = JSON.parse(fs.readFileSync(path.join(root, 'data/history.json')));
    const latestDay = Object.keys(history).sort().at(-1);
    history[latestDay].portals = Object.fromEntries(Object.entries(history[latestDay].portals).slice(0, 2));
    await context.route('**/*', route => {
      const url = new URL(route.request().url());
      if (url.pathname === '/data/history.json') return route.fulfill({ json: history });
      if (url.origin === 'http://status.test' && url.pathname === '/') return route.fulfill({ contentType: 'text/html', body: fs.readFileSync(path.join(root, 'index.html')) });
      return route.fulfill({ status: 200, body: '' });
    });
    const page = await context.newPage();
    await page.goto('http://status.test/', { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('.portal-row');
    assert.equal(await page.locator('.portal-row').count(), 2);
    assert.match(await page.locator('header p').textContent(), /monitoring of 2 Indonesian/);
    for (const selector of ['meta[name="description"]', 'meta[property="og:description"]']) {
      assert.match(await page.locator(selector).getAttribute('content'), /monitoring of 2 Indonesian/);
    }
    await context.close();
    console.log('PASS: dataset-derived rows/counts/metadata and 90-day legend at 390, 768, 980, 1440; no overflow, tooltip clipping, history/status intersection or browser errors; alternate 2-portal snapshot also passed.');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
