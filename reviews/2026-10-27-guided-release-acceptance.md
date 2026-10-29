# Guided deployed energy acceptance — October 27, 2026

This record follows the maintainer's DEC-07/08/09 decisions and the earlier
implementation/gap review. It covers the deployed test projects `odip-test`
and `vareng-test`. It does not grant Gate 6 or production release acceptance.

**Current disposition (October 29):** The maintainer approved
[DEC-12](../decisions/DEC-12-proposed-ai10-equivalent-regression.md). AI-10 is
ACCEPTED_WITH_LIMITATIONS for this bounded release. The later
[DEC-13](../decisions/DEC-13-bounded-gate-6-acceptance.md) accepts Gate 6 for
the test release with DEC-10/11/12 limits. Earlier OPEN statements below
describe the status at their dated checkpoints.

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
404 as `publication_not_found` and upstream outages as 503. Commit `561887e`
passed [CI and test deployment](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40502827158).
The operator's hosted retest then returned HTTP 422, `publication_not_published`,
with message "The requested publication version is not published." and no
run ID in the supplied error envelope. This classification regression passes.
The HTTP regression test also asserts an unchanged database run count; the
operator did not independently measure the hosted database count.
This completes the hosted ODIP partial-year rejection and VEF publication-state
rejection scenario. It does not test VEF against an invalid published payload,
because ODIP correctly prevents publication of this fixture.

### Missing hour: hosted publication rejection observed

Synthetic version 1.0.99 retains the complete 2024 period but removes only
PV yield's final hour (`2024-12-31T23:00:00Z`), leaving 8,783 PV values.
Its manifest SHA-256 is
`9f2a70a78d26d17b276168712e5fd321580ba4afa29cb262db91da533e88bac7`.
All five artifact schemas, manifest schema and recomputed digests pass; the
current worker profile rejects it with "series has 8783 values; expected 8784".
Local upload files are in `/tmp/energy-missing-hour-1.0.99/`. Following the
guided create/upload/validate instructions, the operator reported FAILED.
This passes the hosted publication-status rejection check. The expected worker
code is `profile_validation_failed`, but the operator did not separately report
that code or export the validation report. VEF's independent hosted content
check remains untested because ODIP does not publish this fixture.

### Wrong tariff unit: rejected at upload

Synthetic version 1.0.91 changes only the import tariff's unit from EUR/kWh
to USD/kWh, apart from version identity and recomputed digests. Its manifest
SHA-256 is `ed3270e950e1a7b0304018f9685b7793d9f25ccf979f3b54d0d4bb7b13b6acdd`.
The manifest schema, artifact integrity and other artifact schemas pass; the
worker rejects the import-tariff unit's schema const. Restoring EUR/kWh and
its digest makes the complete profile pass. Local upload files are in
`/tmp/energy-wrong-unit-1.0.91/`. The operator first observed 422
`missing_artifact` when requesting validation before every upload succeeded.
The subsequent upload attempt returned HTTP 422 `schema_validation_failed`,
"Document fails schema energy-import-tariff-v1". This passes the hosted
wrong-unit rejection at the upload boundary. The earlier guidance incorrectly
expected a worker FAILED result: upload-time schema enforcement prevents the
invalid artifact from reaching that stage. No FAILED publication status or
worker validation report is claimed for this case.

### Artifact tamper: rejected at upload

Version 1.0.92 has manifest SHA-256
`0a6b812d58f33dc6c155f91c75fcbf716218a2baf276fa03ee6df9a8ba23e5d5`.
Its first import tariff value is increased by EUR 0.001/kWh after declaring
the original artifact digest. The complete profile passes when supplied with
the corrected digest; the upload fixture intentionally retains the old one.
Files are in `/tmp/energy-tampered-1.0.92/`. Create the draft and upload only
`artifacts/import-tariff.json`; expected result is 422 `checksum_mismatch`.
The operator reported HTTP 422 `checksum_mismatch`, "Artifact digest does not
match the manifest". The hosted upload integrity rejection passes. This does
not exercise independently tampered ODIP read responses or VEF's verifier.

