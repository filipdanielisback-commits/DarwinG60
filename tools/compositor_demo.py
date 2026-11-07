"""Demonstrate metadata-only scene composition and synthetic touch selection."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from darwing60.compositor import Rect, SceneComposer, Surface  # noqa: E402
from darwing60.display_events import DisplayEventPipeline  # noqa: E402
from darwing60.display_touch import TouchFrame, TouchPoint  # noqa: E402
from darwing60.display_touch_profile import load_display_touch_profile  # noqa: E402


def main() -> int:
    profile = load_display_touch_profile()
    pipeline = DisplayEventPipeline(profile.subsystem)
    scene = SceneComposer(800, 600, [
        Surface("background", "Desktop", Rect(0, 0, 800, 600), 0, "background"),
        Surface("status", "Status bar", Rect(0, 0, 800, 40), 10, "status_bar"),
        Surface("settings", "Settings", Rect(100, 100, 300, 250), 20, "window"),
        Surface("quick-panel", "Quick panel", Rect(600, 40, 190, 300), 30, "overlay"),
    ], pipeline)
    print("Synthetic scene:")
    for item in scene.compose().ordered_surfaces:
        print(f"  z={item.z_index:>2} {item.role}: {item.title} ({item.bounds})")
    pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.2, 0.3),)))
    print(f"Selected by synthetic touch: {scene.selected_surface_id}")
    print("Metadata layout only; no pixels rendered and no hardware accessed.")
    scene.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
