#!/usr/bin/env python3
"""Run the DarwinG60 boot-menu concept as a harmless terminal demo."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.bootmenu import ENTRIES, describe_selection  # noqa: E402


def main() -> None:
    print("DarwinG60 — Boot Menu Concept (SIMULATION)")
    print("=" * 46)
    for entry in ENTRIES:
        print(f"{entry.key}. {entry.title}")
        print(f"   {entry.description}")
        print(f"   Status: {entry.status.value}")
    print("\nThis is a menu mock-up, not a real bootloader.")
    choice = input("\nChoose an item (or q to quit): ").strip().lower()
    if choice == "q":
        print("Exiting simulator. No device action was performed.")
        return
    print("\n" + describe_selection(choice))


if __name__ == "__main__":
    main()
