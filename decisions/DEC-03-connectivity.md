# DEC-03: Connectivity

**Status:** Accepted
**Date:** 2026-10-10
**Decision owner:** Integration repository maintainer
**Due date:** 2026-10-10 (completed)

## Context

VEF must retrieve immutable ODIP publications while the applications remain in
separate Developer Platform projects. The first release needs an encrypted,
authenticated route without making a new private-routing platform feature a
prerequisite.

## Decision

- VEF accesses ODIP through ODIP's stable public HTTPS application ingress.
- Public ingress means network-reachable, not anonymously readable. ODIP's
  publication endpoints require the application identity defined by `DEC-04`.
- TLS is mandatory and uses a certificate managed through the target platform
  installation.
- VEF egress is limited to the ODIP API hostname and the Keycloak token endpoint
  on port 443, plus platform-provided DNS.
- ODIP egress is limited to the Keycloak discovery and JWKS endpoints on port
  443 where key retrieval is not supplied locally.
- VEF rejects redirects to another origin. Publication artifact paths are
  relative and may resolve only against the trusted ODIP manifest origin.
- A private cross-project service route is deferred. Adding one later must
  preserve the same application authentication and authorization behavior.

## Acceptance evidence

- VEF resolves the configured ODIP and Keycloak names and verifies their TLS
  certificates.
- An authenticated ODIP publication request succeeds from the VEF project.
- An unauthenticated ODIP request and a request to an unrelated destination
  fail.
- A manifest redirect or artifact path targeting another origin is rejected.

## Consequences

- Developer Platform owns ingress, TLS integration, secret delivery, DNS, and
  least-privilege egress configuration.
- Keycloak and ODIP application authorization remain distinct from Developer
  Platform control-plane authorization.
- Both the ODIP hostname and Keycloak hostname are deployment configuration;
  neither is embedded in images or shared fixtures.
