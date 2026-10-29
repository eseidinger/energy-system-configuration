#!/usr/bin/env python3
"""Run the deployed ODIP-to-VEF consumer regression with protected browser sessions.

The sessions are read from owner-only Netscape cookie jars. No cookie, customer
request, raw response, or AI completion is printed or written to the report.
With --odip-root, the suite also captures and publishes a fresh isolated
synthetic source version with short-lived worker grants. It never mutates
published bytes or tests recovery.
"""

import argparse
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
from http.cookiejar import MozillaCookieJar
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit
import uuid
import zipfile

import requests


ENERGY = "energy-reference-wasserburg-am-inn-2024"
MOBILITY = "non-energy-mobility-counts-2024"
ZIP_SHA = "8fbb0cf6fb7d65da84be8ee554b5ae48abc808bd4cdb048787f99649d46e9d74"
ORIGINAL_MANIFEST_SHA = "252b90b18b594a764a2744ba133a8db56b233e9e375301befc7616e9c18c1715"
ORIGINAL_ORACLE_SHA = "2f078373092a640e138649a2a589231ec6fd8a795538d18358f482481ac2a069"
MOBILITY_MANIFEST_SHA = "f0d4f6b882c1a05154fb43283166953fda7a0dba7f2ed435dd7f46088663bbff"
SOURCE_SHA = "d82aff39f867cb3cd77f7f355ec164b2d43c19d27bb86b13e87306885d082f29"
ISOLATED_DATASET = "energy-ai10-lineage-20261027"
WORKER_PRINCIPAL = "prn_539e69affc154cd7a08e91c5c262f8c3"
MAX_RESPONSE = 4 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    return json.loads(data, parse_float=Decimal)


def checked_origin(value, expected_host):
    parts = urlsplit(value)
    if (parts.scheme != "https" or parts.hostname != expected_host or parts.port
            or parts.username or parts.password or parts.path not in ("", "/")
            or parts.query or parts.fragment):
        raise ValueError(f"Expected HTTPS origin for {expected_host}")
    return f"https://{expected_host}"


def session(origin, cookie_file):
    path = Path(cookie_file)
    if path.is_symlink():
        raise ValueError("Cookie file must not be a symlink")
    if stat.S_IMODE(path.stat().st_mode) & 0o077:
        raise ValueError("Cookie file must be owner-only")
    jar = MozillaCookieJar(str(path))
    jar.load(ignore_discard=True)
    host = urlsplit(origin).hostname
    required = {"__Host-platform-session", "__Host-platform-activity", "__Host-platform-csrf"}
    found = {cookie.name: cookie for cookie in jar if cookie.domain == host}
    if not required.issubset(found):
        raise ValueError("Required platform session cookies are absent")
    client = requests.Session()
    client.cookies = jar
    client.headers.update({"Origin": origin, "X-Platform-CSRF-Token": found["__Host-platform-csrf"].value})
    return client


def request(client, method, url, expected, **kwargs):
    response = client.request(method, url, allow_redirects=False, timeout=(10, 65), **kwargs)
    if len(response.content) > MAX_RESPONSE:
        raise ValueError("Response exceeds capture bound")
    if response.status_code != expected:
        code = None
        if response.headers.get("Content-Type", "").startswith("application/json"):
            try:
                code = response.json().get("code")
            except (ValueError, AttributeError):
                pass
        raise ValueError(f"{method} {urlsplit(url).path}: HTTP {response.status_code}, code {code}")
    return response


def publication(client, origin, drafts, dataset, version, expected_manifest, expected_artifacts):
    matches = [draft for draft in drafts if draft.get("status") == "PUBLISHED"
               and draft.get("manifestSha256") == digest(expected_manifest)]
    if len(matches) != 1:
        raise ValueError(f"{dataset}/{version}: expected published draft is absent or duplicated")
    draft = matches[0]
    manifest = draft["manifest"]
    actual_manifest = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    if actual_manifest != expected_manifest:
        raise ValueError(f"{dataset}/{version}: operator manifest bytes differ")
    if manifest["datasetId"] != dataset or manifest["version"] != version or manifest["status"] != "PUBLISHED":
        raise ValueError(f"{dataset}/{version}: identity or status differs")
    descriptors = manifest["artifacts"]
    if {item["artifactId"] for item in descriptors} != set(expected_artifacts):
        raise ValueError(f"{dataset}/{version}: artifact set differs")
    for item in descriptors:
        url = f"{origin}/api/v1/publication-drafts/{draft['id']}/artifacts/{item['artifactId']}"
        actual = request(client, "GET", url, 200).content
        if actual != expected_artifacts[item["artifactId"]] or digest(actual) != item["sha256"]:
            raise ValueError(f"{dataset}/{version}: artifact {item['artifactId']} differs")
    return {"datasetId": dataset, "version": version, "draftId": draft["id"],
            "manifestSha256": digest(actual_manifest), "artifactCount": len(descriptors),
            "operatorBytesAndDigests": "PASS"}


