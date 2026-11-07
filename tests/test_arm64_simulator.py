import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.arm64_simulator import (
    ARM64BootSimulator,
    MemoryRegion,
    validate_memory_map,
)


class ARM64SimulatorTests(unittest.TestCase):
    def test_startup_sequence_is_simulated(self):
        stages = ARM64BootSimulator().run()
        self.assertEqual(stages[0].name, "reset")
        self.assertEqual(stages[-1].name, "userspace")
        self.assertTrue(all(stage.status == "SIMULATED" for stage in stages))

    def test_report_discloses_simulation(self):
        report = ARM64BootSimulator().report()
        self.assertIn("HOST-SIDE SIMULATION ONLY", report)
        self.assertIn("No firmware", report)

    def test_non_overlapping_memory_map(self):
        regions = [
            MemoryRegion("A", 0x1000, 0x100, "example"),
            MemoryRegion("B", 0x2000, 0x100, "example"),
        ]
        self.assertEqual(validate_memory_map(regions), [])

    def test_overlapping_memory_map_is_rejected(self):
        regions = [
            MemoryRegion("A", 0x1000, 0x300, "example"),
            MemoryRegion("B", 0x1200, 0x100, "example"),
        ]
        self.assertTrue(validate_memory_map(regions))


if __name__ == "__main__":
    unittest.main()
