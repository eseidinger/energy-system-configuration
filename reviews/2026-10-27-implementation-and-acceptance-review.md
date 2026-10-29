# Energy configuration implementation and acceptance review

Date: 2026-10-27. Scope: `UC-ENERGY-01` across Energy System Configuration,
Variability Engineering Framework (VEF), and Open Data Intelligence Platform
(ODIP). This is a source and evidence review, not a new maintainer acceptance.

**Current disposition (October 29):** The maintainer approved
[DEC-12](../decisions/DEC-12-proposed-ai10-equivalent-regression.md). AI-10 is
ACCEPTED_WITH_LIMITATIONS for this release; the later
[DEC-13](../decisions/DEC-13-bounded-gate-6-acceptance.md) accepts bounded
Gate 6 with DEC-10/11/12 limits. The older
case counts and OPEN statements below are historical review checkpoints. Kit
1.0.0 and application v1.0.0 were subsequently released; the bounded
[Gate 6 is closed with limitations](2026-10-29-gate-6-closure.md).

The bounded new-equipment workflow and AI assistance are implemented. Gate 5
remains accepted by maintainer direction; ODIP's publication handoff also remains
accepted. Gate 6 and the final cross-project release are **open**. Five AI case
IDs remain incomplete, and the original use-case scope exceeds the implemented
new-equipment model. The subsequent [gap analysis](2026-10-27-gap-analysis.md)
separates missing implementation, missing evidence, and scope decisions.

Latest same-day acceptance state: hosted AI-05/06 citation and semantic reviews
and the private hosted AI-08/11 validation boundary now pass within their
recorded limits. Only AI-10 and final Gate 6 remain open. The five-case count
above is the original review snapshot; see the [guided acceptance](2026-10-27-guided-release-acceptance.md)
and [current gap status](2026-10-27-gap-analysis.md) for subsequent evidence.
The later private hosted AI-10 probe passed ten verifier/client/optimizer checks
on the CI-published image and was removed from `vareng-test`; its
[sanitized record](evidence/2026-10-27-hosted-ai10-private-regression.json)
closes the independent VEF invalid-content subcase, not the complete unchanged
deployed Gate 5 regression. AI-10 and Gate 6 therefore remain open.
Two subsequent protected browser runs on the current AI-enabled VEF image also
pass the complete original and corrected 252-candidate oracles. Their
[sanitized report](evidence/2026-10-27-ai10-current-image-oracles.json) keeps
deployment, export and oracle hashes. The full cross-project suite remains
unrecorded as one automated run.
An isolated ODIP test publication subsequently passed raw PVGIS byte capture,
linked-input readback, publication and all five artifact digests; its
[sanitized record](evidence/2026-10-27-ai10-isolated-lineage.json) keeps it
separate from immutable reference versions and the failed catalog download.

## Same-day implementation follow-up

