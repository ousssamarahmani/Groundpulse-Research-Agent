from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .artifact_generator import generate_research_package
from .p1_models import ResearchRun, transition_run
from .repository import RunRepository
from .repository_factory import get_run_repository
from .storage import ArtifactStorage, StoredObject
from .storage_factory import get_artifact_storage


AGENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = AGENT_ROOT.parent
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "p0"
SOURCE_SNAPSHOT_ROOT = REPO_ROOT / "evals" / "fixtures"
SOURCE_SNAPSHOT_FILES = {
    "celestrak_gp_25544": SOURCE_SNAPSHOT_ROOT / "celestrak_gp_25544.json",
}

P0_SUBPROCESS_TIMEOUT_SECONDS = 540

TRANSIENT_PROVIDER_MARKERS = (
    "503 UNAVAILABLE",
    "429 RESOURCE_EXHAUSTED",
    "RESOURCE_EXHAUSTED",
    "rate limit",
    "rate_limit",
    "temporarily unavailable",
    "high demand",
    "deadline exceeded",
    "DEADLINE_EXCEEDED",
    "timed out",
    "timeout",
)


def is_transient_provider_failure(message: str) -> bool:
    """Return True when a provider or execution timeout should be retried."""
    normalized = message.lower()
    return any(marker.lower() in normalized for marker in TRANSIENT_PROVIDER_MARKERS)


def execute_local_run(
    run_id: str,
    repository: RunRepository | None = None,
    storage: ArtifactStorage | None = None,
) -> ResearchRun:
    """Execute one queued run and persist immutable evidence objects."""
    repository = repository or get_run_repository()
    storage = storage or get_artifact_storage()

    run = repository.get(run_id)
    if run is None:
        raise KeyError(f"Run not found: {run_id}")

    if run.status != "queued":
        raise ValueError(
            f"Run {run_id} is not queued; current status is {run.status}"
        )

    run = transition_run(run, "running")
    repository.save(run)

    try:
        source_objects = _store_approved_sources(run, storage)

        try:
            completed = subprocess.run(
                [sys.executable, "-m", "groundpulse_agent.run_p0"],
                cwd=AGENT_ROOT,
                capture_output=True,
                text=True,
                timeout=P0_SUBPROCESS_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            failure_text = (
                f"P0 pipeline timed out after "
                f"{P0_SUBPROCESS_TIMEOUT_SECONDS} seconds. "
                f"{stderr[-1500:]} {stdout[-500:]}"
            ).strip()
            failed = transition_run(run, "failed").model_copy(
                update={
                    "error_code": "p0_pipeline_timeout",
                    "review_reason": failure_text,
                }
            )
            repository.save(failed)
            return failed

        if completed.returncode != 0:
            failure_text = (
                completed.stderr[-2000:]
                or completed.stdout[-2000:]
                or "P0 pipeline exited with a non-zero status"
            )
            error_code = (
                "p0_pipeline_transient"
                if is_transient_provider_failure(failure_text)
                else "p0_pipeline_failed"
            )
            failed = transition_run(run, "failed").model_copy(
                update={
                    "error_code": error_code,
                    "review_reason": failure_text,
                }
            )
            repository.save(failed)
            return failed

        latest_artifact = _latest_artifact_directory()
        report_path = latest_artifact / "validation_report.json"
        if not report_path.exists():
            raise RuntimeError(
                "P0 artifact directory has no validation_report.json"
            )

        report = json.loads(report_path.read_text(encoding="utf-8"))
        validation_passed = bool(report.get("passed", False))

        run = transition_run(run, "validating")
        repository.save(run)

        source_id = run.request.allowed_source_ids[0]
        generate_research_package(
            artifact_directory=latest_artifact,
            run_id=run_id,
            source_id=source_id,
            validation_passed=validation_passed,
        )

        artifact_objects = storage.store_directory(
            f"runs/{run_id}/artifact",
            latest_artifact,
        )
        _store_manifest(
            run,
            source_objects=source_objects,
            artifact_objects=artifact_objects,
            storage=storage,
            validation_passed=validation_passed,
        )

        if not validation_passed:
            held = transition_run(run, "held_for_review").model_copy(
                update={
                    "validation_state": "review",
                    "review_reason": (
                        "Deterministic evidence validation failed"
                    ),
                    "artifact_ids": [latest_artifact.name],
                    "snapshot_ids": list(run.request.allowed_source_ids),
                }
            )
            repository.save(held)
            return held

        run = transition_run(run, "packaging")
        run = transition_run(run, "released")
        released = run.model_copy(
            update={
                "validation_state": "passed",
                "artifact_ids": [latest_artifact.name],
                "snapshot_ids": list(run.request.allowed_source_ids),
            }
        )
        repository.save(released)
        return released

    except Exception as exc:
        failure_text = str(exc)
        error_code = (
            "local_worker_transient"
            if is_transient_provider_failure(failure_text)
            else "local_worker_exception"
        )
        failed = transition_run(run, "failed").model_copy(
            update={
                "error_code": error_code,
                "review_reason": failure_text,
            }
        )
        repository.save(failed)
        return failed


def _store_approved_sources(
    run: ResearchRun,
    storage: ArtifactStorage,
) -> list[StoredObject]:
    objects: list[StoredObject] = []
    for source_id in run.request.allowed_source_ids:
        source_path = SOURCE_SNAPSHOT_FILES.get(source_id)
        if source_path is None:
            raise RuntimeError(
                f"No approved local snapshot mapping exists for {source_id}"
            )
        if not source_path.exists():
            raise RuntimeError(
                f"Approved source snapshot does not exist: {source_path}"
            )
        objects.append(storage.store_approved_snapshot(source_id, source_path))
    return objects


def _latest_artifact_directory() -> Path:
    if not ARTIFACT_ROOT.exists():
        raise RuntimeError(
            "P0 pipeline completed without an artifact directory"
        )

    artifact_dirs = [
        path for path in ARTIFACT_ROOT.iterdir() if path.is_dir()
    ]
    if not artifact_dirs:
        raise RuntimeError(
            "P0 pipeline completed without a timestamped artifact directory"
        )

    return max(
        artifact_dirs,
        key=lambda path: path.stat().st_mtime,
    )


def _store_manifest(
    run: ResearchRun,
    *,
    source_objects: list[StoredObject],
    artifact_objects: list[StoredObject],
    storage: ArtifactStorage,
    validation_passed: bool,
) -> StoredObject:
    manifest = {
        "schema_version": "research-storage-manifest.v1",
        "run_id": run.run_id,
        "request_idempotency_key": run.request.idempotency_key,
        "source_objects": [obj.model_dump(mode="json") for obj in source_objects],
        "artifact_objects": [obj.model_dump(mode="json") for obj in artifact_objects],
        "validation_passed": validation_passed,
    }
    content = json.dumps(
        manifest,
        indent=2,
        sort_keys=True,
    ).encode("utf-8")
    return storage.store_bytes(
        f"runs/{run.run_id}/manifest.json",
        content,
        content_type="application/json",
    )
