import json
import tempfile
import unittest
from pathlib import Path

from darwing60.driver_registry import (
    DRIVER_CATEGORIES, build_registry, load_registry, render_registry,
    validate_registry,
)


class DriverRegistryTests(unittest.TestCase):
    def test_template_contains_all_seven_categories(self):
        data = build_registry("hanoip")
        self.assertEqual(len(data["drivers"]), 7)
        self.assertEqual(
            {item["id"] for item in data["drivers"]},
            {item["id"] for item in DRIVER_CATEGORIES},
        )

    def test_template_is_valid_and_metadata_only(self):
        data = build_registry("hanoip")
        self.assertEqual(validate_registry(data), [])
        self.assertIn("no driver implementation", data["scope"].lower())

    def test_invalid_status_is_reported(self):
        data = build_registry("hanoip")
        data["drivers"][0]["status"] = "working"
        self.assertTrue(any("invalid status" in error for error in validate_registry(data)))

    def test_missing_category_is_reported(self):
        data = build_registry("hanoip")
        data["drivers"].pop()
        self.assertTrue(any("Missing driver categories" in error for error in validate_registry(data)))

    def test_duplicate_id_is_reported(self):
        data = build_registry("hanoip")
        data["drivers"][1]["id"] = data["drivers"][0]["id"]
        self.assertTrue(any("Duplicate driver id" in error for error in validate_registry(data)))

    def test_load_and_render(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "drivers.json"
            path.write_text(json.dumps(build_registry("hanoip")), encoding="utf-8")
            data = load_registry(path)
        report = render_registry(data)
        self.assertIn("Display and touchscreen", report)
        self.assertIn("Storage", report)
        self.assertIn("Planning metadata only", report)

    def test_invalid_codename_rejected(self):
        with self.assertRaises(ValueError):
            build_registry("../other")


if __name__ == "__main__":
    unittest.main()
