from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict

from .local_worker import execute_local_run
from .p1_models import ResearchRequest, ResearchRun, transition_run
from .queue import TaskQueue
from .queue_factory import get_task_queue
from .repository import RunRepository
from .repository_factory import get_run_repository


app = FastAPI(
    title="GroundPulse Research API",
    version="p1-cloudtasks-v1",
)

repository: RunRepository = get_run_repository()
task_queue: TaskQueue = get_task_queue()


TRANSIENT_ERROR_CODES = {
    "p0_pipeline_transient",
    "local_worker_transient",
}


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
    existing = repository.get_by_idempotency_key(
        request.idempotency_key
    )

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
    """Move a failed run back to queued and enqueue one retry task."""
    run = repository.get(run_id)

    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )

    try:
        queued = transition_run(run, "queued").model_copy(
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
    """Execute a Cloud Tasks delivery and request retry for transient failures.

    Cloud Run authentication protects this private endpoint. The run_id in the
    JSON body is the authoritative task payload; Cloud Tasks headers are only
    operational metadata.
    """
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

    # Cloud Tasks redelivers after a transient 503. The previous delivery has
    # already persisted the run as failed, so requeue it before executing.
    if (
        current.status == "failed"
        and current.error_code in TRANSIENT_ERROR_CODES
    ):
        current = transition_run(current, "queued").model_copy(
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
        repository.save(current)

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
        # A non-2xx response tells Cloud Tasks to retry the same delivery.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Transient Gemini/provider failure; Cloud Tasks should retry"
            ),
        )

    return result
