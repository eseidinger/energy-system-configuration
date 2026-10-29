# Contract kit 1.0.0 publication and consumer adoption

**Date:** 2026-10-29

**Decision:** The maintainer separately authorized publication after the
bounded [Gate 6 decision](../decisions/DEC-13-bounded-gate-6-acceptance.md).
This record concerns the shared contract kit and the ODIP/VEF consumer pins in
the test-release path. Production deployment is not authorized by that decision
or by this publication.

## Immutable release

| Item | Published pin |
| --- | --- |
| Git tag | Annotated `contract-kit-v1.0.0` at `072b1f4ad807ef981696d35d1fd86c2480371fc6` |
| GitHub release | [contract-kit-v1.0.0](https://github.com/eseidinger/energy-system-configuration/releases/tag/contract-kit-v1.0.0), published, neither draft nor prerelease |
| Archive | `contract-kit-v1.0.0.tar.gz`, SHA-256 `ab101a9d5588283ce30c78149084ba145c4c0a6ce3e678c4defff58749951cb0` |
| Checksum file | Uploaded `SHA256SUMS`; downloaded archive passed `sha256sum --check SHA256SUMS` |
| Source CI | [Run 40880482711](https://github.com/eseidinger/energy-system-configuration/actions/runs/40880482711) PASS at the tagged source commit |

The final archive was built twice with identical bytes. Its extracted source
suite passed 82 tests, and it includes LICENSE, NOTICE, LICENSES and release
notes. The archive was downloaded from the published release and verified
against its published checksum. The reviewed candidate archive SHA-256
`80e2f2f62d90c06dd252f2aacec18195aa0e70fa661cd14046d5c96fb7e0a65a`
in the [Gate 6 candidate inventory](2026-10-29-gate-6-release-candidate-review.md)
is historical: release wording was finalized before the immutable tag and
archive were created. Schemas, API contracts, fixtures and numerical oracles
were not changed by that wording edit.

## Consumer source pins

| Consumer | Adoption commit | Verification |
| --- | --- | --- |
| VEF | `b64e0e111bbb22092f6d041dec7bbe1c46e76151` | Lock pins published URL and archive SHA-256 above; local upstream kit suite (82 tests), packaged API schema-byte comparison, 32 script tests and documentation checks pass. [CI run 40881986516](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40881986516). |
| ODIP | `55a11c47fbb27389527ab0def8e6bcf11fd0828a` | Lock and vendored archive pin the same SHA-256; extracted vendor content passed the byte comparison; 89 worker tests pass. [CI run 40882017308](https://github.com/eseidinger/open-data-intelligence-platform/actions/runs/40882017308). |

Both consumer commits were pushed to `main`. The published 0.5.0 release remains
immutable as a historical baseline. The acceptance scope remains new equipment,
complete UTC calendar years and synthetic reference data. DEC-10/11/12 limits
remain attached to the bounded Gate 6 acceptance; publication does not convert
accepted exceptions into passed tests.
