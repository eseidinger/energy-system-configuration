# Gate 6 release candidate review — bounded energy configuration

**Status:** DRAFT for cross-project owner review; Gate 6 OPEN

**Observed:** 2026-10-29 12:08–12:09 UTC in `vareng-test` and `odip-test`

**Scope:** New installations, complete UTC calendar years, synthetic Wasserburg
reference data. This record prepares an acceptance decision. It does not
authorize production deployment, contract-kit 1.0.0 publication or release
tagging.

## Exact candidate inventory

| Item | Pin and verification |
| --- | --- |
| Shared source | `energy-system-configuration` `f804f79bb65a0336fef842c4bbc77e9e4ab15170`; [Contract kit CI](https://github.com/eseidinger/energy-system-configuration/actions/runs/40869477423) PASS. |
| Released consumer contract | Kit `0.5.0`, archive SHA-256 `ae4edaf6799d4b57510d14d2004c5b65ff6b05f3b225e96bbd5971b30ce8832b`; immutable `contract-kit-v0.5.0` source commit `a244b1e9596fee5c2bc99f7e29b7a42d572cc993`. Both consumers pin this archive hash. |
| VEF source and CI | `a31b3363987a1075c55845077011238ef854c39e`; [Build, test and publish](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40869477768) PASS, including API, UI, packaged integration and contract checks. Compared with tested implementation commit `5cb913f`, the later changes are documentation files only. |
| VEF test deployment | `vareng-test` revision **54**, web image `eseidinger/variability-engineering-framework@sha256:a9a3e10dc9e60d6c65a6b03e0e05e9cf9b8228620209d0d7fc4f6805e1aa322c`, `ready` at 12:08:48 UTC. Canonical JSON SHA-256 of applied spec: `c7a1d54f91dd37be86ba6961e5cdfa9a0db96898231c528d170545cfcafeb901`. Image and revision match the VEF CI run above. |
| ODIP source and CI | Runtime image source `31c4602a256be89287a8df305670269a5da22c1c`; [build and publish](https://github.com/eseidinger/open-data-intelligence-platform/actions/runs/40490378594) PASS. Current repository head `931e11ce08cc9e3910b27be7239e8884d92ebe0a` differs from that build in documentation files only. |
| ODIP test deployment | `odip-test` revision **10**, web image `docker.io/eseidinger/odip-platform@sha256:bf4648d452a4542cf18fda6d1d5b5b0b3b8a2fd600ce460e5594df988fd6ebef`, worker image `docker.io/eseidinger/odip-data-worker@sha256:6acce327d1b15fc0223dddeb7a0f5e1e0f397f3b71a9a7dfbb2ca357465eca02`. Web `ready`, worker `active` at 12:08:49 UTC. Canonical JSON SHA-256 of applied spec: `c8ac99bf75e20f62fab92ceb6591a6c5561fc80bba5f25a777714b642b1750fd`. Images match the ODIP CI run above. |
| VEF deployment source definitions | `application-test.json` SHA-256 `d79df68d4d9f3437884e3eb58cbd402d75d1a3a715d32cf9f0c30d9d22815f93`; production `application.json` SHA-256 `0830cac87c4c36cddbf2b59fdf94ead82d72f047b9ae35e717d2c0b4a3903f81`. These are repository files, distinct from the applied spec hash. |
| ODIP deployment source definitions | `infrastructure/deployments/application-test.json` SHA-256 `e9be64e140887bd1241e8380c44430e131bdd6eec07181ac6d2a589e0a1d98b6`; production `application.json` SHA-256 `692f07b15f6f72617ff36f1cec00cda004b3fe31ad42dce4d1059d45686008d6`. |
| AI model and explanation prompt | Test deployment config `ENERGY_AI_ENABLED=true`, model `gpt-6.1-sol`. Hosted AI-05/06 evidence pins explanation prompt SHA-256 `1264407e104ff69d397b41ae8a7d45319826950b00c920a5f76d5da693002b82` on their tested image. This is a historical prompt evidence pin, not a new prompt-byte readback from revision 54. |
| Numerical models | `energy-model/1.0.0`, `energy-simulation/1.0.0`, `energy-optimizer/1.0.0`, as verified in the deployed [AI-10 current-image record](evidence/2026-10-29-ai10-current-image-regression.json). |
| Fixture and oracles | Released 1.0.0 manifest SHA-256 `252b90b18b594a764a2744ba133a8db56b233e9e375301befc7616e9c18c1715`; corrected 1.0.1 manifest `ebfd2cc7dcdf73cef4ed81a94b693ec23c4448460c8161ca648369ea0a930f93`; non-energy manifest `f0d4f6b882c1a05154fb43283166953fda7a0dba7f2ed435dd7f46088663bbff`. Released 1.0.0 oracle SHA-256 `2f078373092a640e138649a2a589231ec6fd8a795538d18358f482481ac2a069`; independent corrected oracle `8b2f66dd5774c001017f7b3d6158c7999ee4a03bb80031eb5214b25faaeafc13`. The isolated runner's fixture archive was `8fbb0cf6fb7d65da84be8ee554b5ae48abc808bd4cdb048787f99649d46e9d74`. |

The Developer Platform CLI exposes API capabilities and the applied project
specs but did not return an immutable control-plane source/image revision in
these read-only queries. Record that platform build pin before final acceptance
if the owners require it; do not infer one from application revision numbers.

## Acceptance evidence and limits

| Boundary | Current disposition |
| --- | --- |
| Gate 5 deterministic workflow | Accepted by maintainer direction on October 17, without an executable historical suite or report. Current 1.0.0 and corrected 1.0.1 complete 252-candidate oracles pass in the [new source-to-consumer regression](evidence/2026-10-29-deployed-source-to-consumer-regression.json). |
| AI-01–04 and AI-07 | Owner-confirmed walkthrough and manual explanation review, with the capture limits recorded in the [VEF implementation plan](https://github.com/eseidinger/variability-engineering-framework/blob/main/docs/04-development/energy-configuration-implementation-plan.md). |
| AI-05 and AI-06 | Hosted real-model explanation, rendered citation and semantic reviews pass with their [AI-05](evidence/2026-10-27-hosted-ai05-review.json) and [AI-06](evidence/2026-10-27-hosted-ai06-review.json) limits. |
| AI-08 and AI-11 | Hosted private validation boundary passes with the [internal-method/in-memory limits](evidence/2026-10-27-hosted-ai-boundary-probe.json). |
| AI-09 | Guided hosted provider outage, deterministic-result retrieval and recovery pass; malformed output was checked locally. Owner-reported HTTP observations and the absence of an independent run-count capture remain explicit in the [guided record](2026-10-27-guided-release-acceptance.md). |
| AI-10 | [DEC-12](../decisions/DEC-12-proposed-ai10-equivalent-regression.md) classifies it ACCEPTED_WITH_LIMITATIONS for this release. The new isolated source-to-consumer suite passed on VEF revision 51 and ODIP revision 10. Its VEF image differs from currently deployed revision 54; only documentation source changed. Private invalid-content transport was in memory, standard immutable versions were read rather than republished, and the historical unchanged Gate 5 suite was not executable evidence. |
| Recovery and other operations | [DEC-10](../decisions/DEC-10-current-release-recovery-test-exception.md) and [DEC-11](../decisions/DEC-11-current-release-non-ai-acceptance-exceptions.md) are ACCEPTED_EXCEPTION for their stated current-release checks, not test PASS. |
| User-visible scope | New equipment only under DEC-07; complete calendar years under DEC-08. Results warn that the 2024 calendar profile derives from PVGIS 2023 with a synthesized leap day. |

## Exact remaining decisions and release actions

1. **Cross-project owner review:** The Integration Contract Maintainer and the
   ODIP, VEF and Developer Platform boundary maintainers review this inventory,
   case dispositions and DEC-10/11/12 limits. Record who accepts the bounded
   `VEF-05`/Gate 6 outcome and contract version 1.0.0, or record any objection.
   One maintainer's DEC-12 approval is not this final multi-boundary decision.
2. **Version 1.0.0 candidate:** Incorporate approved DEC-07/08 scope and
   compatibility notes into a new immutable kit candidate, review affected
   contracts/consumers, run schema, OpenAPI, example, canonicalization,
   checksum and numerical tests, and produce a deterministic archive plus
   `SHA256SUMS`. Keep the existing 0.5.0 archive and consumer locks unchanged
   until coordinated adoption is approved.
3. **Release only after Gate 6 approval:** Annotated
   `contract-kit-v1.0.0` tag, release archive, checksum and compatibility notes,
   plus coordinated consumer pins and immutable implementation/image/deployment
   identifiers. Production deployment is a separate action requiring explicit
   authorization. Neither tag nor production deployment has been performed.

**Gate 6 decision:** PENDING. **Contract kit 1.0.0 publication:** NOT STARTED.
