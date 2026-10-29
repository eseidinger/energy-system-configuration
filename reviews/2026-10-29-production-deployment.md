# Energy configuration production deployment — 2026-10-29

**Authorization:** [DEC-14](../decisions/DEC-14-production-deployment-authorization.md)
records the maintainer's separate production release approval. DEC-10/11/12
and bounded Gate 6 limits remain in force. This is an application rollout
record, not an independent domain review or a claim of certified suitability.

## Release baseline

The [published contract kit 1.0.0](2026-10-29-contract-kit-1.0.0-release.md)
has archive SHA-256
`ab101a9d5588283ce30c78149084ba145c4c0a6ce3e678c4defff58749951cb0`.
VEF and ODIP pin that same archive. Their kit-adoption CI and automatic test
deployments passed before production authorization. The ODIP test readback on
October 29 confirmed revision 11, web state `ready` at image
`docker.io/eseidinger/odip-platform@sha256:dc27abd5589f7a8532e9a9bb27a357361f5ffeff37ff1e5eb3c49a9cc326f053`,
and active ingestion worker with last result `succeeded`. The VEF test
deployment completed at revision 56 with readiness `ready` and image
`eseidinger/variability-engineering-framework@sha256:f58c9dd95341eed561b295041deb5f4348e06c9a260a0469c58038dee37b9889`.

Before the rollout, the Developer Platform readback showed:

| Project | Revision | Image pin | Readiness |
| --- | ---: | --- | --- |
| `odip` | 19 | web `docker.io/eseidinger/odip-platform@sha256:32356e0997588886a19fdd78e87af85af510e1b96580fbbc2398cc53e550d26b`; worker `docker.io/eseidinger/odip-data-worker@sha256:83039fa16ba2bbf726529f9f328d1af60c230e5822c7c5a276091d45c6a048f2` | web `ready`; worker `active`, previous run `succeeded` |
| `vareng` | 16 | `eseidinger/variability-engineering-framework@sha256:41f980f1f35224d7d720d6f426fbd93790d8f3203a308e7c83776fa573fd1119` | web `ready` |

The production descriptors render tag `v1.0.0` into the respective image
references and retain the existing project targets, platform bindings, source
egress and AI configuration. ODIP is rolled out first, then VEF. The final
tagged CI, applied revisions, image digests and readiness are recorded below.

## ODIP 1.0.0

The annotated ODIP [v1.0.0 release](https://github.com/eseidinger/open-data-intelligence-platform/releases/tag/v1.0.0)
points to commit `2d958fdf6d83fe0cf0f240e6a7b5accdf6ecb957`. Its
[tagged CI run 40885615114](https://github.com/eseidinger/open-data-intelligence-platform/actions/runs/40885615114)
passed the Web, worker, Platform API, image publication and production
deployment jobs. The production deploy applied `odip` revision **20**.

The later Developer Platform readback showed the web `ready`, with only the
new image in its active image IDs:
`docker.io/eseidinger/odip-platform@sha256:fd32cc942d799ea800bab6012fc0d012b1c9dbf253fafc5da56f6051d2f72034`.
The scheduled worker was `active` with resolved image
`docker.io/eseidinger/odip-data-worker@sha256:27e9bb07c791573803529a0d093f3e20df23765dcb01080e0b4a3ea4fe115577`.
A later readback showed a scheduled worker completion at 14:02:49 UTC with
result `succeeded`, after the deployment. The platform status did not expose a
per-run image ID, so this does not independently pin the worker execution
image. No new production dataset publication was performed for this release.

## VEF 1.0.0

The annotated VEF [v1.0.0 release](https://github.com/eseidinger/variability-engineering-framework/releases/tag/v1.0.0)
points to commit `e27902173abbfa64313d447132b4d66188b360d5`. Its
[tagged CI run 40886923681](https://github.com/eseidinger/variability-engineering-framework/actions/runs/40886923681)
passed the pinned kit, documentation, API, UI, Compose package integration,
image publication and production deployment jobs. The workflow's protected
public-entry check also passed. The deploy applied `vareng` revision **17**.

The later Developer Platform readback showed `ready` with only the new
application image active:
`eseidinger/variability-engineering-framework@sha256:83e26c8ba74016cb8b51fdb9f7d2a3ed6bc372ac5190d7595f1a21e1fa61e3ca`.
The production descriptor resolves ODIP to
`https://web-odip.apps.eseidinger.de`, enables the configured AI model, and
retains its existing binding and outbound rules.

## Release conclusion and limits

Both versioned production applications are deployed and ready on the observed
revisions. The same contract-kit 1.0.0 checksum is pinned in both source
trees. The CI and Developer Platform observations establish release packaging,
deployment and readiness; they do not establish a fresh authenticated
end-to-end production optimization run or a new dataset publication.
DEC-10/11/12 exceptions and the missing independent qualified domain review
remain visible under DEC-14. User-visible energy results continue to disclose
the synthetic 2024 reference-profile provenance and are not certified system
designs.
