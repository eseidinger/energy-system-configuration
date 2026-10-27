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
- [Contract kit 0.4.0 cross-project acceptance](reviews/2026-10-14-contract-kit-0.4.0-cross-project-acceptance.md) — shared-kit acceptance by Developer Platform, ODIP, and VEF.
- [Gate 5 acceptance](reviews/2026-10-17-gate-5-acceptance.md) — maintainer acceptance of the deployed workflow; Gate 6 AI assistance and release is next.
- [Contract kit 0.5.0 release review](reviews/2026-10-17-contract-kit-0.5.0-release-review.md) — publication authorization and VEF consumer handoff.
- [VEF AI assistance profile](contract-kit/ai/README.md) — Gate 6 requirements, proposal/explanation schemas, and consumer acceptance cases in kit `0.5.0`.
- [Shared contract kit](contract-kit/) — executable schemas, APIs, examples, fixtures, expected results, and validation tests.

The documents intentionally separate why the integration exists, what participating systems must guarantee, and how the teams should deliver it.

## Current status — October 27, 2026

ODIP and VEF both pin contract kit **0.5.0**. Immutable publication, deterministic
new-equipment optimization and the AI-assisted workflow are implemented. Gate 5
was accepted by maintainer direction on October 17; ODIP's handoff was accepted
on October 19. **Gate 6 and final release acceptance remain open**, including
AI-05, AI-06, AI-08, AI-10 and AI-11.

The [cross-project review](reviews/2026-10-27-implementation-and-acceptance-review.md)
records source revisions, current coverage and executed checks. The subsequent
[gap analysis](reviews/2026-10-27-gap-analysis.md) assigns remaining implementation,
scope and evidence work. Historical acceptance is preserved; it does not imply
that every later regression or recovery scenario has been rerun.

## Licensing

Repository-authored schemas, APIs, tests, and tooling use Apache-2.0.
Repository-authored documentation, synthetic fixtures, and expected results use
CC BY 4.0. Third-party data retains its source terms and attribution. See
[LICENSE](LICENSE) and [NOTICE](NOTICE).
