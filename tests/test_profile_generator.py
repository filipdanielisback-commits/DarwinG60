import json
import tempfile
import unittest
from pathlib import Path

from darwing60.profile_generator import (
    build_templates,
    generate_profile,
    validate_identity,
)


class ProfileGeneratorTests(unittest.TestCase):
    def test_template_keeps_unknown_hardware_values_unknown(self):
        templates = build_templates("sample", "Example", "Example Phone")
        device = json.loads(templates["device.json"])
        self.assertIsNone(device["platform"]["soc_marketing_name"])
        self.assertIsNone(device["battery"]["capacity_mah_typical"])
        self.assertEqual(device["research_status"]["kernel_ported"], False)

    def test_compatibility_starts_as_research_only(self):
        templates = build_templates("sample", "Example", "Example Phone")
        compatibility = json.loads(templates["compatibility.json"])
        self.assertEqual(compatibility["overall_status"], "research_only")
        self.assertTrue(
            all(item["status"] == "unknown" for item in compatibility["components"])
        )

    def test_invalid_codename_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_identity("../bad", "Example", "Example Phone")

    def test_empty_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_identity("sample", "", "Example Phone")

    def test_creates_four_starter_files(self):
        with tempfile.TemporaryDirectory() as temp:
            target = generate_profile(Path(temp), "sample", "Example", "Example Phone")
            self.assertEqual(
                {path.name for path in target.iterdir()},
                {"device.json", "compatibility.json", "sources.md", "README.md"},
            )

    def test_existing_profile_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "sample"
            target.mkdir()
            marker = target / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                generate_profile(root, "sample", "Example", "Example Phone")
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
