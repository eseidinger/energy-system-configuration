# Gate 1 contract-kit review

**Date:** 2026-10-10
**Reviewer:** Sole cross-project maintainer
**Scope:** Bounded integration demonstration
**Outcome:** Numerical and contract evidence approved; immutable release pending

## Reviewed evidence

- JSON Schema 2020-12 contracts and OpenAPI 3.1 descriptions for both service
  boundaries.
- Canonical RFC 8785 serialization and SHA-256 verification.
- The complete 8,784-hour Wasserburg reference fixture, its pinned PVGIS source
  response and request parameters, synthetic inputs, and the non-energy fixture.
- Hand-calculated cases for clipping, import, export, battery efficiency,
  capacity and power limits, and terminal discarded energy.
- The exact 252-candidate reference enumeration, all constraint outcomes, the
  194 feasible candidates, deterministic ranking, and recommendation.
- The reproducible release archive test and required license/notice contents.

## Source-data amendment

PVGIS 5.3 rejected a request for hourly 2024 data and reported 2023 as its
maximum supported year. The review approves the documented transformation of
the pinned PVGIS-ERA5 2023 series onto the 2024 UTC calendar. February 29 uses
the mean of the matching February 28 and March 1 hours. The manifest calls this
a synthetic reference profile and warns that it is not observed 2024 data.

## Numerical result

For the fixed demonstration request (35 m2 roof, 4,500 kWh annual demand,
EUR 18,000 investment ceiling, and 0.55 minimum self-sufficiency), the reviewed
recommendation is:

- 18 `pv-standard-400` modules (7.2 kWp total);
- one `inverter-5kw`;
- one `battery-10kwh`.

Its serialized evidence records EUR 8,240 initial investment, EUR 360.67
annualized cost, 0.889509006 self-sufficiency, 497.209474 kWh grid import,
5,191.571129 kWh grid export, and 233.288106 kWh inverter clipping. This is a
contract-test result under simplified assumptions, not an installation design
or commercial forecast.

## Approval and limitation

The fixture, calculation cases, generation rules, constraints, ranking, and
recommendation are approved as the `0.2.0` demonstration oracle. The automated
suite passes 30 tests in the repository environment.

This remains maintainer review by the only collaborator, not independent review
by a certified energy engineer. Production or certified-engineering use still
requires independent qualified review and replacement of synthetic customer,
tariff, catalog, and calendar-profile assumptions where appropriate.

Gate 1 becomes complete only when `contract-kit-v0.2.0` is committed, tagged,
published with its `SHA256SUMS`, and pinned by ODIP and VEF CI. Subproject
implementation must not begin from the mutable working tree.

## Platform reconciliation note — 2026-10-11

Kit `0.3.0` supersedes the `0.2.0` deployment, identity, classification, and
platform retention assumptions. This historical approval remains the reviewed
energy numerical baseline; it does not approve the new identity profile or
complete its release handoff. See the [platform compatibility notes](../contract-kit/platform/README.md).
The next immutable release and consumer pins now target `0.4.0`, which adds
the operational-envelope and component-monitoring contract, after the required
maintainer review; the earlier numerical fixtures and outputs are unchanged.
