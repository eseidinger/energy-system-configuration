# Contract kit 0.5.0 release review

**Date:** 2026-10-17  
**Reviewer:** Sole cross-project maintainer, eseidinger  
**Scope:** VEF AI assistance implementation handoff  
**Outcome:** Authorized for publication as `contract-kit-v0.5.0`

The maintainer explicitly requested publication of the committed `0.5.0`
contract-kit update. This authorizes the additive VEF handoff and prerelease;
Gate 6 implementation acceptance and the final `1.0.0` release remain open.

## Reviewed scope

- Normative VEF AI profile covering request proposals, current-request user
  confirmation, bounded approved evidence, classified claims, and citations.
- Proposal and explanation schemas, examples, semantic citation validation,
  and eleven VEF workflow acceptance scenarios.
- ODIP publication APIs, energy schemas, numerical fixtures and oracles, and
  platform identity contracts remain unchanged.

## Verification and publication

All 82 kit tests pass locally. Repeated release builds produce identical bytes.
The archive SHA-256 is
`ae4edaf6799d4b57510d14d2004c5b65ff6b05f3b225e96bbd5971b30ce8832b`.
Publication follows passing pull-request CI, which checks the pinned platform
snapshot and runs the suite again from the extracted archive.

The [versioned release page](https://github.com/eseidinger/energy-system-configuration/releases/tag/contract-kit-v0.5.0)
is the publication record for the annotated tag, archive, checksum, and
compatibility notes. Existing release tags and assets remain immutable.

## Consumer handoff

VEF adopts the released `0.5.0` archive and checksum and implements the packaged
AI acceptance scenarios. ODIP can retain its accepted `0.4.0` contract pin until
coordinated adoption. The static kit suite verifies structured envelopes and
citation integrity; VEF must separately establish confirmation enforcement,
claim accuracy, prompt-injection resistance, and unchanged Gate 5 behavior.