def fixture(kit, archive, version):
    if version == "1.0.0":
        base = kit / "fixtures" / ENERGY
        manifest = (base / "manifest.json").read_bytes()
        artifacts = {path.stem: path.read_bytes() for path in (base / "artifacts").glob("*.json")}
        oracle_bytes = (kit / "expected-results" / "optimization-reference.json").read_bytes()
        if digest(manifest) != ORIGINAL_MANIFEST_SHA or digest(oracle_bytes) != ORIGINAL_ORACLE_SHA:
            raise ValueError("Original kit fixture or oracle checksum differs")
        oracle = parse(oracle_bytes)
    else:
        manifest = archive.read("corrected/manifest.json")
        artifacts = {name.split("/")[-1][:-5]: archive.read(name) for name in archive.namelist()
                     if name.startswith("corrected/artifacts/") and name.endswith(".json")}
        oracle = parse(archive.read("corrected/expected.json"))
    return manifest, artifacts, oracle


def wait_for_run(client, origin, run_id):
    url = f"{origin}/api/v1/optimization-runs/{run_id}"
    deadline = time.monotonic() + 360
    while time.monotonic() < deadline:
        response = parse(request(client, "GET", url, 200).content)
        if response["status"] in {"SUCCEEDED", "INFEASIBLE", "FAILED"}:
            return response
        time.sleep(2)
    raise ValueError(f"Run {run_id} did not finish within 360 seconds")


def create_run(client, origin, body, key):
    response = request(client, "POST", origin + "/api/v1/optimization-runs", 202,
                       headers={"Idempotency-Key": key}, json=body)
    run_id = response.json().get("runId")
    if not isinstance(run_id, str) or not run_id.startswith("run-"):
        raise ValueError("Accepted response has no run ID")
    return run_id


def expect_error(client, origin, body, expected_status, expected_code):
    response = request(client, "POST", origin + "/api/v1/optimization-runs", expected_status,
                       headers={"Idempotency-Key": str(uuid.uuid4())}, json=body)
    envelope = response.json()
    if envelope.get("code") != expected_code or envelope.get("status") != expected_status or "runId" in envelope:
        raise ValueError(f"Expected {expected_code} without run ID")
    return {"status": expected_status, "code": expected_code, "runIdInResponse": False}


