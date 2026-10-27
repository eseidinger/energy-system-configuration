# DEC-08: Complete UTC calendar years for energy optimization

**Status:** Accepted by the cross-project maintainer
**Date:** 2026-10-27
**Decision owner:** Integration Contract Maintainer
**Scope revision:** 1

## Decision

The maintainer selected "Nur vollständige Kalenderjahre: 8.760 bzw. 8.784
lückenlose UTC-Stunden" during the guided release review. The current energy
release accepts exactly one complete Gregorian calendar year:

- Start: January 1 at 00:00:00 UTC, with no fractional seconds.
- Exclusive end: January 1 at 00:00:00 UTC of the immediately following year.
- Step: exactly one hour, containing every expected timestamp once in order.
- Count: 8,760 hours in an ordinary year; 8,784 in a leap year, including the
  Gregorian century rule. The interval includes the whole of February 29 when
  applicable. Merely reaching one of these counts is insufficient.
- All four time-series artifacts use that same declared year and aligned hours;
  the reference load shape sums to one within the existing tolerance.
- Partial years, rolling twelve-month windows, shifted midnights, local-time
  years and multiple-year periods are unsupported. They are not extrapolated
  to annual results and cannot start an optimization run.

The reference fixture remains the complete 2024 UTC year. Its transformed
PVGIS 2023 source, derived leap day, provenance and numerical oracle stay
unchanged; complete-year validation does not turn this into observed 2024 data.
Short hand-calculated simulation examples remain valid unit-test inputs to the
low-level simulator; they are not admissible annual optimization publications.

## Responsibility and versioning

ODIP's energy adapter validates the complete-year rule before declaring its
energy validation successful. VEF independently checks it before admitting a
publication to its verified cache, and the typed EnergyProfile enforces it
before use by the optimizer. ODIP's domain-neutral publication API is unchanged.

This resolves GAP-07's annual-period scope question. The agreed rule is recorded
with DEC-07 in use-case prose 0.3, integration-contract prose 0.5 and plan prose
0.3. Released kit 0.5.0 and both consumer pins are immutable. The existing v1
period schema is broader than this cross-document business rule; incorporate
the decision and compatibility note into the next immutable kit release under
DEC-06 before final release acceptance (GAP-10).

Consumers previously admitted shorter periods. This is an intentional tightening
of their energy-release validation boundary. Existing immutable publications
must not be rewritten: any historical short-period publication remains historical
and is unsupported for new annual optimization. Publish a new version with a
complete year when needed. Saved historical run records retain their original
inputs and scope; no migration or recalculation of those records is authorized.

## Closure evidence

Tests cover ordinary/leap/century years and reject partial, missing-leap-day,
rolling, shifted, fractional-boundary and multiple-year periods. Existing
missing/duplicate-hour, common-period, load normalization and digest tests
remain required. Re-run the original 2024 oracle and corrected 1.0.1 regression.
A deployed negative publication/optimization check remains part of AI-10;
accepting this decision is not final hosted release acceptance.
