# AI-Assisted Energy System Configuration Integration Contract

**Status:** Proposed contract, version 0.2  
**Date:** 2026-10-09  
**Owners:** Developer Platform, Open Data Intelligence Platform, and Variability Engineering Framework maintainers  
**Purpose:** Define the normative interfaces and operational boundaries between the three projects for the energy-system configuration use case.

This contract implements the behavior described in the [use case definition](energy-configuration-use-case.md). Delivery order, repository work packages, and integration gates are defined in the [integration plan](energy-configuration-integration-plan.md). Use-case intent belongs in the use case definition; delivery status belongs in the plan. This document is limited to testable obligations at project boundaries.

The proposed endpoints and payloads do not exist in the repositories unless a section explicitly says otherwise. The contract becomes binding only when the three project teams accept a version and add corresponding contract tests. Until then, normative words such as **MUST** express requirements of this proposal, not claims about current behavior.

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
| Authenticate application users and VEF retrieval from ODIP | Supplies runtime and secret facilities; platform administration identity is separate | Enforces dataset-scoped API permissions | Enforces its API permissions and holds a read-only ODIP identity |
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
8. Each API rejects unknown major versions and unknown required fields with a machine-readable error. Additive optional fields may be ignored only when their semantics do not change existing calculations.
9. Service-to-service traffic uses an authenticated, encrypted channel. Secrets and bearer tokens never appear in a publication, result, log, or explanation.

## 3 ODIP publication and energy consumer contract

### 3.1 Publication and retrieval

ODIP MUST expose a generic `DatasetPublication` for any dataset that has passed its applicable validation policy. The proposed read endpoints contain no domain name:

| Method and path | Purpose | Access |
| --- | --- | --- |
| `GET /api/v1/datasets?status=PUBLISHED&schemaRef={schemaRef}` | Discover published dataset IDs and versions. The schema filter is optional. | Dataset-scoped `dataset.read` |
| `GET /api/v1/datasets/{datasetId}/versions/{version}` | Retrieve an immutable publication manifest. | Dataset-scoped `dataset.read` |
| `GET /api/v1/datasets/{datasetId}/versions/{version}/artifacts/{artifactId}` | Download one immutable artifact by ID. | Dataset-scoped `dataset.read` |

ODIP returns `ETag` equal to the manifest or artifact SHA-256 digest and supports conditional retrieval with `If-None-Match`. A version missing from the catalog returns `404`; a version that exists but is not published returns `409 dataset_version_not_published`; lack of authority returns `401` or `403`. ODIP must not return a partially published dataset version. These routes are proposed extensions of the current dataset catalog and version APIs, not claims that they already exist.

The manifest is a small generic JSON document. `schemaRef` identifies the domain contract; `metadata` and artifact `role` values are interpreted by the referenced schema, not by the ODIP core. Large data artifacts are downloaded separately. The example below shows a publication using the energy profile; its values are illustrative rather than real measurements or usable checksums:

