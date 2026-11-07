"""Host-side model of a future DarwinG60 service manager.

This registry only tracks Python objects and lifecycle labels in this process.
It does not start operating-system daemons or interact with the phone.
"""
from dataclasses import dataclass
from enum import Enum


class ServiceState(str, Enum):
    REGISTERED = "registered"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class ServiceRecord:
    name: str
    description: str
    state: ServiceState = ServiceState.REGISTERED


class ServiceRegistry:
    def __init__(self) -> None:
        self._services: dict[str, ServiceRecord] = {}

    def register(self, name: str, description: str) -> ServiceRecord:
        if not name.strip():
            raise ValueError("Service name cannot be empty.")
        if name in self._services:
            raise ValueError(f"Service already registered: {name}")
        record = ServiceRecord(name=name, description=description)
        self._services[name] = record
        return record

    def set_state(self, name: str, state: ServiceState) -> ServiceRecord:
        try:
            record = self._services[name]
        except KeyError as exc:
            raise KeyError(f"Unknown service: {name}") from exc
        record.state = state
        return record

    def get(self, name: str) -> ServiceRecord:
        return self._services[name]

    def list_services(self) -> tuple[ServiceRecord, ...]:
        return tuple(self._services[name] for name in sorted(self._services))
