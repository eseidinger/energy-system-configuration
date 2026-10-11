# DEC-04: Platform-managed hosted application identity

**Status:** Accepted baseline, reconciled with current implementation
**Date:** 2026-10-10; reconciled 2026-10-11
**Decision owner:** Integration repository maintainer
**Related:** [DEC-03](DEC-03-connectivity.md), [authentication flow](../architecture/vef-odip-authentication.md)

## Context

Developer Platform now implements hosted-application authentication and coarse
route authorization as generic resources. Kit `0.3.0` replaces the earlier
application-specific realm, `odip-api` audience, `vef-odip-reader` client, and
`dataset.read` Keycloak role assumptions. This is a breaking identity change;
energy datasets, schema majors, and numerical results are unchanged.

## Decision

- Use one platform-environment identity realm; the supported reference adapter
  uses `https://<identity-host>/realms/platform`. The platform creates clients,
  audiences, and client-scoped group claims from stable resource IDs. Application
  owners declare no OAuth scopes, fixed client IDs, provider roles, or realm.
- ODIP's public API uses a separate access policy with `bearer-token` GET routes
  and an approved reader group. VEF requests service access to application `odip`
  in provider project `odip`. Only the provider's project administrator approves
  the reader group; requesting access does not issue a usable credential.
- VEF explicitly accepts `projectWideCredential: true`. The platform delivers
  `<secretPrefix>_CLIENT_ID`, `_CLIENT_SECRET`, and `_TOKEN_URL` through VEF's
  project secret mechanism. Every component in that project may receive them.
  The prefix comes from the service-access resource. Secrets are not in ordinary
  API responses, source, images, desired state, telemetry, or results.
- VEF obtains access tokens through `client_credentials`. They last at most five
  minutes. The platform access boundary validates signature, issuer, token type,
  derived audience, times, subject, client ID, approved service state, and group
  IDs. Missing/invalid bearer tokens return `401` without a browser redirect;
  unapproved service identities and route-group denials return `403`.
- The boundary removes inbound identity headers, bearer tokens, and platform
  session cookies, then forwards normalized `X-Platform-Principal-*` headers.
  Private backends accept traffic only through this boundary. Middleware rejects
  malformed or missing required context. ODIP and VEF do not repeat coarse
  route-group checks or validate JWTs themselves.
- ODIP applies finer dataset authorization to the stable service principal ID:
  read-only access to `energy-reference-wasserburg-am-inn-2024` and its published
  versions. It denies other datasets and writes. The principal survives normal
  rotation while client IDs change; names and client IDs are not authorization
  keys. Approval is followed by an explicit local dataset grant before use.
- VEF user endpoints use `browser-session` with explicitly approved application
  membership. First login remains pending. Platform administrator status grants
  no application access. State changes require the managed CSRF cookie/header
  and same-origin `Origin`. VEF owns finer run ownership and idempotency scope.
- Route/method matches are non-overlapping and segment-aware. `HEAD` follows
  `GET`, `OPTIONS` requires explicit configuration, and unmatched routes deny.
  The profile has no anonymous or combined session/bearer routes.
- Group and principal IDs are stable, opaque keys. Display name and email are
  optional and disabled in the reference policy; authorization never depends on
  them. Email opt-in would additionally require personal-data governance.
- Rotate credentials at least every 90 days through the platform lifecycle. The
  application owner arranges that schedule. Normal rotation delivers a new
  binding and preserves approved groups with at most 24 hours overlap; confirm
  adoption to revoke the old client. Emergency rotation has no overlap.
- Revocation denies existing token/session claims through the platform view.
  Snapshots expire within five minutes; expired or unavailable authentication
  material fails closed. The platform catalog is authoritative after restoration;
  access remains unavailable until reconciliation, and browser sessions reset.

## Acceptance evidence

- Approved service access obtains a token with the derived target audience and
  relevant group IDs; a pending/unapproved request cannot reach ODIP.
- Missing, expired, wrong-audience, wrong-group, and revoked identities produce
  `401`/`403` at the boundary. Clients accept platform access-error bodies as
  distinct from domain `error/v1`; dependency failure may produce `503`.
- The backend receives normalized service/user context without bearer secrets;
  spoofed headers and direct backend bypass fail, including same-project bypass.
- The reader fetches only approved publications; prohibited dataset and writes
  return `403`. Local grants survive a client-ID change during rotation.
- VEF human approval, CSRF, stable-principal run ownership, credential adoption,
  revocation, outage staleness, and real backup restoration pass in Gate 4/5.
  The upstream neutral run proves only its recorded scope, not the energy flow.

## Sources

- [Pinned access implementation](https://github.com/eseidinger/developer-platform/blob/77820cae05c3be178b5c6eecc762a218b2448c8b/platform/app/access_api.py)
- [Pinned security and authorization contract](https://github.com/eseidinger/developer-platform/blob/77820cae05c3be178b5c6eecc762a218b2448c8b/docs/architecture/security-and-authorization.md)
- [ADR-020](https://github.com/eseidinger/developer-platform/blob/77820cae05c3be178b5c6eecc762a218b2448c8b/docs/architecture/decisions/ADR-020-generic-hosted-application-integration.md)
