"""Deterministic SVG renderer for synthetic DarwinG60 shell snapshots.

This creates a host-viewable image from shell metadata. It is not a display
driver, framebuffer, GPU renderer, or device UI runtime.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

from darwing60.compositor import CompositorSnapshot
from darwing60.shell import ShellSnapshot


class RenderError(ValueError):
    """Invalid input supplied to the synthetic SVG renderer."""


def _text(x: int, y: int, value: str, *, size: int = 14, color: str = "#e8f0f2",
          weight: int = 400) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" font-family="Inter, ui-sans-serif, sans-serif">'
        f'{escape(value)}</text>'
    )


def _rounded_rect(x: int, y: int, width: int, height: int, fill: str,
                  radius: int = 14, stroke: str | None = None) -> str:
    border = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}"{border}/>'
    )


def render_shell_svg(snapshot: ShellSnapshot) -> str:
    """Return a self-contained SVG image for a synthetic shell snapshot."""
    if not isinstance(snapshot, ShellSnapshot) or snapshot.synthetic is not True:
        raise RenderError("Only explicitly synthetic ShellSnapshot values can be rendered.")
    scene = snapshot.scene
    if not isinstance(scene, CompositorSnapshot) or scene.synthetic is not True:
        raise RenderError("A synthetic compositor snapshot is required.")
    width, height = scene.width, scene.height
    if width < 320 or height < 240:
        raise RenderError("Canvas must be at least 320 by 240 pixels.")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">DarwinG60 synthetic desktop</title>',
        '<desc id="desc">A host-rendered preview of the independent DarwinG60 shell prototype. '
        'All controls and indicators are simulated.</desc>',
        '<defs><linearGradient id="wallpaper" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#102c35"/><stop offset="1" stop-color="#17202d"/>'
        '</linearGradient></defs>',
        _rounded_rect(0, 0, width, height, "url(#wallpaper)", 0),
    ]

    visible_ids = {surface.surface_id for surface in scene.ordered_surfaces}
    if "home-screen" in visible_ids:
        parts.append(_text(28, 100, "DARWING60", size=12, color="#75d5c3", weight=700))
        parts.append(_text(28, 137, "A system of our own.", size=28, weight=650))
        parts.append(_text(28, 164, "Independent OS research • synthetic host preview",
                          size=12, color="#a9bdc3"))

    if snapshot.active_app:
        parts.append(_rounded_rect(18, 62, width - 36, height - 82, "#1d3039", 18, "#35515a"))
        parts.append(_text(38, 102, snapshot.active_app.title(), size=23, weight=650))
        parts.append(_text(38, 132, "Application selection is simulated in this prototype.",
                          size=13, color="#b5c7ca"))
        parts.append(_text(38, 164, "No application process is launched.", size=12, color="#8fa8ad"))

    if "status-bar" in visible_ids:
        parts.append(_rounded_rect(0, 0, width, 42, "#0b171e", 0))
        status = snapshot.status_bar
        parts.append(_text(18, 27, status.clock, size=14, weight=650))
        indicators = []
        if status.wifi_enabled:
            indicators.append("Wi-Fi demo: ON")
        if status.bluetooth_enabled:
            indicators.append("Bluetooth demo: ON")
        if status.battery_percent is not None:
            indicators.append(f"Battery demo: {status.battery_percent}%")
        if status.notifications_count:
            indicators.append(f"Alerts: {status.notifications_count}")
        parts.append(_text(width - 18, 27, "  •  ".join(indicators) if indicators else
                           "RADIO / BATTERY NOT CONNECTED", size=10, color="#b5c7ca"))
        parts.append(_text(18, height - 14, "DARWING60 • HOST PREVIEW • NOT DEVICE OUTPUT",
                           size=9, color="#8fa8ad"))

    app_count = len(snapshot.home_apps)
    if app_count and "home-screen" in visible_ids and snapshot.active_app is None:
        gap = 14
        available = width - 48 - gap * (app_count - 1)
        tile_width = max(72, available // app_count)
        total = tile_width * app_count + gap * (app_count - 1)
        start_x = (width - total) // 2
        tile_y = height - 112
        for index, app in enumerate(snapshot.home_apps):
            x = start_x + index * (tile_width + gap)
            parts.append(_rounded_rect(x, tile_y, tile_width, 76, "#24414a", 13, "#42616a"))
            parts.append(_rounded_rect(x + tile_width // 2 - 13, tile_y + 10, 26, 26,
                                       "#397d78", 8))
            parts.append(_text(x + tile_width // 2 - 7, tile_y + 29, app[:1].upper(),
                               size=14, weight=700))
            parts.append(_text(x + tile_width // 2, tile_y + 57, app.title(),
                               size=11, color="#e2eeee"))

    if "quick-settings-panel" in visible_ids and snapshot.quick_settings_open:
        panel_w = min(350, width - 28)
        x, y = width - panel_w - 14, 54
        parts.append(_rounded_rect(x, y, panel_w, min(330, height - 68), "#203943", 18, "#52717a"))
        parts.append(_text(x + 18, y + 30, "Quick controls", size=18, weight=650))
        for index, (name, enabled) in enumerate(snapshot.quick_settings):
            row_y = y + 58 + index * 48
            parts.append(_rounded_rect(x + 14, row_y, panel_w - 28, 38,
                                       "#356e68" if enabled else "#2b4650", 9))
            parts.append(_text(x + 26, row_y + 24, name.replace("_", " ").title(), size=12))
            parts.append(_text(x + panel_w - 48, row_y + 24,
                               "ON" if enabled else "OFF", size=10, color="#b8d6d2"))

    if "notifications-panel" in visible_ids and snapshot.notifications_open:
        panel_w = min(440, width - 28)
        x, y = 14, 54
        parts.append(_rounded_rect(x, y, panel_w, min(390, height - 68),
                                   "#203943", 18, "#52717a"))
        parts.append(_text(x + 18, y + 30, "Notifications", size=18, weight=650))
        if not snapshot.notifications:
            parts.append(_text(x + 18, y + 66, "You're all caught up.", size=13,
                               color="#b5c7ca"))
        for index, item in enumerate(snapshot.notifications[:5]):
            row_y = y + 48 + index * 62
            parts.append(_rounded_rect(x + 12, row_y, panel_w - 24, 54, "#2b4650", 9))
            parts.append(_text(x + 24, row_y + 21, item.title[:48], size=12, weight=650))
            parts.append(_text(x + 24, row_y + 41, item.message[:64], size=10,
                               color="#b5c7ca"))

    parts.append("</svg>")
    return "\n".join(parts) + "\n"
