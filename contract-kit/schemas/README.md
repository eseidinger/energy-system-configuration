# JSON Schemas

Every schema uses JSON Schema 2020-12, has a stable `$id`, rejects unknown
properties, and is versioned independently through its `schemaVersion` value.
Semantic checks that JSON Schema cannot express—such as interval completeness,
chronological ordering, digest matching, and cross-artifact consistency—belong
in the shared validation runner.
