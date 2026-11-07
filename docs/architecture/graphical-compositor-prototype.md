# Host-side graphical compositor prototype

## Purpose

The scene composer models a simple desktop layout using rectangular surfaces:
background, status bar, windows, and overlays. It consumes synthetic touch
events from the display event pipeline to select the topmost visible surface.

## Capabilities

- Validates canvas and surface bounds.
- Maintains unique surface identifiers and visibility.
- Orders visible surfaces by z-index.
- Performs topmost-surface hit testing.
- Updates selected surface from the first point in a synthetic touch event.
- Produces immutable metadata snapshots with a frame sequence.

## Limitations

This is not a pixel renderer or graphical desktop. It does not draw text,
rasterize surfaces, allocate framebuffers, call a GPU, animate, manage windows
as processes, or communicate with display hardware. It accepts only the
synthetic event pipeline. The example canvas is 800x600 and is not Moto G60
panel configuration.

## Run

    python tools/compositor_demo.py

## Tests

    python -m unittest discover -s tests -v
