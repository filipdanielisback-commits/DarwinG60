import unittest
from darwing60.display_touch import (
    DisplayError, DisplayMode, DisplayTouchSubsystem, PanelProfile,
    Rotation, TouchFrame, TouchPoint,
)


def fixture(rotation=Rotation.DEG_0):
    panel = PanelProfile(
        "Synthetic test panel (not Moto G60 hardware)",
        (DisplayMode(800, 600, 60, "test-60hz"),
         DisplayMode(800, 600, 30, "test-low-refresh")),
        "test-60hz",
    )
    return DisplayTouchSubsystem(panel, rotation)


class DisplayTouchTests(unittest.TestCase):
    def test_initial_mode(self):
        self.assertEqual(fixture().current_mode.name, "test-60hz")

    def test_mode_switch(self):
        self.assertEqual(fixture().set_mode("test-low-refresh").refresh_hz, 30)

    def test_unknown_mode_rejected(self):
        with self.assertRaises(DisplayError):
            fixture().set_mode("unknown")

    def test_frame_metadata_sequence(self):
        sub = fixture()
        self.assertEqual(sub.present_metadata_frame().sequence, 1)
        self.assertEqual(sub.present_metadata_frame().sequence, 2)

    def test_touch_to_pixels(self):
        p = fixture().transform_touch_frame(
            TouchFrame(10, (TouchPoint(0, 1.0, 0.5),))
        )[0]
        self.assertEqual((p.x, p.y), (799, 300))

    def test_rotation_90(self):
        p = fixture(Rotation.DEG_90).transform_touch_frame(
            TouchFrame(10, (TouchPoint(0, 0.0, 0.0),))
        )[0]
        self.assertEqual((p.x, p.y), (599, 0))

    def test_monotonic_timestamps(self):
        sub = fixture()
        sub.transform_touch_frame(TouchFrame(20, ()))
        with self.assertRaises(DisplayError):
            sub.transform_touch_frame(TouchFrame(19, ()))

    def test_duplicate_pointer_ids(self):
        with self.assertRaises(DisplayError):
            TouchFrame(1, (TouchPoint(1, .2, .3), TouchPoint(1, .4, .5)))

    def test_invalid_coordinates(self):
        with self.assertRaises(DisplayError):
            TouchPoint(0, 1.2, .5)

    def test_real_profile_rejected(self):
        with self.assertRaises(DisplayError):
            PanelProfile("claimed panel", (DisplayMode(1,1,60,"m"),), "m", synthetic=False)

    def test_hardware_id_rejected(self):
        with self.assertRaises(DisplayError):
            PanelProfile("test", (DisplayMode(1,1,60,"m"),), "m",
                         hardware_identifier="unverified-id")


if __name__ == "__main__":
    unittest.main()
