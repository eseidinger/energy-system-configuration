# DEC-03: Connectivity

**Status:** Accepted
**Date:** 2026-10-10; reconciled 2026-10-11
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
- Cross-project HTTPS TLS is mandatory and uses certificates managed through
  the target installation. PostgreSQL transport is not TLS-protected in the
  accepted single-host lab profile.
- Each VEF calling component declares the ODIP API hostname and managed token
  endpoint hostname on TCP 443, plus platform-provided DNS. Operators approve
  their resolved CIDRs and port. DNS is pinned at apply time; changed addresses
  require explicit reapply.
- ODIP inbound authentication requires no application-side Keycloak egress.
  The platform access boundary retrieves signing keys. Ingestion source access
  belongs to separately declared worker egress.
- VEF rejects redirects to another origin. Publication artifact paths are
  relative and may resolve only against the trusted ODIP manifest origin.
- A private cross-project service route is deferred. Adding one later must
  preserve the same application authentication and authorization behavior.

## Acceptance evidence

- VEF resolves the configured ODIP and Keycloak names and verifies their TLS
  certificates.
- An authenticated ODIP publication request succeeds from the VEF project.
- An unauthenticated ODIP request, unrelated destination, and direct protected
  backend bypass fail. A healthy control request proves each denial is policy
  enforcement rather than a DNS or connectivity failure.
- A manifest redirect or artifact path targeting another origin is rejected.

## Consequences

- Developer Platform owns ingress, TLS integration, secret delivery, DNS, and
  least-privilege egress configuration.
- Keycloak and ODIP application authorization remain distinct from Developer
  Platform control-plane authorization.
- Both the ODIP hostname and Keycloak hostname are deployment configuration;
  neither is embedded in images or shared fixtures.
