"""Offline fixtures are synthetic; they are not government data or live verification."""
import contextlib
import io
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from examples import bi_exchange, bps_inflation, check_ojk, search_halal
from scripts import check_repository


class ExchangeTests(unittest.TestCase):
    HTML = """<table><tr><th>Mata Uang</th><th>Nilai</th><th>Kurs Jual</th>
    <th>Kurs Beli</th></tr><tr><td>JPY</td><td>100</td><td>10.000,00</td>
    <td>9.000,00</td></tr></table>"""

    def test_units_and_sell_buy_are_not_reversed(self):
        self.assertEqual(bi_exchange.parse_exchange_rates(self.HTML), [
            {"currency": "JPY", "units": "100", "sell": "10.000,00", "buy": "9.000,00"}
        ])

    def test_unknown_layout_fails_closed(self):
        for html in ["<html>captcha</html>", "<table><tr><td>USD</td></tr></table>"]:
            with self.assertRaises(ValueError):
                bi_exchange.parse_exchange_rates(html)

    def test_empty_rates_fail_closed(self):
        with self.assertRaises(ValueError):
            bi_exchange.parse_exchange_rates(self.HTML.split("<tr><td>")[0] + "</table>")

    @patch.object(bi_exchange.requests, "get")
    def test_request_timeout_and_http_status(self, get):
        get.return_value = Mock(text=self.HTML)
        bi_exchange.get_exchange_rates(timeout=7)
        self.assertEqual(get.call_args.kwargs["timeout"], 7)
        get.return_value.raise_for_status.assert_called_once()

    @patch.object(bi_exchange.requests, "get")
    def test_http_failure_propagates(self, get):
        get.return_value.raise_for_status.side_effect = requests.HTTPError("failure")
        with self.assertRaises(requests.HTTPError):
            bi_exchange.get_exchange_rates()


class BPSTests(unittest.TestCase):
    @patch.object(bps_inflation.requests, "get")
    def test_payload_is_not_assumed_to_be_flat_year_rows(self, get):
        payload = {"status": "OK", "datacontent": {"synthetic-key": 4.5}, "tahun": []}
        get.return_value = Mock(headers={"Content-Type": "application/json"})
        get.return_value.json.return_value = payload
        self.assertEqual(bps_inflation.get_inflation("secret", "123", "0000", 8), payload)
        self.assertIn("/var/123/key/secret", get.call_args.args[0])
        self.assertEqual(get.call_args.kwargs["timeout"], 8)
        get.return_value.raise_for_status.assert_called_once()

    @patch.object(bps_inflation.requests, "get")
    def test_html_error_is_not_data(self, get):
        get.return_value = Mock(headers={"Content-Type": "text/html"})
        with self.assertRaises(ValueError):
            bps_inflation.get_inflation("secret", "123")

    @patch.object(bps_inflation.requests, "get")
    def test_api_error_and_bad_shape(self, get):
        get.return_value = Mock(headers={"Content-Type": "application/json"})
        for payload in [{"status": "ERROR"}, [], {"status": "OK"}]:
            get.return_value.json.return_value = payload
            with self.assertRaises(ValueError):
                bps_inflation.get_inflation("secret", "123")

    @patch.object(bps_inflation.requests, "get")
    def test_http_error_is_checked_before_json(self, get):
        get.return_value.raise_for_status.side_effect = requests.HTTPError("secret-url")
        with self.assertRaises(requests.HTTPError):
            bps_inflation.get_inflation("secret", "123")
        get.return_value.json.assert_not_called()

    @patch.dict("os.environ", {}, clear=True)
    @patch.object(bps_inflation.requests, "get")
    def test_missing_environment_key_never_calls_network(self, get):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            bps_inflation.main(["--variable", "123"])
        get.assert_not_called()

    @patch.dict("os.environ", {"BPS_API_KEY": "super-secret"})
    @patch.object(bps_inflation.requests, "get", side_effect=requests.Timeout("super-secret"))
    def test_cli_does_not_leak_key_from_exception(self, get):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(bps_inflation.main(["--variable", "123"]), 1)
        self.assertNotIn("super-secret", stderr.getvalue())

    def test_path_segments_reject_injection(self):
        with self.assertRaises(ValueError):
            bps_inflation.get_inflation("secret", "../key/other")


