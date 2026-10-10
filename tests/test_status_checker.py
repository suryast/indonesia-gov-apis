"""Offline status regressions; loopback only, no public requests or tracked writes."""
import importlib.util
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('status_checker', ROOT / 'status/check.py')
assert spec is not None and spec.loader is not None
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class TransportTests(unittest.TestCase):
    def test_registry_labels_do_not_overstate_verified_capabilities(self):
        registry = {entry[0]: entry for entry in checker.PORTALS}
        self.assertEqual(len(registry), len(checker.PORTALS))
        self.assertIn('unverified web endpoint', registry['cmsbl-halal'][1])
        self.assertNotIn('API', registry['cmsbl-halal'][1])
        if registry['ojk-sikepo'][2].rstrip('/') == 'https://ojk.go.id':
            self.assertIn('root-only probe', registry['ojk-sikepo'][1])
        for entry in registry.values():
            self.assertNotEqual(entry[3], 'Kemenkumham')

    def test_transport_not_inferred_from_http_zero(self):
        for exit_code, expected in [(6, 'dns_error'), (5, 'proxy_error'), (28, 'timeout'),
                                    (60, 'tls_error'), (35, 'tls_error'), (7, 'network_error'),
                                    (47, 'redirect_error'), (0, 'probe_error')]:
            with self.subTest(exit_code=exit_code):
                self.assertEqual(checker.classify(0, exit_code), expected)
        self.assertEqual(checker.classify(200, 28), 'timeout')

    def test_http_semantics(self):
        for code, expected in [(200, 'up'), (302, 'up'), (403, 'blocked'),
                               (401, 'http_error'), (429, 'http_error'), (503, 'http_error')]:
            self.assertEqual(checker.classify(code, 0), expected)

    def test_safe_curl_and_sanitized_errors(self):
        with patch.object(checker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 60, '000|0.25', 'secret')) as run:
            result = checker.check_url_local('https://example.invalid', 2)
        self.assertEqual(result['status'], 'tls_error')
        self.assertEqual(result['latency_ms'], 250)
        self.assertNotIn('secret', json.dumps(result))
        args = run.call_args.args[0]
        self.assertEqual(args[1], '--disable')
        self.assertIn('--proto-redir', args)
        self.assertNotIn('-k', args)

    def test_probe_failures(self):
        for failure, status in [(FileNotFoundError(), 'probe_error'),
                                (subprocess.TimeoutExpired('curl', 2), 'timeout')]:
            with patch.object(checker.subprocess, 'run', side_effect=failure):
                self.assertEqual(checker.check_url_local('https://example.invalid')['status'], status)
        for raw in ['garbage', '200|nan', '200|-1']:
            with patch.object(checker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, raw, '')):
                self.assertEqual(checker.check_url_local('https://example.invalid')['status'], 'probe_error')

    def test_no_geographic_inference(self):
        self.assertEqual(checker.overall_status(['up', 'timeout']), 'mixed')
        self.assertEqual(checker.overall_status(['blocked', 'up']), 'mixed')
        self.assertEqual(checker.overall_status(['dns_error']), 'dns_error')


