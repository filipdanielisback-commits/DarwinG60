"""Tests for synthetic display/touch profile integration."""
import json
import tempfile
import unittest
from pathlib import Path

from darwing60.display_touch_profile import (
    DisplayProfileError, load_display_touch_profile,
)


class DisplayTouchProfileTests(unittest.TestCase):
    def test_loads_synthetic_fixture_and_evidence(self):
        profile = load_display_touch_profile()
        self.assertTrue(profile.is_synthetic)
        self.assertEqual(profile.device_label, "synthetic-test-fixture")
        self.assertEqual(profile.subsystem.current_mode.name, "test-60hz")
        self.assertGreaterEqual(len(profile.evidence), 1)

    def test_report_keeps_touch_identity_unresolved(self):
        report = load_display_touch_profile().build_report()
        self.assertIn("No physical hardware was detected", report)
        self.assertIn("Physical touchscreen controller identity", report)
        self.assertIn("[unresolved/unknown]", report)

    def test_mode_switch_uses_loaded_fixture(self):
        profile = load_display_touch_profile()
        mode = profile.subsystem.set_mode("test-low-refresh")
        self.assertEqual(mode.refresh_hz, 30)

    def test_rejects_fixture_not_marked_synthetic(self):
        source = Path(__file__).resolve().parents[1] / "examples" / "display-touch-synthetic.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["synthetic"] = False
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(DisplayProfileError):
                load_display_touch_profile(path)

    def test_rejects_hardware_identifier(self):
        source = Path(__file__).resolve().parents[1] / "examples" / "display-touch-synthetic.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["panel"]["hardware_identifier"] = "unverified-panel"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(DisplayProfileError):
                load_display_touch_profile(path)

    def test_rejects_touch_controller_guess(self):
        source = Path(__file__).resolve().parents[1] / "examples" / "display-touch-synthetic.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["touch"]["controller_identifier"] = "guessed-controller"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(DisplayProfileError):
                load_display_touch_profile(path)


if __name__ == "__main__":
    unittest.main()
