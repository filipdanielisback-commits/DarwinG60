"""Tests for the metadata-only scene compositor."""
import unittest

from darwing60.display_touch import TouchFrame, TouchPoint
from darwing60.display_touch_profile import load_display_touch_profile
from darwing60.display_events import DisplayEventPipeline
from darwing60.compositor import CompositorError, Rect, SceneComposer, Surface


def make_scene():
    profile = load_display_touch_profile()
    pipeline = DisplayEventPipeline(profile.subsystem)
    surfaces = [
        Surface("background", "Desktop", Rect(0, 0, 800, 600), 0, "background"),
        Surface("status", "Status bar", Rect(0, 0, 800, 40), 10, "status_bar"),
        Surface("window", "Settings", Rect(100, 100, 300, 250), 20, "window"),
        Surface("overlay", "Quick panel", Rect(600, 40, 190, 300), 30, "overlay"),
    ]
    return pipeline, SceneComposer(800, 600, surfaces, pipeline)


class SceneComposerTests(unittest.TestCase):
    def test_composes_surfaces_in_z_order(self):
        _, scene = make_scene()
        snapshot = scene.compose()
        self.assertEqual(
            [item.surface_id for item in snapshot.ordered_surfaces],
            ["background", "status", "window", "overlay"],
        )
        self.assertTrue(snapshot.synthetic)
        self.assertEqual(snapshot.frame_sequence, 1)

    def test_touch_selects_topmost_surface(self):
        pipeline, scene = make_scene()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.8, 0.2),)))
        self.assertEqual(scene.selected_surface_id, "overlay")
        pipeline.submit_touch(TouchFrame(2, (TouchPoint(0, 0.2, 0.3),)))
        self.assertEqual(scene.selected_surface_id, "window")

    def test_touch_on_status_bar_selects_status_surface(self):
        pipeline, scene = make_scene()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.5, 0.02),)))
        self.assertEqual(scene.selected_surface_id, "status")

    def test_touch_on_empty_area_selects_nothing(self):
        pipeline, scene = make_scene()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.5, 0.9),)))
        self.assertIsNone(scene.selected_surface_id)

    def test_hidden_surface_is_not_composed_or_hit(self):
        pipeline, scene = make_scene()
        scene.set_visibility("overlay", False)
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.8, 0.2),)))
        self.assertIsNone(scene.selected_surface_id)
        self.assertNotIn("overlay", [s.surface_id for s in scene.compose().ordered_surfaces])

    def test_remove_selected_surface_clears_selection(self):
        pipeline, scene = make_scene()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.2, 0.3),)))
        self.assertTrue(scene.remove_surface("window"))
        self.assertIsNone(scene.selected_surface_id)

    def test_rejects_duplicate_surface_id(self):
        _, scene = make_scene()
        with self.assertRaises(CompositorError):
            scene.add_surface(Surface("window", "Duplicate", Rect(0, 0, 10, 10), 50))

    def test_rejects_surface_outside_canvas(self):
        with self.assertRaises(CompositorError):
            SceneComposer(100, 100, [Surface("bad", "Bad", Rect(90, 90, 20, 20), 1)])

    def test_rejects_invalid_canvas_dimensions(self):
        with self.assertRaises(CompositorError):
            SceneComposer(0, 100)

    def test_close_unsubscribes_from_pipeline(self):
        pipeline, scene = make_scene()
        scene.close()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.2, 0.3),)))
        self.assertIsNone(scene.selected_surface_id)


if __name__ == "__main__":
    unittest.main()
