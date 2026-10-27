# DEC-09: Synthetic tariff correction for version-isolation acceptance

**Status:** Accepted by the cross-project maintainer
**Date:** 2026-10-27
**Decision owner:** Integration Contract Maintainer
**Acceptance scenario revision:** 1

## Approved correction

The maintainer approved using the existing synthetic correction as the joint
version-isolation acceptance case: increase every hourly import tariff by
exactly EUR 0.01/kWh in isolated test publication 1.0.1. Advance the catalog
version metadata to match 1.0.1. Preserve PV yield, reference load shape, export
tariffs and component purchase/technical attributes. Keep original 1.0.0 bytes
and its released oracle immutable. Failed missing-hour drafts use 1.0.99.

The fixture is a synthetic regression scenario, not a commercial price update.
Use the agreed test environment and an isolated namespace/database. Never
replace an existing published 1.0.1; if that version is occupied, establish an
isolated test identity with the required reader permissions first.

## Expected results

ODIP's local harness exports publication bytes after actual restart/restore and
computes the corrected expectation using the independent Python reference model.
VEF has already compared all candidates, metrics and ranking against that
expectation. The maintainer accepts the following case for deployed repetition:

| Field | Original 1.0.0 | Corrected 1.0.1 |
| --- | --- | --- |
| Evaluated / feasible candidates | 252 / 194 | 252 / 194 |
| Recommended configuration | `pv-standard-400-q18-inverter-5kw-battery-10kwh-q1` | Same |
| Initial investment | EUR 8,240.00 | EUR 8,240.00 |
| Annualized cost | EUR 360.67 | EUR 365.64 |
| Self-sufficiency | 0.889509006 | 0.889509006 |
| Grid import / export | 497.209474 / 5191.571129 kWh | Same |

Only tariff-dependent costs change. For each candidate the unrounded cost delta
is EUR 0.01 times its grid import in kWh; compare serialized monetary values
exactly after the existing half-even rounding. The ranking must match the full
independently generated corrected expectation, not merely the summary above.
A coincidentally unchanged recommendation alone is insufficient evidence.

## Remaining deployed evidence

1. Identify pinned ODIP/VEF images, kit checksum, platform/application revisions,
   model/prompt versions and test dataset identity.
2. Retrieve and verify original 1.0.0 and corrected 1.0.1 manifests/artifacts.
3. Preserve/retrieve an owned original run; start a separate owned corrected run.
4. Compare every candidate, feasible ranking, recommendation, metrics and
   provenance against each version's expectation. Read the original run again
   and prove that the correction did not alter it.
5. Retain sanitized results and hashes with the release evidence bundle.

This closes the shared test-input decision in GAP-03. The deployed old/new-run
comparison, the other AI-10 negatives and joint recovery remain open. This
scenario approval does not grant Gate 6 acceptance or authorize rewriting
published data. Include the decision in the next immutable shared-kit release
under GAP-10, preserving kit 0.5.0 and consumer pins.
