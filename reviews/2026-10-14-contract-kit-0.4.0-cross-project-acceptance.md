# Contract kit 0.4.0 cross-project acceptance

**Date:** 2026-10-14  
**Accepted by:** Developer Platform, Open Data Intelligence Platform, and
Variability Engineering Framework maintainers  
**Scope:** Shared contract-kit handoff  
**Outcome:** Accepted for cross-project implementation

The three project owners accept the immutable `contract-kit-v0.4.0` release as
the shared implementation contract for the energy-system configuration work.
The accepted archive SHA-256 is
`884e3590614328c2adafa457153e11575dc1be09b9f53d7b0f53704fe39d02b0`.
The [release page](https://github.com/eseidinger/energy-system-configuration/releases/tag/contract-kit-v0.4.0)
remains the publication record for the tag, archive, and checksum.

## Accepted contract

| Owner | Acceptance |
| --- | --- |
| Developer Platform | Accepts the pinned `b360ddee34444748c95705c597aa7b17491cd05b` compatibility profile, including platform-managed identity and the operational-envelope/log contract. |
| ODIP | Accepts the published schemas, OpenAPI publication contract, fixtures, canonicalization rules, and immutable archive pin. |
| VEF | Accepts the optimization schemas, fixtures, expected simulation and optimization results, and immutable archive pin. |

ODIP and VEF CI pin version `0.4.0` and the accepted archive checksum. The
shared-kit handoff is complete and authorizes the Gate 2 and Gate 3
implementation work.

## Limits of this acceptance

This accepts the shared contract kit only. It does not accept deployed ODIP or
VEF implementations, application images, deployed log ingestion, elapsed
seven-day retention, restore, or end-to-end workflow behavior. Those outcomes
remain subject to their respective integration gates and acceptance evidence.
