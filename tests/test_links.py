"""Offline link-audit contracts; no external requests."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_links.py"
spec = importlib.util.spec_from_file_location("check_links", SCRIPT)
assert spec is not None and spec.loader is not None
links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(links)


class LinkTests(unittest.TestCase):
    def test_extractor_locations_and_balanced_targets(self):
        text = (
            '# Title\n[doc](a(b).md#one "title") ![img](pic.png)\n'
            '[ref][id] and [id]\n[id]: https://site.test/a_(b) "title"\n'
            "```sh\ncurl https://site.test/api/{KEY}/x\n```\n"
            "prose https://site.test/a_(b).\n"
        )
        found = links.extract(text, "README.md")
        self.assertTrue(
            any(x["target"] == "a(b).md#one" and x["line"] == 2 for x in found)
        )
        self.assertTrue(any(x["target"] == "pic.png" for x in found))
        self.assertTrue(
            any(
                x["target"] == "https://site.test/api/{KEY}/x" and x["line"] == 6
                for x in found
            )
        )
        self.assertEqual(
            {x["line"] for x in found if x["target"] == "https://site.test/a_(b)"},
            {3, 4, 8},
        )

    def test_not_requested_safety(self):
        for url in [
            "https://u:p@host.org/x",
            "https://host.org/?api_key=abc",
            "https://host.org/{id}",
            "https://host.org/<TOKEN>/x",
            "https://host.org/$API_KEY",
            "https://example.com/x",
            "https://127.0.0.1/private",
            "https://host.org/key/ABC123",
        ]:
            with self.subTest(url=url):
                self.assertIsNotNone(links.skip_reason(url))
        self.assertIsNone(links.skip_reason("https://www.bmkg.go.id/"))
        self.assertNotIn("abc", links.public_target("https://host.org/?api_key=abc"))
        self.assertNotIn("u:p", links.public_target("https://u:p@host.org/x"))

    def test_credential_never_requested_or_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[x](https://host.org/?token=secret-value)")
            with patch.object(links, "probe", side_effect=AssertionError("network")):
                report = links.audit(root)
            self.assertNotIn("secret-value", json.dumps(report))
            self.assertEqual(report["external"][0]["classification"], "not_requested")

    def test_allowlist_and_report_exclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in [
                "README.md",
                "other.md",
                "docs/a.MD",
                "docs/.cache/x.md",
                "docs/link-audit-2026-10-10.md",
                "status/node_modules/x.md",
                "examples/a.md",
                "private/x.md",
            ]:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("")
            self.assertEqual(
                [p.relative_to(root).as_posix() for p in links.markdown_files(root)],
                ["README.md", "docs/a.MD", "examples/a.md"],
            )

    def test_local_paths_anchors_and_duplicate_headings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Héllo, *world*!\n# Héllo, *world*!\n"
                '```\n# fake\n```\n<a id="explicit"></a>\n'
            )
            for target in ["#héllo-world", "#héllo-world-1", "#explicit"]:
                self.assertEqual(
                    links.check_local(root, "README.md", target)["classification"],
                    "local_ok",
                )
            self.assertEqual(
                links.check_local(root, "README.md", "#fake")["classification"],
                "missing_anchor",
            )
            self.assertEqual(
                links.check_local(root, "README.md", "gone.md")["classification"],
                "missing_path",
            )
            self.assertEqual(
                links.check_local(root, "README.md", "../outside")["classification"],
                "outside_repository",
            )

    def test_http_and_transport_classes(self):
        expected = {
            401: "auth_required",
            403: "blocked",
            429: "rate_limited",
            404: "broken_http",
            500: "server_error",
            200: "reachable",
        }
        for status, category in expected.items():
            self.assertEqual(links.classify_http(status, False), category)
        self.assertEqual(links.classify_http(404, True), "api_request_required")
        for code, category in {
            6: "dns_error",
            28: "timeout",
            60: "tls_error",
            7: "network_error",
            47: "redirect_limit",
        }.items():
            self.assertEqual(links.classify_curl(code), category)

    def test_fragment_identity_redirect_safety_and_cap(self):
        replies = [
            subprocess.CompletedProcess(
                [], 0, "302\nhttps://host.org/?token=secret\n", ""
            ),
            subprocess.CompletedProcess([], 0, "200\n\n", ""),
        ]
        with patch.object(links.subprocess, "run", side_effect=replies) as run:
            result = links.probe("https://host.org/a#one", timeout=2, byte_cap=42)
        self.assertEqual(run.call_count, 1)
        self.assertEqual(result["classification"], "redirect_not_requested")
        self.assertNotIn("secret", json.dumps(result))
        args = run.call_args.args[0]
        self.assertIn("https://host.org/a", args)
        self.assertIn("--max-filesize", args)
        self.assertIn("42", args)
        self.assertNotIn("-k", args)
        self.assertNotIn("--location", args)

    def test_transport_metadata_sanitized_and_body_limit_http_observed(self):
        with patch.object(
            links.subprocess,
            "run",
            return_value=subprocess.CompletedProcess(
                [], 60, "000\n\n", "private secret"
            ),
        ):
            result = links.probe("https://host.org/")
        self.assertEqual(result["classification"], "tls_error")
        self.assertNotIn("private", json.dumps(result))
        with patch.object(
            links.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 63, "200\n\n", ""),
        ):
            result = links.probe("https://host.org/")
        self.assertEqual(result["classification"], "reachable")
        self.assertTrue(result["body_limit_reached"])

    def test_multiline_destination_and_reference_occurrence_count(self):
        text = "[x](\n  <relative.md>)\n[shown][id] [id]\n[id]: https://host.org/a\n"
        found = links.extract(text, "README.md")
        self.assertEqual(found[0]["line"], 2)
        self.assertEqual(found[0]["column"], 4)
        self.assertEqual(sum(x["kind"] == "reference_usage" for x in found), 2)

    def test_direct_probe_rejects_dummy_template_and_fragment_secrets(self):
        targets = [
            "https://api.example.org/x",
            "https://[HOST]/x",
            "https://host.org/x#token=secret-fragment",
            "https://host.org/register/detail/12345",
            "https://host.org/?key=secret",
        ]
        with patch.object(
            links.subprocess, "run", side_effect=AssertionError("network")
        ):
            for target in targets:
                result = links.probe(target)
                self.assertEqual(result["classification"], "not_requested")
                self.assertNotIn("secret-fragment", json.dumps(result))
        self.assertNotIn("secret", links.public_target(targets[-1]))

    def test_redirect_cap_and_timeout(self):
        reply = subprocess.CompletedProcess([], 0, "302\nhttps://host.org/next\n", "")
        with patch.object(links.subprocess, "run", return_value=reply) as run:
            result = links.probe("https://host.org/a", redirect_cap=2)
        self.assertEqual(run.call_count, 3)
        self.assertEqual(result["classification"], "redirect_limit")
        with patch.object(
            links.subprocess, "run", side_effect=subprocess.TimeoutExpired("curl", 1)
        ):
            result = links.probe("https://host.org/a")
        self.assertEqual(result["classification"], "timeout")

    def test_html_anchor_and_invalid_local_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<main id="status"><a name="old"></a></main>'
            )
            for target in ["index.html#status", "index.html#old"]:
                self.assertEqual(
                    links.check_local(root, "README.md", target)["classification"],
                    "local_ok",
                )
            self.assertEqual(
                links.check_local(root, "README.md", "index.html#gone")[
                    "classification"
                ],
                "missing_anchor",
            )
            self.assertEqual(
                links.check_local(root, "README.md", "//[invalid")["classification"],
                "invalid_local_target",
            )

    def test_freshness_and_api_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[api](https://web-api.host.org/1/num)")

            def observed(*args):
                (root / "README.md").write_text("changed")
                (root / "docs").mkdir()
                (root / "docs/new.md").write_text("new")
                return {
                    "classification": links.classify_http(404, args[-1]),
                    "status": 404,
                }

            with patch.object(links, "probe", side_effect=observed):
                report = links.audit(root)
            self.assertEqual(
                report["external"][0]["classification"], "api_request_required"
            )
            self.assertEqual(report["sources_changed_during_audit"], ["README.md"])
            self.assertEqual(report["sources_added_during_audit"], ["docs/new.md"])

    def test_summary_dedupe_hashes_and_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "[a](https://host.org/#a)\n"
                "[b](https://host.org/#a)\n"
                "[c](https://host.org/#b)\n[x](missing.md)\n"
            )
            with patch.object(
                links,
                "probe",
                return_value={
                    "classification": "reachable",
                    "status": 200,
                    "final_url": "https://host.org/",
                },
            ):
                report = links.audit(root)
            self.assertEqual(report["counts"]["unique_external_urls"], 2)
            self.assertEqual(report["counts"]["external_occurrences"], 3)
            self.assertEqual(report["counts"]["local_occurrences"], 1)
            self.assertEqual(
                report["counts"]["external_classifications"], {"reachable": 2}
            )
            self.assertEqual(len(report["sources"][0]["sha256"]), 64)
            self.assertEqual(sum(report["counts"]["local_classifications"].values()), 1)
            self.assertIn("README.md:4", links.render_markdown(report))
            self.assertIn("missing_path", links.render_markdown(report))


if __name__ == "__main__":
    unittest.main()
