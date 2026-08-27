from __future__ import annotations

from mimetypes import guess_type

from fastapi import APIRouter, HTTPException, Query, Response, status

from .dashboard_models import (
    DashboardArtifact,
    DashboardArtifactListResponse,
    DashboardRunListResponse,
    DashboardRunSummary,
)
from .repository_factory import get_run_repository
from .storage_factory import get_artifact_storage


router = APIRouter(prefix="/dashboard", tags=["dashboard"])
_dashboard_repository = get_run_repository()
_dashboard_storage = get_artifact_storage()


@router.get(
    "/runs",
    response_model=DashboardRunListResponse,
    name="dashboard_list_runs",
)
def dashboard_list_runs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> DashboardRunListResponse:
    """Return recent runs for the Mission Control dashboard."""
    runs = _dashboard_repository.list_runs(limit=limit, offset=offset)
    summaries = [DashboardRunSummary.from_run(run) for run in runs]
    return DashboardRunListResponse(
        runs=summaries,
        limit=limit,
        offset=offset,
        returned=len(summaries),
    )


@router.get(
    "/runs/{run_id}",
    response_model=DashboardRunSummary,
    name="dashboard_get_run",
)
def dashboard_get_run(run_id: str) -> DashboardRunSummary:
    """Return a dashboard-safe summary for one persisted run."""
    run = _dashboard_repository.get(run_id)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )
    return DashboardRunSummary.from_run(run)


@router.get(
    "/runs/{run_id}/artifacts",
    response_model=DashboardArtifactListResponse,
    name="dashboard_list_artifacts",
)
def dashboard_list_artifacts(run_id: str) -> DashboardArtifactListResponse:
    """Return immutable artifact metadata without exposing bucket credentials."""
    run = _dashboard_repository.get(run_id)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )

    objects = _dashboard_storage.list_objects(f"runs/{run_id}")
    artifacts = [
        DashboardArtifact.from_object(stored, run_id)
        for stored in objects
        if stored.object_path.startswith(f"runs/{run_id}/")
    ]
    return DashboardArtifactListResponse(
        run_id=run_id,
        artifacts=artifacts,
        returned=len(artifacts),
    )


@router.get(
    "/runs/{run_id}/artifacts/{artifact_name:path}",
    name="dashboard_read_artifact",
)
def dashboard_read_artifact(run_id: str, artifact_name: str) -> Response:
    """Read one artifact through the private backend boundary."""
    run = _dashboard_repository.get(run_id)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Run not found: {run_id}",
        )

    if not artifact_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Artifact name must not be empty",
        )

    object_path = f"runs/{run_id}/{artifact_name}"
    try:
        content = _dashboard_storage.read_bytes(object_path)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact not found: {artifact_name}",
        ) from exc

    media_type = guess_type(artifact_name)[0] or "application/octet-stream"
    return Response(content=content, media_type=media_type)
