import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.bootmenu import ENTRIES, describe_selection, find_entry


class BootMenuTests(unittest.TestCase):
    def test_menu_has_three_entries(self):
        self.assertEqual(len(ENTRIES), 3)

    def test_known_entry_is_found(self):
        self.assertEqual(find_entry("1").title, "Darwin / XNU research")

    def test_unknown_entry_is_rejected(self):
        self.assertIsNone(find_entry("9"))
        self.assertIn("Invalid selection", describe_selection("9"))

    def test_darwin_selection_does_not_claim_to_boot(self):
        result = describe_selection("1")
        self.assertIn("research target only", result)
        self.assertIn("no boot operation", result)

    def test_android_selection_does_not_modify_device(self):
        result = describe_selection("2")
        self.assertIn("does not interact with the phone", result)


if __name__ == "__main__":
    unittest.main()
