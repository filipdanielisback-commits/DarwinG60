# Service architecture

DarwinG60 will need system services for networking, power, display, audio,
storage, and other platform functions.

The current `src/darwing60/services.py` module is a host-side registry model.
It can register named service records and update their lifecycle labels in a
Python process. It does not create background daemons, communicate with device
hardware, or provide working Wi-Fi, battery, or display functionality.

A future implementation will need:
- explicit service interfaces and dependency rules;
- controlled startup and shutdown;
- logging and failure reporting;
- permissions and isolation boundaries;
- integration tests on supported hardware.

Do not interpret a service record marked RUNNING in a local test as a real
phone service.