def load_verifier(path):
    spec = importlib.util.spec_from_file_location("energy_oracle_verifier", path)
    if spec is None or spec.loader is None:
        raise ValueError("Oracle verifier is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def deployment(project, expected_images, ai_required=False):
    command = ["devplat", "--profile", "lab", "status", "--project", project, "--output", "json"]
    result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
    state = json.loads(result.stdout)
    if state["project"]["status"] != "applied":
        raise ValueError(f"{project}: deployment is not applied")
    components = state["components"]["components"]
    observed = {item["name"]: item for item in components}
    if set(observed) != set(expected_images):
        raise ValueError(f"{project}: component set differs")
    for name, image in expected_images.items():
        component = observed[name]
        status = component.get("status", {})
        if name == "web" and (status.get("state") != "ready" or status.get("deployment_image") != image):
            raise ValueError(f"{project}: web component is not ready on pinned image")
        declared = next(item for item in state["project"]["spec"]["components"] if item["name"] == name)
        if declared["resolved_image"] != image:
            raise ValueError(f"{project}: {name} image differs")
    if ai_required and state["project"]["spec"]["configuration"].get("ENERGY_AI_ENABLED") != "true":
        raise ValueError("VEF AI is not enabled")
    return {"project": project, "revision": state["components"]["revision"], "images": expected_images}


def capture_pages(client, origin, run_id):
    pages = []
    for index in range(3):
        url = f"{origin}/api/v1/optimization-runs/{run_id}/candidates?page={index}&pageSize=100"
        pages.append(parse(request(client, "GET", url, 200).content))
    return pages


def isolated_source_publication(client, origin, kit, odip_root, original_artifacts, version):
    """Capture pinned raw input and publish a fresh isolated version, with scoped grants."""
    sys.path.insert(0, str(odip_root / "workers/data-worker/src"))
    from odip_worker.contract import canonical_bytes, load_json
    from odip_worker.energy.profile import reference_outputs
    from odip_worker.fixtures import publish_fixture

    registered = request(client, "GET", origin + "/api/datasets", 200).json()
    matches = [item for item in registered if item.get("name") == ISOLATED_DATASET]
    if len(matches) != 1 or len(matches[0].get("sources", [])) != 1:
        raise ValueError("Isolated dataset or its single source is absent")
    dataset = matches[0]
    if dataset["sources"][0].get("name") != ENERGY:
        raise ValueError("Isolated dataset source differs")
    dataset_id = dataset["id"]
    capabilities = request(client, "GET", origin + "/api/v1/operator-capabilities", 200).json()
    if not capabilities.get("manageGrants") or dataset_id not in capabilities.get("writableDatasetIds", []):
        raise ValueError("Operator lacks isolated dataset and grant capabilities")
    drafts = request(client, "GET", origin + "/api/v1/publication-drafts", 200).json()
    if any(draft.get("manifest", {}).get("datasetId") == ISOLATED_DATASET
           and draft.get("manifest", {}).get("version") == version for draft in drafts):
        raise ValueError("Isolated version already exists; use a fresh version")
    grant_url = f"{origin}/api/v1/dataset-grants/{dataset_id}"
    grants = request(client, "GET", grant_url, 200).json()
    required = ("READ", "INGEST", "VALIDATE")
    if any(item.get("principalId") == WORKER_PRINCIPAL and item.get("permission") in required
           for item in grants):
        raise ValueError("Worker already has temporary rights; inspect before running")
    source = kit / "fixtures" / ENERGY / "source/pvgis-era5-wasserburg-2023.json"
    raw = source.read_bytes()
    if digest(raw) != SOURCE_SHA:
        raise ValueError("Pinned source JSON checksum differs")
    generated = reference_outputs(load_json(source))
    for artifact_id, expected in original_artifacts.items():
        if canonical_bytes(generated[artifact_id]) != expected:
            raise ValueError(f"Generated source artifact differs: {artifact_id}")

    with tempfile.TemporaryDirectory(prefix="energy-ai10-lineage-") as temporary:
        folder = Path(temporary) / ISOLATED_DATASET
        shutil.copytree(kit / "fixtures" / ENERGY, folder)
        manifest_path = folder / "manifest.json"
        manifest = load_json(manifest_path)
        manifest["datasetId"] = ISOLATED_DATASET
        manifest["version"] = version
        expected_manifest = canonical_bytes(manifest)
        manifest_path.write_bytes(expected_manifest)
        added = []
        try:
            for permission in required:
                request(client, "PUT", grant_url, 204,
                        json={"principalId": WORKER_PRINCIPAL, "permission": permission})
                added.append(permission)
            prepared = publish_fixture(origin, folder, client)
            draft_url = f"{origin}/api/v1/publication-drafts/{prepared['id']}"
            deadline = time.monotonic() + 240
            while time.monotonic() < deadline:
                published = request(client, "GET", draft_url, 200).json()
                if published["status"] == "PUBLISHED":
                    break
                if published["status"] == "FAILED":
                    raise ValueError("Isolated ODIP publication validation failed")
                time.sleep(3)
            else:
                raise ValueError("Isolated ODIP publication did not complete within 240 seconds")
            if published["manifestSha256"] != digest(expected_manifest):
                raise ValueError("Isolated publication manifest digest differs")
            inputs = published.get("inputArtifacts", [])
            if len(inputs) != 1 or inputs[0].get("sha256") != SOURCE_SHA:
                raise ValueError("Isolated publication does not link one pinned raw input")
            raw_id = inputs[0]["rawArtifactId"]
            content = request(client, "GET", f"{origin}/api/raw-artifacts/{raw_id}/content", 200).content
            if content != raw:
                raise ValueError("Isolated raw-input readback differs")
            artifact_result = publication(client, origin, [published], ISOLATED_DATASET, version,
                                          expected_manifest, original_artifacts)
            result = {**artifact_result, "rawArtifactId": raw_id,
                      "capturePipelineRunId": inputs[0]["pipelineRunId"],
                      "rawInputSha256": SOURCE_SHA, "rawBytes": len(raw),
                      "workerPrincipal": WORKER_PRINCIPAL}
        finally:
            cleanup_errors = []
            for permission in reversed(added):
                try:
                    request(client, "DELETE", grant_url, 204,
                            params={"principalId": WORKER_PRINCIPAL, "permission": permission})
                except (ValueError, requests.RequestException):
                    cleanup_errors.append(permission)
            if cleanup_errors:
                raise ValueError("Temporary worker grants could not all be revoked")
        remaining = request(client, "GET", grant_url, 200).json()
        if any(item.get("principalId") == WORKER_PRINCIPAL and item.get("permission") in required
               for item in remaining):
            raise ValueError("Temporary worker rights remain after cleanup")
        result["temporaryWorkerGrantsRemoved"] = True
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vef-cookie-file", type=Path, required=True)
    parser.add_argument("--odip-cookie-file", type=Path, required=True)
    parser.add_argument("--vef-root", type=Path, required=True)
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--expected-vef-image", required=True)
    parser.add_argument("--expected-odip-web-image", required=True)
    parser.add_argument("--expected-odip-worker-image", required=True)
    parser.add_argument("--odip-root", type=Path,
                        help="ODIP checkout; enables isolated raw-input capture and publication")
    parser.add_argument("--isolated-version", default="1.0.1",
                        help="Fresh version for the isolated lineage dataset (default: 1.0.1)")
    args = parser.parse_args()
    if args.report.exists() or not args.report.parent.is_dir():
        raise ValueError("Use a new report path in an existing private directory")
    if args.odip_root and (not args.odip_root.is_dir() or not re.fullmatch(r"1\.0\.[0-9]+", args.isolated_version)):
        raise ValueError("Isolated publication requires an ODIP checkout and a fresh 1.0.x version")
    os.umask(0o077)
    vef_deployment = deployment("vareng-test", {"web": args.expected_vef_image}, ai_required=True)
    odip_deployment = deployment("odip-test", {"web": args.expected_odip_web_image,
                                                "ingestion-worker": args.expected_odip_worker_image})
    vef_origin = checked_origin("https://web-vareng-test.apps.eseidinger.de", "web-vareng-test.apps.eseidinger.de")
    odip_origin = checked_origin("https://web-odip-test.apps.eseidinger.de", "web-odip-test.apps.eseidinger.de")
    vef = session(vef_origin, args.vef_cookie_file)
    odip = session(odip_origin, args.odip_cookie_file)
    archive_path = args.vef_root / "apps/prototype/api/src/main/resources/energy-acceptance/ai10-fixtures.zip"
    if digest(archive_path.read_bytes()) != ZIP_SHA:
        raise ValueError("Corrected acceptance fixture archive checksum differs")
    verifier = load_verifier(args.vef_root / "scripts/verify-deployed-energy-oracle.py")
    scope = ("protected deployed ODIP source capture plus VEF consumer regression; recovery excluded"
             if args.odip_root else "protected deployed ODIP-to-VEF consumer regression; source ingest and recovery excluded")
    report = {"schemaVersion": 1, "startedAtUtc": datetime.now(timezone.utc).isoformat(),
              "scope": scope,
              "fixtureArchiveSha256": ZIP_SHA, "vefDeployment": vef_deployment,
              "odipDeployment": odip_deployment, "publications": [], "runs": [], "negativeCases": {}}
    with zipfile.ZipFile(archive_path) as archive:
        original = fixture(args.kit, archive, "1.0.0")
        corrected = fixture(args.kit, archive, "1.0.1")
        if args.odip_root:
            report["isolatedSourcePublication"] = isolated_source_publication(
                odip, odip_origin, args.kit, args.odip_root, original[1], args.isolated_version)
        drafts = request(odip, "GET", odip_origin + "/api/v1/publication-drafts", 200).json()
        if not isinstance(drafts, list):
            raise ValueError("ODIP operator publication list has invalid shape")
        for version, data in (("1.0.0", original), ("1.0.1", corrected)):
            report["publications"].append(publication(odip, odip_origin, drafts, ENERGY, version, data[0], data[1]))
        mobility = args.kit / "fixtures" / MOBILITY
        if digest((mobility / "manifest.json").read_bytes()) != MOBILITY_MANIFEST_SHA:
            raise ValueError("Non-energy kit fixture checksum differs")
        report["publications"].append(publication(odip, odip_origin, drafts, MOBILITY, "1.0.0",
                                                   (mobility / "manifest.json").read_bytes(),
                                                   {p.stem: p.read_bytes() for p in (mobility / "artifacts").glob("*.json")}))
        request_body = json.loads((args.kit / "examples/optimization-request.json").read_text())
        owned = []
        for version, data in (("1.0.0", original), ("1.0.1", corrected)):
            body = json.loads(json.dumps(request_body))
            body["dataset"]["version"] = version
            key = str(uuid.uuid4())
            run_id = create_run(vef, vef_origin, body, key)
            if create_run(vef, vef_origin, body, key) != run_id:
                raise ValueError("Idempotent replay created another run")
            changed = json.loads(json.dumps(body))
            changed["constraints"]["maxInitialInvestmentEUR"] -= 1
            conflict = vef.post(vef_origin + "/api/v1/optimization-runs", json=changed,
                                headers={"Idempotency-Key": key}, allow_redirects=False, timeout=(10, 65))
            if (conflict.status_code != 409 or conflict.json().get("code") != "idempotency_conflict"
                    or "runId" in conflict.json()):
                raise ValueError("Changed body reused an idempotency key")
            result = wait_for_run(vef, vef_origin, run_id)
            pages = capture_pages(vef, vef_origin, run_id)
            verifier(result, pages, data[2])
            owned.append((body, result))
            report["runs"].append({"version": version, "runId": run_id, "manifestSha256": result["dataset"]["manifestSha256"],
                                   "status": result["status"], "fullOracle": "PASS", "candidateCount": 252,
                                   "feasibleCount": 194, "idempotentReplay": "PASS", "changedBodyConflict": "PASS"})
        baseline = owned[1][0]
        existing = json.loads(json.dumps(baseline)); existing["site"]["existingComponentIds"] = ["pv-standard-400"]
        report["negativeCases"]["existingEquipment"] = expect_error(vef, vef_origin, existing, 422, "existing_equipment_not_supported")
        missing = json.loads(json.dumps(baseline)); missing["dataset"]["version"] = "9.9.9"
        report["negativeCases"]["unknownVersion"] = expect_error(vef, vef_origin, missing, 422, "publication_not_found")
        failed = json.loads(json.dumps(baseline)); failed["dataset"]["version"] = "1.0.90"
        report["negativeCases"]["failedVersion"] = expect_error(vef, vef_origin, failed, 422, "publication_not_published")
        budget = json.loads(json.dumps(baseline)); budget["constraints"]["maxInitialInvestmentEUR"] = 0
        budget_id = create_run(vef, vef_origin, budget, str(uuid.uuid4()))
        infeasible = wait_for_run(vef, vef_origin, budget_id)
        if (infeasible["status"] != "INFEASIBLE" or infeasible["evaluatedCandidateCount"] != 252
                or infeasible["feasibleCandidateCount"] != 0 or infeasible["recommendedConfigurationId"] is not None
                or infeasible["optimalityStatus"] != "NOT_APPLICABLE"):
            raise ValueError("Zero-budget result differs from expected infeasibility")
        report["runs"].append({"version": "1.0.1", "runId": budget_id, "status": "INFEASIBLE", "feasibleCount": 0,
                               "candidateCount": 252, "recommendation": None, "optimality": "NOT_APPLICABLE"})
        latest = parse(request(vef, "GET", vef_origin + "/api/v1/optimization-runs/" + owned[1][1]["runId"], 200).content)
        if latest != owned[1][1]:
            raise ValueError("Completed result changed after negative cases")
        report["completedRunUnchanged"] = True
    report["completedAtUtc"] = datetime.now(timezone.utc).isoformat()
    report["status"] = "PASS"
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: protected deployed ODIP-to-VEF consumer regression; report written")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, requests.RequestException,
            subprocess.CalledProcessError, subprocess.TimeoutExpired, zipfile.BadZipFile) as error:
        print(f"FAIL: {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