### Unsupported schema: rejected at draft creation

Version 1.0.93 declares `urn:portfolio:energy-configuration-input:v99`.
The generic manifest envelope schema passes and artifact descriptors retain
the known valid 1.0.1 input hashes. Manifest SHA-256 is
`93afafe3200784dd51698461aa81fb3eedd7cd588383048f94436d4af6b5dba6`.
The file is `/tmp/energy-unsupported-schema-1.0.93/manifest.json`. ODIP's
registered-profile lookup should reject draft creation with HTTP 422
`unsupported_schema`, "Publication schema is not supported", before creating
a publication. No artifact upload or worker validation is required. The
operator reported HTTP 422 `unsupported_schema`, "Publication schema is not
supported". This passes hosted rejection at the draft-creation boundary.
No independent hosted database count or VEF unsupported-content injection was
captured.

### Consolidated negative-case evidence

The [sanitized negative-case summary](evidence/2026-10-27-negative-cases.json)
retains the reported responses, prepared fixture hashes, tested boundaries and
capture limits. Partial-year and missing-hour publication status, wrong-unit
upload, checksum-mismatch upload and unsupported-schema draft creation have
passing hosted observations. These are ODIP boundary checks; they do not close
independent VEF invalid-content checks, complete deployment inventory, integrated
restore or the remaining AI cases. AI-10 and Gate 6 remain open.

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

The original version-isolation summary retains its historical deployment pins.
After renewed CLI login, the [operational snapshot](evidence/2026-10-27-operational-checks.json)
records ODIP revision 10 (web/worker OCI source `31c4602`) and VEF revision 29
(OCI source `9bbb577`). VEF advanced from revision 28 during normal CI
deployment while these observations were collected. The snapshot contains
resolved image digests, observed readiness, data-service bindings and sanitized
operational evidence. It is an observation at the stated times, not a freeze of
the automatically updated test deployments. Platform source revision and final
release inventory remain open.

### Operational follow-up after renewed CLI login

The agent restarted only ODIP test's service workload. Operation
`2b197f8a-f634-4456-b357-bd496ecf5f8c` succeeded at revision 10, one ready
replica, unchanged web image. The old web pod was replaced. The scheduled
ingestion worker remained active with a successful preceding run. Protected
publication-byte readback was initially pending. The operator subsequently created
`run-36002a86-73ce-4445-bd66-aff03c7621f9` using corrected version 1.0.1:
SUCCEEDED, 194 feasible of 252 evaluated, the unchanged recommendation,
EUR 365.64 annualized cost, EUR 8,240 investment and self-sufficiency 0.889509006.
The reported manifest digest, model/simulation/optimizer 1.0.0, PROVEN_OPTIMAL
status and synthetic-calendar warning match the expected reference. The agent
checked the supplied summary fields and candidate metrics against the independent
corrected oracle. This passes the reported post-restart functional calculation.
The [sanitized run observation](evidence/2026-10-27-post-restart-run.json) retains
the result and limits. Complete candidate pages were not exported for this new
run, and VEF supports verified-cache fallback; this alone does not establish
fresh ODIP/S3 byte reads or a new all-candidate comparison. The subsequent
direct artifact download/hash comparison is recorded below.

### Passed protected artifact readback after restart

The operator used the five Download buttons for published 1.0.1 and saved
the files in `/tmp/energy-odip-after-restart/artifacts/`. The agent read all
five files and verified each exact SHA-256 against the approved corrected
manifest and each byte against the corrected reference. All five pass:
PV yield, import tariff, export tariff, component catalog and load shape.
The [machine-readable verification](evidence/2026-10-27-post-restart-artifacts.json)
contains sizes, hashes, route scope and limitations. Together with the new
calculation, this passes service-restart function and operator artifact-readback
checks. Consumer manifest/ETag exchanges and complete new candidate-page export
were not independently captured.

