# AI-Assisted Energy System Configuration Integration Plan

**Status:** Proposed plan, version 0.1
**Date:** 2026-10-09
**Owners:** Developer Platform, Open Data Intelligence Platform, and Variability Engineering Framework maintainers
**Purpose:** Turn the [use case](energy-configuration-use-case.md) and [integration contract](energy-configuration-integration-contract.md) into an ordered, independently testable delivery plan.

**Current gate:** Gate 0 completed on 2026-10-10; contract version `0.2` is the frozen implementation baseline and Gate 1 is next. The bounded demonstration received maintainer domain review because there is only one cross-project collaborator. Independent qualified review remains required before production or certified-engineering use.

The plan deliberately integrates a thin deterministic path before the AI-assisted workflow. Each gate leaves a testable result and prevents later work from hiding contract or numerical defects.

## 1 Delivery strategy

Work proceeds in seven gates:

```text
Decisions
   -> shared contract kit
   -> ODIP publication vertical slice
   -> VEF deterministic vertical slice
   -> authenticated deployed connection
   -> end-to-end acceptance
   -> AI assistance and release
```

ODIP, VEF, and Developer Platform work may proceed in parallel after the shared contract kit is accepted. They converge first on a fixture-backed happy path, then on security, failure handling, durability, and AI assistance.

### Release slices

| Slice | Outcome | Included gates |
| --- | --- | --- |
| A: Contract proof | One fixed dataset produces one deterministic recommendation locally. | 0-3 |
| B: Platform integration | The same flow runs across separately deployed, authenticated ODIP and VEF applications. | 4-5 |
| C: AI-assisted demonstration | Confirmed natural-language input and evidence-grounded explanation are added without changing calculation authority. | 6 |

## 2 Decisions required before implementation

Record these as short architecture decisions. Gate 0 closes only when every item has an owner and a recorded answer.

| ID | Decision | Required outcome |
| --- | --- | --- |
| [`DEC-01`](decisions/DEC-01-reference-data.md) | Reference data | Confirm region, calendar year, source licenses, catalog owner, and whether synthetic fixtures are sufficient for the demonstration. |
| [`DEC-02`](decisions/DEC-02-simulation.md) | Simulation | Domain reviewer approves PV, inverter, battery dispatch, annual operations, component lifetime, rounding, and numeric tolerances. |
| [`DEC-03`](decisions/DEC-03-connectivity.md) | Connectivity | Select authenticated public HTTPS ingress or define a private cross-project service capability. |
| [`DEC-04`](decisions/DEC-04-identity.md) | Identity | Select issuer, token audience, claims, provisioning owner, and rotation process for VEF's read-only ODIP identity. |
| [`DEC-05`](decisions/DEC-05-limits-retention-classification.md) | Limits and retention | Set artifact and publication size limits, candidate/search bounds, run timeout, retention, and customer-data classification. |
| [`DEC-06`](decisions/DEC-06-contract-ownership-and-releases.md) | Contract ownership | Name the owner and release process for shared JSON Schema/OpenAPI definitions and fixtures. |

If a decision changes a contract field or behavior, update the proposed contract before dependent implementation begins.

## 3 Work packages

These IDs are the traceable units to create in the respective repositories.

