# DEC-13: Bounded Gate 6 acceptance

**Status:** ACCEPTED_WITH_LIMITATIONS

**Date:** 2026-10-29

**Decision owner:** The maintainer explicitly confirmed authority to represent
the Energy System Configuration, Variability Engineering Framework, Open Data
Intelligence Platform and Developer Platform responsibility areas for this
bounded release.

**Scope:** Energy configuration for new installations with complete UTC
calendar years in `odip-test` and `vareng-test`, using the synthetic Wasserburg
reference publications and AI assistance. This is an integration acceptance
decision, not a production or publication authorization.

## Decision

The maintainer stated: "Ja, ich vertrete alle Bereiche und akzeptiere Gate 6
mit DEC-10/11/12". Gate 6 and `VEF-05` are therefore accepted for this bounded
test release with exactly the [release candidate inventory](../reviews/2026-10-29-gate-6-release-candidate-review.md)
and its recorded evidence limits. The individual AI case dispositions and
numerical regression evidence are retained, including AI-10's
ACCEPTED_WITH_LIMITATIONS classification under
[DEC-12](DEC-12-proposed-ai10-equivalent-regression.md).

The [DEC-10](DEC-10-current-release-recovery-test-exception.md) joint restore
exception and [DEC-11](DEC-11-current-release-non-ai-acceptance-exceptions.md)
operational exceptions remain ACCEPTED_EXCEPTION, not test PASS. DEC-12's
isolated source publication, private in-memory invalid-content transport,
distinct pinned VEF images and absent historical executable Gate 5 suite remain
explicit limits. The Developer Platform control-plane build revision was not
exposed by the read-only CLI inventory; its absence is recorded under the
current-release final-inventory exception in DEC-11, not inferred from
application deployment revisions. Future release reviews must resolve or
renew these limits.

## Accepted pins and release boundary

The inventory pins released consumer kit `0.5.0` and its archive SHA-256,
implementation commits, test deployment revisions 54 (`vareng-test`) and 10
(`odip-test`), all deployed application image digests and applied-spec hashes,
the AI model and historical tested prompt digest, standard publication manifests
and both independent numerical oracles. The source-to-consumer regression
passed on VEF revision 51 and ODIP revision 10; the later VEF source changes
through revision 54 are documentation only. The exact pins and CI links are in
the inventory, rather than duplicated here.

The maintainer separately accepted [PR #3](https://github.com/eseidinger/energy-system-configuration/pull/3).
Its kit `1.0.0` candidate was merged at
`cab284b0b4c13aa33c4b2346340cfb113c59d650`; its reproducible local
archive SHA-256 is
`80e2f2f62d90c06dd252f2aacec18195aa0e70fa661cd14046d5c96fb7e0a65a`.
The merged-main contract-kit CI passed. This candidate is **not** an immutable
release: no `contract-kit-v1.0.0` tag, GitHub release, archive upload or consumer
pin change has been authorized or performed.

This decision does not authorize production deployment or any external
publication. Kit `1.0.0` tagging/publication and coordinated ODIP/VEF consumer
adoption require their own explicit release authorization and final checksum
verification. The existing immutable kit `0.5.0` and its consumer pins remain
the deployed contract until then.
