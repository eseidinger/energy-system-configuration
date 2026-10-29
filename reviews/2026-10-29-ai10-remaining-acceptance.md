# AI-10 remaining acceptance decision

**Status:** OPEN; review aid, not an acceptance decision

**Environment:** `odip-test` and `vareng-test`

**Contract:** released kit 0.5.0, `AI-10`

## Requirement and evidence

The AI-10 case requires the unchanged deployed Gate 5 suite to pass with AI
enabled and identical confirmed requests to retain their expected feasible
sets, metrics, ranking, recommendation and provenance. The October 17
[Gate 5 decision](2026-10-17-gate-5-acceptance.md) accepted Gate 5 on maintainer
authority. It explicitly did not record an executable suite or test report.
Consequently there is no historical automated suite that can literally be
rerun unchanged.

The following execution evidence exists:

| Boundary | Evidence | Outcome and limit |
| --- | --- | --- |
| ODIP raw source to isolated publication | [October 27 lineage](evidence/2026-10-27-ai10-isolated-lineage.json) | Pinned PVGIS JSON, linked raw artifact, validation, publication and five artifact bytes PASS. It used a new synthetic dataset, not the immutable standard versions. |
| VEF protected numerical and AI checks | [October 29 current-image record](evidence/2026-10-29-ai10-current-image-regression.json) | Both 252-candidate oracles, selected 422 boundaries, infeasibility, stored-result stability and rendered explanation PASS; private ten-check verifier/client probe PASS on its pinned image. The private transport was in memory. |
| ODIP-to-VEF deployed consumer path | [single consumer report](evidence/2026-10-29-deployed-consumer-regression.json) | One automated invocation checked three published manifests, eleven artifact bytes, two new full VEF oracles, idempotency, three 422 denials, infeasibility and retained success. It read existing publications and did not ingest a new source. |
| New isolated source-to-consumer suite | [single source-to-consumer report](evidence/2026-10-29-deployed-source-to-consumer-regression.json) | One automated invocation on AI-enabled VEF revision 51 and ODIP revision 10 captured pinned PVGIS raw bytes, published an isolated 1.0.1 with five matching artifacts, removed the scoped worker grants, read all three standard publications and ran two new full VEF oracles plus idempotency, denials, infeasibility and retained-state checks. The new source publication was isolated; immutable standard versions were not republished. |
| Recovery and additional operational checks | [DEC-10](../decisions/DEC-10-current-release-recovery-test-exception.md), [DEC-11](../decisions/DEC-11-current-release-non-ai-acceptance-exceptions.md) | Current-release exceptions, not test PASS. The exceptions do not automatically accept AI-10. |

The VEF source difference from implementation commit `5cb913f` through
documentation commit `db26bfd` consists only of documentation files. The
recorded tests nevertheless ran on their stated, distinct OCI digests; source
equivalence must not be reported as a same-image execution.

## Exact remaining choice

1. **Accept the newly executed equivalent suite with explicit limits.** The
   owner can accept the single isolated source-to-consumer run together with
   the separate private invalid-content probe and DEC-10/11 exceptions for
   this bounded release. A versioned decision must say that the historical
   *unchanged* Gate 5 suite never existed as executable evidence, the fresh
   source publication used a separate synthetic dataset, and live ODIP bytes
   were not corrupted. This is an acceptance decision, not a claim that those
   unexecuted assertions passed.
2. **Require a literal clean-baseline Gate 5 execution.** Provision a separate
   clean environment where the standard dataset identity/version can be
   freshly published, define an executable baseline for every non-excepted
   assertion, and add a safe live read-fault seam if that boundary must be
   observed through the actual ODIP transport. This remains new test work;
   there is no old executable suite to rerun unchanged.

Until the maintainer chooses and records one path, AI-10 and final Gate 6 stay
OPEN. No production deployment or kit 1.0.0 publication follows from these
test results alone.
