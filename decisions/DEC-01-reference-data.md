# DEC-01: Reference data

**Status:** Accepted
**Date:** 2026-10-10 (amended after source retrieval)
**Decision owner:** Integration repository maintainer
**Due date:** 2026-10-10 (completed)

## Context

The first integration release needs one reproducible reference region and one
complete calendar year of hourly data. The data must be suitable for contract
tests without implying that it is a site-specific engineering forecast.

## Decision

- The reference region is **Wasserburg am Inn, Bavaria, Germany**.
- The region identifier is `DE-BY-09187182`, incorporating the official
  municipality key `09187182`.
- The representative coordinate is the municipality reference point published
  by the Bavarian State Office for Statistics: approximately `48.0622 N`,
  `12.2347 E`.
- The reference calendar is **2024**. It contains 8,784 hourly UTC intervals
  because 2024 is a leap year. It is a synthetic calendar profile, not a claim
  that every value was observed during 2024.
- The dataset ID is `energy-reference-wasserburg-am-inn-2024` and its first
  immutable publication version will be `1.0.0`.
- The `PV_YIELD_PER_KWP` fixture is derived from pinned hourly PVGIS-ERA5 2023
  data for the representative coordinate. At retrieval on 2026-10-10, the
  PVGIS 5.3 hourly endpoint rejected 2024 because its supported maximum year
  was 2023. Source hours are mapped by month, day, and UTC hour onto 2024;
  February 29 is the hourly mean of February 28 and March 1. The source request,
  response, attribution, database/version, retrieval time, orientation,
  inclination, PV technology, loss assumptions, and transformation are
  preserved as provenance.
- The first-release load shape, import tariff, export tariff, and component
  catalog may be synthetic. They must be realistic enough to exercise the
  contract, clearly marked as synthetic, and must not contain customer data or
  imply current commercial offers.
- The cross-project maintainers of this repository own and version the shared
  fixture and synthetic component catalog. ODIP remains responsible for source
  ingestion and publication; VEF remains responsible for interpreting the
  energy profile.
- PVGIS attribution and applicable reuse terms must accompany the source
  snapshot and derived artifact. Synthetic artifacts are released under this
  repository's CC BY 4.0 license.

## Consequences

- Results describe a reproducible regional reference case, not the expected
  output of a particular roof or building in Wasserburg am Inn.
- The 2024 timestamps provide the leap-year simulation boundary, while the PV
  values are a transformed 2023 source profile. Results must not be described
  as observed 2024 production.
- Roof geometry, local shading, customer consumption, live tariffs, taxes,
  subsidies, installation quotes, and current product availability remain out
  of scope for the first release.
- A later site-specific or newer dataset is published under a new dataset ID or
  immutable version; it does not modify the reference publication.
- Schema validation must expect 8,784 intervals for the chosen leap year rather
  than the 8,760 intervals of a non-leap year.

## Sources

- [Bavarian State Office for Statistics: Wasserburg a.Inn, municipality key and representative coordinate](https://www.statistik.bayern.de/mam/produkte/statistik_kommunal/2022/09187182.pdf)
- [European Commission Joint Research Centre: PVGIS](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en)
- [European Commission Joint Research Centre: PVGIS non-interactive API](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/using-pvgis-5/api-non-interactive-service_en)
