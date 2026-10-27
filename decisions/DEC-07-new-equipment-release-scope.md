# DEC-07: New equipment only in the current release

**Status:** Accepted by the cross-project maintainer
**Date:** 2026-10-27
**Decision owner:** Integration Contract Maintainer
**Scope revision:** 1

## Context

The original use case 0.2 and prose contract 0.4 include existing equipment.
The implemented VEF model and released numerical oracle cover new equipment.
The October 27 review records this difference as GAP-06. During the guided
closure review the maintainer explicitly selected: "Neuanlagen für diesen Release".

## Decision

- The current bounded demonstration and its Gate 6 release acceptance cover new
  PV modules, a new inverter and optional new batteries only.
- `site.existingComponentIds` MUST be an empty array. The field remains in the
  v1 request for wire compatibility. Non-empty values MUST fail explicitly with
  HTTP 422 and `existing_equipment_not_supported` before creating a run; they
  MUST NOT be silently discarded or reinterpreted as newly purchased components.
- All selected components in this release are newly purchased. Their complete
  quantities contribute to initial investment. Candidate selections identify
  them as `existing: false`.
- Existing-equipment support is deferred to a later version. Before that work
  ships, define quantities, ownership, compatibility, sunk versus new costs and
  canonical identity, then supply shared fixtures and an independent oracle.
- This decision closes GAP-06 for the current release through explicit scope
  reduction. It does not establish existing-equipment implementation or approve
  the remaining Gate 6 cases.

## Versioning and compatibility

Use-case prose advances from 0.2 to 0.3, integration-contract prose from 0.4 to
0.5, and integration-plan prose from 0.2 to 0.3. These are document versions,
not contract-kit, dataset, schema or model release versions. The narrower
acceptance scope supersedes the existing-equipment obligations of the earlier
prose for this release. Other acceptance and numerical requirements remain.

Released kit 0.5.0, its tags/archive/checksum, both consumer pins and the original
1.0.0 numerical oracle remain immutable. The kit's broader v1 request schema is
supplemented by this application-level scope rule, which the existing VEF model
already enforces. Incorporate this decision and compatibility note into the next
immutable shared-kit release under DEC-06 before declaring final release
acceptance. Release packaging remains tracked by GAP-10; this decision does not
publish a kit or authorize deployment.

## Verification and follow-up

Existing VEF `EnergyFeatureModelTest.neverIgnoresExistingEquipment` checks the
explicit model rejection; input/HTTP validation tests cover the request boundary.
The released reference request uses an empty list and all 252 configurations
select new components. Their numerical results remain the regression baseline.
Include a non-empty-list HTTP 422/no-run case in the deployed release regression.
The subsequent [DEC-08](DEC-08-complete-calendar-year.md) resolves the annual-period
decision to complete UTC calendar years. Hosted AI, recovery and final owner
acceptance remain open.
