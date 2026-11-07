"""Run a small deterministic system-shell state demonstration."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.display_events import DisplayEventPipeline  # noqa: E402
from darwing60.display_touch import TouchFrame, TouchPoint  # noqa: E402
from darwing60.display_touch_profile import load_display_touch_profile  # noqa: E402
from darwing60.shell import Notification, SystemShell  # noqa: E402


def main() -> int:
    profile = load_display_touch_profile()
    pipeline = DisplayEventPipeline(profile.subsystem)
    shell = SystemShell(pipeline)
    shell.set_demo_battery(86)
    shell.set_quick_setting("wifi", True)
    shell.add_notification(Notification("demo-1", "DarwinG60", "System shell prototype is running"))
    print("DarwinG60 synthetic home screen")
    print(f"  Clock: {shell.status_bar.clock}")
    print(f"  Demo battery: {shell.status_bar.battery_percent}% (not read from hardware)")
    print(f"  Wi-Fi toggle: {'on' if shell.status_bar.wifi_enabled else 'off'} (simulated)")
    print(f"  Notifications: {shell.status_bar.notifications_count}")
    shell.open_quick_settings()
    print(f"  Quick Settings open: {shell.snapshot().quick_settings_open}")
    pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.16, 0.9),)))
    print(f"  App selected from home: {shell.snapshot().active_app}")
    print("State model only; no pixels rendered, radios accessed, or apps executed.")
    shell.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