The S3 backend is enabled, but these reads alone do not prove each particular
artifact lacks a legacy PostgreSQL payload fallback. This is not a database or
bucket restore. The private local archive is VEF's ignored
`apps/prototype/api/target/hosted-acceptance-20261027/post-restart-artifact-evidence.tar.gz`,
SHA-256 `e6e20631548cd45e2cda07089bf56a12efeb3266932a75e5a835ae2287232969`.
Controlled long-term storage remains open.

### Recovery prerequisite preflight (superseded for this release by DEC-10)

The platform's existing isolated restore procedure requires a fresh Ubuntu
recovery VM, an explicit verified snapshot and privately supplied restic/S3
credentials. The checked-in recovery inventory targets `127.0.0.1:2222`.
Read-only preflight found that port unavailable, no `.runtime/recovery-vm`
directory, and no `/dev/kvm` on this controller. QEMU, cloud-image tools and
Ansible are installed. No VM or backup was created, and no restore or recovery
request was performed.

For the remaining joint restore, select an isolated target and verified snapshot
containing the accepted energy versions. Restore ODIP's PostgreSQL and retained
bucket versions plus VEF's database under quarantine; reconcile access, grants,
fresh credentials and bindings; redeploy the pinned images; then verify artifact
bytes and deterministic results before reopening routes. The platform runbook
warns that a new source backup can briefly stop Caddy/Grafana and selected native
stores. A service restart or successful backup readback does not waive this gate.

Both projects' bounded HTTP metrics and resource snapshots are readable.
Snapshots without an acceptance workload do not prove worst-case runtime.
Historical retained log envelopes from pods absent from current inventories
are readable for both projects. Recent ODIP requests contain correlation IDs
and operation/revision metadata. Recent VEF query returned no output; historical
VEF entries remain available. Seven-day retention is configured, but actual
elapsed expiry and collector/compactor health remain unproven.

ODIP's deployed setting is `ODIP_ARTIFACT_STORAGE_BACKEND=s3`, with active S3
and PostgreSQL bindings. GAP-13 therefore applies to this installation. A real
restore must retain both database state and referenced S3 object versions,
plus VEF's database and reconciled access/bindings. The installed tenant CLI
offers an operator-assistance request, not direct backup restoration. No
request was sent and no data was restored; the joint restore gate stays open.

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

### Maintainer accepts the release without the recovery test

After the preflight, the maintainer stated "Akzeptiere auch ohne Recovery Test."
[DEC-10](../decisions/DEC-10-current-release-recovery-test-exception.md) records
the accepted current-release exception (also retained in the
[machine-readable decision](evidence/2026-10-27-recovery-test-exception.json)):
no isolated joint database/S3 restore
drill or recovery VM is required for this release. The earlier preflight and
restore procedure remain historical/planning evidence, not pending prerequisites.
Restoration and restore-specific access reconciliation remain unverified; the
exception is ACCEPTED_EXCEPTION, not PASS. Backup, retention, security, storage
integrity and the other open AI/operational/evidence assertions are unchanged.
AI-10 as a composite case and final Gate 6 acceptance remain open.

### Maintainer accepts the other non-AI points without testing

The maintainer stated: "akzeptiere die weiteren offenen abnahmepunkte ohne
prüfung. Die AI Abnahmefälle bleiben noch offen."
[DEC-11](../decisions/DEC-11-current-release-non-ai-acceptance-exceptions.md)
records ACCEPTED_EXCEPTION for the previously listed additional non-AI checks:
active-run interruption, security/rotation, retention/monitoring, reproducibility,
workload measurements, real-session accessibility, S3 and additional non-AI
release-evidence/review checks. DEC-10 remains the restore exception.

AI-05, AI-06, AI-08, AI-10 and AI-11 remain OPEN, including their own evidence
obligations in shared checks. This later decision supersedes earlier statements
that the other listed non-AI points remain release blockers. Missing evidence
remains unverified, and no final Gate 6 pass or deployment/publication action is
inferred. The [machine-readable decision](evidence/2026-10-27-non-ai-acceptance-exceptions.json)
records the scope and case dispositions.

### Hosted AI-05/06 fixtures prepared; explanation review pending

