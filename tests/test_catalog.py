"""Offline catalog integrity tests; these do not validate live APIs."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_catalog", ROOT / "scripts/validate_catalog.py")
assert SPEC is not None and SPEC.loader is not None
catalog_validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog_validator)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "catalog/sources.json").read_text(encoding="utf-8"))

    def errors(self, catalog):
        return catalog_validator.validate_catalog(ROOT, catalog)

    def test_repository_catalog(self):
        self.assertEqual(self.errors(self.catalog), [])

    def test_preserved_aturan_contribution(self):
        records = [s for s in self.catalog["sources"] if s["id"] == "aturan-org"]
        self.assertEqual(len(records), 1)
        source = records[0]
        self.assertEqual((source["tier"], source["kind"], source["monitor_ids"]),
                         ("tier7", "non-government", []))
        doc = (ROOT / source["documentation"]).read_text(encoding="utf-8")
        self.assertIn("https://peraturan.bpk.go.id", doc)
        self.assertNotIn("bpk.peraturan.go.id", doc)
        self.assertIn("Streamable HTTP", doc)
        self.assertIn("POST /query/peraturan-terkait", doc)
        self.assertIn("No authenticated REST request", doc)
        self.assertEqual(self.catalog["totals"]["source_documents"], 59)
        self.assertEqual(self.catalog["totals"]["indonesia_source_documents"], 58)
        self.assertEqual(self.catalog["totals"]["by_tier"]["tier7"], 7)

    def test_duplicate_id(self):
        self.catalog["sources"][1]["id"] = self.catalog["sources"][0]["id"]
        self.assertTrue(any("duplicate id" in e for e in self.errors(self.catalog)))

    def test_duplicate_document(self):
        self.catalog["sources"][1]["documentation"] = self.catalog["sources"][0]["documentation"]
        self.assertTrue(any("duplicate documentation" in e for e in self.errors(self.catalog)))

    def test_omitted_source(self):
        self.catalog["sources"].pop()
        self.assertTrue(any("source documentation coverage" in e for e in self.errors(self.catalog)))

    def test_wrong_totals(self):
        self.catalog["totals"]["source_documents"] += 1
        self.assertTrue(any("totals" in e for e in self.errors(self.catalog)))

    def test_invalid_url(self):
        self.catalog["sources"][0]["portal_url"] = "javascript:alert(1)"
        self.assertTrue(any("portal_url" in e for e in self.errors(self.catalog)))

    def test_secret_in_url(self):
        self.catalog["sources"][0]["portal_url"] = "https://user:secret@example.org/"
        self.assertTrue(any("portal_url" in e for e in self.errors(self.catalog)))

    def test_invalid_date(self):
        self.catalog["sources"][0]["review"]["date"] = "2026-02-30"
        self.assertTrue(any("date" in e for e in self.errors(self.catalog)))

    def test_unknown_review_status(self):
        self.catalog["sources"][0]["review"]["status"] = "working_everywhere"
        self.assertTrue(any("review status" in e for e in self.errors(self.catalog)))

    def test_missing_evidence(self):
        self.catalog["sources"][0]["review"]["evidence"] = []
        self.assertTrue(any("evidence" in e for e in self.errors(self.catalog)))

    def test_invalid_kind(self):
        self.catalog["sources"][0]["kind"] = "official-ish"
        self.assertTrue(any("kind" in e for e in self.errors(self.catalog)))

    def test_escaping_path(self):
        self.catalog["sources"][0]["documentation"] = "../README.md"
        self.assertTrue(any("documentation" in e for e in self.errors(self.catalog)))

    def test_reference_coverage(self):
        self.catalog["supplementary_documents"].pop()
        self.assertTrue(any("reference documentation coverage" in e for e in self.errors(self.catalog)))

    def test_unrecognized_related_source(self):
        self.catalog["sources"][0]["related_sources"] = ["missing-source"]
        self.assertTrue(any("related_sources" in e for e in self.errors(self.catalog)))

    def test_schema_missing_required_field(self):
        del self.catalog["sources"][0]["access"]
        self.assertTrue(any("access" in e for e in self.errors(self.catalog)))

    def test_malformed_records_do_not_crash(self):
        for field, value in [("sources", [None]), ("sources", {}), ("totals", []),
                             ("supplementary_documents", [False])]:
            changed = copy.deepcopy(self.catalog)
            changed[field] = value
            self.assertTrue(self.errors(changed))

    def test_broken_local_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[broken](missing.md)\n", encoding="utf-8")
            self.assertTrue(any("missing local link" in e for e in catalog_validator.validate_links(root, [root / "README.md"])))

    def test_valid_anchor_and_external_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("# Title\n[anchor](#title) [web](https://example.org/)\n", encoding="utf-8")
            self.assertEqual(catalog_validator.validate_links(root, [path]), [])

    def test_missing_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("# Title\n[broken](#no-such-heading)\n", encoding="utf-8")
            self.assertTrue(any("missing anchor" in e for e in catalog_validator.validate_links(root, [path])))


if __name__ == "__main__":
    unittest.main()
