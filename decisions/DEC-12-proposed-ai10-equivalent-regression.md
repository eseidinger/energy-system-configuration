# DEC-12: AI-10 equivalent deployed regression acceptance

**Status:** ACCEPTED_WITH_LIMITATIONS

**Date:** 2026-10-29

**Decision owner:** Integration Contract Maintainer

**Scope:** Current bounded energy release in `odip-test` and `vareng-test`

## Decision

For this release only, AI-10 is accepted on the basis of the newly executed,
automated [source-to-consumer regression](../reviews/evidence/2026-10-29-deployed-source-to-consumer-regression.json),
the separate [private VEF invalid-content probe](../reviews/evidence/2026-10-29-ai10-current-image-regression.json),
and the current-release DEC-10/11 exceptions. AI-10 is classified as
**ACCEPTED_WITH_LIMITATIONS**, without claiming that an unchanged historical
Gate 5 suite passed. The October 17 [Gate 5 acceptance](../reviews/2026-10-17-gate-5-acceptance.md)
explicitly recorded maintainer acceptance without an executable suite or test
report; that historical suite cannot literally be rerun.

The new single invocation used AI-enabled VEF revision 51 and ODIP revision 10.
It captured the pinned PVGIS raw JSON into a new isolated publication, checked
its linked raw artifact and five published artifact bytes, revoked all three
temporary worker grants with independent readback, verified both standard
energy versions and the non-energy publication, and created new VEF 1.0.0 and
1.0.1 runs. Both 252-candidate results passed their independent full oracles.
Idempotency, changed-body conflict, three publication/input denials, zero-budget
infeasibility and unchanged stored success also passed.

## Limits retained in the acceptance record

- The new raw-input publication used `energy-ai10-lineage-20261027/1.0.1`.
  Existing immutable standard reference versions were read byte-for-byte, not
  republished in a clean environment.
- The private VEF invalid-content probe used an in-memory ODIP transport. No
  live ODIP read response was corrupted or replaced, and no public test
  mutation endpoint was introduced.
- The previous private probe and the new source-to-consumer invocation have
  distinct pinned VEF image digests. Their implementation source differs only
  in documentation, but that is not a same-image execution of all subcases.
- DEC-10 excepts actual joint backup restoration. DEC-11 excepts its listed
  additional non-AI operational checks. Neither is represented as a PASS.
- The three rejected VEF responses contained no run ID. An independent run
  inventory was not queried for those requests.

This decision does not approve Gate 6, production deployment, contract-kit
1.0.0 publication or any new exception beyond the listed current-release
limits. Final release acceptance still requires the cross-project owner record
and immutable kit, implementation, image and deployment pins. Future releases
need an executable Gate 5 baseline and a safe isolated read-fault test seam if
that boundary remains mandatory.

**Approval:** On 2026-10-29, the integration contract maintainer explicitly
stated: "Ich bestätige DEC-12". The accepted scope is exactly the bounded
decision and limits above. AI-10 is closed as ACCEPTED_WITH_LIMITATIONS for
this release; Gate 6 remains OPEN pending its separate final owner decision.
