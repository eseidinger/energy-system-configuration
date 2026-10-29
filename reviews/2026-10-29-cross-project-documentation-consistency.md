# Cross-project energy documentation consistency review

**Date:** 2026-10-29

**Scope:** Current entry points, development and integration plans, AI runbook,
system-model overview, shared contract prose and the October 27 review/gap
registers in Energy System Configuration (ESC), ODIP and VEF. Historical
decision and evidence records retain their original dated statements.

## Reconciled baseline

| Topic | Current state |
| --- | --- |
| Shared contract | Published and checksum-pinned kit 1.0.0 in ODIP and VEF. The 0.5.0 archive remains a historical release. |
| Applications | ODIP and VEF v1.0.0 are ready in production at the revisions and image digests in the [deployment record](2026-10-29-production-deployment.md). |
| Gate 6 | [CLOSED_WITH_LIMITATIONS](2026-10-29-gate-6-closure.md) for the bounded 1.0.0 release. AI-10 is ACCEPTED_WITH_LIMITATIONS; DEC-10/11 exceptions are not passed tests. |
| Production calculation | The maintainer-reported run matches every supplied immutable reference-oracle field. The full live API and candidate export is still uncaptured. |
| Scope | New installations, complete UTC calendar years, synthetic Wasserburg reference profile; no certified-engineering claim. |

## Inconsistencies corrected

- ODIP's development plan, documentation index and system-model overview still
  described kit 0.5.0 as the current pin and Gate 6 AI cases as open. They now
  distinguish the October 19 handoff from the current 1.0.0 release.
- VEF's development plan, documentation index, source traceability and AI
  runbook still described Gate 6 as upcoming/open or production as
  unauthorized. Their current status now points to the bounded closure and
  production release; older 0.5.0 evidence is dated as historical.
- ODIP's integration plan mixed a current heading with October 27 claims that
  final acceptance and release packaging were pending. Those passages now
  name their checkpoint or reflect the subsequent DEC-12/13 and kit release.
- The shared contract still called implemented publication GET routes
  proposals. It now identifies them as implemented while preserving the
  normative API obligations. The October 27 gap/review entry points now link
  to the later Gate 6 closure instead of presenting their old OPEN state as
  current.

The old decision records and dated acceptance observations were not rewritten
to imply tests had passed later. Later decisions and release evidence supersede
their status, while the original evidence limits remain visible. This review
changes documentation only; it does not add new runtime or acceptance tests.