class PortalGuidanceTests(unittest.TestCase):
    @patch.object(requests, "get", side_effect=AssertionError("no network"))
    @patch.object(requests, "post", side_effect=AssertionError("no network"))
    def test_halal_is_guidance_not_supervisor_search(self, post, get):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(search_halal.main(["Synthetic Product"]), 0)
        text = out.getvalue()
        self.assertIn("not certification", text)
        self.assertIn("No public certification-search API is verified", text)
        get.assert_not_called()
        post.assert_not_called()

    @patch.object(requests, "get", side_effect=AssertionError("no network"))
    def test_ojk_never_inferrs_safety_from_no_match(self, get):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(check_ojk.main(["Synthetic Entity"]), 0)
        text = out.getvalue()
        self.assertIn("does NOT prove licensed, legal, or safe", text)
        self.assertIn("find.ojk.go.id", text)
        get.assert_not_called()

    def test_help_runs_without_network(self):
        for module in [bi_exchange, bps_inflation, check_ojk, search_halal]:
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as cm:
                module.main(["--help"])
            self.assertEqual(cm.exception.code, 0)

    def test_invalid_timeout(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            bi_exchange.main(["--timeout", "0"])


class ToolingTests(unittest.TestCase):
    def test_runtime_metadata_and_developer_lock_are_consistent(self):
        root = Path(__file__).resolve().parents[1]
        metadata = tomllib.loads((root / "pyproject.toml").read_text())
        runtime = {line.lower().replace("_", "-") for line in
                   (root / "requirements.txt").read_text().splitlines()
                   if line and not line.startswith("#")}
        developer = {line.lower().replace("_", "-") for line in
                     (root / "requirements-dev.txt").read_text().splitlines()
                     if line and not line.startswith("#")}
        self.assertTrue(runtime <= developer)
        self.assertTrue(set(metadata["project"]["dependencies"]) <= runtime)
        for requirement in runtime | developer:
            self.assertIn("==", requirement)
            self.assertNotIn("*", requirement)

    def test_status_workflow_keeps_schedule_and_static_only_deploy(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/portal-status.yml").read_text()
        self.assertIn("30 4 * * *", workflow)
        self.assertNotIn("CLOUDFLARE_PAGES_ENABLED", workflow)
        self.assertNotIn("pages deploy status ", workflow)
        self.assertIn("--stage-static", workflow)
        self.assertIn("--source-location \"Unknown geographic location\"", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("package-manager-cache: false", workflow)
        self.assertIn("Required Cloudflare deployment token is unavailable.", workflow)


class StaticStagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "status"
        (self.source / "data").mkdir(parents=True)
        for name in check_repository.ASSETS:
            (self.source / name).write_text("synthetic asset")
        for name in ["latest.json", "index.json", "history.json", "2026-01-01.json"]:
            (self.source / "data" / name).write_text("{}")
        self.destination = self.root / "public"

    def stage(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return check_repository.stage_static(self.destination, self.source)

    def test_only_allowlist_is_copied(self):
        for path in ["private.key", "check.py", "check-and-deploy.sh", "README.md", "data/secret.json"]:
            (self.source / path).write_text("synthetic excluded content")
        self.stage()
        copied = {str(p.relative_to(self.destination)) for p in self.destination.rglob("*") if p.is_file()}
        self.assertEqual(copied, set(check_repository.ASSETS) | {
            "data/latest.json", "data/index.json", "data/history.json", "data/2026-01-01.json"
        })

    def test_invalid_json_fails_before_copying(self):
        (self.source / "data" / "latest.json").write_text("not JSON")
        with self.assertRaises(ValueError):
            self.stage()
        self.assertFalse(self.destination.exists())

    def test_asset_and_dataset_symlinks_are_rejected(self):
        for relative in ["index.html", "data/latest.json"]:
            with self.subTest(relative=relative):
                path = self.source / relative
                path.unlink()
                path.symlink_to(self.source / "og-image.png")
                with self.assertRaises(ValueError):
                    self.stage()
                path.unlink()
                path.write_text("{}")

    def test_symlinked_data_directory_is_rejected(self):
        data = self.source / "data"
        data.rename(self.source / "real-data")
        data.symlink_to(self.source / "real-data", target_is_directory=True)
        with self.assertRaises(ValueError):
            self.stage()

    def test_existing_or_nested_destination_is_rejected(self):
        self.destination.mkdir()
        for destination in [self.destination, self.source / "public"]:
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                check_repository.stage_static(destination, self.source)

    def test_required_publication_unit_is_required(self):
        (self.source / "data" / "history.json").unlink()
        with self.assertRaises(ValueError):
            self.stage()


if __name__ == "__main__":
    unittest.main()
