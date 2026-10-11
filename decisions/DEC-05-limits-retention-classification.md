# DEC-05: Limits, retention, and data classification

**Status:** Accepted
**Date:** 2026-10-10; reconciled 2026-10-11
**Decision owner:** Integration repository maintainer
**Due date:** 2026-10-10 (completed)

## Context

ODIP publication, VEF candidate generation, and retained evidence must be
bounded before implementation. The first release demonstrates the integration
with reference fixtures and does not require identifying customer information.

## Decision

### Publication limits

- A publication manifest is at most 1 MiB after transfer decoding.
- An individual artifact is at most 10 MiB after transfer decoding.
- The sum of all artifacts in one publication is at most 50 MiB.
- ODIP rejects an oversized upload before publication. VEF rejects an oversized
  response before fully buffering or persisting it.

### Search and execution limits

- A component catalog contains at most 20 models of each component type.
- A configuration contains between 1 and 100 PV modules, exactly one inverter,
  and between 0 and 4 batteries.
- VEF estimates the bounded search space before starting a run and rejects a
  request requiring more than 100,000 candidate evaluations.
- A run has a five-minute execution timeout. A timeout produces `FAILED`, not
  `INFEASIBLE`.
- Candidate-list responses are paginated with at most 100 candidates per page.
- Limits are validated before execution where possible and violations use
  machine-readable errors rather than silently truncating the search space.

### Classification

| Data | Classification |
| --- | --- |
| Published reference fixtures and their provenance | `Public` |
| ODIP ingestion working data | `Internal` |
| VEF customer inputs, runs, results, and evidence | `Confidential` |
| Client secrets, access tokens, and signing material | `Restricted` |
| Operational logs and metrics | `Internal` |

Project governance uses the platform classification vocabulary above and is
separate from the application declaration. ODIP declares a maximum of `Internal`,
VEF declares `Confidential`, and both declare telemetry `Internal`. `Restricted`
is limited to managed credentials, not ordinary project data. Stable identity
IDs remain security identifiers; optional display name/email release is disabled.

The first release does not collect names, exact street addresses, account
numbers, or free-form customer notes. Customer details and credentials are
excluded from publications, logs, metrics, traces, and AI explanations.

### Retention

- Published ODIP versions, artifacts, and provenance are retained while their
  contract version is supported and for one year after support ends.
- VEF customer requests, runs, results, and evidence are retained for 180 days
  after run completion.
- Applications enforce domain-row expiration in active storage. Project workload
  retirement retains its database until an explicitly authorized purge.
- Centralized workload logs now collect only minimized operational envelopes,
  with seven-day retention configured. Deployed ingestion/readback and elapsed
  expiry/compactor evidence remain open; collection outages can lose entries.
  Free-text logs remain best-effort kubelet diagnostics. Metrics retain seven
  days or 4 GB.
- Envelope correlation is an opaque lowercase UUID/32-hex value, Internal under
  the reference governance. Domain IDs remain in application-owned evidence;
  customer details and secrets never enter the envelope. Shared Loki/Grafana are
  operator-only; retained reads use fixed project-authorized Platform API queries.
  Backend `state: unavailable` is failure even when HTTP status is `200`.
- Application-owned security audit records retain 180 days. Platform audit events
  are append-only with no automatic expiry in the lab; review growth annually.
- Platform backups retain the latest verified snapshot plus 14 daily, 8 weekly,
  and 6 monthly recovery points. Active-row deletion does not delete those copies;
  expired records leave recovery storage only when containing snapshots expire.
- Pending access requests expire after 30 days; terminal requests and revoked
  memberships retain 90 days. These platform records are distinct from VEF runs.
- The original 30-day log/backup assumptions are superseded for kit `0.3.0` by
  this platform-aligned policy. Application retention owners, purge authority,
  and recovery owners are recorded through the separate governance API.

## Rejection behavior

- An oversized HTTP request or artifact returns `413 payload_too_large`.
- A publication exceeding aggregate limits returns
  `422 publication_limit_exceeded` and is not published.
- A request whose estimated search space exceeds the limit returns
  `422 search_space_limit_exceeded` and no run is created.
- A run exceeding five minutes ends as `FAILED` with the safe error code
  `run_timeout`.

## Consequences

- ODIP and VEF must enforce limits while streaming where practical instead of
  relying only on proxy limits or post-persistence validation.
- VEF must expose the applicable search bounds to the UI and capability
  endpoint.
- A future release that accepts identifying customer data requires a separate
  privacy and retention review.
- Retention cleanup and backup expiry require automated tests and operational
  evidence.
