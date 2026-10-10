"""Offline monitor-only inventory gates; no endpoint requests or checker import."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("monitor_catalog_validator", ROOT / "scripts/validate_catalog.py")
assert SPEC is not None and SPEC.loader is not None
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


class MonitorOnlyTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((ROOT / "catalog/monitor-only.json").read_text())
        self.catalog = json.loads((ROOT / "catalog/sources.json").read_text())
        self.linked = [i for s in self.catalog["sources"] for i in s["monitor_ids"]]
        self.portals = {i: (i, i, "https://example.org", "fixture", 1) for i in self.linked}
        self.portals.update({e[0]: e for e in v.MONITOR_ONLY_APPROVED})

    def errors(self):
        return v.validate_monitor_inventory(ROOT, self.linked, self.registry, self.portals)

    def test_exact_75_union_without_source_inflation(self):
        before = copy.deepcopy(self.catalog)
        self.assertEqual(len(self.linked), 57)
        self.assertEqual(len(self.portals), 75)
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.catalog, before)
        self.assertEqual(v.compute_totals(self.catalog["sources"], self.catalog["supplementary_documents"])["source_documents"], 59)

    def test_duplicate(self):
        self.registry["endpoints"].append(copy.deepcopy(self.registry["endpoints"][0]))
        self.assertTrue(any("duplicate" in e for e in self.errors()))

    def test_removed(self):
        self.registry["endpoints"].pop()
        self.assertTrue(any("exactly 18" in e for e in self.errors()))
        self.assertTrue(any("coverage" in e for e in self.errors()))

    def test_each_tuple_field_mismatch(self):
        original = copy.deepcopy(self.registry)
        for key, value in [("url", "https://example.org/wrong"), ("name", "wrong"), ("agency", "wrong"), ("tier", 8)]:
            self.registry = copy.deepcopy(original)
            self.registry["endpoints"][0][key] = value
            self.assertTrue(any("tuple mismatch" in e for e in self.errors()), key)

    def test_portals_url_mismatch(self):
        pid = self.registry["endpoints"][0]["id"]
        row = list(self.portals[pid]); row[2] = "https://example.org/wrong"
        self.portals[pid] = tuple(row)
        self.assertTrue(any("PORTALS tuple" in e for e in self.errors()))

    def test_unapproved_extra(self):
        entry = copy.deepcopy(self.registry["endpoints"][0]); entry["id"] = "unapproved"
        self.registry["endpoints"].append(entry)
        self.assertTrue(any("unapproved" in e for e in self.errors()))

    def test_unmapped_checker_extra(self):
        self.portals["unapproved"] = ("unapproved", "extra", "https://example.org", "fixture", 1)
        self.assertTrue(any("coverage" in e for e in self.errors()))

    def test_cross_inventory_duplicate(self):
        self.linked.append(self.registry["endpoints"][0]["id"])
        self.assertTrue(any("duplicate" in e for e in self.errors()))

    def test_no_false_review_success(self):
        self.registry["endpoints"][0]["review"]["status"] = "endpoint_observed"
        self.assertTrue(any("unverified" in e for e in self.errors()))

    def test_old_checker_is_blocked_when_registry_exists(self):
        self.portals = {i: self.portals[i] for i in self.linked}
        self.assertTrue(any("coverage" in e for e in self.errors()))

    def test_optional_registry_only_with_exact_old_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            old = {i: self.portals[i] for i in self.linked}
            self.assertEqual(v.validate_monitor_inventory(Path(directory), self.linked, portals=old), [])
            self.assertTrue(v.validate_monitor_inventory(Path(directory), self.linked, portals=self.portals))

    def test_current_checker_exact_identity(self):
        self.assertEqual(v.validate_monitor_inventory(ROOT, self.linked), [])


if __name__ == "__main__":
    unittest.main()
