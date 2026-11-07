import unittest

from darwing60.services import ServiceRegistry, ServiceState


class ServiceRegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = ServiceRegistry()

    def test_register_service(self):
        service = self.registry.register("network", "Future networking service")
        self.assertEqual(service.state, ServiceState.REGISTERED)

    def test_duplicate_registration_is_rejected(self):
        self.registry.register("network", "Networking")
        with self.assertRaises(ValueError):
            self.registry.register("network", "Duplicate")

    def test_state_can_be_updated(self):
        self.registry.register("display", "Future display service")
        service = self.registry.set_state("display", ServiceState.RUNNING)
        self.assertEqual(service.state, ServiceState.RUNNING)

    def test_unknown_service_is_rejected(self):
        with self.assertRaises(KeyError):
            self.registry.set_state("missing", ServiceState.RUNNING)

    def test_listing_is_sorted(self):
        self.registry.register("wifi", "Future Wi-Fi service")
        self.registry.register("audio", "Future audio service")
        self.assertEqual(
            [item.name for item in self.registry.list_services()],
            ["audio", "wifi"],
        )


if __name__ == "__main__":
    unittest.main()
