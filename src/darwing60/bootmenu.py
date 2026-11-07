"""A safe, host-side model of a future DarwinG60 boot menu.

This is deliberately a simulator: selecting an entry reports its status. It
never starts a kernel, changes boot variables, writes storage, or reboots.
"""
from dataclasses import dataclass
from enum import Enum


class EntryStatus(str, Enum):
    RESEARCH = "research-only"
    NOT_IMPLEMENTED = "not-implemented"


@dataclass(frozen=True)
class MenuEntry:
    key: str
    title: str
    description: str
    status: EntryStatus


ENTRIES = (
    MenuEntry(
        "1",
        "Darwin / XNU research",
        "Future experimental path; no bootable kernel is available.",
        EntryStatus.RESEARCH,
    ),
    MenuEntry(
        "2",
        "Android",
        "Original device operating system; this simulator cannot launch it.",
        EntryStatus.NOT_IMPLEMENTED,
    ),
    MenuEntry(
        "3",
        "Project information",
        "Show project status and safety notes.",
        EntryStatus.RESEARCH,
    ),
)


def find_entry(key: str) -> MenuEntry | None:
    """Return a menu entry by key, or None for an unknown key."""
    return next((entry for entry in ENTRIES if entry.key == key), None)


def describe_selection(key: str) -> str:
    """Describe a selection without performing a boot action."""
    entry = find_entry(key)
    if entry is None:
        return "Invalid selection. Choose 1, 2, or 3."

    if key == "1":
        return (
            "Darwin/XNU is a research target only. No kernel is built here, "
            "and no boot operation was attempted."
        )
    if key == "2":
        return (
            "Android remains the device's existing OS. This host-side "
            "prototype does not interact with the phone or change its boot."
        )
    return (
        "DarwinG60 0.1.0-dev — research-only. No bootable release exists. "
        "This program runs on the host and does not modify a device."
    )