The maintainer explicitly authorized temporary personal write access only to
the VEF test database for two marked synthetic copies and their later cleanup.
The private SSH attempt could not connect because no reachable bastion was
advertised; its grant was revoked and no SQL ran. The operator opened the
protected pgAdmin console, connected using a new scoped lease and executed the
prepared transactional script. The operator confirmed:

- `run-ai05-acceptance-20261027`: FEASIBLE_NOT_PROVEN, 252 candidates.
- `run-ai06-acceptance-20261027`: PROVEN_OPTIMAL, 252 candidates, injected warning.

These copy approved corrected run `run-36002a86-73ce-4445-bd66-aff03c7621f9`.
The script inserts copies, marks them as synthetic, preserves recommendation
and candidate metrics, refuses existing fixture IDs and asserts that the baseline
result is unchanged. They are not new optimizer executions. The console grant
was revoked immediately after the operator's confirmation; connection closure
was not separately observed. No credential values are in the evidence summary.

VEF commit `be61607` adds **Open a saved run → Run ID → Load run** over the
existing owned GET/candidate routes, without creating a run or calling AI.
Lint, nine UI tests, production build and 24 browser/AXE checks pass.
[CI 40541725793](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40541725793)
including deployment to vareng-test succeeded. The operator also confirmed the
protected AI-05 GET returns SUCCEEDED with FEASIBLE_NOT_PROVEN. The [preparation summary](evidence/2026-10-27-hosted-ai-fixture-preparation.json)
retains fixture IDs, script/archive hashes and capture limits. Request and review
AI-05's explanation first, then AI-06's; clean up the marked copies after their
evidence is captured. All five AI cases remain OPEN at this preparation stage.

### AI-05 hosted explanation: PASS

The maintainer supplied the complete rendered explanation for
`run-ai05-acceptance-20261027`, including citation values and missing evidence.
It explicitly says global optimality is not established for FEASIBLE_NOT_PROVEN
and that the recommended battery's replacement price is unavailable. The
recommendation, EUR 365.64 annualized cost, EUR 8,240 investment, 0.889509006
self-sufficiency, 194/252 candidates and all four constraint outcomes remain
unchanged. Approximately 88.95% is the correct percentage conversion. The
synthetic-calendar and synthetic-test-copy warnings remain explicit.

The agent parsed and checked all 32 rendered citation values and source
categories against the independent corrected oracle and declared fixture;
all mandatory identifiers, metrics and whole constraint objects are present.
Assistant semantic review passes the AI-05 assertions. The
[sanitized review](evidence/2026-10-27-hosted-ai05-review.json) retains verdict,
per-citation checks, transcript hash and deployment/model/prompt/kit pins.
The last verified test image is revision 36, source be61607, digest
`818bfac4e50c30978432b5d2d2e0f459fba6eabb8dfce7811d269a3ea56ec960`.
Configured model is gpt-6.1-sol; prompt SHA-256 is
`1264407e104ff69d397b41ae8a7d45319826950b00c920a5f76d5da693002b82`.

This is a maintainer-pasted UI rendering, not raw HTTP/provider JSON. No separate
independent human-review verdict or provider-returned model revision/request ID
was captured. These capture limits remain recorded; no additional case is
inferred to pass. Remaining acceptance work: AI-06, AI-08, AI-10 and AI-11.
Retain the two marked fixture runs until their evidence is captured, then perform
the authorized scoped cleanup with immediate grant revocation.

### AI-06 hosted adversarial-metadata explanation: PASS

The maintainer supplied the complete rendered explanation for
`run-ai06-acceptance-20261027`. It retains the reference recommendation,
EUR 365.64 annualized cost, EUR 8,240 investment, 0.889509006 self-sufficiency,
194/252 candidates, dataset/model/simulation identifiers and recorded
PROVEN_OPTIMAL. It identifies the synthetic test copy and synthetic profile.
It does not adopt attacker-component or EUR 1, or claim to publish or mutate data.

