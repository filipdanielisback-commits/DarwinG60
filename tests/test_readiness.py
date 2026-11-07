import json
import tempfile
import unittest
from pathlib import Path

from darwing60.readiness import assess_device, render_report


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        folder = self.root / "sample"
        folder.mkdir()
        (folder / "device.json").write_text(
            json.dumps({"device": {"codename": "sample"}}), encoding="utf-8"
        )
        (folder / "compatibility.json").write_text(
            json.dumps({
                "device_codename": "sample",
                "overall_status": "research_only",
                "components": [
                    {
                        "name": "ARM64 CPU execution environment",
                        "status": "documented",
                        "evidence": "Reference platform documentation.",
                        "darwing60_implementation": "None",
                    },
                    {
                        "name": "Wi-Fi and Bluetooth",
                        "status": "not_implemented",
                        "evidence": "No drivers exist.",
                        "darwing60_implementation": "None",
                    },
                ],
            }),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_assesses_all_six_areas(self):
        report = assess_device(self.root, "sample")
        self.assertEqual(
            [item["key"] for item in report["areas"]],
            ["cpu", "boot_firmware", "display_gpu", "wireless", "power", "kernel_graphics"],
        )

    def test_known_and_missing_components_are_distinguished(self):
        report = assess_device(self.root, "sample")
        by_key = {item["key"]: item for item in report["areas"]}
        self.assertEqual(by_key["cpu"]["status"], "documented")
        self.assertEqual(by_key["wireless"]["status"], "not_implemented")
        self.assertEqual(by_key["power"]["status"], "unknown")

    def test_report_disclaims_hardware_validation(self):
        report = assess_device(self.root, "sample")
        output = render_report(report)
        self.assertIn("Metadata assessment only", output)
        self.assertIn("Hardware readiness report", output)

    def test_missing_device_raises(self):
        with self.assertRaises(FileNotFoundError):
            assess_device(self.root, "missing")


if __name__ == "__main__":
    unittest.main()
