# Energy System Configuration Contract Kit

Version `0.2.0` is the executable form of the frozen integration-contract
baseline. ODIP and VEF consume released archives of this directory and pin both
the version and archive checksum.

## Contents

- `schemas/` contains JSON Schema 2020-12 contracts.
- `openapi/` contains OpenAPI 3.1 service descriptions.
- `examples/` contains small valid payload examples.
- `fixtures/` will contain the complete energy and non-energy reference inputs.
- `expected-results/` will contain reviewed simulation and optimization outputs.
- `contractkit/` contains the repository-neutral validation utilities.
- `tests/` validates schemas, APIs, examples, canonical serialization, and
  fixture integrity.

## Validate

Install the pinned environment and execute the suite:

```text
uv sync --frozen
uv run --frozen pytest
```

Canonicalize a JSON document and print its SHA-256 digest:

```text
uv run python -m contractkit.canonical path/to/document.json
```

The semantic validator checks the energy publication as one unit after JSON
Schema validation. It enforces the five required roles, canonical artifact
digests, aligned and complete hourly intervals, load-shape normalization, and
catalog identity and model-count rules.

Build the deterministic release archive and `SHA256SUMS` file under `dist/`:

```text
uv run --frozen python -m tools.build_release
```

## Licensing

Schemas, OpenAPI definitions, runner code, and tests use Apache-2.0. Examples,
fixtures, and expected results authored in this repository use CC BY 4.0.
Third-party source material retains its source terms and attribution as stated
in the repository `NOTICE` and artifact provenance.
