# Device profile sources

These references support the descriptive hardware profile. Community device trees are useful evidence for the codename and platform family, but are not treated as official Motorola specifications.

## References

1. Motorola specifications spreadsheet/PDF: https://p1-ofp.static.pub/MOTO/Columbia/Motorola_Informacion_fichas_tecnicas_2024.99ff3703fd4516c1.pdf
   - Lists Moto G60 with Snapdragon 732G, Android 11, memory/storage configurations and 6000 mAh battery.
2. Moto G60 specification overview: https://www.phonearena.com/phones/Motorola-Moto-G60_id11684
   - Cross-check for display, processor and graphics specifications.
3. Community device tree for Moto G40 Fusion/Moto G60: https://github.com/bhawesh2002/android_device_motorola_hanoip
   - Identifies the shared device family and the hanoip codename; includes a community-maintained specification summary.
4. Community device-tree organization: https://github.com/moto-hanoip
   - Describes its repositories as device sources for Moto G40 Fusion and Moto G60.

## Confidence and limitations

- **Codename:** hanoip is supported by multiple community device-tree references.
- **SoC marketing name and GPU:** Snapdragon 732G and Adreno 618 are consistently listed in the references above.
- **Exact SoC silicon identifier, board revision, memory map, boot chain, interrupt controller details and panel controller:** not asserted by this profile. These require stronger primary evidence.
- **Regional variants:** RAM, storage and model numbers may differ. The profile lists common configurations, not the exact configuration of every handset.

References are provided for research context. DarwinG60 does not include or claim ownership of third-party device-tree code.
