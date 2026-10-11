# Energy System Configuration

This repository defines the cross-project reference scenario for AI-assisted energy-system configuration:

- [Use case definition](energy-configuration-use-case.md) — user goal, scope, actors, scenarios, and observable acceptance conditions.
- [Integration contract](energy-configuration-integration-contract.md) — normative APIs, schemas, calculations, security boundaries, and contract tests.
- [Integration plan](energy-configuration-integration-plan.md) — decisions, repository work packages, ordered integration gates, handoffs, and completion criteria.
- [Architecture decisions](decisions/) — accepted cross-project choices that establish the implementation baseline.
- [VEF-to-ODIP authentication flow](architecture/vef-odip-authentication.md) — sequence, trust boundaries, threats, and required controls.
- [Gate 0 domain review](reviews/2026-10-10-gate-0-domain-review.md) — approval and limitations of the version 0.2 implementation baseline.
- [Gate 1 contract-kit review](reviews/2026-10-10-gate-1-domain-review.md) — reviewed fixture, numerical oracle, recommendation, and release prerequisite.
- [Platform reconciliation](contract-kit/platform/README.md) — pinned implementation, breaking identity changes, deployment examples, and remaining acceptance work.
- [Contract kit 0.4.0 release review](reviews/2026-10-11-contract-kit-0.4.0-release-review.md) — maintainer publication authorization, verification, and remaining consumer handoff.
- [Shared contract kit](contract-kit/) — executable schemas, APIs, examples, fixtures, expected results, and validation tests.

The documents intentionally separate why the integration exists, what participating systems must guarantee, and how the teams should deliver it.

## Licensing

Repository-authored schemas, APIs, tests, and tooling use Apache-2.0.
Repository-authored documentation, synthetic fixtures, and expected results use
CC BY 4.0. Third-party data retains its source terms and attribution. See
[LICENSE](LICENSE) and [NOTICE](NOTICE).