```json
{
  "schemaVersion": "dataset-publication/v1",
  "datasetId": "energy-reference-berlin-2025",
  "version": "1.0.0",
  "status": "PUBLISHED",
  "schemaRef": "urn:portfolio:energy-configuration-input:v1",
  "metadata": {
    "regionCode": "DE-BE",
    "period": {
      "start": "2025-01-01T00:00:00Z",
      "endExclusive": "2026-01-01T00:00:00Z",
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

| Role | Required contents and validation |
| --- | --- |
| `PV_YIELD_PER_KWP` | Non-negative hourly DC energy per installed kWp, before inverter and battery losses, for the stated region and period. Method, source, orientation assumptions, and included upstream losses are versioned in provenance. |
| `IMPORT_TARIFF` and `EXPORT_TARIFF` | Non-negative hourly prices in EUR/kWh; each has exactly the same intervals as the yield series. Taxes and fixed fees are excluded in v1 and disclosed as limitations. |
| `REFERENCE_LOAD_SHAPE` | Non-negative hourly fractions summing to 1 within a declared tolerance of `1e-6`. VEF multiplies the shape by the user's annual demand; it records that this is an estimate. |
| `COMPONENT_CATALOG` | Stable component ID, type (`PV_MODULE`, `INVERTER`, or `BATTERY`), display name, purchase price in EUR, technical attributes with units, availability flag, source, and catalog version. IDs are never reused for materially different equipment. |

For v1, the component catalog MUST include `ratedPowerKWp` and `areaM2` for a PV module; `acPowerKW` and `efficiencyFraction` for an inverter; and `usableCapacityKWh`, `maxChargePowerKW`, `maxDischargePowerKW`, and `roundTripEfficiencyFraction` for a battery. Every component has `unitPriceEUR`. Fractions are in `[0, 1]`; capacities, power, area, and price are non-negative. VEF owns compatibility and configuration rules; ODIP publishes the attributes and their provenance. Missing required technical attributes or unknown units make a component ineligible.

ODIP core MUST verify generic publication integrity, recorded provenance, access policy, and the result of the named validation policy. The energy adapter MUST check interval completeness, duplicate timestamps, numeric ranges, currency and unit consistency, catalog identity, and usage rights under `urn:portfolio:energy-quality:v1`. A published manifest identifies the policy version and result of every required check. The generic manifest schema belongs in ODIP `contracts/`; the energy profile and fixtures are shared contract artifacts that the reference adapter and VEF both test. Their repository location and ownership remain an open decision.

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
    "datasetId": "energy-reference-berlin-2025",
    "version": "1.0.0",
    "schemaRef": "urn:portfolio:energy-configuration-input:v1"
  },
  "site": {
    "regionCode": "DE-BE",
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

VEF MUST reject negative areas, demand, prices, or limits; a self-sufficiency threshold outside `[0, 1]`; an unsupported region, dataset version, or `schemaRef`; and requests exceeding published model or search bounds. The exact limits are advertised by a capability endpoint or documented with the v1 contract. VEF derives the hourly load from `annualDemandKWh × REFERENCE_LOAD_SHAPE` and records the load-shape artifact digest.

### 4.1 Feasibility and simulation

VEF MUST version its energy feature model, compatibility rules, and simulation algorithm independently of the ODIP dataset publication. A candidate is feasible only if component availability, roof area, electrical ratings, battery limits, existing-equipment compatibility, investment limit, and minimum self-sufficiency all pass. The first release may enumerate a bounded catalog exhaustively; larger spaces require a solver and an explicit optimality statement.

The proposed v1 hourly dispatch uses PV generation to serve the building load first. Surplus charges the battery within its power and capacity limits; remaining surplus is exported. When PV is insufficient, the battery discharges within its limits; the remainder is imported. Grid charging is excluded. Inverter AC output is bounded by `acPowerKW` and calculated from DC yield with the selected inverter's efficiency. Charge and discharge each use the square root of the battery's recorded round-trip efficiency. Battery state of charge begins and ends the modeled year at zero. A domain reviewer must approve these assumptions before v1 is accepted.

The hourly simulation MUST conserve energy within a documented numeric tolerance, bound battery state of charge, and prevent simultaneous contradictory flows. It calculates yearly grid import, grid export, on-site solar use, and unmet demand. The first release treats unmet demand as invalid. Existing equipment is included in compatibility and output calculations but excluded from new initial investment. It computes:

```text
selfSufficiency = 1 - annualGridImportKWh / annualDemandKWh
annualizedCostEUR = initialInvestmentEUR * capitalRecoveryFactor
                  + annualOperationsEUR
                  + sum(hourlyGridImportKWh * hourlyImportTariffEURPerKWh)
                  - sum(hourlyGridExportKWh * hourlyExportTariffEURPerKWh)
