# Contract kit 0.4.0 release review

**Date:** 2026-10-11
**Reviewer:** Sole cross-project maintainer, eseidinger
**Scope:** Platform reconciliation and prerelease publication
**Outcome:** Publication authorized; passing pull-request checks required

The maintainer requested reconciliation against the current Developer Platform,
requested a second check, and then explicitly requested commitment and
publication of the resulting kit. This records that maintainer authorization;
it is not an independent external review or deployed integration acceptance.

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

## Verification and release conditions

- All 54 kit tests pass, including validation from an extracted archive.
- Repeated archive builds produce the same bytes and SHA-256 checksum.
- The generated input-schema snapshot and pinned platform source digests match.
- The focused upstream suite passes 128 tests; two PostgreSQL fixture tests
  are skipped. Upstream request validators accept the platform examples.
- The pull request must pass the repository CI checks before merge and tagging.
- Publish a new annotated `contract-kit-v0.4.0` tag and prerelease with the
  deterministic archive, `SHA256SUMS`, and compatibility notes. Preserve all
  existing release tags and assets.

ODIP and VEF still need to pin the published archive version and checksum in
their CI before Gate 1 closes. Deployed log ingestion, elapsed seven-day
retention, restore, and end-to-end acceptance remain open; this prerelease
does not assert those outcomes.
