# DEC-05: Limits, retention, and data classification

**Status:** Accepted
**Date:** 2026-10-10
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
| Published reference fixtures and their provenance | `PUBLIC` |
| ODIP ingestion working data | `INTERNAL` |
| VEF customer inputs, runs, results, and evidence | `CUSTOMER_CONFIDENTIAL` |
| Client secrets, access tokens, and signing material | `SECRET` |
| Operational logs and metrics | `INTERNAL` |

The first release does not collect names, exact street addresses, account
numbers, or free-form customer notes. Customer details and credentials are
excluded from publications, logs, metrics, traces, and AI explanations.

### Retention

- Published ODIP versions, artifacts, and provenance are retained while their
  contract version is supported and for one year after support ends.
- VEF customer requests, runs, results, and evidence are retained for 180 days
  after run completion.
- Operational logs are retained for 30 days.
- Security audit records are retained for 180 days.
- Backups are retained for 30 days.
- Expiration triggers automatic deletion from active storage. Expired records
  disappear from backups as those backups pass their retention period.

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