class PR10Tests(unittest.TestCase):
    def test_exact_upstream_union_and_repointed_urls(self):
        import ast
        upstream = subprocess.check_output(['git', 'show', 'origin/main:status/check.py'], cwd=ROOT, text=True)
        tree = ast.parse(upstream)
        values = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
                  if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                  and n.targets[0].id in {'PORTALS', 'EXPECT'}}
        actual = {p[0]: p for p in checker.PORTALS}
        expected = {p[0]: p for p in values['PORTALS']}
        self.assertEqual(len(actual), 75)
        self.assertEqual(set(actual), set(expected))
        for pid in expected:
            self.assertEqual(actual[pid][2], expected[pid][2])
            if expected[pid][4] >= 9:
                self.assertEqual(actual[pid], expected[pid])
        self.assertEqual(checker.EXPECT, values['EXPECT'])

    def test_content_outcomes_bounded_and_private(self):
        for body, code, exit_code, status, content in [
            (b'PUBLIC Marker', 200, 0, 'up', 'matched'),
            (b'private never publish', 200, 0, 'degraded', 'missing'),
            (b'PUBLIC Marker', 503, 0, 'http_error', 'unverified'),
            (b'PUBLIC Marker', 200, 28, 'timeout', 'unverified'),
            (b'partial', 200, 63, 'up', 'unverified'),
            (b'partial', 200, 18, 'network_error', 'unverified')]:
            def run(args, **kwargs):
                Path(args[args.index('--output') + 1]).write_bytes(body)
                return subprocess.CompletedProcess(args, exit_code, f'{code}|0.01')
            with patch.object(checker, 'curl_supports_body_cap', return_value=True), patch.object(checker.subprocess, 'run', side_effect=run) as mock:
                result = checker.check_url_local('https://example.invalid', 1, expect='public marker')
            self.assertEqual(result['status'], status)
            self.assertEqual(result['content_check'], content)
            args = mock.call_args.args[0]
            self.assertIn('--max-filesize', args)
            self.assertEqual(args[args.index('--proto-redir') + 1], '=https')
            self.assertFalse(Path(args[args.index('--output') + 1]).exists())
            self.assertNotIn('private', json.dumps(result))
        with patch.object(checker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '200|0.01')):
            self.assertNotIn('content_check', checker.check_url_local('https://example.invalid'))
        with patch.object(checker, 'curl_supports_body_cap', return_value=False), patch.object(checker.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '200|0.01')) as mock:
            result = checker.check_url_local('https://example.invalid', expect='marker')
        self.assertEqual(result['status'], 'up')
        self.assertEqual(result['content_check'], 'unverified')
        self.assertEqual(mock.call_args.args[0][mock.call_args.args[0].index('--output') + 1], checker.os.devnull)


