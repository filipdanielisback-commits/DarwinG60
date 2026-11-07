"""Tests for the simulated host-side system shell."""
import unittest

from darwing60.display_touch import TouchFrame, TouchPoint
from darwing60.display_touch_profile import load_display_touch_profile
from darwing60.display_events import DisplayEventPipeline
from darwing60.shell import Notification, ShellError, SystemShell


def make_shell():
    profile = load_display_touch_profile()
    pipeline = DisplayEventPipeline(profile.subsystem)
    return pipeline, SystemShell(pipeline)


class SystemShellTests(unittest.TestCase):
    def test_initial_home_and_status_state(self):
        _, shell = make_shell()
        state = shell.snapshot()
        self.assertEqual(state.home_apps, ("settings", "files", "about"))
        self.assertEqual(state.status_bar.clock, "09:41")
        self.assertIsNone(state.status_bar.battery_percent)
        self.assertFalse(state.quick_settings_open)

    def test_status_bar_touch_opens_quick_settings(self):
        pipeline, shell = make_shell()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.5, 0.02),)))
        self.assertTrue(shell.snapshot().quick_settings_open)

    def test_quick_settings_toggle_is_simulated_state(self):
        _, shell = make_shell()
        self.assertTrue(shell.toggle_quick_setting("wifi"))
        self.assertTrue(shell.status_bar.wifi_enabled)
        self.assertFalse(shell.toggle_quick_setting("wifi"))

    def test_notifications_update_status_count(self):
        _, shell = make_shell()
        shell.add_notification(Notification("n1", "Welcome", "DarwinG60 shell demo"))
        self.assertEqual(shell.status_bar.notifications_count, 1)
        self.assertTrue(shell.dismiss_notification("n1"))
        self.assertEqual(shell.status_bar.notifications_count, 0)

    def test_duplicate_notification_is_rejected(self):
        _, shell = make_shell()
        item = Notification("n1", "Title", "Message")
        shell.add_notification(item)
        with self.assertRaises(ShellError):
            shell.add_notification(item)

    def test_panels_are_mutually_exclusive(self):
        _, shell = make_shell()
        shell.open_quick_settings()
        shell.open_notifications()
        state = shell.snapshot()
        self.assertFalse(state.quick_settings_open)
        self.assertTrue(state.notifications_open)

    def test_launch_home_app_and_return_home(self):
        _, shell = make_shell()
        shell.launch_app("settings")
        self.assertEqual(shell.snapshot().active_app, "settings")
        shell.return_home()
        self.assertIsNone(shell.snapshot().active_app)

    def test_touch_on_home_app_launches_it(self):
        pipeline, shell = make_shell()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.16, 0.9),)))
        self.assertEqual(shell.snapshot().active_app, "settings")

    def test_invalid_clock_and_battery_are_rejected(self):
        _, shell = make_shell()
        with self.assertRaises(ShellError):
            shell.set_clock("25:99")
        with self.assertRaises(ShellError):
            shell.set_demo_battery(140)

    def test_unknown_toggle_and_app_are_rejected(self):
        _, shell = make_shell()
        with self.assertRaises(ShellError):
            shell.toggle_quick_setting("cellular")
        with self.assertRaises(ShellError):
            shell.launch_app("unknown")

    def test_close_unsubscribes(self):
        pipeline, shell = make_shell()
        shell.close()
        pipeline.submit_touch(TouchFrame(1, (TouchPoint(0, 0.5, 0.02),)))
        self.assertFalse(shell.snapshot().quick_settings_open)


if __name__ == "__main__":
    unittest.main()
