# Boot-process research

## Scope

This document is a high-level study guide for understanding boot architecture. It does not provide device-modification or flashing instructions.

## Questions to investigate

- Which boot stages are documented for the Moto G60?
- What information is passed between stages?
- Which execution environment and image formats does the platform expect?
- What interfaces would a later kernel need?
- Which parts of the chain are vendor-specific or undocumented?
- How can hypotheses be tested in an emulator or source-level experiment first?

## Evidence standard

For each finding, record:

- the claim;
- the source URL and relevant revision or publication date;
- whether it is confirmed, inferred, or unknown;
- how it could be independently checked.

Do not assume that an EFI-style menu can replace or integrate with a phone's existing boot chain. That is a separate feasibility question requiring platform-specific evidence.
