# AI-Assisted Energy System Configuration Use Case

**Status:** Accepted current-release scope, version 0.4
**Date:** 2026-10-27
**Owners:** Developer Platform, Open Data Intelligence Platform, and Variability Engineering Framework maintainers
**Purpose:** Define the user outcome, bounded scope, and observable behavior of the first end-to-end energy-system configuration demonstration.

The normative system interfaces are defined in the [integration contract](energy-configuration-integration-contract.md). The work needed to deliver them is ordered in the [integration plan](energy-configuration-integration-plan.md).

The maintainer accepted a new-equipment-only current release on October 27 in [DEC-07](decisions/DEC-07-new-equipment-release-scope.md). Version 0.3 narrows the original 0.2 scope accordingly; existing-equipment support is deferred. Implementation and remaining acceptance evidence are tracked in the [cross-project review](reviews/2026-10-27-implementation-and-acceptance-review.md) and [gap register](reviews/2026-10-27-gap-analysis.md).

Version 0.4 also records [DEC-10](decisions/DEC-10-current-release-recovery-test-exception.md): the maintainer accepts the current release without an isolated joint backup/restore test. This is an explicit acceptance exception with restoration unverified; remaining acceptance cases and backup/storage/security duties are unchanged.

## 1 Use case summary

| Field | Definition |
| --- | --- |
| ID | `UC-ENERGY-01` |
| Name | Configure a modular building energy system |
| Primary actor | Energy consultant |
| Goal | Find the least expensive technically valid photovoltaic, inverter, and battery configuration that satisfies the customer's constraints. |
| Trigger | The consultant starts a configuration for a building. |
| Result | A reproducible recommendation with cost and self-sufficiency estimates, or a precise infeasibility explanation. |
| Release type | Bounded demonstration; not a certified engineering design or production quotation. |

The consultant provides the building region, usable roof area, annual electricity demand, investment limit and minimum desired self-sufficiency for a new installation. Existing-equipment inputs must be empty in this release. The system evaluates technically valid combinations against identified reference data and a versioned simulation model. An AI assistant may turn the consultant's words into a proposed structured request and may explain the recorded result, but it does not determine feasibility or calculate numerical results.

## 2 Intended value and success condition

The use case demonstrates that three independently owned projects can cooperate without sharing databases or hiding the origin of calculated results:

- ODIP supplies governed, versioned, and traceable reference data.
- VEF applies the energy configuration model, simulation, and optimization.
- Developer Platform deploys and operates both applications with explicit connectivity, identity, persistence, and observability.

The use case succeeds when a consultant can submit a request, receive at least one valid configuration or a precise infeasibility explanation, inspect the data and model versions behind every number, change a constraint, and reproduce the same result from recorded inputs. The complete flow runs with ODIP and VEF deployed as separate applications on the Developer Platform.

## 3 Scope

### 3.1 First release

The first release contains:

- one reference region;
- one complete Gregorian calendar year of hourly UTC reference data: January 1 at 00:00 UTC through January 1 of the following year, 8,760 or 8,784 aligned hours under [DEC-08](decisions/DEC-08-complete-calendar-year.md);
- a small catalog of photovoltaic modules, inverters, and batteries;
- new-equipment configurations with customer constraints for roof area, investment and self-sufficiency;
- a documented and versioned hourly simulation;
- deterministic candidate ranking by annualized cost;
- provenance from the recommendation back to the exact data, model, and simulation versions;
- a user-reviewed natural-language input proposal and an evidence-grounded result explanation for the AI-assisted release.

Synthetic fixtures are acceptable for the initial deployed demonstration. Real building measurements and commercial offers enter scope only after usage rights, quality, and privacy requirements have been established.

### 3.2 Excluded from the first release

The first release excludes partial-year and rolling-year optimization, reuse, expansion or replacement planning for existing equipment, as well as heat pumps, electric vehicles, grid-connection approval, installation labor, taxes, subsidies, dynamic degradation, automatic purchasing, multi-objective Pareto search, and conversational data exploration.

## 4 Actors and responsibilities

| Actor or system | Use-case responsibility |
| --- | --- |
| Consultant | Supplies and confirms customer inputs, reviews the recommendation and limitations, and may adjust constraints. |
| ODIP | Ingests, validates, versions, and publishes the reference dataset and its provenance. |
| Energy adapter | Maps source data into the energy input profile and applies energy-specific quality rules without introducing energy semantics into ODIP core. |
| VEF | Validates the request and dataset, generates compatible configurations, simulates them, applies constraints, ranks feasible candidates, and presents the outcome. |
| AI assistant | Proposes structured inputs for confirmation and explains only evidence present in a completed run. |
| Developer Platform | Runs ODIP and VEF as isolated applications and provides their databases, secrets, routing, health checks, resource controls, and observability. |
| Domain reviewer | For the bounded demonstration, the sole cross-project maintainer reviews the energy-model and simulation assumptions. Independent qualified review is required before production or certified-engineering use. |

## 5 Preconditions

1. A reference dataset has passed its required quality checks and is published as an immutable version.
2. Its source owner, usage right or license, retrieval time, source version where available, and transformation version are recorded.
3. VEF supports the dataset's energy-profile major version and has loaded compatible model, simulation, and optimizer versions.
4. The consultant is authorized to use the VEF workflow, and VEF is authorized to read the selected ODIP dataset.
5. The reference region, search bounds, and documented modeling limitations are visible to the consultant.

## 6 Main success scenario

