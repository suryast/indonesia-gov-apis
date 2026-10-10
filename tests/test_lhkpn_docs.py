"""Offline regressions for issue #1; never request officials' personal data."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "apis/tier2-scrapeable/kpk-lhkpn/README.md"


class LhkpnDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_broken_routes_and_fake_selectors_removed(self):
        for token in ("/portal/user/search_pejabat", "/register/detail/12345",
                      ".result-item", ".nama", ".instansi", ".total-harta"):
            with self.subTest(token=token):
                self.assertNotIn(token, self.text)

    def test_official_entry_point_is_linked(self):
        self.assertIn("](https://elhkpn.kpk.go.id/portal/user/login)", self.text)
        self.assertIn("e-Announcement", self.text)

    def test_manual_search_and_download_flow(self):
        for token in ("CAPTCHA", "manually", "Cari", "Siapakah Anda", "Download"):
            with self.subTest(token=token):
                self.assertIn(token, self.text)

    def test_public_announcement_and_filing_are_separate(self):
        self.assertIn("e-Filing", self.text)
        self.assertIn("activated, authorized account", self.text)
        self.assertIn("Do not infer that all", self.text)
        self.assertIn("public announcements require an e-Filing account", self.text)

    def test_observation_limit_and_no_guessed_working_api(self):
        for token in ("HTTP 200 is not API success", "URLError", "historical",
                      "No public JSON API contract", "Current API access remains unverified",
                      "No search for a person", "not a completed"):
            with self.subTest(token=token):
                self.assertIn(token, self.text)
        self.assertNotIn("```python", self.text)

    def test_suggested_repository_not_endorsed(self):
        self.assertIn("nichsedge/lhkpn", self.text)
        self.assertIn("read-only", self.text)
        self.assertIn("nothing was installed or executed", self.text)
        self.assertIn("untrusted third-party claims", self.text)
        self.assertIn("not independently", self.text)
        self.assertIn("Do not bypass CAPTCHA", self.text)

    def test_catalog_scope_matches_documentation(self):
        catalog = json.loads((ROOT / "catalog/sources.json").read_text(encoding="utf-8"))
        entry = next(source for source in catalog["sources"] if source["id"] == "kpk-lhkpn")
        self.assertEqual(entry["documentation"], str(DOC.relative_to(ROOT)))
        self.assertEqual(entry["review"]["status"], "primary_documentation_reviewed")
        self.assertTrue(any(e["url"] == "https://elhkpn.kpk.go.id/portal/user/login" for e in entry["review"]["evidence"]))
        self.assertIn("manual", entry["access"]["auth"])


if __name__ == "__main__":
    unittest.main()
