# AI-Assisted Energy System Configuration Integration Contract

**Status:** Current-release scope revision, version 0.7
**Date:** 2026-10-27
**Owners:** Developer Platform, Open Data Intelligence Platform, and Variability Engineering Framework maintainers
**Purpose:** Define the normative interfaces and operational boundaries between the three projects for the energy-system configuration use case.

This contract implements the behavior described in the [use case definition](energy-configuration-use-case.md). Delivery order, repository work packages, and integration gates are defined in the [integration plan](energy-configuration-integration-plan.md). Use-case intent belongs in the use case definition; delivery status belongs in the plan. This document is limited to testable obligations at project boundaries.

Version 0.5 applies the maintainer-approved [DEC-07](decisions/DEC-07-new-equipment-release-scope.md): the current release covers new equipment only. It supersedes the existing-equipment obligations in prose version 0.4 for this release. It also records [DEC-08](decisions/DEC-08-complete-calendar-year.md): energy optimization requires a complete UTC calendar year. Published kit 0.5.0 and consumer pins remain immutable; both decisions must accompany the next shared-kit release before final acceptance.

Version 0.6 additionally applies [DEC-10](decisions/DEC-10-current-release-recovery-test-exception.md): the maintainer accepts this current release without an isolated joint backup/restore test. This explicit exception supersedes the restore-execution acceptance clauses below for this release only; backup, retention and access duties remain. Restoration is unverified, and all other open acceptance cases remain open. Released kit 0.5.0 and consumer pins are unchanged.

Version 0.7 applies [DEC-11](decisions/DEC-11-current-release-non-ai-acceptance-exceptions.md): the maintainer accepts the remaining listed non-AI acceptance points without further verification for this release. Their status is ACCEPTED_EXCEPTION; unperformed tests are not PASS. The AI cases are outside the exception, including their own evidence obligations; see the guided record for subsequent test dispositions. Together with DEC-10, this supersedes additional non-AI release-check requirements below without removing implemented controls or authorizing publication/deployment.

Subsequently, the maintainer approved [DEC-12](decisions/DEC-12-proposed-ai10-equivalent-regression.md): AI-10 is ACCEPTED_WITH_LIMITATIONS for the current bounded release. [DEC-13](decisions/DEC-13-bounded-gate-6-acceptance.md) accepts Gate 6/`VEF-05` for the bounded test release with DEC-10/11/12 limits. These decisions do not change the contract schema or immutable kit 0.5.0; the merged kit 1.0.0 candidate is not published and production deployment is not authorized.

Implementation and acceptance status are recorded in the [October 27 cross-project review](reviews/2026-10-27-implementation-and-acceptance-review.md). ODIP publication and VEF deterministic/AI endpoints are implemented; remaining conformance and evidence gaps do not change the normative obligations below. The October 27 status review itself changed no API, schema or calculation. The separately approved scope revision changes the release acceptance boundary, while retaining v1 wire fields and numerical results. Version `0.4` reconciles the platform integration boundary with Developer Platform revision `b360ddee34444748c95705c597aa7b17491cd05b`. It retains the `0.3` deployment and identity reconciliation and adds the implemented component-monitoring and minimized central-log profile; energy payloads and numerical oracles are unchanged. Normative words such as **MUST** express baseline requirements, not claims about current repository behavior. Contract version `1.0.0` becomes the accepted release only after the integration and release gates pass.

## Repositories