| ID | Project | Deliverable | Acceptance evidence |
| --- | --- | --- | --- |
| `SHARED-01` | Cross-project | Versioned contract kit containing schemas, examples, fixtures, expected digests, simulation totals, and recommendation. | ODIP and VEF validate the same kit in CI. |
| `DP-01` | Developer Platform | Deploy ODIP API, ODIP worker, and VEF as separate projects with immutable images, databases, secrets, readiness, and bounded resources. | Applications become ready after restart and retain data. |
| `DP-02` | Developer Platform | Permit the selected VEF-to-ODIP route with least-privilege egress. | Allowed ODIP request succeeds; an unrelated destination is denied. |
| `DP-03` | Developer Platform | Document application identity and, if selected, private cross-project routing as explicit capabilities. | Capability contract and isolation tests pass. |
| `ODIP-01` | ODIP core | Add a generic immutable dataset-publication manifest with schema reference, multiple artifacts, provenance, and validation-policy result. | Energy and non-energy fixtures publish without domain branching in ODIP core. |
| `ODIP-02` | ODIP core | Serve immutable manifests and artifacts with versions, ETags, conditional reads, and checksums. | Repeated reads match digests; corrections require a new version. |
| `ODIP-03` | ODIP | Enforce application authentication, dataset-scoped read/write authorization, and constrained source retrieval. | Unauthorized operations and disallowed source locations fail. |
| `ENERGY-01` | Energy adapter | Implement five energy artifact schemas, source mappings, quality rules, and license metadata outside ODIP core semantics. | Expected fixture is reproduced; incomplete hourly data and invalid components fail. |
| `VEF-01` | VEF | Fetch, verify, validate, persist, and cache a pinned ODIP energy publication. | Wrong schema or checksum fails; verified data survives restart. |
| `VEF-02` | VEF | Implement energy feature model, compatibility rules, quantities, units, and bounded candidate generation. | Exhaustive fixture yields exactly the expected configurations. |
| `VEF-03` | VEF | Implement hourly simulation, constraint evaluation, costing, deterministic ranking, and optimality status. | Hand-calculated cases match totals and ordering within agreed tolerance. |
| `VEF-04` | VEF | Expose run APIs, audit trail, user workflow, and evidence bundle. | A submitted request is reproducible and every result field is attributable. |
| `VEF-05` | VEF | Add confirmed natural-language input and evidence-grounded explanation. | AI tests reject unsupported claims and prompt injection in source metadata. |
| `INT-01` | Cross-project | Automate the deployed happy path and required failure scenarios. | Gate 5 acceptance suite passes on Developer Platform. |

## 4 Ordered integration steps

### Gate 0 — Resolve design decisions

1. Assign one decision owner and due date to `DEC-01` through `DEC-06`.
2. Review the use-case assumptions with the domain reviewer.
3. Record the chosen route and identity flow with a sequence diagram and threat notes.
4. Amend the contract wherever a decision resolves a currently open parameter.
5. Freeze proposed contract version `0.2` as the implementation baseline.

**Exit:** All six decisions are recorded; no unresolved choice changes schema shape, simulation math, identity, or deployment topology.

### Gate 1 — Build the shared contract kit

1. Create versioned JSON Schemas for the generic publication manifest, energy artifacts, optimization request, candidate, result, and machine-readable errors.
2. Add a compact but complete one-year energy fixture plus a non-energy publication fixture.
3. Record canonical serialization rules and compute artifact and manifest SHA-256 values.
4. Add hand-calculated simulation cases covering PV clipping, charge/discharge efficiency, capacity and power limits, import, export, and the year-end battery condition.
5. Record the expected feasible configurations, constraint outcomes, ranking, and recommendation.
6. Publish the kit in the location chosen by `DEC-06`; pin its version from ODIP and VEF CI rather than consuming a mutable branch.

**Exit:** Schema validation and digest calculation pass in a repository-neutral test runner; expected numerical outputs have domain-review approval.

### Gate 2 — Deliver the ODIP publication vertical slice

1. Implement the generic publication model and state transition so partially published data is never visible.
2. Implement immutable manifest and artifact retrieval, ETags, conditional reads, and error responses.
3. Implement the energy adapter and its quality policy outside ODIP core.
4. Run both the energy and non-energy shared fixtures through the same core publication path.
5. Add authentication and dataset-scoped authorization; deny unpublished, unauthorized, and unsafe source retrieval.
6. Publish the reference dataset version and capture its manifest digest for VEF tests.

**Exit:** `ODIP-01` through `ODIP-03` and `ENERGY-01` pass; a clean client can retrieve and verify every artifact using only the contract.

### Gate 3 — Deliver the deterministic VEF vertical slice

1. Implement ODIP client retrieval against a stub serving the exact shared fixture.
2. Validate trusted-origin artifact paths, schema major version, roles, units, intervals, and all checksums before persisting a verified import.
3. Implement bounded candidate generation and assert the exact expected configuration set.
4. Implement the hourly simulator and compare each reference case to hand-calculated totals.
5. Implement feasibility, cost, deterministic tie-breaking, and correct optimality claims.
6. Implement idempotent run creation, status transitions, immutable results, candidate retrieval, and infeasibility diagnostics.
7. Expose a deterministic evidence view suitable for both the UI and the later AI explanation.