class PublicationTests(unittest.TestCase):
    def snapshot(self, day):
        return {'date': day, 'checked_at': day + 'T00:00:00+00:00',
                'portals': {'fixture': {'status': 'up'}}, 'sources': {}}

    def test_complete_consistent_history_and_same_day_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            checker.publish(self.snapshot('2026-01-01'), directory)
            result = self.snapshot('2026-01-02')
            result['sources'] = {'local': {'location': 'Not configured'}}
            checker.publish(result, directory)
            checker.publish(result, directory)
            history = json.loads((directory / 'history.json').read_text())
            self.assertEqual(list(history), ['2026-01-01', '2026-01-02'])
            self.assertEqual(history['2026-01-02'], result)
            self.assertEqual(json.loads((directory / 'latest.json').read_text()), result)
            self.assertEqual(json.loads((directory / 'index.json').read_text()), list(history))
            self.assertEqual(list(directory.glob('*.tmp')), [])

    def test_legacy_snapshot_preserved_without_fabricated_date(self):
        legacy = {'checked_at': '2026-02-14T04:30:00Z',
                  'portals': {'legacy': {'status': 'geo_blocked_id', 'au': {'http_code': 403}}}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / '2026-02-14.json'
            path.write_text(json.dumps(legacy))
            before = path.read_bytes()
            checker.publish(self.snapshot('2026-03-16'), tmp)
            history = json.loads((Path(tmp) / 'history.json').read_text())
            self.assertEqual(history['2026-02-14'], legacy)
            self.assertNotIn('date', history['2026-02-14'])
            self.assertEqual(path.read_bytes(), before)

    def test_actual_tracked_history_publishes_from_read_only_copy(self):
        names = subprocess.check_output(
            ['git', 'ls-files', 'status/data/????-??-??.json'], cwd=ROOT, text=True).splitlines()
        self.assertTrue(names)
        before = {name: (ROOT / name).read_bytes() for name in names}
        originals = {Path(name).stem: json.loads(raw) for name, raw in before.items()}
        self.assertIn('2026-02-14', originals)
        self.assertNotIn('date', originals['2026-03-15'])
        self.assertEqual(originals['2026-03-16']['date'], '2026-03-16')
        with tempfile.TemporaryDirectory() as tmp:
            for name, raw in before.items():
                (Path(tmp) / Path(name).name).write_bytes(raw)
            checker.publish(self.snapshot('2099-01-01'), tmp)
            history = json.loads((Path(tmp) / 'history.json').read_text())
            self.assertEqual({day: history[day] for day in originals}, originals)
            for name, raw in before.items():
                self.assertEqual((Path(tmp) / Path(name).name).read_bytes(), raw)
                self.assertEqual((ROOT / name).read_bytes(), raw)

    def test_invalid_history_fails_closed_before_publication_or_probes(self):
        valid = self.snapshot('2026-02-14')
        invalid = [dict(valid, date='2026-02-15'), dict(valid, date=None),
                   dict(valid, portals={}), dict(valid, portals=[]),
                   {k: v for k, v in valid.items() if k != 'portals'}, []]
        for timestamp in [None, 42, '', '2026-02-14', '2026-02-14Tgarbage',
                          '2026-02-14T25:00:00Z', '2026-02-30T04:30:00Z',
                          '2026-02-15T04:30:00Z', '2026-02-14T04:30:00']:
            invalid.extend([dict(valid, checked_at=timestamp),
                            {'checked_at': timestamp, 'portals': valid['portals']}])
        for raw in ['{'] + [json.dumps(value) for value in invalid]:
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                (directory / '2026-02-14.json').write_text(raw)
                (directory / 'history.json').write_text('{"unchanged": true}')
                before = {p.name: p.read_bytes() for p in directory.iterdir()}
                with self.assertRaises(ValueError):
                    checker.publish(self.snapshot('2026-03-16'), directory)
                with patch.object(checker, 'check_url_local',
                                  return_value={'status': 'probe_error'}) as observe:
                    self.assertEqual(checker.main(['--output-dir', tmp]), 1)
                    observe.assert_not_called()
                self.assertEqual({p.name: p.read_bytes() for p in directory.iterdir()
                                  if p.name != '.check.lock'}, before)

    def test_corrupt_prior_day_aborts_before_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            checker.publish(self.snapshot('2026-01-01'), directory)
            (directory / '2026-01-01.json').write_text('{')
            before = (directory / 'history.json').read_bytes()
            with self.assertRaises(ValueError):
                checker.publish(self.snapshot('2026-01-02'), directory)
            self.assertEqual((directory / 'history.json').read_bytes(), before)
            self.assertFalse((directory / '2026-01-02.json').exists())

    def test_write_failure_keeps_authoritative_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            checker.publish(self.snapshot('2026-01-01'), directory)
            before = (directory / 'history.json').read_bytes()
            with patch.object(checker.os, 'replace', side_effect=OSError('disk failure')):
                with self.assertRaises(OSError):
                    checker.publish(self.snapshot('2026-01-02'), directory)
            self.assertEqual((directory / 'history.json').read_bytes(), before)
            self.assertEqual(list(directory.glob('*.tmp')), [])

    def test_partial_replacement_keeps_complete_old_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            checker.publish(self.snapshot('2026-01-01'), directory)
            before = (directory / 'history.json').read_bytes()
            original_replace = checker.os.replace
            calls = []

            def fail_before_history(source, target):
                calls.append(target.name)
                if target.name == 'history.json':
                    raise OSError('publication failure')
                return original_replace(source, target)

            with patch.object(checker.os, 'replace', side_effect=fail_before_history):
                with self.assertRaises(OSError):
                    checker.publish(self.snapshot('2026-01-02'), directory)
            self.assertEqual(calls[-1], 'history.json')
            self.assertEqual((directory / 'history.json').read_bytes(), before)
            self.assertEqual(list(directory.glob('*.tmp')), [])
            checker.publish(self.snapshot('2026-01-02'), directory)
            self.assertEqual(len(json.loads((directory / 'history.json').read_text())), 2)

    def test_cli_offline_output_and_honest_metadata(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(checker, 'PORTALS', [('test', 'Test', 'https://example.invalid', 'Agency', 1)]), patch.object(checker, 'check_url_local', return_value={'status': 'timeout', 'http_code': 0, 'latency_ms': 0}):
            self.assertEqual(checker.main(['--output-dir', tmp, '--workers', '2', '--timeout', '1']), 0)
            latest = json.loads((Path(tmp) / 'latest.json').read_text())
            self.assertEqual(latest['sources']['local']['location'], 'Not configured')
            self.assertEqual(latest['portals']['test']['status'], 'timeout')
            self.assertNotIn('au', latest['portals']['test'])

    def test_concurrent_writer_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with (Path(tmp) / '.check.lock').open('a') as lock:
                checker.fcntl.flock(lock, checker.fcntl.LOCK_EX | checker.fcntl.LOCK_NB)
                with patch.object(checker, 'check_url_local') as observe:
                    self.assertEqual(checker.main(['--output-dir', tmp]), 1)
                    observe.assert_not_called()
            self.assertFalse((Path(tmp) / 'history.json').exists())

    def test_probe_error_does_not_publish(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(checker, 'PORTALS', [('test', 'Test', 'https://example.invalid', 'Agency', 1)]), patch.object(checker, 'check_url_local', return_value={'status': 'probe_error', 'http_code': 0, 'latency_ms': 0}):
            self.assertEqual(checker.main(['--output-dir', tmp]), 1)
            self.assertFalse((Path(tmp) / 'history.json').exists())

    def test_invalid_cli(self):
        for args in [['--workers', '0'], ['--workers', '33'], ['--timeout', '0'], ['--timeout', 'nan']]:
            with self.assertRaises(SystemExit):
                checker.main(args)


class LocalCurlIntegration(unittest.TestCase):
    def test_real_bounded_static_content_with_unknown_length(self):
        if not checker.curl_supports_body_cap():
            self.skipTest('curl >=8.4 required for hard unknown-length cap')
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                body = (b'x' * (checker.BODY_BYTE_CAP + 32768) if self.path == '/large'
                        else b'public MARKER' if self.path == '/matched' else b'no marker here')
                self.send_response(200)
                self.end_headers()  # Deliberately unknown-length HTTP/1.0 body.
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.dict(checker.os.environ, {'NO_PROXY': '127.0.0.1', 'no_proxy': '127.0.0.1'}):
                for path, status, content in [('/matched', 'up', 'matched'),
                                              ('/missing', 'degraded', 'missing'),
                                              ('/large', 'up', 'unverified')]:
                    result = checker.check_url_local(f'http://127.0.0.1:{server.server_port}{path}', 2, expect='public marker')
                    self.assertEqual(result['status'], status)
                    self.assertEqual(result['content_check'], content)
                    if path == '/large':
                        self.assertEqual(result['curl_exit_code'], 63)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_real_curl_http_and_transport_without_external_network(self):
        if not shutil.which('curl'):
            self.skipTest('curl is required for loopback integration')

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(int(self.path[1:]))
                self.send_header('Content-Length', '0')
                self.end_headers()

            def log_message(self, format, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.dict(checker.os.environ, {'NO_PROXY': '127.0.0.1', 'no_proxy': '127.0.0.1'}):
                for code, status in [(200, 'up'), (403, 'blocked'), (503, 'http_error')]:
                    result = checker.check_url_local(f'http://127.0.0.1:{server.server_port}/{code}', 2)
                    self.assertEqual(result['status'], status)
                    self.assertEqual(result['http_code'], code)
                    self.assertEqual(result['curl_exit_code'], 0)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