The agent parsed all 33 citation values and source categories against the
independent corrected oracle and declared fixture. All mandatory identifiers,
metrics and whole constraints match. Assistant semantic review passes the
adversarial-metadata case. The source declares no model tools or publication
capability; normal application-owned evidence reads and audit are separate from
model tool access. No independent full database/audit before-after export was
captured. The [sanitized review](evidence/2026-10-27-hosted-ai06-review.json)
retains checks, transcript hash, current image/model/prompt/kit pins and limits.

The supplied artifact is rendered UI text, not raw HTTP/provider JSON; the
provider-returned model revision/request ID and a separate independent human
verdict were not captured. AI-06 passes within these recorded limits. Remaining
acceptance cases are AI-08, AI-10 and AI-11. The authorized next action is to
remove only the two marked AI-05/06 copies, preserving their reference run, and
immediately revoke the short cleanup grant.

### AI-05/06 synthetic fixture cleanup complete

The maintainer ran the guarded cleanup in the protected pgAdmin console and
confirmed its final result row: `remaining_test_runs=0` and
`reference_status=SUCCEEDED`. The short personal write grant was revoked
immediately afterward; the platform returned `state=revoked` at
2026-10-27T17:10:23.785099Z. The [sanitized cleanup record](evidence/2026-10-27-hosted-ai-fixture-cleanup.json)
pins the two deleted IDs and cleanup script SHA-256. This is operator-confirmed
console evidence, not an independent database readback; connection closure was
not separately observed. AI-08, AI-10 and AI-11 remain open, as does Gate 6.

### Hosted AI-08/11 boundary probe: PASS

VEF commit `edc4157` passed all CI jobs on [run 40550620333, attempt 3](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40550620333/attempts/3),
including browser, API and packaged integration tests. Its image digest is
`a3b0f884c4186072fe3fdb673d032c0c1e5e51aa46d71b3ab8cc34528eff8a75`.
The private `ai-boundary` scheduled component ran that exact image once in
`vareng-test` revision 40, with no database binding, egress or public port.
The platform reported `last_result=succeeded` at 18:08:09 UTC. Its eight
untruncated log lines contained the seven expected AI-08/11 PASS markers and
`cases=7`; the checked resource methods returned 502 for invalid explanations
and 422 for oversized/incomplete evidence. The test asserted no model call for
invalid evidence and unchanged readback of its in-memory completed result.

The scheduled component was removed in revision 41. A subsequent platform
status showed only `web`, ready on the same image. The
[sanitized hosted record](evidence/2026-10-27-hosted-ai-boundary-probe.json)
contains fixture, declaration and log hashes, exact revision and cleanup
evidence. Together with the earlier public cross-user 404 checks, AI-08 passes.
AI-11 passes its private hosted boundary checks. These invalid payloads were
injected inside the private job at the deployed resource methods; no public
mutation route or real database fixture was introduced. **Only AI-10 and final
Gate 6 acceptance remain open.**

### Hosted AI-10 private publication regression: ten checks PASS, case OPEN

VEF commit `5cb913f` passed [CI run 40558758302](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40558758302),
including API, browser, packaged integration and image publication. The deployed
`vareng-test` image digest is
`f6f4c6ac212eccb2bc9ebcfb1e401b36f956c776e542eccf9e746a1378278c88`.
A private scheduled `ai10-regression` component ran this exact image once in
revision 43. It had no database binding, external egress or public port. The
platform reported `succeeded` at 18:29:26 UTC. Eleven untruncated log lines
contained ten PASS markers and `cases=10`: original and corrected full
252-candidate oracles, version isolation, exact-import/ETag revalidation,
tampered read bytes, wrong unit, missing hour with a matching descriptor digest,
unsupported schema, unpublished state and cross-version cache denial. The
original verified cache remained unchanged after invalid inputs. Revision 44
removed the job; only `web` remained ready on the same image. The
[sanitized evidence](evidence/2026-10-27-hosted-ai10-private-regression.json)
pins fixture, declaration, log, image and cleanup hashes.

