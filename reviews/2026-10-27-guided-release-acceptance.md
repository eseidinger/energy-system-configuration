# Guided deployed energy acceptance — October 27, 2026

This record follows the maintainer's DEC-07/08/09 decisions and the earlier
implementation/gap review. It covers the deployed test projects `odip-test`
and `vareng-test`. It does not grant Gate 6 or production release acceptance.

## Passed corrected-version isolation — GAP-03

The maintainer approved DEC-09's synthetic increase of every hourly import
tariff by EUR 0.01/kWh. The operator created corrected 1.0.1 with manifest
`ebfd2cc7dcdf73cef4ed81a94b693ec23c4448460c8161ca648369ea0a930f93`,
attached all five checksum-matching artifacts, and reported `PUBLISHED`.
Original 1.0.0 and its released oracle were retained.

| Observation | Original 1.0.0 | Corrected 1.0.1 |
| --- | --- | --- |
| Owned run | `run-3c6e5462-9156-4bdd-a740-7258962fab6b` | `run-5e24cbd7-91a6-4b0b-8444-296cf8f9cdff` |
| Status | SUCCEEDED | SUCCEEDED |
| Evaluated / feasible candidates | 252 / 194 | 252 / 194 |
| Recommendation | `pv-standard-400-q18-inverter-5kw-battery-10kwh-q1` | Same |
| Annualized cost | EUR 360.67 | EUR 365.64 |
| Initial investment | EUR 8,240.00 | EUR 8,240.00 |
| Self-sufficiency | 0.889509006 | 0.889509006 |

The operator then fetched the original run and candidate through the protected
GET routes after the correction, confirming version 1.0.0 and EUR 360.67.
For each run, the operator exported the result and candidate pages 0–2 at
pageSize 100 from the authenticated browser. The agent parsed those eight JSON
files and ran the same full verifier against the released 1.0.0 oracle and the
independent Python corrected oracle. **Both passed**: all 252 candidates,
assignments, metrics, constraint objects, feasible ranking, recommendation and
result provenance matched. Run IDs/timestamps alone are excluded from oracle
value equality. The corrected run's version and approved manifest digest were
asserted explicitly. Comparing the two actual candidate sets also confirmed
unchanged assignments, feasibility, constraints and every non-tariff metric.

GAP-03 is therefore closed for this configured test environment. This is one
passed AI-10 regression scenario; AI-10 as a whole remains open.

## Passed request rejections

The operator reported these protected POST responses from browser Network:

- Non-empty `existingComponentIds: ["pv-standard-400"]` with version 1.0.1:
  HTTP 422, `existing_equipment_not_supported`.
- Empty existing list with nonexistent version 9.9.9:
  HTTP 422, `publication_not_found`.

These match the approved new-installation scope and unpublished-version rule.
The inspected resource rejects both before run reservation. A server-side
before/after run count was not captured, so this record does not claim that
additional database observation.

## Additional zero-budget observation

A valid version-1.0.1 request with budget EUR 0 created
`run-64dd8cc4-608c-492b-9b3d-58162d63f645` and the operator observed
`INFEASIBLE`, with no recommendation and guidance to adjust the constraints.
This distinguishes engineering infeasibility from the two rejected requests.
The operator also supplied the AI explanation: it correctly states that none
of the 252 evaluated candidates is feasible, there is no recommendation, and
optimality is NOT_APPLICABLE. It separates customer inputs, calculated outputs
and model assumptions, retains the synthetic-calendar warning, and explicitly
declines to infer per-candidate failure causes or unavailable cost, tariff,
profile and measured-data evidence. This semantic AI-07 review passes. The
raw explanation JSON, individual citation values and current provider/image
pins remain uncaptured. These observations are separate from the immutable
version-isolation evidence archive below.

## Partial-calendar rejection and HTTP classification defect

The isolated synthetic version 1.0.90 has manifest SHA-256
`657b6d6e293355e3c88e881dece819815cc9d0a5d9bb3b3c8454ee757c65901d`.
Its four aligned hourly series cover January 1 through July 1, 2024
(4,368 hours); normalized load fractions, artifact digests, released schemas
and generic semantic checks pass. It deliberately violates DEC-08's complete
calendar-year requirement. The operator observed ODIP status FAILED with
`profile_validation_failed`: the hosted publication rejection passes.

The subsequent VEF request using this failed version was rejected with HTTP
503 `publication_unavailable`. This prevents invalid data use but incorrectly
classifies a permanent publication-state rejection as a temporary outage.
The pinned ODIP contract specifies HTTP 409 for an existing version that is
not published; VEF previously translated only upstream 404 to a 422 response.
The VEF correction maps 409 to HTTP 422 `publication_not_published` and retains
404 as `publication_not_found` and upstream outages as 503. Its hosted retest
is pending; do not count this VEF negative case as passed yet.

## Evidence and limits

The [sanitized machine-readable summary](evidence/2026-10-27-version-isolation.json)
contains per-file/oracle hashes, verdicts, known limits and last recorded platform
snapshots. Both consumers still pin kit 0.5.0, archive SHA-256
`ae4edaf6799d4b57510d14d2004c5b65ff6b05f3b225e96bbd5971b30ce8832b`.
The VEF model, simulation and optimizer versions remain 1.0.0.

The complete local exports/oracles/notices bundle is in VEF's ignored
`apps/prototype/api/target/hosted-acceptance-20261027/version-isolation-evidence.tar.gz`.
Its hash is recorded in the tracked summary. Copy it to controlled release
storage before cleaning build outputs; long-term retention remains GAP-10 work.
Raw browser cookies, credentials and request authorization headers are not in
the bundle or summary.

The last recorded VEF platform snapshot is revision 24 at commit `c7155b5`,
image `sha256:bda91b2d67f0f3126060061418c1c4921a7499943dffc77a222e0931116a1b54`.
The last ODIP snapshot is revision 9 at `1fe3251`; it predates the native source
reuse UI change `31c4602`, whose CI/test deployment succeeded. A fresh complete
image inventory could not be read after the human CLI login expired. Do not
present the old ODIP snapshot as the current image inventory. Refresh these
pins in the final release bundle before final acceptance.

### Observation: hosted raw-input lineage

The operator's 1.0.0 view contains manifest source attribution but no captured
raw-input entries; no matching energy/PVGIS ingestion run was visible. Draft
rawArtifactIds are optional in the existing operator API. The version-isolation
case used ordinary draft creation and does not prove the hosted raw-ingestion
path. Retain this observation for the remaining AI-10 ingestion/traceability
review. Do not retroactively modify immutable 1.0.0 or claim captured raw data.

The remaining hosted AI cases, negative profile/data scenarios, integrated
restore, runtime/security/retention evidence and final owner acceptance stay
open in the [gap register](2026-10-27-gap-analysis.md).
