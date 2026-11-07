# Synthetic shell SVG renderer

The renderer converts a `ShellSnapshot` and its synthetic compositor snapshot
into a self-contained SVG image using only Python's standard library.

## Generate a preview

From the repository root:

```bash
python tools/render_shell.py
```

The output is written to `build/darwing60-shell-demo.svg`. Open that SVG in
a browser or vector-image viewer. The generated preview is deterministic and
uses a distinct DarwinG60 visual direction: dark slate surfaces, teal accents,
and project-specific labels.

## Scope and limitations

- Draws the host-side shell snapshot into actual SVG vector graphics.
- Includes the wallpaper, status bar, app tiles, simulated app view, quick
  controls, and notification cards.
- Escapes notification text before inserting it into SVG markup.
- Uses no external fonts, images, scripts, network requests, or third-party
  packages.
- Does not render pixels through a GPU, create a framebuffer, drive a panel,
  read real time/battery/radio state, execute applications, or communicate
  with Moto G60 hardware.
- The preview is a development artifact, not a bootable operating system.

The renderer deliberately uses DarwinG60-specific visual styling rather than
reproducing Apple's iOS interface.
