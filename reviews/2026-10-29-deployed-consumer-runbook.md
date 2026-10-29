# Deployed energy consumer regression

This runbook reproduces the protected ODIP-to-VEF consumer test recorded in
[the October 29 evidence](evidence/2026-10-29-deployed-consumer-regression.json).
It does not publish a dataset, mutate ODIP responses or exercise recovery.

## Preparation

1. Verify the deployed VEF and ODIP image digests and note their exact values.
   The script refuses a changed image, missing component or disabled VEF AI.
2. Prepare and verify contract kit 0.5.0 with VEF's
   `scripts/validate-energy-contract-kit.py --prepare-only` command. The script
   also pins the original manifest and oracle, the non-energy manifest and the
   corrected synthetic fixture ZIP by SHA-256.
3. Create a private temporary directory with mode `700`. Capture fresh ODIP
   and VEF browser sessions into separate owner-only Netscape cookie files.
   The existing ODIP `scripts/capture-operator-session.py` accepts each HTTPS
   origin via `ODIP_API_URL` and its target via `ODIP_OPERATOR_COOKIE_FILE`.
   Copy only the appropriate authenticated request's Cookie header to the
   Windows clipboard; never paste it into chat, a command or a tracked file.
   Clear the clipboard after each capture. The two cookie files must have
   mode `600`.

## Execution

Run `scripts/run-deployed-energy-consumer-regression.py --help` for the required
paths and image pins. Point `--report` to a new file inside the private
temporary directory. The script first checks deployment readiness and three
ODIP published drafts, including all eleven artifact bytes. Only after those
checks does it create synthetic VEF runs. It verifies both complete oracles,
idempotent replay and changed-body conflict, three 422 denials, a zero-budget
infeasible result and unchanged completed-run JSON. It writes only a sanitized
report with mode `600`.

The human ODIP operator session may receive `401 application_access_denied` on
the service-consumer publication route. The script therefore checks ODIP bytes
through protected operator draft routes; the VEF runs exercise the configured
ODIP service binding. Do not turn a 401 into a temporary broad user READ grant.

After reviewing the report, remove both cookie files and clear the clipboard.
Keep the sanitized report hash and deployment pins in tracked acceptance
evidence. A PASS here is a consumer regression PASS; AI-10 remains open until
the complete Gate 5 suite or an explicit versioned acceptance decision covers
the still missing source-ingestion and live-read boundaries.