**Exit:** `VEF-01` through `VEF-04` pass locally against the shared kit; no AI component is needed to obtain or explain the deterministic fields.

### Gate 4 — Connect the deployed applications

1. Build ODIP and VEF immutable images and record their digests.
2. Deploy ODIP API, worker, and database; publish the agreed reference fixture.
3. Deploy VEF and its separate database with the exact supported contract and model versions.
4. Provision VEF's read-only ODIP credential through the platform secret mechanism.
5. Apply the selected route, DNS, TLS, and least-privilege egress policy.
6. Verify successful token validation and dataset-scoped access from VEF to ODIP.
7. Verify that an unauthorized identity, prohibited dataset, and unrelated egress destination are denied.
8. Enable correlation on dataset ID, dataset version, and run ID without recording customer details or tokens.

**Exit:** `DP-01` through `DP-03` pass; VEF completes a real authenticated publication fetch from deployed ODIP.

### Gate 5 — Run cross-project acceptance

Execute the following in one automated environment:

1. Ingest the source fixtures, publish energy dataset `1.0.0`, retrieve its manifest and all five artifacts, and verify checksums and quality status.
2. Publish the non-energy fixture through the same ODIP API to prove that ODIP core remains domain-neutral.
3. Submit the agreed request pinned to energy dataset `1.0.0` and verify the exact feasible set, metrics, recommendation, versions, and provenance.
4. Assert rejection of a modified artifact, wrong unit, missing hour, unpublished version, unsupported schema major, invalid customer input, unauthorized caller, and changed body under a reused idempotency key.
5. Publish corrected dataset `1.0.1`; reproduce the existing `1.0.0` run unchanged, then explicitly start and verify a new `1.0.1` run.
6. Interrupt ODIP after VEF has verified `1.0.0` and confirm that only the verified cached version can be reused.
7. Restart ODIP and VEF, verify retained state, reproduce one completed run, and capture resource and observability evidence.
8. Restore the tested state from backup and reproduce the reference result.

**Exit:** `INT-01` passes in full. Local tests or three independently healthy deployments are not substitutes for this gate.

### Gate 6 — Add AI assistance and release

1. Add natural-language-to-request proposal generation behind mandatory user confirmation.
2. Restrict explanation input to the bounded run result and approved evidence view.
3. Require citations to run, dataset, model, simulation, configuration, constraint, cost, and self-sufficiency identifiers or values.
4. Test missing evidence, misleading user prompts, and instructions embedded in source metadata.
5. Run the deterministic Gate 5 suite unchanged to prove that AI assistance did not alter calculation authority.
6. Record contract acceptance by all three owners and tag the shared kit, implementations, images, and deployment definitions used for the release.

**Exit:** `VEF-05` and the AI acceptance scenarios pass; contract version 1 can be accepted and released.

## 5 Dependency and handoff rules

| Producer | Consumer | Handoff artifact | Ready when |
| --- | --- | --- | --- |
| Cross-project owners | ODIP and VEF | Shared contract kit | Version is immutable and expected results are reviewed. |
| ODIP | VEF | Published fixture manifest and client-facing API | Retrieval, integrity, authorization, and error tests pass. |
| VEF | Developer Platform | Image, configuration contract, readiness behavior, and resource bounds | Local vertical slice and migration tests pass. |
| ODIP | Developer Platform | API/worker images, schedules, configuration contract, and readiness behavior | Publication vertical slice and migration tests pass. |
| Developer Platform | Integration suite | Deployed endpoints, issuer/audience, test identities, and observability access | Allowed and denied connectivity checks pass. |
| Deterministic workflow | AI workflow | Bounded evidence view | Numerical and provenance acceptance tests pass without AI. |

Consumers pin handoff versions. A producer may add backward-compatible optional fields, but a breaking schema, behavior, or assumption change starts a new contract major version and updates the shared expected results before rollout.

## 6 Verification matrix

| Concern | Earliest gate | Final evidence |
| --- | --- | --- |
| Domain-neutral publication | 2 | Energy and non-energy fixtures traverse the same deployed ODIP API. |
| Data integrity and immutability | 1 | Digests, ETags, tamper rejection, and `1.0.0`/`1.0.1` isolation pass. |
| Simulation correctness | 1 | Reviewed hand calculations and deployed end-to-end totals agree. |
| Deterministic optimization | 3 | Expected feasible set, tie-breaking, and optimality status match. |
| Authentication and isolation | 2 | Allowed and denied service-to-service tests pass after deployment. |
| Durability and recovery | 4 | Restart and backup-restore reproduce the recorded result. |
| Explainability and AI safety | 6 | Evidence completeness, missing-evidence, and prompt-injection tests pass. |

