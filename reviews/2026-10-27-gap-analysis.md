# Energy configuration gap analysis

Date: 2026-10-27. Basis: the reconciled
[implementation and acceptance review](2026-10-27-implementation-and-acceptance-review.md),
the [use case](../energy-configuration-use-case.md),
[contract](../energy-configuration-integration-contract.md), and Gate 5/6 exit
criteria with the explicit current-release
[DEC-10 recovery-test exception](../decisions/DEC-10-current-release-recovery-test-exception.md)
and [DEC-11 non-AI acceptance exceptions](../decisions/DEC-11-current-release-non-ai-acceptance-exceptions.md).
Prior maintainer acceptances remain valid. This register records that exception
and does not grant final acceptance or silently waive other requirements.

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
The maintainer now accepts the other listed non-AI points without further testing
under DEC-11. Hosted AI-05/06 and AI-08/11 now pass within their recorded
evidence limits. Only AI-10 remains acceptance work; final Gate 6 is open.

The later [current-image oracle report](evidence/2026-10-27-ai10-current-image-oracles.json)
adds two protected browser runs on AI-enabled VEF revision 45. Both full
252-candidate oracles, result provenance and per-version ranking pass; a
cross-version comparison confirms unchanged non-cost metrics and constraints.
The report also records ODIP non-energy publication readback and catalog source
association. It does not convert the separately captured scenarios into the
single unchanged deployed Gate 5 suite required by AI-10.
An ODIP energy pipeline attempt ended `FAILED` with worker `NewConnectionError`;
the registered source points to a GitHub release page rather than the pinned
PVGIS JSON. No successful raw artifact or publication input link is inferred.
The [guided record](2026-10-27-guided-release-acceptance.md#odip-source-catalog-and-failed-pipeline-attempt)
keeps this source-ingestion gap separate from the passed numerical regressions.

| Gap | Current closure status | Still required |
| --- | --- | --- |
| GAP-01 | **Closed for hosted AI-05/06 review:** unproven optimality/missing replacement price and adversarial-metadata resistance pass; 32 and 33 rendered citations respectively match the oracle/fixtures, with assistant semantic review. Marked fixture copies were removed and the short grant revoked. | Retain recorded capture limits; these cases do not prove AI-10. |
| GAP-02 | **Closed within recorded scope:** the private synthetic probe in VEF commit `edc4157` passed seven AI-08/11 checks in local and hosted image execution. The scheduled component succeeded in `vareng-test` revision 40, then was removed in revision 41; earlier public cross-user route checks also passed. See the [hosted record](evidence/2026-10-27-hosted-ai-boundary-probe.json). | Retain the internal resource-method versus public gateway distinction and the in-memory fixture limit. No further AI-08/11 test is required for this release. |
| GAP-03 | **Closed in the configured test environment.** DEC-09 correction published as 1.0.1; both owned runs and all 252 candidates/metrics/ranking/provenance match their independent oracles. Original 1.0.0 readback stays unchanged. See the [guided record](2026-10-27-guided-release-acceptance.md). | Version isolation remains PASS. Additional non-AI archive/inventory checks are ACCEPTED_EXCEPTION (DEC-11); distinct AI-10 obligations remain open. |
| GAP-04 | ODIP's deployed request/upload/status denials passed as recorded in the guided review. VEF commit `5cb913f` then passed ten private hosted checks on the CI-published image: both 252-candidate oracles, exact-version cache behavior and independent verifier/client rejection of tampered bytes, wrong unit, missing hour with matching digest, unsupported schema and unpublished state. The scheduled job succeeded in revision 43 and was removed in revision 44. See the [sanitized AI-10 record](evidence/2026-10-27-hosted-ai10-private-regression.json). | The independent hosted VEF invalid-content subcase is closed within the fake-transport boundary. A real ODIP read-response mutation and the complete unchanged deployed Gate 5 suite on one pinned release image remain unproven; AI-10 stays OPEN. |
| GAP-05 | ODIP actual local restore and VEF transactional interrupted-claim/stale-token tests pass. Hosted ODIP service restart succeeded with a new pod and unchanged image; post-restart corrected-run summary matches the independent oracle. All five subsequent protected operator artifact downloads match manifest hashes and reference bytes. | **ACCEPTED_EXCEPTION:** joint restore under DEC-10; additional non-AI interrupted-workload checks under DEC-11. No recovery VM is required and no unexecuted test is claimed PASS. AI-10-specific assertions remain open. |
| GAP-06 | **Closed for this release by scope decision:** the maintainer selected new installations; [DEC-07](../decisions/DEC-07-new-equipment-release-scope.md), use case 0.3 and prose contract 0.5 record it. Existing-equipment support is deferred. | New-equipment scope remains accepted. Additional non-AI release-review checks are ACCEPTED_EXCEPTION (DEC-11). Carry scope decisions into the next release record without rewriting the immutable kit. |
| GAP-07 | Schema conformance is implemented. The maintainer selected complete UTC calendar years in [DEC-08](../decisions/DEC-08-complete-calendar-year.md); VEF profile/import and ODIP energy validation enforce the rule with boundary tests. Hosted ODIP rejected the isolated 4,368-hour fixture 1.0.90; the later private hosted VEF probe rejected a missing hour even after its descriptor digest was updated. | Annual scope remains accepted and implemented. Additional non-AI acceptance checks are excepted under DEC-11. The private fake-transport boundary does not prove a mutated live ODIP read; carry the decision into the next release record. |
| GAP-08 | 180-day terminal-run/candidate/audit cleanup implemented and tested; minimized ownership-read audit and reproducible model-source capture added. | **ACCEPTED_EXCEPTION (DEC-11):** additional retention/backlog/backup-semantics, durable retention and upgrade-replay verification. Missing evidence remains unverified; implemented controls are retained. |
| GAP-09 | Historical retained envelopes from retired pods are readable for both projects; recent ODIP request correlation metadata and configured seven-day retention were captured. | **ACCEPTED_EXCEPTION (DEC-11):** additional security/rotation, collector/compactor and elapsed-expiry checks. AI-specific evidence required by an open AI case is not accepted by this exception. |
| GAP-10 | Sanitized tracked local and hosted AI evidence summaries, the private hosted AI-10 report and hash-addressed source/corrected-publication bundle created. | **ACCEPTED_EXCEPTION (DEC-11):** additional non-AI storage/inventory/review checks. The complete AI-10 regression and final Gate 6 decision remain open. |
| GAP-11 | Separate dependency metrics, concurrent reservation/claims, stale-claim recovery, timeout classification and exact-limit local compute measurement pass. | **ACCEPTED_EXCEPTION (DEC-11):** additional deployed workload time/memory, queue/persistence/serialization and interrupted-workload verification. No additional performance assurance is claimed. |
| GAP-12 | 24 production-bundle browser/axe checks pass on desktop/mobile; focus/landmark/overflow and stale-poll issues fixed. | **ACCEPTED_EXCEPTION (DEC-11):** additional real-session keyboard/screen-reader/session-expiry review; no new accessibility compliance evidence is claimed. |
| GAP-13 | Hosted ODIP is confirmed to use S3 with active database and bucket bindings. | **ACCEPTED_EXCEPTION:** joint restore under DEC-10; remaining S3 versioning/migration/outage checks under DEC-11. Storage controls remain; unperformed tests are not PASS. |

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
| GAP-02 / P1 | **Closed within recorded scope:** hosted private VEF probe passes invalid source/pointer/value/run and evidence-limit cases; public cross-user checks passed earlier. | VEF | Retain [hosted probe evidence](evidence/2026-10-27-hosted-ai-boundary-probe.json) and its internal-method/in-memory limits; no public mutation endpoint is needed. |
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

## Remaining acceptance execution order

1. Preserve the completed hosted AI-05/06, AI-08/11 and private AI-10 evidence;
   the marked AI-05/06 copies and temporary AI jobs have been removed.
2. Run and record the unchanged deployed Gate 5 suite on the AI-enabled pinned
   release image as one traceable AI-10 regression. Reuse the separate protected
   browser and ODIP observations where the suite permits, but do not label the
   private fake-transport check as a live ODIP read mutation. Apply DEC-10 to
   the joint restore portion and DEC-11 only to its stated non-AI checks.
3. After AI-10 passes, record the three-owner release decision and immutable
   kit, implementation, image and deployment pins for Gate 6.

Historical findings below and earlier operational snapshots remain evidence of
what was and was not tested. DEC-11 supersedes them as non-AI release blockers.

## Work outside this release

General-purpose VEF expression evaluation/configuration completion, portfolio
optimization, reusable SDKs, ODIP Parquet/DuckDB analytics and broader AI data
exploration are separate roadmap work. They are not prerequisites for this
bounded energy demonstration. Commercial offers, measured building profiles and
certified design require the further data/domain review already excluded by the
use case; this analysis does not silently add them to Gate 6.
