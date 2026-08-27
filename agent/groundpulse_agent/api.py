from __future__ import annotations

import os
from datetime import timedelta

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from .dashboard_api import router as dashboard_router
from .local_worker import execute_local_run, is_transient_provider_failure
from .p1_models import ResearchRun, ResearchRequest, transition_run, utc_now
from .queue import TaskQueue
from .queue_factory import get_task_queue
from .repository import RunRepository
from .repository_factory import get_run_repository


app = FastAPI(
    title="GroundPulse Research API",
    version="p1-cloudtasks-v1",
)

# Local development uses Vite on ports 3000/3001. Production deployments should
# set GROUND_PULSE_CORS_ORIGINS to the exact trusted frontend origins.
def _cors_origins() -> list[str]:
    configured = os.getenv("GROUND_PULSE_CORS_ORIGINS", "")
    if configured.strip():
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:3001",
        "http://localhost:3001",
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

repository: RunRepository = get_run_repository()
task_queue: TaskQueue = get_task_queue()

app.include_router(dashboard_router)

TRANSIENT_ERROR_CODES = {
    "p0_pipeline_transient",
    "p0_pipeline_timeout",
    "local_worker_transient",
}

STALE_RUNNING_AFTER = timedelta(minutes=2)


class CreateRunResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    status: str
    status_url: str
    task_id: str
    reused: bool


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the GroundPulse Research API is running."""
    return {
        "status": "ok",
        "service": "groundpulse-research-api",
    }


@app.post(
    "/runs",
    response_model=CreateRunResponse,
    status_code=status.HTTP_202_ACCEPTED,
    name="create_run",
)
def create_run(request: ResearchRequest) -> CreateRunResponse:
    """Create or reuse a run and enqueue exactly one active task."""
    existing = repository.get_by_idempotency_key(request.idempotency_key)

    if existing is not None:
        task = task_queue.enqueue_for_run(existing.run_id)
        return CreateRunResponse(
            run_id=existing.run_id,
            status=existing.status,
            status_url=f"/runs/{existing.run_id}",
            task_id=task.task_id,
            reused=True,
        )

    run = repository.create(request)
    queued = transition_run(run, "queued")
    repository.save(queued)
    task = task_queue.enqueue_for_run(queued.run_id)

    return CreateRunResponse(
        run_id=queued.run_id,
        status=queued.status,
        status_url=f"/runs/{queued.run_id}",
        task_id=task.task_id,
        reused=False,
    )


@app.get(
    "/runs/{run_id}",
    response_model=ResearchRun,
    name="get_run",
)
def get_run(run_id: str) -> ResearchRun:
    """Return a persisted run by ID."""
    run = repository.get(run_id)

    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )

    return run


@app.post(
    "/runs/{run_id}/execute",
    response_model=ResearchRun,
    name="execute_local_run",
)
def execute_run(run_id: str) -> ResearchRun:
    """Execute one run directly for local development and regression tests."""
    try:
        return execute_local_run(run_id, repository=repository)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@app.post(
    "/runs/{run_id}/retry",
    response_model=ResearchRun,
    name="retry_run",
)
def retry_run(run_id: str) -> ResearchRun:
    """Move an eligible run back to queued and enqueue one retry task."""
    run = repository.get(run_id)

    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )

    try:
        queued = _reset_run_for_retry(run)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    repository.save(queued)
    task_queue.enqueue_for_run(queued.run_id)
    return queued


@app.post(
    "/worker/execute",
    response_model=ResearchRun,
    name="execute_worker_run",
)
def execute_worker_run(
    payload: dict[str, str],
    request: Request,
) -> ResearchRun:
    """Execute a Cloud Tasks delivery and request retry for transient failures."""
    del request

    run_id = payload.get("run_id", "").strip()
    if not run_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Worker payload must contain a non-empty run_id",
        )

    current = repository.get(run_id)
    if current is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )

    if current.status == "failed" and current.error_code in TRANSIENT_ERROR_CODES:
        current = _reset_run_for_retry(current)
        repository.save(current)
    elif current.status == "running":
        if _is_stale_running(current):
            current = _reset_run_for_retry(current)
            repository.save(current)
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Run is already running; Cloud Tasks should not duplicate "
                    "an active worker lease"
                ),
            )

    try:
        result = execute_local_run(run_id, repository=repository)
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if result.error_code in TRANSIENT_ERROR_CODES:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Transient provider or worker timeout; Cloud Tasks should retry",
        )

    if result.error_code and is_transient_provider_failure(
        result.review_reason or ""
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Transient provider failure; Cloud Tasks should retry",
        )

    return result


def _is_stale_running(run: ResearchRun) -> bool:
    if run.started_at is None:
        return True
    return utc_now() - run.started_at >= STALE_RUNNING_AFTER


def _reset_run_for_retry(run: ResearchRun) -> ResearchRun:
    if run.status == "failed":
        queued = transition_run(run, "queued")
    elif run.status == "running":
        queued = transition_run(run, "queued")
    else:
        raise ValueError(
            f"Run {run.run_id} is not eligible for retry from status {run.status}"
        )

    return queued.model_copy(
        update={
            "started_at": None,
            "completed_at": None,
            "artifact_ids": [],
            "snapshot_ids": [],
            "validation_state": "pending",
            "error_code": None,
            "review_reason": None,
        }
    )