## 7 Current baseline and sequencing risks

This plan is based on the repositories inspected on 2026-10-09.

| Project | Reviewed baseline | Consequence for sequencing |
| --- | --- | --- |
| Developer Platform [`27a45e1`](https://github.com/eseidinger/developer-platform/tree/27a45e14c82b109894ec9d1781e1e1cf3c1ec0bd) | [Application schema](https://github.com/eseidinger/developer-platform/blob/27a45e14c82b109894ec9d1781e1e1cf3c1ec0bd/platform/app/spec.py) and [manifests](https://github.com/eseidinger/developer-platform/blob/27a45e14c82b109894ec9d1781e1e1cf3c1ec0bd/platform/app/manifests.py) support services, schedules, PostgreSQL, and declared egress; the [security model](https://github.com/eseidinger/developer-platform/blob/27a45e14c82b109894ec9d1781e1e1cf3c1ec0bd/docs/architecture/security-and-authorization.md) separates application authorization from platform authorization. | Decide the application identity and route before Gate 4; do not assume platform OIDC grants authorize ODIP data access. |
| ODIP [`accc027`](https://github.com/eseidinger/open-data-intelligence-platform/tree/accc027194014b38677aa761566ed57682825767) | The [ingestion service](https://github.com/eseidinger/open-data-intelligence-platform/blob/accc027194014b38677aa761566ed57682825767/services/platform-api/src/main/kotlin/de/eseidinger/odip/platform/ingestion/service/IngestionService.kt) and [worker](https://github.com/eseidinger/open-data-intelligence-platform/blob/accc027194014b38677aa761566ed57682825767/workers/data-worker/src/odip_worker/run.py) exist, but the [normalizer](https://github.com/eseidinger/open-data-intelligence-platform/blob/accc027194014b38677aa761566ed57682825767/workers/data-worker/src/odip_worker/normalization.py) currently handles a narrow energy observation; broader analytics remain in the [development plan](https://github.com/eseidinger/open-data-intelligence-platform/blob/accc027194014b38677aa761566ed57682825767/docs/development-plan.md). | Complete the generic publication model before coupling VEF to energy-specific ODIP behavior. |
| VEF [`43ee5cc`](https://github.com/eseidinger/variability-engineering-framework/tree/43ee5cc1c981970fd9068c7a9e0119a935c925ea) | The [analysis engine](https://github.com/eseidinger/variability-engineering-framework/blob/43ee5cc1c981970fd9068c7a9e0119a935c925ea/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/core/AnalysisEngine.java) uses a [fixture-backed population](https://github.com/eseidinger/variability-engineering-framework/blob/43ee5cc1c981970fd9068c7a9e0119a935c925ea/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/http/FoodServicePopulationStore.java); generative configuration and optimization are [roadmap](https://github.com/eseidinger/variability-engineering-framework/blob/43ee5cc1c981970fd9068c7a9e0119a935c925ea/docs/01-product/roadmap.md) work, and current [variant identity](https://github.com/eseidinger/variability-engineering-framework/blob/43ee5cc1c981970fd9068c7a9e0119a935c925ea/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/core/Variant.java) has no quantities or units. | Prove candidate identity, quantities, units, and simulation math against small fixtures before adding deployed or AI concerns. |

The main delivery risk is integrating on illustrative payloads before the shared schemas and numerical fixtures are executable. Gate 1 is therefore a prerequisite for implementation convergence, not documentation cleanup to defer until the end.

## 8 Completion criteria

The integration is complete only when:

- every Gate 0 decision is recorded;
- all work packages have acceptance evidence;
- the shared kit and all deployed images are pinned to immutable versions;
- the complete Gate 5 suite passes after restart and backup restoration;
- the AI-assisted Gate 6 suite passes without weakening the deterministic suite;
- the three project owners accept the contract version used by the release;
- known limitations from the use case are visible in the user-facing result.
