"""Offline browser compatibility/security and deployment guard regressions."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DeployGuards(unittest.TestCase):
    def run_wrapper(self, args, checker_exit=0, stage_exit=0, deploy_exit=0, token=True):
        # Mock only the network-bearing checker and Wrangler. Execute the REAL
        # stager against read-only repository assets in a temporary directory.
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            python = f'''#!/bin/sh
if [ "$1" = "scripts/check_repository.py" ]; then
  if [ "{stage_exit}" != 0 ]; then exit {stage_exit}; fi
  exec "{sys.executable}" "$@"
fi
exit {checker_exit}
'''
            wrangler = f'''#!/bin/sh
set -eu
[ "$1" = pages ] && [ "$2" = deploy ] && [ "$3" != status ]
[ -f "$3/index.html" ] && [ -f "$3/data/history.json" ]
[ ! -e "$3/check.py" ] && [ ! -e "$3/check-and-deploy.sh" ]
[ ! -e "$3/private.key" ] && [ ! -e "$3/README.md" ]
printf 'deployed %s\\n' "$3"
exit {deploy_exit}
'''
            for name, body in [('python3', python), ('wrangler', wrangler)]:
                path = directory / name
                path.write_text(body)
                path.chmod(0o700)
            env = dict(os.environ, PATH=str(directory) + ':' + os.environ['PATH'],
                       TMPDIR=str(directory), STATUS_PAGES_PROJECT='offline-test')
            if token:
                env['CLOUDFLARE_API_TOKEN'] = 'offline-placeholder'
            else:
                env.pop('CLOUDFLARE_API_TOKEN', None)
            result = subprocess.run(['bash', str(ROOT / 'status/check-and-deploy.sh'), *args],
                                    env=env, capture_output=True, text=True)
            # Validate cleanup before TemporaryDirectory itself removes anything.
            self.assertEqual(list(directory.glob('gov-status-pages.*')), [])
            return result

    def test_check_only_does_not_deploy(self):
        result = self.run_wrapper([])
        self.assertEqual(result.returncode, 0)
        self.assertNotIn('deployed', result.stdout)

    def test_failed_check_prevents_deployment(self):
        result = self.run_wrapper(['--deploy'], checker_exit=1)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('deployed', result.stdout)

    def test_successful_deploy_uses_static_staging_and_cleans_up(self):
        result = self.run_wrapper(['--deploy'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Staged ', result.stdout)
        self.assertIn('deployed ', result.stdout)

    def test_staging_failure_prevents_deployment_and_cleans_up(self):
        result = self.run_wrapper(['--deploy'], stage_exit=1)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('deployed ', result.stdout)

    def test_deployment_failure_cleans_up(self):
        result = self.run_wrapper(['--deploy'], deploy_exit=1)
        self.assertNotEqual(result.returncode, 0)

    def test_missing_token_fails_closed(self):
        result = self.run_wrapper(['--deploy'], token=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('deployed ', result.stdout)

    def test_scratch_output_cannot_deploy(self):
        for value in [['--output-dir', '/unused'], ['--output-dir=/unused']]:
            result = self.run_wrapper(['--deploy', *value])
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('deployed', result.stdout)


class DashboardBrowser(unittest.TestCase):
    def test_new_schema_transport_statuses_and_injection(self):
        node = shutil.which('node')
        module = os.environ.get('PLAYWRIGHT_MODULE', '')
        chromium = os.environ.get('CHROMIUM_PATH', '')
        if not node or not module or not chromium or not Path(module).exists() or not Path(chromium).exists():
            self.skipTest('Set PLAYWRIGHT_MODULE and CHROMIUM_PATH for offline browser security regression')
        script = r'''
const fs = require('node:fs');
const assert = require('node:assert/strict');
const { chromium } = require(process.argv[1]);
(async () => {
  const browser = await chromium.launch({headless: true, executablePath: process.argv[2]});
  try {
    const statuses = ['dns_error','timeout','tls_error','network_error','proxy_error','redirect_error','http_error','probe_error','mixed','degraded'];
    const payload = '<img src=x onerror="globalThis.injected=true">';
    const portals = Object.fromEntries(statuses.map((status,i) => [String(i), {
      name: payload, agency: payload, url: 'javascript:globalThis.injected=true', tier: 9 + i % 3,
      status, observations: {local: {status, http_code: 0}}
    }]));
    portals.bad = {name: payload, agency: payload, url: 'https://example.invalid/"<script>',
      status: '" onclick="globalThis.injected=true', tier: payload,
      observations: {[payload]: {status:'timeout', http_code: payload}}};
    const snapshot = {schema_version:2, checked_at:'2026-01-01T00:00:00Z', portals,
      sources:{local:{location:'Not configured',provider:payload,type:payload,available:true}}};
    const context = await browser.newContext();
    await context.route('**/*', route => {
      const url = new URL(route.request().url());
      if (url.origin === 'http://status.test' && url.pathname === '/')
        return route.fulfill({contentType:'text/html', body:fs.readFileSync(process.argv[3])});
      if (url.pathname === '/data/history.json')
        return route.fulfill({json:{'2026-01-01':snapshot}});
      return route.fulfill({body:''});
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('http://status.test/');
    await page.waitForSelector('.portal-row');
    assert.equal(await page.locator('.portal-row').count(), 11);
    assert.equal(await page.locator('#portals img, #portals script, #last-check img').count(), 0);
    assert.equal(await page.evaluate(() => globalThis.injected), undefined);
    for (const href of await page.locator('.portal-name a').evaluateAll(nodes => nodes.map(n => n.getAttribute('href'))))
      assert.ok(href === '#' || href.startsWith('https://'));
    assert.ok((await page.locator('#last-check').textContent()).includes(payload));
    assert.ok((await page.locator('#last-check').textContent()).includes('local: Not configured'));
    for (const status of statuses)
      assert.equal(await page.locator('.badge.'+status).count(), status === 'probe_error' ? 2 : 1);
    assert.equal(await page.locator('.pill').count(), 11);
    const summary = await page.locator('#summary .num').allTextContents();
    assert.equal(summary.map(Number).reduce((a,b)=>a+b), 11);
    for (const text of ['Procurement & Program Data','Data APIs & Catalogues','Courts & Law'])
      assert.ok((await page.locator('#portals').textContent()).includes(text));
    assert.equal(await page.locator('.spark-bar.degraded').count(), 1);
    assert.deepEqual(errors, []);
    // Failure text must never interpolate server or exception payloads.
    await context.route('**/data/history.json', route => route.fulfill({status:500, body:payload}));
    await page.reload();
    await page.waitForFunction(() => document.querySelector('#portals').textContent.startsWith('Unable to load'));
    assert.equal(await page.locator('#portals img').count(), 0);
    console.log('PASS: new transport statuses, local metadata, safe DOM/URLs, summary totals, fetch failure');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode=1; });
'''
        result = subprocess.run([node, '-e', script, module, chromium, str(ROOT / 'status/index.html')],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
