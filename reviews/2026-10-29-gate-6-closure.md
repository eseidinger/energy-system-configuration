# Gate 6 closure — bounded energy configuration release

**Status:** CLOSED_WITH_LIMITATIONS

**Date:** 2026-10-29

**Scope:** New installations, complete UTC calendar years and the disclosed
synthetic Wasserburg reference profile. This closes `VEF-05` and Gate 6 for
the accepted kit and application 1.0.0 release, not an unrestricted or
certified-engineering use case.

## Basis for closure

1. [DEC-13](../decisions/DEC-13-bounded-gate-6-acceptance.md) accepted
   Gate 6/`VEF-05` with the DEC-10/11/12 evidence limits. The accepted AI
   cases, source-to-consumer regression and review pins are in its
   [candidate inventory](2026-10-29-gate-6-release-candidate-review.md).
2. The separately authorized [contract kit 1.0.0](2026-10-29-contract-kit-1.0.0-release.md)
   was published, checksum-verified and pinned by both consumers.
3. The maintainer separately granted [production authorization](../decisions/DEC-14-production-deployment-authorization.md).
   ODIP and VEF application `v1.0.0` tagged CI runs passed. Both production
   deployments were read back as `ready` at their versioned image digests;
   see the [deployment record](2026-10-29-production-deployment.md).
4. The maintainer reported a successful authenticated production optimization
   on dataset 1.0.0. Every supplied result and evidence field matches the
   immutable reference oracle exactly. The [owner-report record](evidence/2026-10-29-production-optimization-owner-report.json)
   pins the run ID and values.

## Retained limits

DEC-10's joint restore test and DEC-11's other listed non-AI tests were
accepted as exceptions, not passed. AI-10 remains
ACCEPTED_WITH_LIMITATIONS under DEC-12; the historical unchanged Gate 5 suite
was not retained as one executable run. The production run's API JSON and
all 252 live candidates were not independently exported; that export is useful
for stronger evidence but was not a requirement of DEC-13 or DEC-14. The
maintainer's production result view and exact oracle match are the evidence
used here. Independent qualified domain review is still absent, and this
closure does not claim certified-engineering suitability.

These limits must be resolved or explicitly renewed for a later release.
The closure does not change the old fixture bytes, calculation authority or
the scope decisions DEC-07 and DEC-08.
