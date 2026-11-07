# Host-side display event pipeline

## Purpose

The event pipeline connects the synthetic display/touch subsystem into one
ordered, deterministic event flow. It is an in-process host prototype, not an
OS input stack or physical device driver.

## Event types

- `mode_changed`: a synthetic display mode was selected.
- `rotation_changed`: the logical coordinate rotation changed.
- `touch_input`: normalized synthetic touch points were transformed into
  logical pixel coordinates using the active mode and rotation.
- `frame_metadata`: the existing metadata-only frame counter advanced.

Every event includes a global sequence number, monotonic timestamp, current
display mode, and current rotation. Touch and frame events also carry their
respective payload metadata.

## Dispatch model

Subscribers are called synchronously, in registration order. The pipeline
does not create threads, timers, queues, pixels, framebuffers, or hardware I/O.
Timestamps are non-decreasing across all event types. Subscription tokens can
be removed with `unsubscribe`.

## Run the demonstration

    python tools/display_event_demo.py

## Tests

    python -m unittest discover -s tests -v

All data is synthetic. This does not provide physical touch input, display
scanout, a compositor, a graphics API, or a bootable interface.
