# VEF-to-ODIP authentication flow and threat notes

**Status:** Reconciled identity baseline from kit `0.3.0`, retained in `0.4.0`, 2026-10-11
**Related decisions:** [DEC-03](../decisions/DEC-03-connectivity.md), [DEC-04](../decisions/DEC-04-identity.md)

## Provisioning and sequence

VEF requests service access through the Platform API. ODIP's project
administrator approves only its reader group. The platform reconciles the
confidential client and target groups, then delivers a project-wide secret
binding to VEF. ODIP records a finer dataset grant for the stable service
principal ID. Applications configure no dedicated realm, fixed client ID,
OAuth scope, or Keycloak role.

```mermaid
sequenceDiagram
    participant VEF as VEF application
    participant IDP as Environment identity provider
    participant EDGE as Platform ODIP access boundary
    participant ODIP as Private ODIP backend
    participant AUTHZ as ODIP dataset policy
    VEF->>IDP: client_credentials using managed binding
    IDP-->>VEF: Short-lived token with derived audience and group IDs
    VEF->>EDGE: HTTPS GET publication with bearer token
    EDGE->>EDGE: Verify token, active service, route, groups, revocation snapshot
    EDGE->>ODIP: Strip credentials and spoofed headers; add normalized principal context
    ODIP->>ODIP: Require well-formed trusted context
    ODIP->>AUTHZ: Check stable principal ID and dataset permission
    AUTHZ-->>ODIP: Permit published dataset read
    ODIP-->>VEF: Manifest/artifact through boundary with ETag
    VEF->>VEF: Verify trusted origin, schema, and SHA-256
```

VEF reacquires tokens before expiry and sends them only to the configured ODIP
origin. The platform boundary owns signing-key discovery and caching. ODIP
requires no identity-provider egress for caller authentication. Header validation
alone cannot establish trust: network policy must prevent direct backend access.

## Trust boundaries

- Platform grants authorize control-plane changes; application groups authorize
  hosted routes. Neither grants ODIP dataset access or VEF run ownership alone.
- The provider boundary authenticates and checks coarse route-group authority,
  including effective revocation even when a token still asserts membership.
- ODIP owns dataset-specific decisions keyed to stable principal ID. VEF owns
  run ownership and caller-scoped idempotency through the same identity context.
- The consumer project is the service-secret boundary. All VEF components may
  receive its credential; component-specific attribution is not available.
- Public cross-project HTTPS is encrypted. PostgreSQL transport in the accepted
  single-host lab profile is not TLS-protected.

## Threats and controls

| Threat | Required control | Acceptance evidence |
| --- | --- | --- |
| Stolen service credential | Project-scoped managed binding, at least 90-day rotation, no telemetry exposure. | Retired client cannot obtain tokens; all components in the project are within the accepted trust boundary. |
| Stolen or invalid token | At most five-minute lifetime; boundary validates exact issuer, derived audience, type, times, subject, and client. | Expired/wrong-audience token returns `401` without redirect. |
| Unapproved client or wrong group | Provider approval and active service state, route group IDs, and current snapshot. | Unapproved/wrong-group request returns `403` before reaching ODIP. |
| Reader targets other data or writes | ODIP principal-to-dataset grant and no writer route membership. | Prohibited dataset and write operations return `403`. |
| Forged identity headers | Strip all inbound reserved headers; only boundary reaches backend. | Spoofed header replaced and direct/same-project backend bypass denied with healthy controls. |
| Rotation changes client identity | Local domain grants use stable principal ID; normal adoption confirms new binding. | Principal remains stable, new client works, old client is revoked. |
| Malicious path or redirect | Only trusted-origin relative paths; reject cross-origin redirects and ambiguous path encodings. | Unsafe retrieval fails before data use. |
| Intercepted traffic | Verify certificate and hostname; configure origins outside payloads. | Invalid TLS fails closed. |
| Stale authorization or provider outage | Snapshots expire within five minutes; unusable signing keys and expired snapshots fail closed. | Existing claims cannot bypass revocation; outage tests demonstrate the bound. |
| Excessive network access | Explicit hostname/443 exceptions approved by operator and pinned at apply. | Allowed requests pass; unrelated egress fails; changed DNS requires reapply. |
| Sensitive-data leakage | Disable optional profile attributes; exclude customer details and secrets from telemetry. | Sanitized correlation and automated log assertions. |
| Browser forgery | VEF browser route requires approved user membership, managed CSRF token, and same-origin header. | Pending human, missing CSRF, and cross-origin mutation fail. |

## Failure and recovery behavior

- Token acquisition fails: VEF reports a dependency failure and never falls
  back to anonymous access.
- Access boundary returns `401`/`403`: no indefinite retry or fallback. The
  platform's access-error body differs from application `error/v1`.
- Expired authorization snapshot or unavailable authentication material:
  boundary fails closed; `503` is an operational dependency failure.
- ODIP unavailable after immutable data verification: VEF may use only the
  exact verified cached publication, retaining its version and digests.
- After actual backup restore: platform catalog reconciles clients/groups and
  revocation outward, browser sessions invalidate, and inconsistent credentials
  rotate before access reopens. A reconciliation rehearsal is not restore proof.

The upstream neutral acceptance run covers core identity/isolation behavior;
its nine deferred checks, including actual restore, outages, log retention, and
the external energy suite, remain integration obligations.
