# OpenAPI contracts

- `odip-publication-v1.yaml` describes domain-neutral dataset discovery,
  immutable manifest retrieval, and artifact retrieval.
- `vef-optimization-v1.yaml` describes optimization submission, run status,
  ranked candidate retrieval, and advertised limits.

Both descriptions use OpenAPI 3.1 and reference the JSON Schema 2020-12 files
in `../schemas/`. Deployment-specific server URLs and Keycloak endpoints replace
the illustrative hosts without changing the API contract.
