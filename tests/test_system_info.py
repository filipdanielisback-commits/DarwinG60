import json
import unittest

from darwing60.system_info import build_system_info, render_dashboard, to_json


class SystemInfoTests(unittest.TestCase):
    def test_report_contains_device_and_mode(self):
        data = build_system_info()
        self.assertEqual(data["device"]["codename"], "hanoip")
        self.assertEqual(data["mode"], "HOST-SIDE RESEARCH ONLY")

    def test_startup_stages_are_explicitly_simulated(self):
        data = build_system_info()
        self.assertTrue(data["simulated_startup"])
        self.assertTrue(all(
            stage["status"] == "SIMULATED"
            for stage in data["simulated_startup"]
        ))

    def test_dashboard_is_readable_and_discloses_limits(self):
        dashboard = render_dashboard(build_system_info())
        self.assertIn("DARWING60 SYSTEM INFO", dashboard)
        self.assertIn("no phone communication", dashboard.lower())
        self.assertIn("Boot image: False", dashboard)

    def test_json_is_valid(self):
        data = build_system_info()
        parsed = json.loads(to_json(data))
        self.assertEqual(parsed["project"], "DarwinG60")

    def test_metadata_validation_is_reported(self):
        data = build_system_info()
        self.assertIsInstance(data["validation_errors"], list)


if __name__ == "__main__":
    unittest.main()
