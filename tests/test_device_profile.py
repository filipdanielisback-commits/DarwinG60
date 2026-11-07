"""Tests for DarwinG60 device profile metadata."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.device_profile import (  # noqa: E402
    build_report,
    load_compatibility,
    load_device_profile,
    validate_profiles,
)


class DeviceProfileTests(unittest.TestCase):
    def test_device_identity(self):
        profile = load_device_profile()
        self.assertEqual(profile["device"]["marketing_name"], "Moto G60")
        self.assertEqual(profile["device"]["codename"], "hanoip")

    def test_chipset_and_graphics(self):
        profile = load_device_profile()
        self.assertEqual(profile["platform"]["soc_marketing_name"], "Qualcomm Snapdragon 732G")
        self.assertEqual(profile["platform"]["gpu"], "Qualcomm Adreno 618")

    def test_compatibility_has_components(self):
        compatibility = load_compatibility()
        self.assertGreater(len(compatibility["components"]), 0)

    def test_profile_validation_passes(self):
        self.assertEqual(validate_profiles(), [])

    def test_report_is_honest_about_status(self):
        report = build_report()
        self.assertIn("XNU kernel ported: False", report)
        self.assertIn("Bootable image available: False", report)
        self.assertIn("research-only", report.lower())


if __name__ == "__main__":
    unittest.main()
