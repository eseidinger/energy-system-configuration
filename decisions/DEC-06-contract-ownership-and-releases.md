# DEC-06: Contract ownership and releases

**Status:** Accepted
**Date:** 2026-10-10
**Decision owner:** Integration Contract Maintainer
**Due date:** 2026-10-10 (completed)

## Context

ODIP and VEF must validate the same immutable schemas, fixtures, and expected
results. Consuming independently copied files or a mutable branch would allow
the implementations to pass against different contracts.

## Decision

### Ownership

- This repository is the source of truth for the shared contract kit.
- The `Integration Contract Maintainer` owns versioning and releases.
- ODIP, VEF, and Developer Platform maintainers review changes affecting their
  boundaries.
- Changes to simulation behavior, tolerances, fixtures, or numerical expected
  results additionally require domain-review approval.
- Repository ownership rules must represent these review responsibilities.

### Layout

The shared kit is maintained under `contract-kit/`:

```text
contract-kit/
├── VERSION
├── schemas/
├── openapi/
├── examples/
├── fixtures/
├── expected-results/
├── platform/
└── tests/
```

Generated artifacts must be reproducible from reviewed source files. Generated
files state how they were produced and are checked for drift in CI.

### Versioning

- The kit uses semantic versions.
- A breaking schema, API, simulation, validation, or expected-result change
  increments the major version. During the pre-1.0 design phase, an incompatible
  change increments the minor version and is called out as breaking.
- Backward-compatible optional fields and additive fixtures increment the minor
  version.
- Documentation and test-runner corrections that do not change contract
  behavior increment the patch version.
- The original implementation baseline was `0.2.0`. Any already published
  `contract-kit-v0.2.0` tag or artifact remains immutable; the reconciled Gate 1
  handoff now targets `0.4.0`.
- The `0.3.0` identity reconciliation breaks the earlier security integration
  assumptions. The reviewed `0.2.0` numerical oracle stays unchanged.
- The subsequent `0.4.0` reconciliation adds the operational-envelope schema,
  example, and component-monitoring/log contract. It is an additive minor change
  with unchanged deployment/access input schemas. Publish `contract-kit-v0.4.0`
  only after review and release checks.
- The proposed `0.5.0` handoff adds the VEF AI assistance profile, proposal and
  explanation schemas, citation validation, examples, and consumer acceptance
  cases. It leaves ODIP APIs, platform identity, and numerical oracles unchanged.
  Publication requires review and release checks; Gate 6 acceptance remains open.
- The first accepted release is `1.0.0`, tagged `contract-kit-v1.0.0` only after
  the integration and release gates pass.

### Release process

1. Submit the change through a reviewed pull request and identify affected
   contracts and consuming projects.
2. Run schema, OpenAPI, example, canonical-serialization, checksum, and expected
   numerical-result tests.
3. Produce a deterministic release archive and a `SHA256SUMS` file.
4. Create an annotated Git tag and publish the archive, checksum file, and
   compatibility notes as an immutable release.
5. ODIP and VEF pin the exact kit version and archive checksum in CI. They do
   not consume the mutable default branch.
6. Never replace an existing release artifact or move an existing version tag.
   A correction receives a new version.

### Licensing

- Repository-authored schemas, OpenAPI definitions, tests, tooling, and software
  configuration use Apache-2.0.
- Repository-authored documentation, examples, synthetic fixtures, and expected
  results use CC BY 4.0.
- Third-party source data is not relicensed. Its source terms, attribution, and
  modification status are carried in `NOTICE` and artifact provenance.
- Every release archive contains `LICENSE`, `NOTICE`, and both complete license
  texts from `LICENSES/`.

## Acceptance evidence

- A clean, repository-neutral runner validates the released archive.
- Rebuilding the same version produces the same archive contents and checksums.
- ODIP and VEF CI report the same pinned kit version and checksum.
- An attempted release without required reviews or passing checks is rejected.

## Consequences

- `SHARED-01` is implemented in this repository rather than copied into one of
  the consuming projects.
- Consumers may cache or vendor a released kit but must retain its version and
  checksum and must not edit the vendored copy.
- Any correction affecting existing expected results requires a new release and
  explicit consumer upgrades.
