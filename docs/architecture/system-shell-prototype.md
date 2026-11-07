# Host-side system shell prototype

## Scope

The system shell is a deterministic state model layered over the synthetic
scene compositor. It models a home screen, status bar, Quick Settings,
notifications, and a small app-launch list.

## Features

- Status bar clock, optional demo battery percentage, Wi-Fi/Bluetooth flags,
  and notification count.
- Quick Settings toggles for Wi-Fi, Bluetooth, and Do Not Disturb.
- Mutually exclusive Quick Settings and notifications panels.
- Add/dismiss notification records.
- Home-screen app shortcuts and active-app state.
- Synthetic touch on the status bar opens Quick Settings; touching a home
  shortcut selects that app.
- Immutable shell snapshots for inspection and tests.

## Important limitations

Every indicator and toggle is simulated state. No system clock is read
automatically, no battery or radio hardware is queried, no networking occurs,
and no applications are launched as operating-system processes. The shell
does not render pixels or communicate with a display. The default 800x600
canvas is a synthetic development fixture, not a Moto G60 panel mode.

## Run

    python tools/shell_demo.py

## Tests

    python -m unittest discover -s tests -v
