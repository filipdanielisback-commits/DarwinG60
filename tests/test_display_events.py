"""Tests for the synchronous synthetic display event pipeline."""
import unittest

from darwing60.display_touch import Rotation, TouchFrame, TouchPoint
from darwing60.display_touch_profile import load_display_touch_profile
from darwing60.display_events import (
    DisplayEventError,
    DisplayEventKind,
    DisplayEventPipeline,
)


def pipeline():
    profile = load_display_touch_profile()
    return DisplayEventPipeline(profile.subsystem)


class DisplayEventPipelineTests(unittest.TestCase):
    def test_emits_ordered_mode_rotation_touch_and_frame_events(self):
        bus = pipeline()
        events = []
        bus.subscribe(events.append)

        bus.change_mode("test-low-refresh", 10)
        bus.change_rotation(Rotation.DEG_90, 11)
        touch = bus.submit_touch(
            TouchFrame(12, (TouchPoint(3, 0.0, 0.0),))
        )
        frame = bus.present_frame(13)

        self.assertEqual(
            [event.kind for event in events],
            [
                DisplayEventKind.MODE_CHANGED,
                DisplayEventKind.ROTATION_CHANGED,
                DisplayEventKind.TOUCH_INPUT,
                DisplayEventKind.FRAME_METADATA,
            ],
        )
        self.assertEqual([event.sequence for event in events], [1, 2, 3, 4])
        self.assertEqual(events[0].mode.name, "test-low-refresh")
        self.assertEqual(events[1].rotation, Rotation.DEG_90)
        self.assertEqual((touch.touch_points[0].x, touch.touch_points[0].y), (599, 0))
        self.assertEqual(frame.frame_sequence, 1)

    def test_touch_uses_current_mode_and_rotation(self):
        bus = pipeline()
        bus.change_mode("test-low-refresh", 1)
        bus.change_rotation(Rotation.DEG_180, 2)
        event = bus.submit_touch(
            TouchFrame(3, (TouchPoint(0, 0.0, 0.0),))
        )
        self.assertEqual((event.touch_points[0].x, event.touch_points[0].y), (799, 599))
        self.assertEqual(event.mode.name, "test-low-refresh")

    def test_timestamp_order_is_global(self):
        bus = pipeline()
        bus.present_frame(20)
        with self.assertRaises(DisplayEventError):
            bus.change_mode("test-low-refresh", 19)

    def test_invalid_timestamp_rejected_before_frame_counter_changes(self):
        bus = pipeline()
        with self.assertRaises(DisplayEventError):
            bus.present_frame(-1)
        self.assertEqual(bus.subsystem._frame_sequence, 0)

    def test_unknown_mode_does_not_emit_event(self):
        bus = pipeline()
        with self.assertRaises(DisplayEventError):
            bus.change_mode("not-a-mode", 1)
        self.assertEqual(bus.last_sequence, 0)

    def test_invalid_rotation_rejected(self):
        bus = pipeline()
        with self.assertRaises(DisplayEventError):
            bus.change_rotation(45, 1)
        self.assertEqual(bus.last_sequence, 0)

    def test_subscribe_and_unsubscribe(self):
        bus = pipeline()
        received = []
        token = bus.subscribe(received.append)
        self.assertTrue(bus.unsubscribe(token))
        self.assertFalse(bus.unsubscribe(token))
        bus.present_frame(1)
        self.assertEqual(received, [])

    def test_non_callable_subscriber_rejected(self):
        bus = pipeline()
        with self.assertRaises(DisplayEventError):
            bus.subscribe("not a callback")

    def test_rejects_non_touch_frame(self):
        bus = pipeline()
        with self.assertRaises(DisplayEventError):
            bus.submit_touch(None)


if __name__ == "__main__":
    unittest.main()