- [Developer Platform](https://github.com/eseidinger/developer-platform)
- [Open Data Intelligence Platform](https://github.com/eseidinger/open-data-intelligence-platform)
- [Variability Engineering Framework](https://github.com/eseidinger/variability-engineering-framework)

The repository links point to the projects' current default branches. The exact baseline assessed for this proposal is recorded in the integration plan.

## 1 Responsibilities and collaboration

| Responsibility | Developer Platform | ODIP | VEF |
| --- | --- | --- | --- |
| Deploy and operate containers, project databases, secrets, routing, scheduled jobs, and observability | Owns | Consumes | Consumes |
| Ingest, catalog, validate, version, and publish datasets through a domain-neutral API | Hosts workloads | Owns the platform capability | Consumes |
| Normalize energy sources and validate the energy input profile | Hosts adapter workload | Reference energy adapter owns this mapping; it remains outside the ODIP core | Validates the consumed profile independently |
| Own customer request and building-specific input | Hosts workload | Does not receive it in the first release | Owns |
| Define technical compatibility, generate configurations, simulate outcomes, and optimize | Hosts workload | Supplies factual attributes and reference profiles | Owns |
| Authenticate application users and VEF retrieval from ODIP | Owns hosted authentication, route-group authorization, normalized identity headers, and service credentials; platform grants are separate | Enforces finer dataset-scoped permissions | Enforces run ownership and holds an approved read-only ODIP service binding |
| Present the recommendation and AI explanation | Hosts workload | May expose data lineage | Owns the user journey and explanation boundary |

The projects remain separate owners of their databases. No project reads another project's PostgreSQL database directly. The exchange is through versioned application APIs and immutable data artifacts. The Developer Platform's OIDC grants authorize its control plane; they do not automatically authorize hosted application APIs.

ODIP's catalog, publication, and retrieval contract MUST remain usable for any dataset domain. The energy schema is a reference profile and may be implemented by an isolated adapter or plugin. ODIP core code and URL paths do not contain energy concepts. VEF is responsible for interpreting the energy profile for configuration and optimization.

### 1.1 Runtime flow

```text
Licensed sources and catalog fixtures
             |
             v
ODIP ingest -> validate -> normalize -> publish DatasetPublication v1
                                      schemaRef: energy-configuration-input/v1
                                                |
                                   authenticated HTTPS retrieval
                                                |
                                                v
Customer -> VEF request -> model validation -> candidate generation
                                  -> hourly simulation -> optimization
                                  -> result with versions and evidence
                                                |
                                                v
                                  VEF UI and optional AI explanation

Developer Platform deploys and observes ODIP and VEF, supplies each with its
own database and secrets, and permits only declared network destinations.
```

ODIP publication is asynchronous. VEF pins one published dataset version at the start of a run and never silently switches to a newer version. If ODIP is temporarily unavailable, VEF may use a previously verified immutable publication from its cache; the result must still identify the exact dataset, version, schema reference, and checksum.

## 2 General contract rules

1. Public contract versions use a major version in their schema or API path. A breaking change requires a new major version and a migration plan.
2. All persisted input and output objects have stable IDs, an explicit version, creation time in UTC, and an integrity checksum where bytes are exchanged.
3. ODIP's generic publication contract carries units and schema references without prescribing them. The energy input profile uses `kWh`, `kWp`, `kWh/kWp`, `m2`, `EUR`, `EUR/kWh`, and `EUR/year`. Currency is fixed to EUR for this use case.
4. Timestamps are ISO 8601 UTC instants. In the energy profile, hourly series use half-open intervals `[start, end)` and exactly one value per interval. Missing intervals are rejected rather than silently interpolated.
5. A published ODIP dataset version is immutable. Corrected data receives a new version and checksum. VEF results never change in place after completion.
6. Every externally obtained source records owner, license or usage rights, retrieval time, source version when available, and transformation version.
7. An input failing a required quality check is not eligible for optimization. Warnings that are allowed by policy remain visible in the result.
8. Each application API rejects unknown major versions and unknown required fields with a machine-readable error. Additive optional fields may be ignored only when their semantics do not change existing calculations.
9. Cross-project service-to-service API traffic uses an authenticated, encrypted channel. Secrets and bearer tokens never appear in a publication, result, log, or explanation.
10. A manifest is at most 1 MiB, an individual artifact is at most 10 MiB, and all artifacts in one publication total at most 50 MiB, measured after transfer decoding. Oversized input returns `413 payload_too_large` or, for an aggregate publication violation, `422 publication_limit_exceeded`; the dataset version is not published.

## 3 ODIP publication and energy consumer contract

### 3.1 Publication and retrieval

ODIP MUST expose a generic `DatasetPublication` for any dataset that has passed its applicable validation policy. The proposed read endpoints contain no domain name:

| Method and path | Purpose | Access |
| --- | --- | --- |
| `GET /api/v1/datasets?status=PUBLISHED&schemaRef={schemaRef}` | Discover published dataset IDs and versions. The schema filter is optional. | Approved platform reader group and ODIP dataset allow-list |
| `GET /api/v1/datasets/{datasetId}/versions/{version}` | Retrieve an immutable publication manifest. | Approved platform reader group and ODIP dataset allow-list |
| `GET /api/v1/datasets/{datasetId}/versions/{version}/artifacts/{artifactId}` | Download one immutable artifact by ID. | Approved platform reader group and ODIP dataset allow-list |

ODIP returns `ETag` equal to the manifest or artifact SHA-256 digest and supports conditional retrieval with `If-None-Match`. A version missing from the catalog returns `404`; a version that exists but is not published returns `409 dataset_version_not_published`; lack of authority returns `401` or `403`. ODIP must not return a partially published dataset version. These routes are proposed extensions of the current dataset catalog and version APIs, not claims that they already exist.

The manifest is a small generic JSON document. `schemaRef` identifies the domain contract; `metadata` and artifact `role` values are interpreted by the referenced schema, not by the ODIP core. Large data artifacts are downloaded separately. The example below shows a publication using the energy profile; its values are illustrative rather than real measurements or usable checksums:

```json
{
  "schemaVersion": "dataset-publication/v1",
  "datasetId": "energy-reference-wasserburg-am-inn-2024",
  "version": "1.0.0",
  "status": "PUBLISHED",
  "schemaRef": "urn:portfolio:energy-configuration-input:v1",
  "metadata": {
    "regionCode": "DE-BY-09187182",
    "period": {
      "start": "2024-01-01T00:00:00Z",
      "endExclusive": "2025-01-01T00:00:00Z",
      "step": "PT1H"
    }
  },
  "publishedAt": "2026-10-09T10:00:00Z",
  "artifacts": [
    {
      "artifactId": "pv-yield",
      "role": "PV_YIELD_PER_KWP",
      "mediaType": "application/json",
      "unit": "kWh/kWp",
      "sha256": "<64 lowercase hexadecimal characters>",
      "path": "artifacts/pv-yield"
    },
    {
      "artifactId": "import-tariff",
      "role": "IMPORT_TARIFF",
      "mediaType": "application/json",
      "unit": "EUR/kWh",
      "sha256": "<64 lowercase hexadecimal characters>",
      "path": "artifacts/import-tariff"
    },
    {
      "artifactId": "export-tariff",
      "role": "EXPORT_TARIFF",
      "mediaType": "application/json",
      "unit": "EUR/kWh",
      "sha256": "<64 lowercase hexadecimal characters>",
      "path": "artifacts/export-tariff"
    },
    {
      "artifactId": "component-catalog",
      "role": "COMPONENT_CATALOG",
      "mediaType": "application/json",
      "sha256": "<64 lowercase hexadecimal characters>",
      "path": "artifacts/component-catalog"
    },
    {
      "artifactId": "reference-load-shape",
      "role": "REFERENCE_LOAD_SHAPE",
      "mediaType": "application/json",
      "unit": "fraction",
      "sha256": "<64 lowercase hexadecimal characters>",
      "path": "artifacts/reference-load-shape"
    }
  ],
  "quality": {
    "status": "PASS",
    "policyRef": "urn:portfolio:energy-quality:v1",
    "warnings": []
  },
  "provenance": [
    {
      "sourceId": "solar-demo-source",
      "sourceVersion": "2025",
      "license": "<recorded license or usage right>",
      "rawArtifactId": "<ODIP raw artifact ID>",
      "transformationVersion": "solar-normalizer/1.0.0"
    }
  ]
}
```

The energy profile requires all five artifact roles in the first release. The generic publication contract does not require these roles for other datasets. A domain-specific adapter validates the profile before publication, and VEF validates it again as a consumer. VEF MUST verify each downloaded SHA-256 digest against the manifest before using it. Relative `path` values are resolved only against the manifest's trusted ODIP origin; VEF must not follow an arbitrary external URL supplied in a manifest.

### 3.2 Energy profile semantics

Under DEC-08, the energy profile period MUST begin on January 1 at 00:00:00 UTC and end exclusively on January 1 at 00:00:00 UTC of the next Gregorian year, with no fractional boundary seconds. It MUST contain exactly 8,760 hourly UTC intervals, or 8,784 in a leap year, including February 29. All four time series MUST share the period and contain every expected timestamp exactly once in order. A matching hour count alone is insufficient. The ODIP energy adapter and VEF MUST reject partial, rolling, shifted or multiple-year periods before accepting them for annual optimization; they MUST NOT silently annualize shorter data. This restriction belongs to the energy profile, not the generic ODIP publication API.

| Role | Required contents and validation |
| --- | --- |
| `PV_YIELD_PER_KWP` | Non-negative hourly DC energy per installed kWp, before inverter and battery losses, for the stated region and period. Method, source, orientation assumptions, and included upstream losses are versioned in provenance. |
| `IMPORT_TARIFF` and `EXPORT_TARIFF` | Non-negative hourly prices in EUR/kWh; each has exactly the same intervals as the yield series. Taxes and fixed fees are excluded in v1 and disclosed as limitations. |
| `REFERENCE_LOAD_SHAPE` | Non-negative hourly fractions summing to 1 within a declared tolerance of `1e-6`. VEF multiplies the shape by the user's annual demand; it records that this is an estimate. |
| `COMPONENT_CATALOG` | Stable component ID, type (`PV_MODULE`, `INVERTER`, or `BATTERY`), display name, purchase price in EUR, technical attributes with units, availability flag, source, and catalog version. IDs are never reused for materially different equipment. |

For v1, the component catalog MUST include `ratedPowerKWp` and `areaM2` for a PV module; `acPowerKW` and `efficiencyFraction` for an inverter; and `usableCapacityKWh`, `maxChargePowerKW`, `maxDischargePowerKW`, and `roundTripEfficiencyFraction` for a battery. Every component has `unitPriceEUR`. Fractions are in `[0, 1]`; capacities, power, area, and price are non-negative. VEF owns compatibility and configuration rules; ODIP publishes the attributes and their provenance. Missing required technical attributes or unknown units make a component ineligible.

ODIP core MUST verify generic publication integrity, recorded provenance, access policy, and the result of the named validation policy. The energy adapter MUST check interval completeness, duplicate timestamps, numeric ranges, currency and unit consistency, catalog identity, and usage rights under `urn:portfolio:energy-quality:v1`. A published manifest identifies the policy version and result of every required check. ODIP implements the generic manifest contract and pins its schema from the released shared kit; the energy profile and fixtures are shared contract artifacts that the reference adapter and VEF both test. Their repository location and ownership are defined by DEC-06: this repository owns the released shared kit.

## 4 Customer request and optimization contract

VEF owns the customer-facing API and the request. The proposed endpoints are:

| Method and path | Purpose |
| --- | --- |
| `POST /api/v1/optimization-runs` | Validate and start a run; return an immutable run ID and initial status. |
| `GET /api/v1/optimization-runs/{runId}` | Read status, pinned inputs, result, warnings, and failure details. |
| `GET /api/v1/optimization-runs/{runId}/candidates` | Read bounded ranked candidates and their metrics. |

`POST` accepts an `Idempotency-Key` scoped to the authenticated caller. Repeating the same key and identical body returns the original run; reusing the key with different content returns `409 idempotency_conflict`. A run transitions `QUEUED → RUNNING → SUCCEEDED`, `FAILED`, or `INFEASIBLE`. A failed run must not masquerade as an infeasible engineering problem. The response identifies whether optimality was proved.

Example request, with illustrative values:

```json
{
  "schemaVersion": "energy-optimization-request/v1",
  "dataset": {
    "datasetId": "energy-reference-wasserburg-am-inn-2024",
    "version": "1.0.0",
    "schemaRef": "urn:portfolio:energy-configuration-input:v1"
  },
  "site": {
    "regionCode": "DE-BY-09187182",
    "usableRoofAreaM2": 35.0,
    "annualDemandKWh": 4500.0,
    "existingComponentIds": []
  },
  "constraints": {
    "maxInitialInvestmentEUR": 18000.0,
    "minSelfSufficiency": 0.55
  },
  "objective": "MIN_ANNUALIZED_COST",
  "assumptions": {
    "analysisYears": 20,
    "discountRate": 0.04
  }
}
```

VEF MUST reject negative areas, demand, prices, or limits; a self-sufficiency threshold outside `[0, 1]`; an unsupported region, dataset version, or `schemaRef`; and requests exceeding published model or search bounds. A catalog contains at most 20 models of each component type. A configuration contains 1 to 100 PV modules, exactly one inverter, and 0 to 4 batteries. VEF estimates the search space before starting a run and returns `422 search_space_limit_exceeded` without creating a run if more than 100,000 candidate evaluations would be required. Candidate-list responses are paginated with at most 100 candidates per page. The limits are advertised by a capability endpoint. VEF derives the hourly load from `annualDemandKWh × REFERENCE_LOAD_SHAPE` and records the load-shape artifact digest.

`site.existingComponentIds` MUST be `[]` for the current new-equipment release. A non-empty list MUST return `422 existing_equipment_not_supported` before run creation. All selected components MUST be new (`existing: false` in candidate selections). VEF MUST NOT silently ignore existing-equipment inputs. Support for existing equipment requires a later version with shared quantity, ownership, compatibility, costing and identity examples under DEC-07.

### 4.1 Feasibility and simulation

VEF MUST version its energy feature model, compatibility rules, and simulation algorithm independently of the ODIP dataset publication. A candidate is feasible only if component availability, roof area, electrical ratings, battery limits, investment limit, and minimum self-sufficiency all pass. The first release may enumerate a bounded catalog exhaustively; larger spaces require a solver and an explicit optimality statement.

The v1 simulation uses one-hour intervals. DC generation is installed PV capacity in `kWp` multiplied by that interval's `PV_YIELD_PER_KWP`. Inverter efficiency is applied before the AC power limit: `pvAcKWh = min(pvDcKWh * inverterEfficiency, inverterAcPowerKW * 1 h)`. The difference between efficiency-adjusted potential output and the inverter limit is recorded as inverter clipping.

PV generation serves the building load first. Surplus charges the battery within its usable-capacity and charge-power limits; remaining surplus is exported. When PV is insufficient, the battery discharges within its state-of-charge and discharge-power limits; the remainder is imported. Grid charging and simultaneous charging and discharging are prohibited. Battery charge and discharge power limits are AC-side limits. Charge and discharge efficiencies each use the square root of the battery's recorded round-trip efficiency. State of charge changes by `chargeAcKWh * chargeEfficiency - dischargeAcKWh / dischargeEfficiency` and begins at zero. Any state of charge remaining after the final interval is recorded as `terminalDiscardedEnergyKWh`, receives no cost or self-sufficiency credit, and is discarded so the modeled year ends at zero. A domain reviewer must approve these assumptions before v1 is accepted.

The hourly simulation MUST conserve energy within a documented numeric tolerance, bound battery state of charge, and prevent simultaneous contradictory flows. It calculates yearly grid import, grid export, on-site solar use, and unmet demand. The first release treats unmet demand as invalid. Every selected component is new in this release and contributes to the simulated output and initial investment. It computes:

```text
selfSufficiency = 1 - annualGridImportKWh / annualDemandKWh
annualizedCostEUR = initialInvestmentEUR * capitalRecoveryFactor
                  + annualOperationsEUR
                  + sum(hourlyGridImportKWh * hourlyImportTariffEURPerKWh)
                  - sum(hourlyGridExportKWh * hourlyExportTariffEURPerKWh)
capitalRecoveryFactor = r(1+r)^n / ((1+r)^n - 1), or 1/n when r = 0
```

`n` is `analysisYears`, and `r` is `discountRate`. The first release fixes these values at 20 years and `0.04`. Every component has a modeled economic lifetime of 20 years. Replacement, residual value, maintenance, installation labor, taxes, and subsidies are excluded, and `annualOperationsEUR` is zero. Initial investment is the sum of unit price multiplied by every selected new component quantity. Existing-equipment costing is deferred under DEC-07. VEF must not compare candidates whose metrics were computed under different dataset, model, or simulation versions within one run. The recommendation minimizes `annualizedCostEUR` rounded to cents; ties use initial investment rounded to cents and then lexical configuration ID. The result discloses the excluded costs and assumptions.

Implementations use IEEE-754 binary64 calculations without intermediate rounding. Energy outputs are serialized to six decimal places and monetary outputs to two decimal places using round-half-to-even. The absolute energy-balance tolerance is `1e-6 kWh` per hourly interval; dimensionless comparisons, including self-sufficiency, use an absolute tolerance of `1e-9`. Contract tests compare serialized monetary values exactly and serialized energy values within `1e-6 kWh`.

### 4.2 Result envelope

Every completed or infeasible run MUST expose the following fields, even if its candidate list is empty:

```json
{
  "schemaVersion": "energy-optimization-result/v1",
  "runId": "<stable run ID>",
  "status": "SUCCEEDED",
  "dataset": {
    "datasetId": "energy-reference-wasserburg-am-inn-2024",
    "version": "1.0.0",
    "schemaRef": "urn:portfolio:energy-configuration-input:v1",
    "manifestSha256": "<verified digest>"
  },
  "modelVersion": "energy-model/1.0.0",
  "simulationVersion": "energy-simulation/1.0.0",
  "optimizerVersion": "energy-optimizer/1.0.0",
  "optimalityStatus": "PROVEN_OPTIMAL",
  "evaluatedCandidateCount": 120,
  "feasibleCandidateCount": 8,
  "recommendedConfigurationId": "<configuration ID>",
  "warnings": [],
  "createdAt": "<UTC instant>",
  "completedAt": "<UTC instant>"
}
```

An individual candidate includes component IDs and quantities, constraint evaluations, initial investment, annualized cost, self-sufficiency, import/export energy, inverter clipping, terminal discarded energy, and a deterministic configuration ID. `optimalityStatus` is one of `PROVEN_OPTIMAL`, `FEASIBLE_NOT_PROVEN`, or `NOT_APPLICABLE`. VEF may claim `PROVEN_OPTIMAL` only with exhaustive enumeration or a solver proof for the exact stated search space. An infeasible run returns violated requirements and diagnostic counts where available; it must not fabricate a recommendation.

## 5 AI assistance contract

Kit `0.5.0` packages these requirements in the normative
[VEF AI assistance profile](contract-kit/ai/README.md), proposal and explanation
schemas, examples, semantic citation checks, and consumer acceptance cases.
This additive VEF handoff leaves the accepted `0.4.0` ODIP and numerical
contracts unchanged. The `0.5.0` implementation handoff does not establish
Gate 6 acceptance or authorize the final `1.0.0` release.

The AI layer belongs to the VEF user journey in the first release. It may propose a structured customer request from natural language and explain a completed run. The structured request is shown to the user for confirmation before optimization. The AI layer reads only a bounded result and approved evidence from ODIP and VEF; it does not call database connections, change component rules, publish ODIP data, or choose a recommendation independently of the optimizer.

An explanation MUST cite the run ID, dataset ID and version, model and simulation versions, recommended configuration ID, main constraint outcomes, and at least the cost and self-sufficiency metrics. It MUST distinguish measured source data, derived reference profiles, customer inputs, model assumptions, and calculated outputs. If evidence is absent, the explanation reports the gap. A deterministic template is useful while validating the configuration contract, but the AI-assisted release additionally requires the reviewed natural-language input proposal and evidence-grounded AI explanation described here.

## 6 Security and operational contract

### 6.1 Hosted identity and application authorization

- Hosted identity uses the platform-managed access boundary, one environment realm (the reference profile uses `/realms/platform`), separate application clients and audiences, and project-scoped application groups. Applications do not configure a dedicated realm, client IDs, OAuth scopes, or provider roles. Platform administration grants do not confer application-group membership.
- ODIP exposes its generic publication GET routes through a `bearer-token` access policy on its one public component. Its project administrator approves VEF's service-access request with only the reader group's stable ID. VEF obtains access tokens through `client_credentials` using the managed project-secret binding; token lifetime is at most five minutes. The boundary validates signature, issuer, access-token type, derived audience, validity times, subject, client ID, approved service state, and client-scoped groups. Missing or invalid bearer authentication returns `401` without a redirect; group or service-approval denial returns `403`.
- The boundary strips caller-supplied identity headers, bearer tokens, and platform session cookies and forwards normalized `X-Platform-Principal-*` context. ODIP and VEF middleware MUST reject missing or malformed required context. Headers are trusted only on the enforced boundary-to-private-backend path; direct backend ingress, including from another component in the same project, MUST be denied. Applications do not repeat platform JWT validation or coarse route-group checks.
- ODIP independently authorizes the stable VEF service principal against a read-only allow-list containing `energy-reference-wasserburg-am-inn-2024` and its published versions. This finer dataset decision is not inferred from the reader-group name, client ID, or network location. Normal credential rotation preserves the principal ID and changes the client ID. Catalog, ingestion, and publication writes require separately approved writer routes and domain authority; the reference reader policy exposes no writes.
- VEF's customer routes use `browser-session` with an approved application-user group. First login creates a pending request, not access. An administrator approves membership explicitly. VEF scopes run ownership and `Idempotency-Key` to the stable principal ID. State-changing browser requests require the boundary's CSRF token and same-origin `Origin` header. A route/method cannot simultaneously accept browser and bearer authentication; machine VEF access requires separate non-overlapping routes and policy changes.
- Stable principal ID, kind, issuer, subject, and space-delimited group IDs are required; service context additionally includes a validated client ID. Display name and email are optional, disabled in the reference policies, and never authorization keys. The exact executable context schema and examples are in the kit.
- Membership revocation overrides still-valid token claims. Authorization snapshots expire within five minutes and fail closed after expiry; signing-key verification failures fail closed. Access-layer errors use the platform `application_access_*` body rather than the application's `error/v1` envelope. Browser login may return `302`; dependency failure may return `503`. Public OpenAPI contracts describe these responses separately.

### 6.2 Deployment, network, and credentials

- ODIP and VEF use separate projects, each declaring `platform.example/v1alpha2`, one public service, at most five total service/scheduled components, and its own `shared-dev` PostgreSQL database with `deletionPolicy: retain`. The ODIP API and worker share the ODIP project/database. Application owners supply images, commands, schedules, readiness, and bounded resources. Image digests are recorded before deployment; illustrative kit image tags are not released workloads.
- VEF reaches ODIP through stable public HTTPS. Each calling component declares only the ODIP hostname and managed token-endpoint hostname on TCP 443; platform DNS is supplied separately. Operators must approve the destination CIDRs/port. DNS declarations are resolved to fixed addresses at apply time; address changes require reapply. ODIP itself needs no identity-provider egress to authenticate inbound requests; the platform access layer owns signing-key retrieval. Ingestion-source exceptions are declared separately on the worker. Cross-origin artifact paths and redirects are rejected.
- Credentials are delivered through the consumer project's managed secret path. The project, not the component, is the isolation boundary: every VEF component may receive the service binding. Components needing another trust boundary require another project. Secrets are write-only through ordinary platform APIs and absent from desired state, images, logs, metrics, publications, and results. Read the binding's `secretPrefix` and its `_CLIENT_ID`, `_CLIENT_SECRET`, and `_TOKEN_URL` values instead of hard-coding client names.
- Rotate at least every 90 days through the platform service-access lifecycle. Normal rotation publishes a replacement binding, permits at most 24 hours overlap, and requires consumer adoption confirmation; emergency rotation revokes the old client without overlap. The platform does not itself establish a 90-day rotation schedule; the consumer owner must arrange it.
- Cross-project traffic is encrypted through public HTTPS. Application-to-PostgreSQL traffic is not TLS-protected in this accepted single-host lab profile. Do not claim all application traffic is encrypted. Applications use the platform-injected `PG*` connection values and never read another project's database.
- Readiness is private and application-owned: ODIP checks API/database availability; VEF checks API/database/rules while reporting temporary ODIP unavailability separately. A schedule has no readiness dependency ordering and must retry transient failures. Restricted containers run without root, with a read-only root filesystem and bounded ephemeral `/tmp`; persistent artifacts and results belong in backed-up project storage. The current profile supplies no application PVC. ODIP must persist artifact bytes in its database or separately provision supported durable storage before claiming restart/recovery acceptance.
- Public component monitoring uses the declared hostname/readiness path. Protected probes are unauthenticated access-boundary checks expecting `302`, `401`, or `403`, without redirects; `200` and `503` fail them. Kubernetes readiness is the separate semantic health signal. Private services and schedules have no public probe. Monitoring grants no application membership and creates no anonymous health route.
- Central operational logs use the domain-neutral `operational-envelope-v1` JSON shape: an allowed event, level, and optional opaque lowercase UUID/32-hex correlation ID. ODIP and VEF propagate that ID and retain its association with dataset/version/run in their owned evidence. Customer details, tokens, domain IDs, and arbitrary messages do not belong in the central envelope. The collector strips unknown fields and drops invalid/oversized/free-text lines. The kit emission schema excludes extra fields; applications emit compact JSON within 4 KB. Correlation is Internal under the reference governance and never a metric or stream-index label.
- The platform supplies project/component attribution, dedicated read-only Kubernetes collection, and revision/operation annotations as non-indexed log metadata. Existing pods require reapply/restart for new metadata. Authenticated control-plane `GET /projects/{name}/retained-logs` requires project view permission, enforces fixed selectors and bounded filters, and audits reads; applications/users receive no direct shared Loki/Grafana access. HTTP `200` with `state: unavailable` and `reason: CentralLogUnavailable` is a backend failure, not successful empty output. Seven-day retention is configured; deployed ingestion and elapsed expiry remain open acceptance work. Collection outages may lose events.
- Application metrics must include publication/retrieval failures, queue age, run duration, invalid requests, infeasible results, and simulation errors. Workload usage scrapes, application request metrics, and traces are not supplied by this platform logging increment; application metrics and any future tracing require their own implementation/evidence.
- ODIP backs up manifests, artifacts, and provenance; VEF backs up requests, pinned inputs, models, and results. Backup restoration must reconcile the platform access catalog, provider clients/groups, and credentials before protected routes reopen, invalidate browser sessions, and preserve revocation denial. A restart or reconciliation rehearsal alone is not a backup-restore proof.
- A run has a five-minute execution timeout and ends as `FAILED` with `run_timeout`, never `INFEASIBLE`, on timeout.

### 6.3 Governance and retention

Project governance is submitted separately from deployment and access policies. Platform classifications are `Public` for published fixtures/provenance, `Internal` for ODIP working data and sanitized telemetry, `Confidential` for VEF requests/results/evidence, and `Restricted` for managed secrets. `Restricted` is not a supported ordinary project-data declaration. The reference governance records declare ODIP's maximum as `Internal`, VEF's as `Confidential`, telemetry as `Internal`, no optional personal attributes, and named retention/purge/recovery owners. The first release does not collect names, exact street addresses, account numbers, or free-form customer notes.

ODIP versions remain while their contract is supported and for one year afterward; VEF rows/evidence remain for 180 days after completion. Applications enforce domain-row deletion while projects are active. Platform retirement retains the whole project database until explicitly authorized purge. The platform backup policy keeps the latest verified snapshot plus 14 daily, 8 weekly, and 6 monthly recovery points; expired live rows may remain until containing snapshots expire. Minimized centralized workload logs have seven-day retention configured, with deployed ingestion and elapsed-retention acceptance still open, and metrics retain seven days or 4 GB. Platform audit events are append-only without automatic expiry; application-owned security audit records retain 180 days. Platform pending access requests expire after 30 days; terminal requests and revoked memberships retain 90 days. These replace the earlier blanket 30-day log/backup retention assumption; domain deletion must not be presented as deletion from all recovery points.

The pinned implementation, generated input-schema snapshot, deployment/access/governance examples, compatibility notes, and remaining acceptance obligations are shipped under `contract-kit/platform/`. They describe a reconciled implementation boundary, not completed energy-workflow deployment evidence.

## 7 Contract tests and release acceptance

Before the contract is marked accepted, the teams MUST commit common fixtures with expected manifest, artifact digests, feasible configurations, simulation totals, and recommendation. ODIP and VEF should each run the same schema and example checks in CI. The deployed test must include:

1. Ingest source fixtures, publish energy dataset version `1.0.0` through the generic ODIP API, retrieve its manifest and all five artifacts, and verify checksums and quality status. Publish a non-energy fixture through the same API to prove that the core is domain independent.
2. Submit a request using that exact dataset version and energy `schemaRef`; verify the expected feasible set, cost and self-sufficiency values, recommendation, and provenance.
3. Reject a modified artifact, wrong unit, missing hour, partial or non-calendar-year period, unpublished version, unsupported schema major, invalid customer input, non-empty existing-equipment list, unauthorized caller, and repeated idempotency key with a changed body.
4. Publish dataset version `1.0.1`, confirm an existing run still names and reproduces `1.0.0`, then start a new run explicitly pinned to `1.0.1`.
5. Verify public component probes separately from Kubernetes readiness and authenticated publication retrieval. Emit/propagate safe operational correlation and read it only through project-authorized retained-log access; prove foreign-project denial and treat backend-unavailable state as failure.
6. Restart ODIP and VEF, verify retained state and one reproducible completed run, and verify retained operational events after pod retirement/restart. Capture collector/backend health and gaps; record separate seven-day expiry/compactor evidence and actual backup restore.
7. For the AI-assisted release, turn representative natural-language requests into structured proposals for user confirmation; verify that explanations cite the recorded result and refuse to invent a price, capability, or optimality claim when the evidence is absent. Test prompt injection contained in source metadata.

Passing local unit tests or deploying the three containers separately does not satisfy this end-to-end acceptance condition.

Contract acceptance is the final integration gate in the [integration plan](energy-configuration-integration-plan.md). Changes to this document MUST identify affected contract versions and corresponding tests.

## 8 Shared contract kit ownership and releases

This repository is the source of truth for the shared contract kit under `contract-kit/`. The Integration Contract Maintainer owns its versions and releases. ODIP, VEF, and Developer Platform maintainers review changes affecting their boundaries; simulation behavior, tolerances, fixtures, and numerical expected results additionally require domain-review approval.

The kit uses semantic versions. Breaking schema, API, simulation, validation, or expected-result changes increment the major version; during pre-1.0 development, incompatible changes increment the minor version and are explicitly identified as breaking. Backward-compatible optional fields and additive fixtures increment the minor version. Corrections that do not alter contract behavior increment the patch version.

A release is created only from a reviewed change after schema, OpenAPI, example, canonical-serialization, checksum, and numerical-result tests pass. It contains a deterministic archive, `SHA256SUMS`, compatibility notes, and an annotated Git tag named `contract-kit-v{version}`. Release artifacts and tags are immutable. ODIP and VEF pin both the exact version and archive checksum in CI and do not consume a mutable branch. The original implementation baseline was `0.2.0`; the identity reconciliation was `0.3.0`. Kit `0.4.0` adds operational envelopes/monitoring without changing those identity or energy contracts. Version `1.0.0` is released only after the integration and release gates pass.

Repository-authored schemas, OpenAPI definitions, tests, tooling, and software configuration are licensed under Apache-2.0. Repository-authored documentation, examples, synthetic fixtures, and expected results are licensed under CC BY 4.0. Third-party material retains its source terms; every release carries its attribution and modification status in `NOTICE` and artifact provenance and includes the complete applicable license texts.
