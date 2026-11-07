import unittest

from darwing60.driver_framework import (
    DeviceDescriptor, DriverDescriptor, DriverManager, DriverState,
)


class DriverFrameworkTests(unittest.TestCase):
    def setUp(self):
        self.manager = DriverManager()
        self.driver = DriverDescriptor(
            name="example-i2c-sensor",
            buses=("i2c",),
            vendor_device_ids=(("vendor-a", "sensor-1"),),
            compatibles=("example,sensor-v1",),
        )
        self.manager.register(self.driver)

    def test_matches_by_vendor_and_device_id(self):
        device = DeviceDescriptor(
            name="fixture sensor", bus="i2c",
            vendor_id="vendor-a", device_id="sensor-1",
        )
        self.assertEqual(self.manager.find_matches(device), (self.driver,))

    def test_matches_by_compatible(self):
        device = DeviceDescriptor(
            name="fixture sensor", bus="i2c",
            compatible=("example,sensor-v1",),
        )
        self.assertEqual(self.manager.find_matches(device), (self.driver,))

    def test_wrong_bus_does_not_match(self):
        device = DeviceDescriptor(
            name="fixture sensor", bus="spi",
            compatible=("example,sensor-v1",),
        )
        self.assertEqual(self.manager.find_matches(device), ())

    def test_simulated_bind_is_explicit(self):
        device = DeviceDescriptor(
            name="fixture sensor", bus="i2c",
            compatible=("example,sensor-v1",),
        )
        binding = self.manager.simulate_bind(device, self.driver.name)
        self.assertEqual(binding.state, DriverState.BOUND_SIMULATED)
        self.assertIn("no hardware was accessed", binding.notes[0])

    def test_bind_rejects_non_matching_device(self):
        device = DeviceDescriptor(name="other", bus="spi")
        with self.assertRaises(ValueError):
            self.manager.simulate_bind(device, self.driver.name)

    def test_duplicate_driver_registration_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.register(self.driver)

    def test_empty_identity_rejected(self):
        with self.assertRaises(ValueError):
            DeviceDescriptor(name="", bus="i2c")


if __name__ == "__main__":
    unittest.main()
