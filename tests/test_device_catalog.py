import json
import tempfile
import unittest
from pathlib import Path

from darwing60.device_catalog import (
    compatibility_matrix,
    list_devices,
    load_device,
    validate_catalogue,
)


class DeviceCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.device = self.root / "sample"
        self.device.mkdir()
        (self.device / "device.json").write_text(
            json.dumps({"device": {"marketing_name": "Sample Phone"}}),
            encoding="utf-8",
        )
        (self.device / "compatibility.json").write_text(
            json.dumps({
                "device_codename": "sample",
                "components": [{
                    "name": "Wi-Fi",
                    "status": "not_implemented",
                    "darwing60_implementation": "None",
                }],
            }),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_lists_only_complete_profiles(self):
        (self.root / "incomplete").mkdir()
        self.assertEqual(list_devices(self.root), ["sample"])

    def test_loads_device_and_compatibility(self):
        record = load_device(self.root, "sample")
        self.assertEqual(record["codename"], "sample")
        self.assertEqual(record["device"]["device"]["marketing_name"], "Sample Phone")

    def test_matrix_flattens_components(self):
        record = load_device(self.root, "sample")
        self.assertEqual(compatibility_matrix(record)[0]["component"], "Wi-Fi")

    def test_catalogue_validates(self):
        self.assertEqual(validate_catalogue(self.root), [])

    def test_mismatched_codename_is_rejected(self):
        path = self.device / "compatibility.json"
        path.write_text(json.dumps({"device_codename": "other"}), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_device(self.root, "sample")

    def test_invalid_status_is_reported(self):
        path = self.device / "compatibility.json"
        path.write_text(json.dumps({
            "device_codename": "sample",
            "components": [{"name": "Wi-Fi", "status": "working-ish"}],
        }), encoding="utf-8")
        self.assertTrue(validate_catalogue(self.root))


if __name__ == "__main__":
    unittest.main()