1. The consultant describes the building and desired outcome, either through structured fields or natural language.
2. If natural language is used, the AI assistant proposes structured values and marks missing or uncertain fields.
3. The consultant reviews and confirms the structured request before calculation begins.
4. VEF validates the customer input and pins one published ODIP dataset version.
5. VEF obtains and independently validates the complete energy input profile and its integrity evidence.
6. VEF generates complete configurations that satisfy component compatibility and bounded search rules.
7. VEF simulates each candidate against the same pinned data and model versions.
8. VEF rejects candidates that violate technical or customer constraints and ranks the remaining candidates by annualized cost.
9. VEF records an immutable run containing the request, versions, evaluated candidates, constraint outcomes, recommendation, warnings, and execution metadata.
10. The consultant receives the recommended configuration, its annualized cost and self-sufficiency estimate, the principal assumptions and exclusions, and links to the evidence behind the result.
11. The AI assistant may explain the recorded result while distinguishing customer input, source data, derived reference profiles, model assumptions, and calculated outputs.
12. The consultant changes a constraint and starts a new, separately reproducible run when comparison is desired.

## 7 Alternative and failure scenarios

| ID | Condition | Expected outcome |
| --- | --- | --- |
| `UC-ALT-01` | Required customer input is missing, malformed, or outside supported bounds. | The request is not started; the consultant receives field-level correction guidance. |
| `UC-ALT-02` | The selected dataset is unpublished, unsupported, incomplete, or fails integrity validation. | No calculation uses it; the failure identifies the dataset and validation reason without exposing secrets. |
| `UC-ALT-03` | No candidate satisfies all constraints. | The run is marked infeasible, no recommendation is fabricated, and violated constraints or diagnostic counts are shown where available. |
| `UC-ALT-04` | Calculation fails for an operational reason. | The run is marked failed rather than infeasible, with a safe diagnostic and correlation identifier. |
| `UC-ALT-05` | ODIP is temporarily unavailable after VEF has cached a verified immutable publication. | VEF may use that exact cached version and still identifies its version and checksums in the result. |
| `UC-ALT-06` | Evidence required for an explanation is absent. | The explanation reports the evidence gap and omits unsupported numbers or claims. |
| `UC-ALT-07` | Source metadata contains instructions directed at the AI assistant. | The text is treated as untrusted data and cannot change rules, inputs, recommendation, or evidence policy. |

## 8 Postconditions and invariants

After a completed run:

- the original request and selected dataset version are unchanged;
- every reported number can be attributed to customer input, a specific immutable data artifact, or a named calculation version;
- candidates within the run were calculated with the same dataset, model, simulation, and optimizer versions;
- the recommendation is produced by deterministic optimization rules, not by the AI assistant;
- changing data or customer constraints creates a new dataset version or run rather than modifying history;
- customer details and credentials are absent from shared publications, logs, and explanations.

## 9 Business rules

1. The recommendation minimizes annualized cost among feasible candidates. Ties prefer lower initial investment and then lexical configuration ID.
2. A candidate is feasible only when component availability, roof area, electrical ratings, battery limits, investment limit, and minimum self-sufficiency all pass.
3. Reference profiles estimate building behavior; they are not represented as measurements of the customer's building.
4. The result discloses excluded costs and assumptions and does not represent a certified design or quotation.
5. The system makes an optimality claim only when it evaluated the complete stated search space or holds an equivalent solver proof.
6. The AI assistant cannot publish source data, alter technical rules, select a recommendation independently, or supply missing numerical evidence.

The precise formulas, state transitions, schemas, endpoints, and validation rules that make these rules testable are part of the integration contract.

## 10 Acceptance scenarios

| Scenario | Observable acceptance condition |
| --- | --- |
| Successful recommendation | A valid request returns the expected feasible set and least-cost recommendation for the agreed fixture. |
| Infeasible request | A deliberately impossible constraint returns an infeasibility explanation and no recommendation. |
| Unsupported period | A partial, rolling, shifted or multiple-year profile cannot start an annual optimization run; no annualization is inferred. |
| Unsupported existing equipment | A non-empty `existingComponentIds` list returns HTTP 422 with `existing_equipment_not_supported` and creates no run. |
| Reproducibility | Re-running the same recorded inputs and versions returns the same metrics and recommendation. |
| Data version isolation | Publishing corrected reference data does not change an earlier run; a new run can explicitly select the new version. |
| Traceability | The result identifies the dataset, artifact checksums, model, simulation, optimizer, and configuration used. |
| Safe AI assistance | Natural-language input is confirmed before execution, and the explanation contains no unsupported technical or numerical claim. |
| Deployed integration | The full scenario passes with ODIP and VEF isolated on Developer Platform, including authentication, restart, and retained state. |

## 11 Terms

| Term | Meaning |
| --- | --- |
| Dataset publication | Immutable, domain-neutral ODIP dataset version with a schema reference, artifacts, quality results, and provenance. |
| Energy input profile | Domain-specific schema defining the five artifact roles and energy-specific validation rules within a dataset publication. |
| Customer request | Site properties, constraints, and optimization goal supplied to VEF. |
| Configuration | Complete assignment of selected component models and quantities. |
| Candidate | A valid configuration plus simulation metrics under specified data and model versions. |
| Optimization run | One immutable request, its evaluated candidates, recommendation or infeasibility result, and execution metadata. |
| Explanation | Human-readable account derived from a recorded optimization run and cited input data; it is not a source of technical truth. |
