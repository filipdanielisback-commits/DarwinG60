# DarwinG60 roadmap

This roadmap describes research stages, not promised delivery dates. Items move to complete only when evidence and notes are committed.

## Stage 0 — Project foundation

- [x] Establish repository, scope, and licensing for original work.
- [x] Document current limitations and project status.
- [ ] Add a source bibliography for the device and relevant upstream projects.

## Stage 1 — Platform research

- [ ] Verify Moto G60 hardware details from reliable sources.
- [ ] Map the documented Android boot chain at a high level.
- [ ] Identify the platform assumptions made by the relevant ARM64 XNU source.
- [ ] Record licensing and provenance for every external source used.

## Stage 2 — Controlled experiments

- [ ] Set up a reproducible host-side development environment.
- [ ] Study relevant boot concepts using emulation or other non-device experiments.
- [ ] Create small, independently testable research prototypes.
- [ ] Record logs, limitations, and exact source revisions for each experiment.

## Stage 3 — Feasibility assessment

- [ ] Compare required platform support with documented Moto G60 hardware.
- [ ] Identify missing drivers, firmware interfaces, and platform integration.
- [ ] Publish a clear feasibility report before considering device-side work.

## Stage 4 — Only if justified by evidence

- [ ] Define a narrowly scoped prototype and its recovery requirements.
- [ ] Review safety, data-loss, licensing, and device-support risks.
- [ ] Publish artifacts only after reproducible tests and clear compatibility notes.

## Release policy

There are currently no official bootable releases. A release must state exactly what it contains, what was tested, what is unsupported, and whether it is intended for emulation or hardware. Never label an untested file as a bootable Moto G60 image.
