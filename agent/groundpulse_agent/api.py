from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .local_repo import FileRunRepository
from .local_worker import execute_local_run
from .p1_models import ResearchRequest, ResearchRun, transition_run


app = FastAPI(
    title="GroundPulse Research API",
    version="p1-local-v1",
)

repository = FileRunRepository()


class CreateRunResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    status: str
    status_url: str


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the local Research API is running."""
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
    """Validate a bounded request, create a run, and queue it locally."""
    run = repository.create(request)
    queued = transition_run(run, "queued")
    repository.save(queued)

    return CreateRunResponse(
        run_id=queued.run_id,
        status=queued.status,
        status_url=f"/runs/{queued.run_id}",
    )


@app.get(
    "/runs/{run_id}",
    response_model=ResearchRun,
    name="get_run",
)
def get_run(run_id: str) -> ResearchRun:
    """Return a persisted local run by ID."""
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
    """Execute one queued run through the local ADK/P0 pipeline.

    This endpoint is for local development only. Cloud Tasks will replace
    this direct trigger in the cloud-backed P1 implementation.
    """
    try:
        return execute_local_run(run_id)
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
    """Move a failed run back to queued for a controlled retry."""
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
    return queued
