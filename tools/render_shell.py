"""Generate a viewable SVG preview of the synthetic DarwinG60 shell."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.display_events import DisplayEventPipeline  # noqa: E402
from darwing60.display_touch_profile import load_display_touch_profile  # noqa: E402
from darwing60.renderer import render_shell_svg  # noqa: E402
from darwing60.shell import Notification, SystemShell  # noqa: E402


def main() -> int:
    output = ROOT / "build" / "darwing60-shell-demo.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    profile = load_display_touch_profile()
    pipeline = DisplayEventPipeline(profile.subsystem)
    shell = SystemShell(pipeline)
    try:
        shell.set_clock("10:24")
        shell.set_demo_battery(86)
        shell.set_quick_setting("wifi", True)
        shell.set_quick_setting("bluetooth", True)
        shell.add_notification(Notification(
            "preview-1", "DarwinG60", "The independent shell preview is ready"
        ))
        shell.open_quick_settings()
        output.write_text(render_shell_svg(shell.snapshot()), encoding="utf-8")
    finally:
        shell.close()
    print(f"Generated synthetic SVG preview: {output.relative_to(ROOT)}")
    print("This is a host-rendered image, not a bootable OS or device display.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