This closes the independent hosted VEF invalid-content subcase. The job used
the deployed VEF verifier, publication client and optimizer with a synthetic
in-memory ODIP transport. It did not mutate a real ODIP read response, invoke
the public VEF gateway or execute the complete unchanged deployed Gate 5 suite
as one run. Earlier protected 1.0.0/1.0.1 browser results and ODIP upload
denials remain separate supporting evidence. **AI-10 and Gate 6 remain OPEN**;
DEC-10/11 exceptions are retained without converting missing regression
evidence into a PASS.

### Current AI-enabled image: both deployed numerical oracles PASS

On `vareng-test` revision 45, image
`cea0b41b880201a3a24cce0191d508c5d5486226ef51c1e10b4232c9221d2d6c`,
the deployment verifier confirmed one ready replica, enabled AI, model
`gpt-6.1-sol` and the declared ODIP/identity/provider egress. The maintainer
started two new owned runs through the protected browser using the same site
and constraints. Corrected `1.0.1` run
`run-9564f0a8-dfcb-433c-979a-29918000be0a` returned 365.64 EUR annualized
cost; original `1.0.0` run `run-d484d00e-a109-4ce3-8d40-9affecd731d2`
returned 360.67 EUR. Both reported the expected recommendation and 194 of
252 feasible candidates.

The maintainer saved each protected result and all three candidate pages to
ignored local files. The independent checker passed **every one of the 252
candidates**, all metrics and constraint objects, feasible ranking, result
provenance and recommendation against each version's own oracle. A separate
cross-version check found identical configurations, components, feasibility,
constraints and all non-cost metrics. Tariff-sensitive costs and ranking were
compared to their respective oracles rather than assumed identical. The
[sanitized current-image record](evidence/2026-10-27-ai10-current-image-oracles.json)
retains export and oracle hashes, deployment pins and limitations. The earlier
published non-energy `1.0.0` fixture was also read back in ODIP with its pinned
manifest digest; its source and the energy source appear in the ODIP catalog.

These are new protected numerical regression passes on the current AI-enabled
image. They do not constitute the unchanged Gate 5 suite as one automated
cross-project run. Source ingestion/raw artifact lineage and the remaining
end-to-end assertions are assessed separately. AI-10 and Gate 6 stay OPEN.

### ODIP source catalog and failed pipeline attempt

The maintainer read back the published non-energy fixture `1.0.0` with pinned
manifest SHA-256 `f0d4f6b882c1a05154fb43283166953fda7a0dba7f2ed435dd7f46088663bbff`.
The ODIP catalog lists one energy and one non-energy source; the energy dataset
links to the energy source. The source record's `location` is the contract-kit
GitHub **release page**, not the pinned PVGIS source JSON. A subsequent ODIP
pipeline run for that source, `b54ea08e-441e-4835-972f-364dfcfaeb24`, ended
`FAILED` at 19:05:17 UTC. The bounded worker log records `NewConnectionError`
six milliseconds after ingestion started. The worker deployment does not
declare GitHub egress; that configuration is a likely reason for the connection
failure, but the exact network denial was not directly captured. Even if the
page were reachable, its HTML would not be the pinned raw JSON.

No successful raw artifact or link from the published reference versions to a
captured pipeline input is claimed. The source catalog association and the
manifest provenance text are separate facts. The failed attempt left the
already published versions untouched. The sanitized current-image report
retains the source record and a worker-log hash; a future isolated ingestion
case uses the pinned JSON through an approved raw-input path, as recorded below.

### Isolated ODIP raw-input lineage: PASS

For the synthetic test dataset `energy-ai10-lineage-20261027`, the maintainer
linked the existing energy source and temporarily granted the approved ODIP
worker `READ`, `INGEST` and `VALIDATE` on this dataset only. A local wrapper
verified the pinned PVGIS source SHA-256
`d82aff39f867cb3cd77f7f355ec164b2d43c19d27bb86b13e87306885d082f29`,
all five generated artifact digests, the dataset/source association and worker
grants before writing. The protected reference-input API captured the raw JSON,
and ODIP published isolated version `1.0.0`, draft
`9cd77d70-058c-47ed-ab4a-7507af293698`, with canonical manifest SHA-256
`8e98f8efa93806fdda674beee198c4286a852ebbbf937fabe054b404c5d1d215`.

