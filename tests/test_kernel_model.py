import unittest

from darwing60.kernel_model import (
    SUBSYSTEMS,
    KernelSubsystem,
    SubsystemStatus,
    subsystem_report,
    validate_subsystems,
)


class KernelModelTests(unittest.TestCase):
    def test_catalogue_has_expected_foundation_areas(self):
        names = {item.name for item in SUBSYSTEMS}
        self.assertTrue({"scheduler", "memory-manager", "ipc", "vfs"} <= names)

    def test_all_current_entries_are_not_claimed_as_real_kernel(self):
        self.assertTrue(
            all(item.status == SubsystemStatus.PLANNED for item in SUBSYSTEMS)
        )

    def test_catalogue_validates(self):
        self.assertEqual(validate_subsystems(), [])

    def test_unknown_dependency_is_reported(self):
        sample = (
            KernelSubsystem(
                "example", "Example subsystem.", SubsystemStatus.PLANNED,
                ("missing",),
            ),
        )
        self.assertTrue(any("unknown subsystem" in error for error in validate_subsystems(sample)))

    def test_report_is_explicit_about_host_side_status(self):
        self.assertIn("host-side catalogue", subsystem_report())
        self.assertIn("No kernel code is running", subsystem_report())


if __name__ == "__main__":
    unittest.main()
