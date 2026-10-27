# DEC-10: Accept the current energy release without a recovery test

**Status:** Accepted by the cross-project maintainer
**Date:** 2026-10-27
**Decision owner:** Integration Contract Maintainer
**Scope revision:** 1

## Decision

After the successful service restart, corrected-version calculation and exact
five-artifact readback, the maintainer stated: "Akzeptiere auch ohne Recovery
Test." No recovery VM is available. For this current bounded energy release,
acceptance does not require the isolated backup-restoration exercise for ODIP's
database and retained S3 object versions together with VEF's database.
Provisioning a recovery VM is therefore not a prerequisite for this release.

This is an explicit acceptance exception, not a passed recovery test. No actual
database/bucket restoration, post-restore authorization reconciliation, measured
RPO/RTO or recovered application transactions have been demonstrated by this
decision. The successful restart/readback observations remain valid on their
own terms.

## Boundaries

- Applies to the current energy release reviewed in `odip-test` and `vareng-test`.
- Supersedes only the requirement to execute the joint backup/restore drill as
  a release gate, including its restore-specific reconciliation/readback steps.
- Does not remove backup, retention, access-control or storage-integrity duties.
- Does not waive hosted in-progress workload interruption, security, observability,
  AI semantic/citation/boundary checks, evidence retention or other open cases.
- Does not grant final Gate 6 acceptance, production deployment authorization or
  approval to publish a release. Other acceptance decisions remain separate.
- Does not waive recovery evidence for future releases or installations. A future
  full-recovery claim requires an executed, retained restore test.

## Documentation and versioning

Use-case prose 0.4, integration-contract prose 0.6 and integration-plan prose 0.4
record this exception. Released contract kit 0.5.0, its archives/tags, numerical
fixtures and consumer pins remain immutable. Carry DEC-10 with DEC-07/08/09 in
the next shared release's acceptance/compatibility record under DEC-06; the
exception changes acceptance scope, not a wire schema or calculation.

The restore portions of GAP-05, GAP-13 and AI-10 are **ACCEPTED_EXCEPTION** for
this release. They are not PASS; remaining assertions in those composite cases
stay open. The [guided record](../reviews/2026-10-27-guided-release-acceptance.md)
and [gap register](../reviews/2026-10-27-gap-analysis.md) retain the distinction.