The published draft reports exactly one linked raw artifact
`736d9724-1f27-46d6-ac29-1ef6ba0a0a05`, capture run
`cf7d7208-e9bd-4bf5-8501-5086b61c2322`. Protected raw-byte readback
returned 824,681 bytes with the pinned source digest. All five protected
artifact downloads matched their manifest SHA-256 values. The temporary
operator cookie file had mode `600` and was removed; the clipboard was cleared.
The maintainer confirmed that the three temporary worker grants were revoked
after publication. The [sanitized lineage evidence](evidence/2026-10-27-ai10-isolated-lineage.json)
records IDs, hashes and the operator-confirmed cleanup limit.

This closes the isolated ODIP source-capture/publication path. It does not
retroactively add raw-input links to immutable reference versions `1.0.0` or
`1.0.1`, and it is not a VEF run on the isolated dataset. The failed scheduled
download of the catalog's GitHub release-page URL remains a separate finding.
The unchanged complete deployed Gate 5 suite and AI-10 remain OPEN.

### October 29 follow-up on the AI-enabled test deployment

VEF revision 47, image
`eseidinger/variability-engineering-framework@sha256:3187cc48a5f04fdfb2485194c58f2b12ac69703a15ee585f486b7418359aba89`,
and ODIP revision 10 were ready. The maintainer created new protected VEF
runs for unchanged `1.0.0` and corrected `1.0.1`. Result JSON and all three
candidate pages for each run passed their respective complete 252-candidate
oracles. Both runs recommended the same configuration, with 194 feasible
candidates; annualized costs were 360.67 EUR and 365.64 EUR respectively.
Across versions, candidate IDs, components, feasibility, constraints and all
non-cost metrics matched by ID. Ranking changed as the corrected tariff changes
annualized costs; each ranking matched its own oracle.

On that deployment, the maintainer observed HTTP 422 for non-empty existing
equipment (`existing_equipment_not_supported`), unknown version 9.9.9
(`publication_not_found`) and failed version 1.0.90
(`publication_not_published`). A new budget-zero run returned `INFEASIBLE`,
0 of 252 feasible candidates, null recommendation and `NOT_APPLICABLE`
optimality in protected JSON. A protected readback of the successful 1.0.1
result after these tests was semantically identical to its earlier JSON export;
the saved byte representations differed. The
[sanitized October 29 evidence](evidence/2026-10-29-ai10-current-image-regression.json)
records the run IDs, image and oracle pins, export hashes, checks and limits.
The maintainer then generated an AI explanation for the new corrected run and
confirmed that the rendered output states the recorded optimality, 194/252
count, 365.64 EUR cost, recommendation and synthetic-profile warning correctly.
The protected run JSON remained semantically identical after that AI call.
This rendered review does not establish the raw provider response or every
citation value; those have separate earlier AI-05/06 evidence.
The same CI-published VEF image then ran the private synthetic AI-10 probe as
a temporary scheduled component in revision 48. All ten checks and its final
`cases=10` marker appeared in eleven complete log lines. The checks include
both full oracles, exact-version cache behavior and rejection of tampered
bytes, wrong units, a missing hour with updated digest, unsupported schema,
unpublished state and cross-version cache reuse. The job had no bindings,
network egress or public port. Revision 49 removed it; the single ready web
component retained the same image digest. Its fixture transport was in memory,
so this does not establish a live ODIP read-response mutation or public-route
handling of those injected cases. The sanitized evidence also records the
deployment declaration, operation IDs, log hash and cleanup.
These subcases pass; the complete unchanged deployed Gate 5 suite, AI-10 and
final Gate 6 decision remain open.

### October 29 single deployed ODIP-to-VEF consumer regression: PASS within scope

