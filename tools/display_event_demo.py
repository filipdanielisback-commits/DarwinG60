"""Demonstrate the synthetic display event flow on the host."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.display_touch import Rotation, TouchFrame, TouchPoint  # noqa: E402
from darwing60.display_touch_profile import load_display_touch_profile  # noqa: E402
from darwing60.display_events import DisplayEventPipeline  # noqa: E402


def main() -> int:
    profile = load_display_touch_profile()
    pipeline = DisplayEventPipeline(profile.subsystem)

    def show(event):
        details = (
            f"mode={event.mode.name} rotation={event.rotation.value}"
        )
        if event.touch_points:
            point = event.touch_points[0]
            details += f" touch=({point.x},{point.y})"
        if event.frame_sequence is not None:
            details += f" frame={event.frame_sequence}"
        print(
            f"#{event.sequence} t={event.timestamp_ms}ms "
            f"{event.kind.value}: {details}"
        )

    pipeline.subscribe(show)
    pipeline.change_mode("test-low-refresh", 10)
    pipeline.change_rotation(Rotation.DEG_90, 11)
    pipeline.submit_touch(TouchFrame(12, (TouchPoint(0, 0.25, 0.5),)))
    pipeline.present_frame(13)
    print("Synthetic host-side demonstration only; no hardware was accessed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
