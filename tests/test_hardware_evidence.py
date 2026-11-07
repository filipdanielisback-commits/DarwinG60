"""Tests for the source-backed hardware evidence ledger."""
import copy
import unittest
from darwing60.hardware_evidence import build_report, load_evidence, validate_evidence

class HardwareEvidenceTests(unittest.TestCase):
    def test_repository_ledger_is_valid(self):
        self.assertEqual(validate_evidence(load_evidence()), [])
    def test_unresolved_claim_can_have_no_sources(self):
        data = load_evidence()
        claim = next(item for item in data["claims"] if item["status"] == "unresolved")
        self.assertEqual(claim["sources"], [])
        self.assertEqual(validate_evidence(data), [])
    def test_source_observed_claim_requires_source(self):
        data = copy.deepcopy(load_evidence())
        claim = next(item for item in data["claims"] if item["status"] == "source_observed")
        claim["sources"] = []
        self.assertTrue(any("needs at least one source" in error for error in validate_evidence(data)))
    def test_bad_url_is_rejected(self):
        data = copy.deepcopy(load_evidence())
        data["claims"][0]["sources"][0]["url"] = "not-a-url"
        self.assertTrue(any("HTTP(S)" in error for error in validate_evidence(data)))
    def test_duplicate_claim_ids_are_rejected(self):
        data = copy.deepcopy(load_evidence())
        data["claims"].append(copy.deepcopy(data["claims"][0]))
        self.assertTrue(any("Duplicate claim id" in error for error in validate_evidence(data)))
    def test_report_preserves_unresolved_controller_status(self):
        report = build_report(load_evidence())
        self.assertIn("Physical touchscreen controller identity", report)
        self.assertIn("[unresolved/unknown]", report)
        self.assertIn("Unresolved claims: 2", report)

if __name__ == "__main__":
    unittest.main()