capitalRecoveryFactor = r(1+r)^n / ((1+r)^n - 1), or 1/n when r = 0
```

`n` is `analysisYears`, and `r` is `discountRate`. VEF documents what is included in initial investment and annual operations. It must not compare candidates whose metrics were computed under different dataset, model, or simulation versions within one run. The recommendation minimizes `annualizedCostEUR` among feasible candidates; ties use lower initial investment, then lexical configuration ID. The result discloses excluded costs and assumptions.

### 4.2 Result envelope

Every completed or infeasible run MUST expose the following fields, even if its candidate list is empty:

```json
{
  "schemaVersion": "energy-optimization-result/v1",
  "runId": "<stable run ID>",
  "status": "SUCCEEDED",
  "dataset": {
    "datasetId": "energy-reference-berlin-2025",
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

An individual candidate includes component IDs and quantities, constraint evaluations, initial investment, annualized cost, self-sufficiency, import/export energy, and a deterministic configuration ID. `optimalityStatus` is one of `PROVEN_OPTIMAL`, `FEASIBLE_NOT_PROVEN`, or `NOT_APPLICABLE`. VEF may claim `PROVEN_OPTIMAL` only with exhaustive enumeration or a solver proof for the exact stated search space. An infeasible run returns violated requirements and diagnostic counts where available; it must not fabricate a recommendation.

## 5 AI assistance contract

The AI layer belongs to the VEF user journey in the first release. It may propose a structured customer request from natural language and explain a completed run. The structured request is shown to the user for confirmation before optimization. The AI layer reads only a bounded result and approved evidence from ODIP and VEF; it does not call database connections, change component rules, publish ODIP data, or choose a recommendation independently of the optimizer.

An explanation MUST cite the run ID, dataset ID and version, model and simulation versions, recommended configuration ID, main constraint outcomes, and at least the cost and self-sufficiency metrics. It MUST distinguish measured source data, derived reference profiles, customer inputs, model assumptions, and calculated outputs. If evidence is absent, the explanation reports the gap. A deterministic template is useful while validating the configuration contract, but the AI-assisted release additionally requires the reviewed natural-language input proposal and evidence-grounded AI explanation described here.

## 6 Security and operational contract

- ODIP validates dataset-scoped read permission on generic publication endpoints and write permission on catalog, ingestion, and publication endpoints. VEF uses a read-only service identity. Hosted-application permissions are separate from Developer Platform grants.
- The initial inter-project route may use ODIP's HTTPS application ingress with a Developer Platform egress allow-list. The teams must verify DNS resolution, TLS, routing, and allowed/denied traffic in the target installation. A private cross-project route is a separate platform feature if public ingress is unsuitable.
- Each deployment uses an immutable image digest or release-specific tag. Configuration and credentials are injected through the platform's supported configuration and secret mechanisms. ODIP and VEF use separate project databases.
- ODIP readiness requires its API and database to serve published metadata. VEF readiness requires its API, database, and loaded rules; temporary ODIP unavailability is reported separately and does not erase cached validated dataset versions.
- Logs and traces correlate `datasetId`, `datasetVersion`, and `runId` without logging customer details or tokens. Metrics include publication failures, dataset retrieval failures, queue age, run duration, invalid requests, infeasible results, and simulation errors.
- ODIP backs up manifests, artifacts, and provenance. VEF backs up customer requests, pinned input digests, models, and optimization results. A recovery drill must recreate an application container and reproduce one recorded result.

## 7 Contract tests and release acceptance

Before the contract is marked accepted, the teams MUST commit common fixtures with expected manifest, artifact digests, feasible configurations, simulation totals, and recommendation. ODIP and VEF should each run the same schema and example checks in CI. The deployed test must include:

1. Ingest source fixtures, publish energy dataset version `1.0.0` through the generic ODIP API, retrieve its manifest and all five artifacts, and verify checksums and quality status. Publish a non-energy fixture through the same API to prove that the core is domain independent.
2. Submit a request using that exact dataset version and energy `schemaRef`; verify the expected feasible set, cost and self-sufficiency values, recommendation, and provenance.
3. Reject a modified artifact, wrong unit, missing hour, unpublished version, unsupported schema major, invalid customer input, unauthorized caller, and repeated idempotency key with a changed body.
4. Publish dataset version `1.0.1`, confirm an existing run still names and reproduces `1.0.0`, then start a new run explicitly pinned to `1.0.1`.
5. Restart ODIP and VEF containers, verify retained state and one reproducible completed run, and record resource usage and relevant logs.
6. For the AI-assisted release, turn representative natural-language requests into structured proposals for user confirmation; verify that explanations cite the recorded result and refuse to invent a price, capability, or optimality claim when the evidence is absent. Test prompt injection contained in source metadata.

Passing local unit tests or deploying the three containers separately does not satisfy this end-to-end acceptance condition.

Contract acceptance is the final integration gate in the [integration plan](energy-configuration-integration-plan.md). Changes to this document MUST identify affected contract versions and corresponding tests.
