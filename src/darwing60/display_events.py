"""Deterministic host-side event pipeline for synthetic display/touch data.

Events are dispatched synchronously in-process. This module has no hardware,
thread, timer, framebuffer, or operating-system device integration.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from darwing60.display_touch import (
    DisplayError,
    DisplayMode,
    DisplayTouchSubsystem,
    PixelTouchPoint,
    Rotation,
    TouchFrame,
)


class DisplayEventError(ValueError):
    """Invalid event, timestamp, rotation, or subscription operation."""


class DisplayEventKind(str, Enum):
    MODE_CHANGED = "mode_changed"
    ROTATION_CHANGED = "rotation_changed"
    TOUCH_INPUT = "touch_input"
    FRAME_METADATA = "frame_metadata"


@dataclass(frozen=True)
class DisplayEvent:
    sequence: int
    timestamp_ms: int
    kind: DisplayEventKind
    mode: DisplayMode
    rotation: Rotation
    touch_points: tuple[PixelTouchPoint, ...] = ()
    frame_sequence: int | None = None


EventHandler = Callable[[DisplayEvent], None]


class DisplayEventPipeline:
    """Synchronous event dispatcher over a synthetic display/touch subsystem.

    The global event sequence orders all event types. Timestamps must be
    non-decreasing across the complete pipeline, not just touch input.
    Subscribers receive immutable event snapshots in subscription order.
    """

    def __init__(self, subsystem: DisplayTouchSubsystem):
        if not isinstance(subsystem, DisplayTouchSubsystem):
            raise DisplayEventError("A DisplayTouchSubsystem instance is required.")
        self.subsystem = subsystem
        self._sequence = 0
        self._last_timestamp_ms = -1
        self._next_subscription = 1
        self._subscribers: dict[int, EventHandler] = {}

    @property
    def last_sequence(self) -> int:
        return self._sequence

    def subscribe(self, handler: EventHandler) -> int:
        """Register a callback and return its subscription token."""
        if not callable(handler):
            raise DisplayEventError("Event handler must be callable.")
        token = self._next_subscription
        self._next_subscription += 1
        self._subscribers[token] = handler
        return token

    def unsubscribe(self, token: int) -> bool:
        """Remove a callback; return False when the token is not registered."""
        return self._subscribers.pop(token, None) is not None

    def _validate_timestamp(self, timestamp_ms: int) -> None:
        if isinstance(timestamp_ms, bool) or not isinstance(timestamp_ms, int):
            raise DisplayEventError("Event timestamp must be an integer.")
        if timestamp_ms < 0:
            raise DisplayEventError("Event timestamp cannot be negative.")
        if timestamp_ms < self._last_timestamp_ms:
            raise DisplayEventError("Pipeline timestamps must be monotonic.")

    def _emit(
        self,
        timestamp_ms: int,
        kind: DisplayEventKind,
        *,
        touch_points: tuple[PixelTouchPoint, ...] = (),
        frame_sequence: int | None = None,
    ) -> DisplayEvent:
        self._sequence += 1
        event = DisplayEvent(
            sequence=self._sequence,
            timestamp_ms=timestamp_ms,
            kind=kind,
            mode=self.subsystem.current_mode,
            rotation=self.subsystem.rotation,
            touch_points=touch_points,
            frame_sequence=frame_sequence,
        )
        self._last_timestamp_ms = timestamp_ms
        for handler in tuple(self._subscribers.values()):
            handler(event)
        return event

    def change_mode(self, name: str, timestamp_ms: int) -> DisplayEvent:
        self._validate_timestamp(timestamp_ms)
        try:
            self.subsystem.set_mode(name)
        except DisplayError as exc:
            raise DisplayEventError(str(exc)) from exc
        return self._emit(timestamp_ms, DisplayEventKind.MODE_CHANGED)

    def change_rotation(
        self, rotation: Rotation, timestamp_ms: int
    ) -> DisplayEvent:
        self._validate_timestamp(timestamp_ms)
        if not isinstance(rotation, Rotation):
            raise DisplayEventError("Rotation must be a supported Rotation value.")
        self.subsystem.rotation = rotation
        return self._emit(timestamp_ms, DisplayEventKind.ROTATION_CHANGED)

    def submit_touch(self, frame: TouchFrame) -> DisplayEvent:
        if not isinstance(frame, TouchFrame):
            raise DisplayEventError("Touch input must be a TouchFrame.")
        self._validate_timestamp(frame.timestamp_ms)
        try:
            points = self.subsystem.transform_touch_frame(frame)
        except DisplayError as exc:
            raise DisplayEventError(str(exc)) from exc
        return self._emit(
            frame.timestamp_ms,
            DisplayEventKind.TOUCH_INPUT,
            touch_points=points,
        )

    def present_frame(self, timestamp_ms: int) -> DisplayEvent:
        self._validate_timestamp(timestamp_ms)
        frame = self.subsystem.present_metadata_frame()
        return self._emit(
            timestamp_ms,
            DisplayEventKind.FRAME_METADATA,
            frame_sequence=frame.sequence,
        )
