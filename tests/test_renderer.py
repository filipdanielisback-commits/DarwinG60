"""Tests for the self-contained synthetic shell SVG renderer."""
from __future__ import annotations

import unittest
import xml.etree.ElementTree as ET

from darwing60.display_events import DisplayEventPipeline
from darwing60.display_touch_profile import load_display_touch_profile
from darwing60.renderer import RenderError, render_shell_svg
from darwing60.shell import Notification, SystemShell


class RendererTests(unittest.TestCase):
    def setUp(self):
        profile = load_display_touch_profile()
        self.pipeline = DisplayEventPipeline(profile.subsystem)
        self.shell = SystemShell(self.pipeline)
        self.shell.set_clock("10:24")
        self.shell.set_demo_battery(86)
        self.shell.set_quick_setting("wifi", True)
        self.shell.add_notification(Notification(
            "preview-1", "DarwinG60", "Your host-side preview is ready"
        ))

    def tearDown(self):
        self.shell.close()

    def test_renders_valid_standalone_svg(self):
        svg = render_shell_svg(self.shell.snapshot())
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(root.attrib["width"], "800")
        self.assertIn("DARWING60", svg)
        self.assertIn("10:24", svg)
        self.assertIn("Battery demo: 86%", svg)
        self.assertIn("NOT DEVICE OUTPUT", svg)

    def test_renders_quick_settings_state(self):
        self.shell.open_quick_settings()
        svg = render_shell_svg(self.shell.snapshot())
        self.assertIn("Quick controls", svg)
        self.assertIn("Wi-Fi", svg)
        self.assertIn(">ON</text>", svg)

    def test_renders_notifications(self):
        self.shell.open_notifications()
        svg = render_shell_svg(self.shell.snapshot())
        self.assertIn("Notifications", svg)
        self.assertIn("Your host-side preview is ready", svg)

    def test_escapes_untrusted_notification_text(self):
        self.shell.add_notification(Notification("xss-safe", "<script>", "A & B"))
        self.shell.open_notifications()
        svg = render_shell_svg(self.shell.snapshot())
        self.assertIn("&lt;script&gt;", svg)
        self.assertIn("A &amp; B", svg)
        ET.fromstring(svg)

    def test_renders_selected_app_as_simulated_view(self):
        self.shell.launch_app("settings")
        svg = render_shell_svg(self.shell.snapshot())
        self.assertIn("Settings", svg)
        self.assertIn("No application process is launched.", svg)

    def test_rejects_non_shell_input(self):
        with self.assertRaises(RenderError):
            render_shell_svg(object())


if __name__ == "__main__":
    unittest.main()
