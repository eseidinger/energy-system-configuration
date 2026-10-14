# Contract kit 0.4.0 release review

**Date:** 2026-10-11
**Reviewer:** Sole cross-project maintainer, eseidinger
**Scope:** Platform reconciliation and release implementation
**Outcome:** Implemented and published as `contract-kit-v0.4.0`

The reconciled contract kit was implemented, merged through pull request #1,
and published under the annotated `contract-kit-v0.4.0` tag. The release
archive SHA-256 is
`884e3590614328c2adafa457153e11575dc1be09b9f53d7b0f53704fe39d02b0`.
The [release page](https://github.com/eseidinger/energy-system-configuration/releases/tag/contract-kit-v0.4.0)
is the publication record for the immutable tag, archive, and checksum.

This records implementation and publication of the shared kit; it is not an
independent external review or deployed integration acceptance.

## Reviewed change

- Pin Developer Platform revision
  `b360ddee34444748c95705c597aa7b17491cd05b`.
- Replace the earlier application-managed authentication assumptions with the
  platform-managed identity, access-policy, service-binding, and governance
  contracts. This includes the breaking `0.3.0` identity migration.
- Add the `0.4.0` operational-envelope schema and example, protected-boundary
  monitoring semantics, and authorized retained-log integration profile.
- Preserve the previously approved energy schemas, fixtures, calculations,
  candidate enumeration, and numerical expected results.

The affected consumers are ODIP, VEF, and their Developer Platform deployment
configuration. Compatibility and migration details are in the
[platform notes](../contract-kit/platform/README.md).

## Verification and release evidence

- All 54 kit tests pass, including validation from an extracted archive.
- Repeated archive builds produce the same bytes and SHA-256 checksum.
- The generated input-schema snapshot and pinned platform source digests match.
- The focused upstream suite passes 128 tests; two PostgreSQL fixture tests
  are skipped. Upstream request validators accept the platform examples.
- Pull request #1 passed repository CI before merge and tagging.
- The annotated `contract-kit-v0.4.0` tag and prerelease contain the
  deterministic archive, `SHA256SUMS`, and compatibility notes. Existing
  release tags and assets were preserved.

ODIP and VEF still need to pin the published archive version and checksum in
their CI before Gate 1 closes. Deployed log ingestion, elapsed seven-day
retention, restore, and end-to-end acceptance remain open; this prerelease
does not assert those outcomes.
