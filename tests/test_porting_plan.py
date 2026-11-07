import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from darwing60 import porting_plan


class PortingPlanTests(unittest.TestCase):
    def test_lists_device_directories_with_profiles(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "hanoip").mkdir()
            (root / "hanoip" / "device.json").write_text("{}", encoding="utf-8")
            (root / "empty").mkdir()
            with patch.object(porting_plan, "DEVICE_ROOT", root):
                self.assertEqual(
                    [name for name, _ in porting_plan.device_profiles()],
                    ["hanoip"],
                )

    def test_loads_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "test-device"
            folder.mkdir()
            (folder / "device.json").write_text(
                json.dumps({"codename": "test-device"}), encoding="utf-8"
            )
            with patch.object(porting_plan, "DEVICE_ROOT", root):
                self.assertEqual(
                    porting_plan.load_profile("test-device")["codename"],
                    "test-device",
                )

    def test_missing_profile_raises(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(porting_plan, "DEVICE_ROOT", Path(temp)):
                with self.assertRaises(FileNotFoundError):
                    porting_plan.load_profile("unknown")

    def test_check_profiles_accepts_valid_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "hanoip"
            folder.mkdir()
            (folder / "device.json").write_text("{}", encoding="utf-8")
            with patch.object(porting_plan, "DEVICE_ROOT", root):
                self.assertEqual(porting_plan.check_profiles(), [])


if __name__ == "__main__":
    unittest.main()
