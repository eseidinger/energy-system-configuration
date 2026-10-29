# DEC-11: Accept remaining non-AI points without further testing

**Status:** Accepted by the cross-project maintainer
**Date:** 2026-10-27
**Decision owner:** Integration Contract Maintainer
**Scope revision:** 1

**Later status:** [DEC-12](DEC-12-proposed-ai10-equivalent-regression.md)
subsequently accepted AI-10 with documented limits on 2026-10-29. The AI
case status below records the state when DEC-11 was made.

## Decision

The maintainer stated: "akzeptiere die weiteren offenen abnahmepunkte ohne
prüfung. Die AI Abnahmefälle bleiben noch offen."

For the current bounded energy release, the additional non-AI acceptance points
listed in the preceding review are accepted without further verification:

- Hosted interruption of an active calculation and subsequent processing.
- Direct-backend/egress denial, credential rotation and revocation probes.
- Deployed retention cleanup, elapsed log expiry and collector/compactor checks.
- Durable model/source/image retention and replay after upgrades.
- Deployed workload time/memory, queue, persistence and serialization measurements.
- Real-session keyboard/screen-reader and session-expiry review.
- Remaining installation-specific S3 versioning, migration and outage checks.
- Additional non-AI evidence-storage, final inventory and release-review checks.

DEC-10's restore-test exception remains effective. These points are recorded as
ACCEPTED_EXCEPTION, not PASS. Existing successful tests remain valid; missing
evidence is not created by accepting the exception.

## AI cases remain open

AI-05, AI-06, AI-08, AI-10 and AI-11 remain OPEN. This decision does not accept
any additional AI assertion or infer that deterministic regression is complete
merely because the general operational points have been accepted.

Where a shared check also supplies evidence specifically required by an open
AI case, that AI evidence obligation remains open. In particular, AI-10 still
needs its outstanding independent VEF invalid-content and AI-enabled regression
evidence. General operational exceptions must not be used to mark AI-10 PASS.
DEC-10 remains the explicit exception for its restore-execution portion.

The remaining acceptance work is therefore the five AI cases. Final Gate 6
remains open on that basis. The maintainer has accepted the additional non-AI
review items; do not request the same acceptance again. This decision does not
authorize production deployment, tag publication or an external release action.

## Scope and documentation

Applies only to the current release reviewed in `odip-test` and `vareng-test`.
It supersedes DEC-10's statement that the listed non-AI checks still require
release acceptance, while preserving its unverified-recovery classification.
It does not remove implemented backup/security/retention/storage controls or
claim general future operational assurance.

Use-case prose 0.5, integration-contract prose 0.7 and integration-plan prose 0.5
record the current acceptance scope. Released kit 0.5.0, tags, archives, numerical
fixtures and consumer pins remain immutable. Include this decision in the next
release's scope/compatibility record; no schema or model version changes here.

The [gap register](../reviews/2026-10-27-gap-analysis.md) distinguishes accepted
non-AI exceptions from the five still-open AI cases, including overlapping gaps.
