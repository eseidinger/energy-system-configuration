# DEC-14: Production deployment authorization

**Status:** APPROVED_WITH_RECORDED_LIMITS

**Date:** 2026-10-29

**Decision owner:** The maintainer, who previously confirmed authority for the
Energy System Configuration, VEF, ODIP and Developer Platform responsibility
areas for this release.

## Decision

After [DEC-13](DEC-13-bounded-gate-6-acceptance.md) and publication of
[contract kit 1.0.0](../reviews/2026-10-29-contract-kit-1.0.0-release.md), the
maintainer stated: "Produktionsfreigabe erteilt". This separately authorizes
the versioned production deployments of ODIP and VEF for the same energy
configuration release. ODIP is deployed first, followed by VEF. The release
uses the exact kit 1.0.0 archive checksum pinned by both consumers.

The authorization carries forward the DEC-10/11/12 evidence limits and the
bounded Gate 6 decision. Accepted exceptions remain exceptions, not passed
tests. The workflow covers new installations, complete UTC calendar years and
the disclosed synthetic Wasserburg reference profile. It does not approve
existing-equipment support or claim measured 2024 site data.

Independent qualified domain review was not supplied with this authorization.
The previous integration plan named it as a prerequisite for production or
certified-engineering use. The maintainer's explicit authorization permits the
bounded production deployment while leaving that evidence gap visible; this
decision does not claim certified-engineering suitability.

## Evidence and deployment record

The published kit and successful consumer CI runs are pinned in the
[release record](../reviews/2026-10-29-contract-kit-1.0.0-release.md). Exact
application tags, image digests, deployment revisions, readiness and any
remaining operational limits belong in the separate production deployment
record once observed. A successful CI job alone is not a claim that the
production service is ready or that a new end-to-end production calculation
has been performed.
