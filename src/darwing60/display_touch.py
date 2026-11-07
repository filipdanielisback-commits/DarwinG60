"""Synthetic display/touch interfaces for host-side DarwinG60 research.

No display hardware, touch controller, framebuffer, bus, or device is accessed.
All profiles are explicitly supplied test metadata.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class DisplayError(ValueError):
    """Invalid display profile, mode, or touch event."""


class Rotation(int, Enum):
    DEG_0 = 0
    DEG_90 = 90
    DEG_180 = 180
    DEG_270 = 270


@dataclass(frozen=True)
class DisplayMode:
    width: int
    height: int
    refresh_hz: float
    name: str = "synthetic"

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0 or self.refresh_hz <= 0:
            raise DisplayError("Dimensions and refresh rate must be positive.")
        if not self.name.strip():
            raise DisplayError("Mode name cannot be empty.")


@dataclass(frozen=True)
class PanelProfile:
    name: str
    modes: tuple[DisplayMode, ...]
    preferred_mode: str
    synthetic: bool = True
    hardware_identifier: str | None = None

    def __post_init__(self):
        if not self.name.strip() or not self.synthetic:
            raise DisplayError("Only named synthetic panel profiles are accepted.")
        if not self.modes:
            raise DisplayError("At least one mode is required.")
        names = [mode.name for mode in self.modes]
        if len(names) != len(set(names)) or self.preferred_mode not in names:
            raise DisplayError("Mode names must be unique and preferred mode must exist.")
        if self.hardware_identifier is not None:
            raise DisplayError("Unverified hardware identifiers are not accepted.")

    def mode(self, name: str | None = None) -> DisplayMode:
        selected = name or self.preferred_mode
        for mode in self.modes:
            if mode.name == selected:
                return mode
        raise DisplayError(f"Unknown display mode: {selected}")


@dataclass(frozen=True)
class TouchPoint:
    pointer_id: int
    x: float
    y: float
    pressure: float = 1.0

    def __post_init__(self):
        if self.pointer_id < 0:
            raise DisplayError("Pointer ID cannot be negative.")
        if not 0 <= self.x <= 1 or not 0 <= self.y <= 1:
            raise DisplayError("Touch coordinates must be normalized to [0, 1].")
        if not 0 <= self.pressure <= 1:
            raise DisplayError("Pressure must be normalized to [0, 1].")


@dataclass(frozen=True)
class TouchFrame:
    timestamp_ms: int
    points: tuple[TouchPoint, ...]

    def __post_init__(self):
        if self.timestamp_ms < 0:
            raise DisplayError("Timestamp cannot be negative.")
        ids = [point.pointer_id for point in self.points]
        if len(ids) != len(set(ids)):
            raise DisplayError("Pointer IDs must be unique within a frame.")


@dataclass(frozen=True)
class PixelTouchPoint:
    pointer_id: int
    x: int
    y: int
    pressure: float


@dataclass(frozen=True)
class DisplayFrame:
    mode: DisplayMode
    sequence: int
    source: str = "synthetic-frame-metadata"

    @property
    def pixel_count(self):
        return self.mode.width * self.mode.height


class DisplayTouchSubsystem:
    """Metadata model only; never discovers or communicates with hardware."""

    def __init__(self, panel: PanelProfile, rotation: Rotation = Rotation.DEG_0):
        self.panel = panel
        self.rotation = rotation
        self._mode = panel.mode()
        self._frame_sequence = 0
        self._last_touch_timestamp = -1

    @property
    def current_mode(self):
        return self._mode

    def set_mode(self, name: str) -> DisplayMode:
        self._mode = self.panel.mode(name)
        return self._mode

    def present_metadata_frame(self) -> DisplayFrame:
        """Advance a counter only; no pixels are rendered or scanned out."""
        self._frame_sequence += 1
        return DisplayFrame(self._mode, self._frame_sequence)

    def transform_touch_frame(self, frame: TouchFrame) -> tuple[PixelTouchPoint, ...]:
        if frame.timestamp_ms < self._last_touch_timestamp:
            raise DisplayError("Touch timestamps must be monotonic.")
        self._last_touch_timestamp = frame.timestamp_ms
        width, height = self._mode.width, self._mode.height
        result = []
        for point in frame.points:
            x, y = point.x, point.y
            if self.rotation == Rotation.DEG_90:
                x, y, out_w, out_h = 1-y, x, height, width
            elif self.rotation == Rotation.DEG_180:
                x, y, out_w, out_h = 1-x, 1-y, width, height
            elif self.rotation == Rotation.DEG_270:
                x, y, out_w, out_h = y, 1-x, height, width
            else:
                out_w, out_h = width, height
            px = min(out_w-1, max(0, round(x*(out_w-1))))
            py = min(out_h-1, max(0, round(y*(out_h-1))))
            result.append(PixelTouchPoint(point.pointer_id, px, py, point.pressure))
        return tuple(result)
