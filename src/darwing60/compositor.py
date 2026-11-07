"""Host-side scene/layout compositor model; no pixels or scanout are produced."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from darwing60.display_events import DisplayEvent, DisplayEventKind, DisplayEventPipeline


class CompositorError(ValueError):
    """Invalid scene, surface geometry, or composition operation."""


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        if any(isinstance(value, bool) or not isinstance(value, int)
               for value in (self.x, self.y, self.width, self.height)):
            raise CompositorError("Rectangle values must be integers.")
        if self.x < 0 or self.y < 0 or self.width <= 0 or self.height <= 0:
            raise CompositorError("Rectangle origin must be non-negative and size positive.")

    def contains(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


@dataclass(frozen=True)
class Surface:
    surface_id: str
    title: str
    bounds: Rect
    z_index: int
    role: str = "window"
    visible: bool = True

    def __post_init__(self):
        if not self.surface_id.strip() or not self.title.strip():
            raise CompositorError("Surface ID and title cannot be empty.")
        if self.role not in {"background", "status_bar", "window", "overlay"}:
            raise CompositorError(f"Unsupported surface role: {self.role}")
        if isinstance(self.z_index, bool) or not isinstance(self.z_index, int):
            raise CompositorError("z_index must be an integer.")


@dataclass(frozen=True)
class CompositorSnapshot:
    width: int
    height: int
    ordered_surfaces: tuple[Surface, ...]
    selected_surface_id: str | None
    frame_sequence: int
    synthetic: bool = True


class SceneComposer:
    """Compose ordered rectangular UI surfaces into metadata snapshots.

    This is layout and hit-testing only: no rasterization, GPU calls, pixels,
    framebuffer, display server, or physical input are involved.
    """

    def __init__(
        self,
        width: int,
        height: int,
        surfaces: Iterable[Surface] = (),
        pipeline: DisplayEventPipeline | None = None,
    ):
        if any(isinstance(value, bool) or not isinstance(value, int) or value <= 0
               for value in (width, height)):
            raise CompositorError("Canvas dimensions must be positive integers.")
        self.width = width
        self.height = height
        self._surfaces: dict[str, Surface] = {}
        self._selected_surface_id: str | None = None
        self._frame_sequence = 0
        self._pipeline = pipeline
        self._subscription: int | None = None
        for surface in surfaces:
            self.add_surface(surface)
        if pipeline is not None:
            self._subscription = pipeline.subscribe(self.handle_event)

    @property
    def selected_surface_id(self) -> str | None:
        return self._selected_surface_id

    def _validate_bounds(self, surface: Surface) -> None:
        rect = surface.bounds
        if rect.x + rect.width > self.width or rect.y + rect.height > self.height:
            raise CompositorError(f"Surface {surface.surface_id!r} exceeds the canvas.")

    def add_surface(self, surface: Surface) -> None:
        if not isinstance(surface, Surface):
            raise CompositorError("Only Surface instances can be added.")
        if surface.surface_id in self._surfaces:
            raise CompositorError(f"Duplicate surface ID: {surface.surface_id}")
        self._validate_bounds(surface)
        self._surfaces[surface.surface_id] = surface

    def remove_surface(self, surface_id: str) -> bool:
        removed = self._surfaces.pop(surface_id, None) is not None
        if self._selected_surface_id == surface_id:
            self._selected_surface_id = None
        return removed

    def set_visibility(self, surface_id: str, visible: bool) -> None:
        if surface_id not in self._surfaces:
            raise CompositorError(f"Unknown surface ID: {surface_id}")
        if not isinstance(visible, bool):
            raise CompositorError("visible must be a boolean.")
        current = self._surfaces[surface_id]
        self._surfaces[surface_id] = Surface(
            current.surface_id, current.title, current.bounds,
            current.z_index, current.role, visible,
        )
        if not visible and self._selected_surface_id == surface_id:
            self._selected_surface_id = None

    def hit_test(self, x: int, y: int) -> str | None:
        if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, int) or not isinstance(y, int):
            raise CompositorError("Hit-test coordinates must be integers.")
        candidates = sorted(
            (item for item in self._surfaces.values()
             if item.visible and item.bounds.contains(x, y)),
            key=lambda item: item.z_index,
            reverse=True,
        )
        return candidates[0].surface_id if candidates else None

    def handle_event(self, event: DisplayEvent) -> None:
        if event.kind == DisplayEventKind.TOUCH_INPUT:
            if event.mode.width != self.width or event.mode.height != self.height:
                return
            if event.touch_points:
                point = event.touch_points[0]
                self._selected_surface_id = self.hit_test(point.x, point.y)

    def compose(self) -> CompositorSnapshot:
        self._frame_sequence += 1
        ordered = tuple(sorted(
            (item for item in self._surfaces.values() if item.visible),
            key=lambda item: item.z_index,
        ))
        return CompositorSnapshot(
            width=self.width,
            height=self.height,
            ordered_surfaces=ordered,
            selected_surface_id=self._selected_surface_id,
            frame_sequence=self._frame_sequence,
        )

    def close(self) -> None:
        if self._pipeline is not None and self._subscription is not None:
            self._pipeline.unsubscribe(self._subscription)
            self._subscription = None
