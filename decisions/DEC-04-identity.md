# DEC-04: Keycloak application identity

**Status:** Accepted
**Date:** 2026-10-10
**Decision owner:** Integration repository maintainer
**Due date:** 2026-10-10 (completed)

## Context

Public HTTPS supplies a network route but does not identify VEF or authorize it
to read a dataset. Developer Platform administration grants do not authorize
hosted application APIs. The target identity provider is Keycloak.

## Decision

### Realm and clients

- Application identities use a dedicated Keycloak realm named `energy-system`,
  separate from Developer Platform administration identities.
- The issuer is deployment-specific and has the form
  `https://<keycloak-host>/realms/energy-system`.
- `odip-api` is the OAuth resource-server client and defines the client role
  `dataset.read`.
- `vef-odip-reader` is a confidential client with client authentication and
  service accounts enabled. Browser standard flow and direct access grants are
  disabled.
- The `vef-odip-reader` service account receives only the
  `odip-api/dataset.read` client role.
- Keycloak's audience mapping adds `odip-api` to the access-token `aud` claim.

### Token use and validation

- VEF uses the OAuth 2.0 client-credentials grant and authenticates to Keycloak
  with a client secret for the first release.
- Access tokens have a five-minute lifetime. Consumers allow at most 60 seconds
  of clock skew.
- ODIP validates the JWT signature, exact issuer, `odip-api` audience,
  expiration and issue time, `vef-odip-reader` authorized party, and the
  `dataset.read` client role under `resource_access.odip-api.roles`.
- ODIP maps the authenticated VEF client to a local read-only allow-list
  containing `energy-reference-wasserburg-am-inn-2024` and its published
  versions. Dataset authorization is not inferred from network location.
- Missing, malformed, expired, wrong-issuer, or wrong-audience tokens return
  `401`. A valid identity without the role, dataset permission, or requested
  operation returns `403`.

### Provisioning and rotation

- The Keycloak administrator provisions both clients, their role and audience
  mappings, and the VEF service-account role assignment.
- Developer Platform injects the `vef-odip-reader` client secret into only the
  VEF project through its secret mechanism. Secrets are absent from images,
  source control, logs, publications, and results.
- The client secret rotates at least every 90 days with no more than 24 hours of
  overlap before the old credential is revoked.
- ODIP discovers signing keys from the realm's HTTPS discovery/JWKS metadata and
  caches valid keys. An unknown signing key fails closed if a refresh cannot
  retrieve it.

## Acceptance evidence

- A `vef-odip-reader` client-credentials token contains the expected issuer,
  `odip-api` audience, authorized party, and `dataset.read` client role.
- VEF can read the approved published dataset and cannot read a prohibited
  dataset or invoke an ODIP write operation.
- Missing, expired, wrong-audience, and unauthorized-identity tokens produce the
  specified `401` or `403` responses.
- Credential rotation succeeds without rebuilding either application image,
  and the retired credential no longer obtains a token.

## Sources

- [Keycloak: Securing applications and services with OpenID Connect](https://www.keycloak.org/securing-apps/oidc-layers)
- [Keycloak Server Administration Guide: audience support](https://www.keycloak.org/docs/latest/server_admin/#_audience)