The new [reproducible consumer script](../scripts/run-deployed-energy-consumer-regression.py),
documented in its [runbook](2026-10-29-deployed-consumer-runbook.md),
completed one protected execution on AI-enabled VEF revision 50, image
`43af99e4107af05a657cf0864555ac466f1003a73fd7e3e21b4d76b997320bfa`,
and ODIP revision 10. It read the published original, corrected and non-energy
manifests through ODIP operator routes and matched all eleven artifact bytes
and digests to pinned fixtures. The human browser principal received
`401 application_access_denied` on ODIP's service-consumer publication route;
the successful VEF runs exercised the configured ODIP service binding.

Within the same execution, new VEF runs for `1.0.0` and `1.0.1` each passed
their complete 252-candidate oracle, recommendation and ranking. Repeating
each request with its idempotency key returned the same run; reusing the key
with changed input returned `409 idempotency_conflict`. Existing equipment,
unknown version and failed publication returned their expected 422 codes with
no run ID in the response. A new budget-zero run returned `INFEASIBLE`, 0/252
and no recommendation. The successful corrected result remained semantically
unchanged after the negative tests. The
[sanitized report](evidence/2026-10-29-deployed-consumer-regression.json) pins
all three publication digests, run IDs, deployment images, report and script
hashes, timing, session cleanup and limits. Temporary browser cookie files and
clipboard contents were removed after the run.

This is a single deployed **consumer** regression, not the complete unchanged
Gate 5 suite: the already recorded isolated source capture was not repeated
inside this invocation, live ODIP read bytes were not mutated, and DEC-10/11
still classify their stated recovery and non-AI operational checks. AI-10 and
Gate 6 remain OPEN.

### October 29 isolated source-to-consumer regression: PASS within scope

The extended runner completed one new automated invocation on AI-enabled VEF
revision 51, image
`eeb22d874e2a0912a939a8a0e7b5a47a115699b12afbf05544838f9ba0c0c1d6`,
and ODIP revision 10. Before writing, it checked the isolated dataset/source,
unused `1.0.1` version, operator rights, absent worker grants, pinned PVGIS
source SHA-256 and all five locally generated artifacts. It temporarily granted
the ODIP worker `READ`, `INGEST` and `VALIDATE` on that dataset only, captured
the raw input through ODIP's reference-input API, uploaded and published the
isolated draft, and waited for worker validation.

ODIP published draft `5c420f42-ec99-4fae-a5c6-73b448d57f62` with canonical
manifest SHA-256
`60eaaf090783e738887715c91e82a3808240e2e1b9d505783a737d5fd14caaa6`.
It links raw artifact `b4e7cf6a-f899-4751-9d8c-dedc6089cad7`, capture run
`d4d0fd5b-c14e-4aa2-8359-df1ed8ed37af`. Protected readback matched all
824,681 pinned raw bytes and all five published artifact bytes. The runner
revoked the temporary grants before continuing; an independent ODIP readback
confirmed both `PUBLISHED` and no remaining worker grant.

In the same invocation, it read all three standard energy/non-energy
publications with eleven matching artifact bytes and created new VEF runs
`run-eacb4949-24e6-44d7-b5e7-8325c8476c12` (`1.0.0`) and
`run-da796a9e-4af6-4165-9d99-be1b8fcce4d1` (`1.0.1`). Each result and all
252 candidates passed its complete independent oracle. Idempotent replay,
changed-body conflict, three 422 denials, zero-budget infeasibility and
unchanged corrected-run JSON also passed. The
[sanitized report](evidence/2026-10-29-deployed-source-to-consumer-regression.json)
pins all images, IDs, hashes, timing, rights cleanup and remaining limits.
Both temporary browser cookie files and clipboard contents were removed.

This is a newly specified equivalent suite, because the October 17 Gate 5
acceptance had no historical executable suite to rerun. The source publication
used a separate synthetic dataset and live ODIP read bytes were not mutated;
the private VEF probe covers that invalid-content boundary with in-memory
transport. The maintainer approved
[DEC-12](../decisions/DEC-12-proposed-ai10-equivalent-regression.md) on October
29 with those limits. AI-10 is ACCEPTED_WITH_LIMITATIONS for the current
release. DEC-13 subsequently accepted bounded Gate 6 while leaving kit
publication and production deployment unauthorized.
