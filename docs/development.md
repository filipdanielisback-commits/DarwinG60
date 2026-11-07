# Development guide

DarwinG60 can be developed from a phone using GitHub's web interface or a
mobile Git client. A computer is not required for editing documentation or
reviewing source, although compiling and testing some future components may
need a suitable development environment.

## Current host-side demo

The menu concept is a Python program. If a Python 3 environment is available,
run:

```sh
python3 tools/menu_demo.py
```

Run the tests with:

```sh
python3 -m unittest discover -s tests -v
```

The demo is only a simulation. It cannot boot either operating system and
does not connect to or modify a phone.

## Contributing from a phone

1. Open a file in the repository.
2. Use GitHub's edit function to make a focused change.
3. Preview the Markdown where possible.
4. Commit with a message describing the change.
5. Keep technical claims linked to sources and mark unknowns clearly.