This review preserves the initial source/evidence assessment. After that audit,
the independently actionable schema, retention/audit, runtime, browser and local
corrected-version findings were addressed. See the
[updated gap status](2026-10-27-gap-analysis.md#follow-up-status-after-autonomous-local-implementation)
and [VEF verification record](https://github.com/eseidinger/variability-engineering-framework/blob/main/docs/04-development/energy-gap-closure-verification.md)
for the new tests and remaining boundaries. In particular, full schema validation
and 180-day cleanup are now implemented locally, ODIP uses genuinely corrected
1.0.1 data in its local harness, and Kotlin lint/build passed. These changes do
not rewrite the initial findings below or close hosted Gate 6 acceptance.

## Subsequent maintainer scope decision

On October 27 the maintainer selected new installations for the current release.
[DEC-07](../decisions/DEC-07-new-equipment-release-scope.md) closes GAP-06 by explicit
scope reduction. Use case 0.3 and prose contract 0.5 supersede the original
existing-equipment obligations for this release. The maintainer subsequently
selected complete UTC calendar years in [DEC-08](../decisions/DEC-08-complete-calendar-year.md);
VEF and ODIP enforce that annual boundary. The initial assessment and
released kit 0.5.0 remain historical baselines; Gate 6 is still open.

## Baseline and evidence rules

The three working trees were clean at the start of this review. Reviewed source
revisions, before these documentation changes:

| Repository | Revision | Role |
| --- | --- | --- |
| Energy System Configuration | `a244b1e9596fee5c2bc99f7e29b7a42d572cc993` | Shared requirements, contracts, fixture, oracle, gates. |
| [VEF](https://github.com/eseidinger/variability-engineering-framework/tree/64b9293fedb83d581a060008d1db844bdc710eb0) | `64b9293fedb83d581a060008d1db844bdc710eb0` | Configuration, simulation, optimization, owned runs and AI workflow. |
| [ODIP](https://github.com/eseidinger/open-data-intelligence-platform/tree/60f1b27bf4a8c6392c9e33631a13b508337b0746) | `60f1b27bf4a8c6392c9e33631a13b508337b0746` | Publication, input lineage, access control and artifact storage. |

Both consumer locks pin kit **0.5.0**, archive SHA-256
`ae4edaf6799d4b57510d14d2004c5b65ff6b05f3b225e96bbd5971b30ce8832b`.
The prose integration contract remains version **0.4**; its AI profile is additive
in kit 0.5.0. Publication/energy schemas remain **v1**; reference dataset, model,
simulation and optimizer versions remain **1.0.0**. These version numbers do not
imply acceptance of the final contract release 1.0.0.

Evidence is distinguished as source implementation, local automated checks,
recorded CI, guided hosted observations, and explicit maintainer acceptance.
None substitutes automatically for another. Historical dated records retain
their original scope; newer observations supersede their open-item snapshots.
Hosted observations below are taken from the repositories, not from a fresh
inspection of running deployments. Developer Platform is an external dependency;
its current deployment, backups and access boundary were not independently
re-audited here.

## Implementation and work-package status

| Package | Implemented behavior / evidence | Remaining boundary |
| --- | --- | --- |
| SHARED-01 | Released kit, schemas, OpenAPI, energy/non-energy fixtures, reviewed numerical oracle, AI cases; identical consumer pins. | Final release evidence and scope reconciliation. |
| ODIP-01/02 | Generic draft/validation/publication lifecycle; immutable bytes, SHA-256 ETags, conditional reads, discovery and versioned retrieval. | Corrected-data deployed regression; local version-isolation harness does not cover the full VEF scenario. |
| ODIP-03 | Stable-principal dataset grants, scoped worker claims, platform principal checks, constrained source retrieval. | Complete retained hosted boundary/rotation/revocation evidence. |
| ENERGY-01 | Isolated worker energy profile reproduces five artifacts from pinned PVGIS input and synthetic profiles/catalog; semantic validation. | Commercial catalogs and measured building profiles are outside this demonstration. |
| VEF-01 | HTTPS exact-version import, managed credentials, byte/role/unit/period checks, atomic verified cache and outage fallback. | Full schema conformance, corrected-version and remaining negative-case evidence. |
| VEF-02/03 | Bounded new-equipment generation, hourly simulation, exhaustive cost ranking; 252 evaluated and 194 feasible reference candidates. | Non-empty existing equipment is explicitly rejected; general framework generation is separate roadmap work. |
| VEF-04 | Owned durable runs, principal-scoped idempotency, candidate paging, evidence, UI, startup requeue and timeout. | 180-day deletion/audit, model snapshot/replay assurance, in-progress recovery, complete backup-restore proof. |
| VEF-05 | Natural-language proposals, current-request confirmation, bounded evidence, citation validation, provider failure handling and live explanations. | Five incomplete AI case IDs; semantic review and hosted fixtures. |
| DP-01/02/03 | Deployment declarations, managed bindings, protected HTTPS route and operational integration recorded. | Complete release-specific runtime/security/retention/recovery evidence; descriptors alone are insufficient. |
| INT-01 | Gate 5 accepted on maintainer authority; substantial later hosted regression recorded. | Unchanged complete Gate 5 regression required again by AI-10. |

Source anchors: VEF's [architecture](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/docs/02-architecture/energy-configuration.md),
[energy implementation](https://github.com/eseidinger/variability-engineering-framework/tree/64b9293fedb83d581a060008d1db844bdc710eb0/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/energy),
[publication verifier](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/apps/prototype/api/src/main/java/de/eseidinger/variabilityengineering/adapter/odip/EnergyPublicationVerifier.java),
ODIP's [publication service](https://github.com/eseidinger/open-data-intelligence-platform/blob/60f1b27bf4a8c6392c9e33631a13b508337b0746/services/platform-api/src/main/kotlin/de/eseidinger/odip/platform/publication/PublicationService.kt)
and [energy adapter](https://github.com/eseidinger/open-data-intelligence-platform/blob/60f1b27bf4a8c6392c9e33631a13b508337b0746/workers/data-worker/src/odip_worker/energy/profile.py).

ODIP has also implemented an optional S3 adapter and controlled artifact migration
after its accepted PostgreSQL publication milestone. Migration V13 retains
metadata/lineage in PostgreSQL, pins exact object versions and queues deletions.
Parquet/DuckDB analytics remain future work. Source availability of S3 does not
prove activation or joint database/bucket recovery in an installation, and is
not a prerequisite for the PostgreSQL energy demonstration.

## Acceptance and use-case coverage

| Milestone | Recorded status | Evidence limit |
| --- | --- | --- |
| Gates 0–1 | Decisions/domain review and shared baseline accepted. | Bounded maintainer-reviewed demonstration. |
| Gates 2–5 | [Accepted 2026-10-17](2026-10-17-gate-5-acceptance.md) for progression. | Maintainer authority; no new automated suite or digest inventory supplied by that decision. |
| ODIP handoff | [Accepted 2026-10-19](https://github.com/eseidinger/open-data-intelligence-platform/blob/60f1b27bf4a8c6392c9e33631a13b508337b0746/docs/energy-configuration-integration-plan.md#completion-criteria), ODIP 0.5.0 / kit 0.5.0, including maintainer-confirmed restoration. | No new independent execution bundle accompanied confirmation; does not close later cross-project AI-10 recovery. |
| Deployed VEF AI journey | Owner-confirmed 2026-10-19 after VEF v0.5.1; guided test checks through 2026-10-26. | Environment- and case-specific evidence. |
| Gate 6 / final release | Open. | AI-05/06/08/10/11 incomplete; final owner acceptance and release inventory absent. |

The authoritative chronological consumer evidence is VEF's
[verification record](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/docs/04-development/energy-contract-kit-verification.md).
Its latest recorded test deployment is revision 21 on October 26, image
`sha256:e4ab9ac14f97001f3bb39f4b2b3745715699a63ab45da1645d53990c35162967`,
following recorded CI run `40353197285`. This is a historical deployment
observation, not a claim about the image currently running.

| Use-case acceptance scenario | Evidence through October 26 | Still required |
| --- | --- | --- |
| Successful recommendation | Exported deployed result and all 252 candidates matched the released oracle on October 24, including 194 feasible candidates, ranking, metrics and provenance. | Preserve a release-specific complete evidence bundle. |
| Infeasible request | Guided zero-budget result and AI-07 checks; local calculation tests. | Include in the final regression execution. |
| Reproducibility | Exact reference comparison, fresh cached-outage run, idempotent replay and completed-run retrieval after VEF restart. | Actual integrated backup restoration and interrupted-run replay. |
| Data version isolation | ODIP has immutable version storage and a local multi-version harness. | Publish genuinely corrected data and verify old/new VEF runs; neither missing `1.0.1` nor a byte-identical `1.0.2` fixture establishes this. |
| Traceability | Verified manifest/artifact bytes, recorded model versions, candidate evidence and validated citations. | Durable release captures and model/audit lifecycle assurance. |
| Safe AI assistance | AI-01–04 and AI-07 guided evidence; AI-09 guided outage/recovery plus controlled malformed-output tests. | Hosted AI-05/06/08/11 and complete AI-10; no blanket “six fully hosted passes” claim. |
| Deployed integration | ODIP-backed journey, dataset denial, verified cache fallback, VEF restart, replay/conflict, negative-demand 422 retest. | Remaining security, ODIP restart/observability and integrated recovery scenarios. |

Alternative scenarios are partly covered: invalid customer input (`UC-ALT-01`),
infeasibility (`03`) and ODIP outage with verified cache (`05`) have guided hosted
evidence. Invalid/incomplete data and tamper rejection (`02`), missing AI
evidence (`06`) and malicious metadata (`07`) have local/controlled coverage but
still need the outstanding hosted cases and release review. Operational run
failure (`04`) has an implemented failed-run path; final hosted timeout/recovery
evidence remains part of GAP-05/11. See the
[AI runbook](https://github.com/eseidinger/variability-engineering-framework/blob/64b9293fedb83d581a060008d1db844bdc710eb0/docs/04-development/energy-ai-acceptance-runbook.md)
for per-case assertions and limitations.

## Checks executed for this review

All commands use local checkouts; no hosted mutation, live AI call, publication,
deployment or release was performed. These checks assess the inspected source,
not the historical hosted image.

| Check | Result on 2026-10-27 |
| --- | --- |
| Shared kit: `uv run --offline --frozen pytest -q` in `contract-kit` | 82 passed. |
| ODIP: `python3 scripts/verify-contract-kit.py` | Archive checksum and every vendored byte match kit 0.5.0. |
| ODIP worker: locked offline `python -m unittest discover -s workers/data-worker/tests` | 87 passed. |
| VEF: `python3 -m unittest discover -s scripts -p 'test_*.py'` | 29 passed; bootstrap operations are mocked. |
| VEF API: offline Maven `test` selecting the ten classes below against ODIP's checksum-verified vendored kit | 41 passed, zero failures/errors/skips; Checkstyle also passed. No database-backed HTTP suite or live model call. |
| VEF UI: `npm test -- --watch=false` | 6 passed in 2 files. |
| ODIP UI: `npm test -- --watch=false` | 13 passed in 4 files. |
| ODIP worker: `uv sync --offline --locked` and locked offline `ruff check src tests ../../scripts` | Passed. |
| ODIP API: `./gradlew --offline --no-daemon ktlintCheck` | Could not start: the sandbox made the Gradle wrapper cache lock under `~/.gradle` read-only. No Kotlin lint result is claimed. |
| Documentation | VEF's link checker passed; 425 local link targets across the repositories resolved, including changed cross-project links mapped to local checkouts. Whitespace checks passed in all three repositories. |

The API selection was `EnergyFeatureModelTest,EnergyFeatureModelConformanceTest,EnergyInputValidationTest,EnergyOptimizerConformanceTest,EnergyPublicationClientTest,EnergyPublicationVerifierTest,EnergySimulationConformanceTest,EnergyExplanationTest,ProposalPromptTest,ProposalServiceTest`.
Run from `apps/prototype/api` with `ENERGY_CONTRACT_KIT_DIRECTORY` pointing to the
verified kit and `./mvnw --offline --batch-mode --no-transfer-progress
-Dtest=<selection> test`. All 258 selected automated tests passed. Logs from this
review are local `/tmp/energy-review-vef-maven.log`,
`/tmp/energy-review-vef-ui.log` and `/tmp/energy-review-odip-ui.log`; these transient
logs are not a durable release acceptance bundle.

Full PostgreSQL/Compose, deployed security/recovery, hosted AI and S3 provider
acceptance must not be inferred from these checks. Existing reports remain
historical evidence unless an explicit fresh execution is listed here.

## Documentation reconciliation

The current shared plan now names the adopted 0.5.0 baseline and implemented AI
workflow. VEF summaries reflect October 24–26 observations instead of the older
deferred cross-user/outage status. ODIP distinguishes its accepted publication
milestone from subsequent regression and documents S3 as implemented, including
V13 storage references, while keeping analytical work planned. Historical review
records, released kit bytes and acceptance decisions remain unchanged.

The [gap register](2026-10-27-gap-analysis.md) is the common follow-up baseline.
Consumer implementation plans link to it; their detailed verification records
remain the authority for individual observations.
