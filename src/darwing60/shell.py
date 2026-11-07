"""Host-side system shell state model built on the synthetic scene compositor."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from darwing60.compositor import Rect, SceneComposer, Surface
from darwing60.display_events import DisplayEvent, DisplayEventKind, DisplayEventPipeline


class ShellError(ValueError):
    """Invalid shell state or operation."""


@dataclass(frozen=True)
class StatusBarState:
    clock: str
    battery_percent: int | None
    wifi_enabled: bool
    bluetooth_enabled: bool
    notifications_count: int

    def __post_init__(self):
        try:
            parsed = datetime.strptime(self.clock, "%H:%M")
        except (TypeError, ValueError) as exc:
            raise ShellError("Clock must use 24-hour HH:MM format.") from exc
        if parsed.strftime("%H:%M") != self.clock:
            raise ShellError("Clock must use zero-padded HH:MM format.")
        if self.battery_percent is not None and (
            isinstance(self.battery_percent, bool)
            or not isinstance(self.battery_percent, int)
            or not 0 <= self.battery_percent <= 100
        ):
            raise ShellError("Battery percentage must be an integer from 0 to 100.")
        if not isinstance(self.wifi_enabled, bool) or not isinstance(self.bluetooth_enabled, bool):
            raise ShellError("Connectivity indicators must be booleans.")
        if isinstance(self.notifications_count, bool) or not isinstance(self.notifications_count, int) or self.notifications_count < 0:
            raise ShellError("Notification count cannot be negative.")


@dataclass(frozen=True)
class Notification:
    notification_id: str
    title: str
    message: str

    def __post_init__(self):
        if not self.notification_id.strip() or not self.title.strip() or not self.message.strip():
            raise ShellError("Notification ID, title, and message are required.")


@dataclass(frozen=True)
class ShellSnapshot:
    status_bar: StatusBarState
    quick_settings_open: bool
    notifications_open: bool
    quick_settings: tuple[tuple[str, bool], ...]
    notifications: tuple[Notification, ...]
    home_apps: tuple[str, ...]
    active_app: str | None
    scene: object
    synthetic: bool = True


class SystemShell:
    """A deterministic shell model; indicators and controls are simulated values."""

    def __init__(
        self,
        pipeline: DisplayEventPipeline,
        *,
        width: int = 800,
        height: int = 600,
        home_apps: Iterable[str] = ("settings", "files", "about"),
    ):
        if not isinstance(pipeline, DisplayEventPipeline):
            raise ShellError("A DisplayEventPipeline is required.")
        if width <= 0 or height <= 0:
            raise ShellError("Shell dimensions must be positive.")
        if pipeline.subsystem.current_mode.width != width or pipeline.subsystem.current_mode.height != height:
            raise ShellError("Shell dimensions must match the active synthetic display mode.")
        apps = tuple(home_apps)
        if not apps or any(not isinstance(app, str) or not app.strip() for app in apps):
            raise ShellError("At least one named home app is required.")
        if len(apps) != len(set(apps)):
            raise ShellError("Home app identifiers must be unique.")
        self.pipeline = pipeline
        self.width = width
        self.height = height
        self._clock = "09:41"
        self._battery_percent: int | None = None
        self._toggles = {"wifi": False, "bluetooth": False, "do_not_disturb": False}
        self._quick_settings_open = False
        self._notifications_open = False
        self._notifications: list[Notification] = []
        self._home_apps = apps
        self._active_app: str | None = None
        surfaces = [
            Surface("desktop-background", "Home background", Rect(0, 0, width, height), 0, "background"),
            Surface("status-bar", "Status bar", Rect(0, 0, width, 42), 10, "status_bar"),
            Surface("home-screen", "Home screen", Rect(0, 42, width, height - 42), 5, "window"),
        ]
        slot_width = width // len(apps)
        for index, app in enumerate(apps):
            x = index * slot_width
            item_width = slot_width if index < len(apps) - 1 else width - x
            surfaces.append(Surface(f"app:{app}", app.title(), Rect(x, max(42, height - 110), item_width, 90), 20, "window"))
        surfaces.extend([
            Surface("quick-settings-panel", "Quick Settings", Rect(width - min(360, width), 42, min(360, width), min(360, height - 42)), 50, "overlay", False),
            Surface("notifications-panel", "Notifications", Rect(0, 42, width, min(420, height - 42)), 60, "overlay", False),
        ])
        self.compositor = SceneComposer(width, height, surfaces, pipeline)
        self._subscription = pipeline.subscribe(self._on_event)

    @property
    def status_bar(self) -> StatusBarState:
        return StatusBarState(
            self._clock,
            self._battery_percent,
            self._toggles["wifi"],
            self._toggles["bluetooth"],
            len(self._notifications),
        )

    def set_clock(self, value: str) -> None:
        self._clock = StatusBarState(value, self._battery_percent, self._toggles["wifi"], self._toggles["bluetooth"], len(self._notifications)).clock

    def set_demo_battery(self, percent: int | None) -> None:
        # Explicitly demo-only: no battery device is queried.
        StatusBarState(self._clock, percent, self._toggles["wifi"], self._toggles["bluetooth"], len(self._notifications))
        self._battery_percent = percent

    def set_quick_setting(self, name: str, enabled: bool) -> None:
        if name not in self._toggles:
            raise ShellError(f"Unknown quick setting: {name}")
        if not isinstance(enabled, bool):
            raise ShellError("Quick-setting value must be a boolean.")
        self._toggles[name] = enabled

    def toggle_quick_setting(self, name: str) -> bool:
        if name not in self._toggles:
            raise ShellError(f"Unknown quick setting: {name}")
        self._toggles[name] = not self._toggles[name]
        return self._toggles[name]

    def open_quick_settings(self) -> None:
        self._quick_settings_open = True
        self._notifications_open = False
        self.compositor.set_visibility("notifications-panel", False)
        self.compositor.set_visibility("quick-settings-panel", True)

    def close_quick_settings(self) -> None:
        self._quick_settings_open = False
        self.compositor.set_visibility("quick-settings-panel", False)

    def open_notifications(self) -> None:
        self._notifications_open = True
        self._quick_settings_open = False
        self.compositor.set_visibility("quick-settings-panel", False)
        self.compositor.set_visibility("notifications-panel", True)

    def close_notifications(self) -> None:
        self._notifications_open = False
        self.compositor.set_visibility("notifications-panel", False)

    def add_notification(self, notification: Notification) -> None:
        if not isinstance(notification, Notification):
            raise ShellError("Expected a Notification instance.")
        if any(item.notification_id == notification.notification_id for item in self._notifications):
            raise ShellError(f"Duplicate notification ID: {notification.notification_id}")
        self._notifications.append(notification)

    def dismiss_notification(self, notification_id: str) -> bool:
        for index, item in enumerate(self._notifications):
            if item.notification_id == notification_id:
                del self._notifications[index]
                return True
        return False

    def launch_app(self, app_id: str) -> None:
        if app_id not in self._home_apps:
            raise ShellError(f"App is not on the home screen: {app_id}")
        self._active_app = app_id
        self.close_quick_settings()
        self.close_notifications()

    def return_home(self) -> None:
        self._active_app = None
        self.close_quick_settings()
        self.close_notifications()

    def _on_event(self, event: DisplayEvent) -> None:
        if event.kind != DisplayEventKind.TOUCH_INPUT:
            return
        selected = self.compositor.selected_surface_id
        if selected == "status-bar":
            self.open_quick_settings()
        elif selected and selected.startswith("app:"):
            self.launch_app(selected.split(":", 1)[1])

    def snapshot(self) -> ShellSnapshot:
        return ShellSnapshot(
            status_bar=self.status_bar,
            quick_settings_open=self._quick_settings_open,
            notifications_open=self._notifications_open,
            quick_settings=tuple(sorted(self._toggles.items())),
            notifications=tuple(self._notifications),
            home_apps=self._home_apps,
            active_app=self._active_app,
            scene=self.compositor.compose(),
        )

    def close(self) -> None:
        self.pipeline.unsubscribe(self._subscription)
        self.compositor.close()
