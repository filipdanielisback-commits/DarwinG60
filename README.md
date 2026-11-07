# DarwinG60

**Experimental ARM64 Darwin/XNU research for the Motorola Moto G60 (device codename: `hanoip`).**

DarwinG60 is an exploratory, open-source research project. Its long-term goal is to investigate what would be required to bring parts of the Darwin/XNU ecosystem to the Moto G60 platform. At this stage, it is a documentation and research project—not a working iOS port, not a bootable Darwin image, and not a replacement for Android.

> [!WARNING]
> No Darwin/XNU build, EFI loader, device driver set, or bootable image is currently provided by this repository. Do not flash experimental files or assume that an image is safe for your phone. Early development will focus on source research, emulation, documentation, and non-destructive testing.

## Project status

<badge>Research / pre-alpha</badge>

- [x] Repository and project scope established
- [ ] Verify device hardware and boot-chain documentation
- [ ] Set up a reproducible research/build environment
- [ ] Investigate ARM64 Darwin/XNU boot requirements
- [ ] Prototype components in an emulator before device experiments
- [ ] Document Moto G60-specific hardware gaps
- [ ] Evaluate whether any safe, meaningful device-side prototype is feasible

Nothing in the unchecked list should be interpreted as implemented.

## Goals

- Study the ARM64 Darwin/XNU boot process and its platform assumptions.
- Document the Moto G60 (`hanoip`) hardware and existing open-source device support.
- Explore boot-chain and EFI concepts in a controlled, reversible development environment.
- Keep Android preservation and recovery considerations central to any future device research.
- Publish reproducible notes, source changes, and test results.

## Non-goals and limitations

- This project does **not** contain or distribute Apple's proprietary iOS components.
- It does **not** claim to run iOS 18 or any version of iOS on the Moto G60.
- It does **not** promise that XNU can be made to boot on this device.
- It does **not** provide instructions or images for bypassing device security or performing risky flashing.
- A menu, kernel build, or image file alone would not demonstrate working hardware support.

Darwin/XNU is not the same thing as the complete iOS operating system. iOS also depends on proprietary frameworks, services, drivers, signing, and hardware integration that are outside this repository's scope.

## Device target

| Item | Value |
|---|---|
| Device | Motorola Moto G60 |
| Device codename | `hanoip` |
| CPU architecture | ARM64 (to be confirmed against reliable device documentation) |
| Project phase | Research and feasibility |
| Current bootable release | None |

Hardware details will be added only after they are checked against reliable documentation or measured and recorded.

## Repository layout

```text
DarwinG60/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── ROADMAP.md
├── SECURITY.md
└── docs/
    ├── architecture.md
    ├── boot-process.md
    └── compatibility.md
```

## Getting involved

Start with [CONTRIBUTING.md](CONTRIBUTING.md), then review the [roadmap](ROADMAP.md) and the documents in [docs/](docs/). Research notes should include links to primary sources and clearly distinguish confirmed facts from hypotheses.

## Licensing

Original project code and documentation are offered under the MIT License in [LICENSE](LICENSE). This license does not apply to third-party code, trademarks, firmware, or proprietary components. Any future third-party source imports must retain their original licenses and notices.

Apple, iOS, and Darwin are trademarks or products of their respective owners. This is an independent community research project and is not affiliated with or endorsed by Apple or Motorola.
