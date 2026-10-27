# Energy configuration gap analysis

Date: 2026-10-27. Basis: the reconciled
[implementation and acceptance review](2026-10-27-implementation-and-acceptance-review.md),
the [use case](../energy-configuration-use-case.md),
[contract](../energy-configuration-integration-contract.md), and unchanged Gate 5/6
exit criteria. Prior maintainer acceptances remain valid. This register does not
grant a new acceptance or silently reduce the required scope.

**P1** blocks a claim of complete use-case / Gate 6 release acceptance.
**P2** is operational or usability follow-up that must be resolved or explicitly
scoped for the release. Priorities indicate execution order, not new due dates.
Owners below are responsible project roles, not new individual assignments.

## Follow-up status after autonomous local implementation

The initial findings below describe the source at the start of October 27.
The subsequent [VEF implementation and verification record](https://github.com/eseidinger/variability-engineering-framework/blob/main/docs/04-development/energy-gap-closure-verification.md)
and [ODIP corrected-version runbook](https://github.com/eseidinger/open-data-intelligence-platform/blob/main/docs/energy-configuration-integration-runbook.md#corrected-version-regression-boundary)
supersede their implementation-state statements as follows. The subsequent
[guided deployed record](2026-10-27-guided-release-acceptance.md) closes the
configured test-environment version-isolation case and records request,
publication, upload-integrity, unit and unsupported-schema rejections. Other local checks remain limited to their stated environment;
Gate 6 and final release acceptance remain open.

| Gap | Current closure status | Still required |
| --- | --- | --- |
| GAP-01 | Fresh controlled synthetic AI-05/06 live-model retest passed on October 27 after explicit consent; output/prompt digests and assistant review retained. | Hosted cases and final owner semantic review. |
| GAP-02 | Extended local HTTP tests reject foreign run/source/pointer/value and preserve results; schema and exact UTF-8 boundary checks pass. | Hosted private fixture setup and AI-08/11 execution. |
| GAP-03 | **Closed in the configured test environment.** DEC-09 correction published as 1.0.1; both owned runs and all 252 candidates/metrics/ranking/provenance match their independent oracles. Original 1.0.0 readback stays unchanged. See the [guided record](2026-10-27-guided-release-acceptance.md). | Retain evidence and refresh complete deployment pins under GAP-10. Other AI-10 negatives, ingestion/traceability observation and integrated recovery remain separate open work. |
| GAP-04 | Local suites pass. Deployed non-empty-existing-list and nonexistent-version requests return the expected HTTP 422 codes. ODIP rejects partial-year 1.0.90 as FAILED; after correction 561887e, VEF's hosted retest returns 422 publication_not_published. ODIP missing-hour 1.0.99 is FAILED (worker report/code not captured); wrong-unit 1.0.91 is rejected at upload with 422 schema_validation_failed; tampered 1.0.92 is rejected at upload with 422 checksum_mismatch; unsupported-schema 1.0.93 is rejected at draft creation with 422 unsupported_schema. | Publication-state classification and ODIP missing-hour status checks pass; independent hosted VEF invalid-content checks remain open. Tampered read-response checks and complete release-specific regression remain open. See the guided record for capture limits. |
| GAP-05 | ODIP actual local restore and VEF transactional interrupted-claim/stale-token tests pass. Hosted ODIP service restart succeeded with a new pod and unchanged image; post-restart corrected-run summary matches the independent oracle. All five subsequent protected operator artifact downloads match manifest hashes and reference bytes. | Joint deployed ODIP/VEF database and ODIP S3 object-version restore, real in-progress workload interruption and boundary reconciliation. Configured recovery VM is unavailable and /dev/kvm is absent; isolated target/snapshot selection remains required. |
| GAP-06 | **Closed for this release by scope decision:** the maintainer selected new installations; [DEC-07](../decisions/DEC-07-new-equipment-release-scope.md), use case 0.3 and prose contract 0.5 record it. Existing-equipment support is deferred. | Include the decision in the next immutable kit release under GAP-10. Deployed HTTP 422 existing_equipment_not_supported is now recorded; database run-count capture remains absent. No existing-equipment implementation is claimed. |
| GAP-07 | Schema conformance is implemented. The maintainer selected complete UTC calendar years in [DEC-08](../decisions/DEC-08-complete-calendar-year.md); VEF profile/import and ODIP energy validation enforce the rule with boundary tests. Hosted ODIP rejected the isolated 4,368-hour fixture 1.0.90. | Carry the rule in the next immutable kit release (GAP-10). The hosted VEF HTTP-classification retest passed under GAP-04; the failed ODIP publication is intentionally unavailable for independent hosted VEF content validation. Local verification is recorded in the [VEF scope verification](https://github.com/eseidinger/variability-engineering-framework/blob/main/docs/04-development/energy-release-scope-verification.md). |
| GAP-08 | 180-day terminal-run/candidate/audit cleanup implemented and tested; minimized ownership-read audit and reproducible model-source capture added. | Deployment/retention monitoring, backlog and backup semantics, durable source/image retention and executable upgrade replay. |
| GAP-09 | Historical retained envelopes from retired pods are readable for both projects; recent ODIP request correlation metadata and configured seven-day retention were captured. | Security denial/rotation probes, collector/compactor health and actual elapsed expiry remain open. |
| GAP-10 | Sanitized tracked local evidence summary and hash-addressed source/corrected-publication bundle created. | Fresh timestamped ODIP/VEF image/source inventories now captured in the guided operational snapshot; controlled artifact storage, final platform revision and release-pinned complete inventory/owner acceptance remain open. |
| GAP-11 | Separate dependency metrics, concurrent reservation/claims, stale-claim recovery, timeout classification and exact-limit local compute measurement pass. | Hosted bounded HTTP metrics and current usage snapshots are readable; workload-specific queue/persistence/serialization resource measurements and in-progress recovery remain open. |
| GAP-12 | 24 production-bundle browser/axe checks pass on desktop/mobile; focus/landmark/overflow and stale-poll issues fixed. | Real platform sessions and manual assistive-technology review; mocked HTTP checks do not establish full WCAG compliance. |
| GAP-13 | Hosted ODIP is confirmed to use S3 with active database and bucket bindings. | GAP-13 applies here: joint database/bucket-version restore is required, not optional for this installation. |

The initial October 27 VEF API run found 88 tests: 87 passed and one deployed-only test skipped.
An additional 100,000-candidate × 8,784-hour compute benchmark passed in 15.4 s
with a verified 512-MiB heap limit; it excludes HTTP/database/platform overhead.
The combined API XML inventory at that checkpoint was 91 discovered, 90 passed and 1 skipped,
including the benchmark and two freshly passed controlled AI-05/06 live tests.
There are also 7 passing VEF UI tests, 32 VEF script tests, 87 ODIP worker tests,
and 24 successful browser checks. ODIP Kotlin lint and jar build now pass; the
initial sandbox-related lint limitation was resolved. No local result substitutes
for the unchanged Gate 6 exit criteria. The later publication-classification fix
passed the full API suite with 95 discovered, 93 passed and two explicit skips;
its CI/test deployment and hosted retest also passed. See the guided record.

## Initial gaps and required closure evidence

| ID / priority | Type and gap | Owner | Concrete closure evidence |
| --- | --- | --- | --- |
| GAP-01 / P1 | AI acceptance: AI-05 and AI-06 passed controlled local live-model checks, but hosted unproven-optimality and malicious-metadata scenarios remain open. | VEF | Controlled hosted evidence with `FEASIBLE_NOT_PROVEN` and injected metadata; model/prompt/image/configuration pins, valid citations and human claim review; unchanged result and no unauthorized action. |
| GAP-02 / P1 | AI evidence boundary: AI-08 lacks hosted unapproved-source, unresolved-pointer and altered-value rejection; AI-11 lacks a hosted oversized/incomplete-evidence fixture mechanism. | VEF | Private test setup, hosted rejection before display/model call where applicable, 16/17-source and 64-KiB boundaries, unchanged owned run. Retain the already passed cross-user route checks. Do not add a public evidence-mutation endpoint. |
| GAP-03 / P1 | Corrected-version regression: shared Gate 5 requires corrected `1.0.1`; ODIP's local harness reserves that version for a failed missing-hour draft and republishes unchanged fixture content as `1.0.2`. Neither proves a changed-data VEF result. | Shared contract owner, ODIP, VEF | Agree a deterministic correction and independently reviewed expected deltas; keep the original `1.0.0` oracle immutable. In an isolated test dataset/environment publish valid `1.0.1`, then compare old/new pinned VEF runs and all required provenance. Keep failed-draft tests in a separate identity/version. Existing published versions must never be overwritten. |
| GAP-04 / P1 | AI-10 negative regression: full deployed tamper, wrong-unit, missing-hour, unpublished-version and unsupported-schema scenarios are not evidenced together with the accepted happy path. | ODIP, VEF | One traceable regression report against pinned images, covering every Gate 5 assertion, including rejected runs and preserved earlier state. Include existing invalid-input/idempotency evidence with its environment limitations. |
| GAP-05 / P1 | Integrated recovery: completed VEF run retrieval after workload restart is proven by guided checks; ODIP restart and actual cross-project backup restoration for AI-10 are still missing. ODIP's October 19 confirmation is a separate accepted handoff. | ODIP, VEF, Developer Platform | Restore isolated backups of both applications, reconcile grants/bindings, retrieve publication bytes and candidate pages, and reproduce the reference result. Exercise an in-progress run interruption separately; record actual restore operations, versions and digests. |
| GAP-06 / P1 | Contract implementation: non-empty `existingComponentIds` are in the original use-case scope but `EnergyFeatureModel` rejects them. | Shared model owner, VEF | Define quantities, ownership, compatibility, costs and identity with shared fixtures and implement/test them, or obtain an explicit versioned scope decision narrowing the release to new equipment. Rejection alone is not full existing-equipment support. |
| GAP-07 / P1 | Contract implementation: VEF enforces a typed energy profile, not complete JSON Schema conformance. The publication verifier admits periods of 1–8,784 whole hours; the reference scope specifies a complete year. | VEF, shared contract owner | Trace all schema/profile requirements to validation and negative tests, including optional provenance fields and the supported annual period. Establish equivalent complete validation or add schema validation; retain byte/digest checks. Clarify whether shorter periods are valid outside the reference workflow. |
| GAP-08 / P1 | Lifecycle: VEF lacks the specified 180-day completed-run/evidence purge and dedicated application security-audit lifecycle; model version strings alone do not retain executable model snapshots for future replay. | VEF | Implement and test expiry, related candidate/evidence cleanup and audit retention; define version-to-code/model retention and replay across upgrades. Record backup residual-retention semantics. ODIP already has publication support-end and audit cleanup, so this is not a shared absence. |
| GAP-09 / P1 | Operational evidence: full direct-backend denial, credential rotation/revocation, unrelated-egress denial, retained-log correlation, retired-pod readback and elapsed seven-day expiry are not established by this review. | Developer Platform with ODIP/VEF | Release-linked allowed/denied probes, rotation/adoption/revocation results, separate boundary/readiness signals, retained sanitized correlation, collector/compactor health and actual elapsed expiry. Preserve historical acceptance while closing the current evidence gap. |
| GAP-10 / P1 | Final release record: evidence spans multiple dates, environments and images; several captures are only in ignored `target/` directories or `/tmp`. No complete three-owner Gate 6 acceptance exists. | All cross-project owners | Durable sanitized evidence manifest with case results, repository commits, kit checksum, ODIP/VEF images, deployment definitions, platform revision, model/prompt versions, fixture/oracle hashes and explicit final owner acceptance. Review AI-09's owner-reported HTTP observations and absent run-count capture explicitly. |
| GAP-11 / P2 | Runtime assurance: VEF readiness checks food population and the run table; separate ODIP dependency reporting is absent. Worst-case supported search/resource measurements and concurrent/in-progress recovery evidence remain incomplete. | VEF with Developer Platform | Report dependency health without disabling verified-cache service; measure bounded workload memory/time, queue/timeout/concurrency behavior and interrupted-run recovery on the release configuration. |
| GAP-12 / P2 | User workflow: complete VEF browser accessibility and session-expiry/denial workload evidence is missing. | VEF | Reproducible browser checks for keyboard/screen-reader flow, current-request confirmation, expired/denied identity, recoverable errors and visible model limitations. |
| GAP-13 / P2, conditional | ODIP S3 activation: source and local test infrastructure exist, but installation-specific migration and joint database/bucket restore must be evidenced when S3 is enabled. | ODIP with Developer Platform | Exact object-version reads, unchanged consumer bytes/grants, migration/outage checks and restore of both metadata and retained bucket versions. PostgreSQL-only energy acceptance does not require S3; PostgreSQL-only backup cannot restore new S3-only uploads. |

## Evidence behind implementation gaps

- `GAP-03`: ODIP's
  [local publication harness](https://github.com/eseidinger/open-data-intelligence-platform/blob/60f1b27bf4a8c6392c9e33631a13b508337b0746/scripts/local-publication-acceptance.py)
  mutates `1.0.1` by removing an hour; its `1.0.2` publication has no content
  mutation. The VEF October 26 record reports neither corrected version visible
  in the operator's draft list.
- `GAP-06/07`: VEF's
  [feature model](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/energy/EnergyFeatureModel.java)
  and [publication verifier](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/adapter/odip/EnergyPublicationVerifier.java)
  establish the implemented rejection and validation boundaries. This source
  review does not claim an exploit or a fresh hosted failure.
- `GAP-08/11`: VEF's
  [implementation plan](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/docs/04-development/energy-configuration-implementation-plan.md)
  records the lifecycle, snapshot and readiness gaps; the current repository has
  V1–V3 persistence migrations and startup requeue, not the missing lifecycle.
- `GAP-13`: ODIP's
  [storage runbook](https://github.com/eseidinger/open-data-intelligence-platform/blob/60f1b27bf4a8c6392c9e33631a13b508337b0746/docs/artifact-storage.md)
  and V13 explicitly distinguish exact-version storage from deployed recovery.

## Recommended execution order

1. Retain the passed DEC-09 corrected-data evidence (`GAP-03`) and execute the
   remaining deployed negative/recovery scenarios. The existing-equipment
   release scope (`GAP-06`) and annual period (`GAP-07`) are now resolved by
   maintainer-approved DEC-07/08: new installations and complete UTC calendar years.
   This prevents a technically passing suite from accepting the wrong scope.
2. Complete VEF lifecycle/conformance work and the private hosted AI fixtures
   (`GAP-01/02/07/08`). Keep production calculations and the original oracle
   unchanged unless a separately versioned model decision requires otherwise.
3. Execute the unchanged deployed regression with the release candidate,
   including negative, security, observability, restart and restore scenarios
   (`GAP-03/04/05/09`), plus runtime/UI checks (`GAP-11/12`). Add `GAP-13` only
   for an S3-enabled installation.
4. Assemble durable evidence and request the final owner acceptance only after
   it is reviewable (`GAP-10`). Passing local tests and prior maintainer
   acceptance do not auto-close the remaining Gate 6 cases.

## Work outside this release

General-purpose VEF expression evaluation/configuration completion, portfolio
optimization, reusable SDKs, ODIP Parquet/DuckDB analytics and broader AI data
exploration are separate roadmap work. They are not prerequisites for this
bounded energy demonstration. Commercial offers, measured building profiles and
certified design require the further data/domain review already excluded by the
use case; this analysis does not silently add them to Gate 6.
