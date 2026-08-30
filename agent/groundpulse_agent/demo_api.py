from __future__ import annotations

import os
from mimetypes import guess_type

from fastapi import APIRouter, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware

from .dashboard_models import (
    DashboardArtifact,
    DashboardArtifactListResponse,
    DashboardRunListResponse,
    DashboardRunSummary,
)
from .repository_factory import get_run_repository
from .storage_factory import get_artifact_storage


DEMO_RUN_ID = os.getenv("GROUNDPULSE_DEMO_RUN_ID", "run_p1_55cbb0817ecd").strip()

app = FastAPI(
    title="GroundPulse Public Demo API",
    version="p2-demo-readonly-v1",
)


def _cors_origins() -> list[str]:
    configured = os.getenv("GROUNDPULSE_DEMO_CORS_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"],
)

repository = get_run_repository()
storage = get_artifact_storage()
router = APIRouter(prefix="/demo", tags=["public-demo"])


def _get_demo_run():
    if not DEMO_RUN_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Demo run is not configured",
        )

    run = repository.get(DEMO_RUN_ID)
    if run is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo run is not available",
        )
    return run


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "groundpulse-demo-api"}


@router.get("/runs", response_model=DashboardRunListResponse)
def demo_list_runs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> DashboardRunListResponse:
    """Expose only the approved fixed demonstration run."""
    if offset > 0 or limit < 1:
        return DashboardRunListResponse(
            runs=[], limit=limit, offset=offset, returned=0
        )
    run = _get_demo_run()
    return DashboardRunListResponse(
        runs=[DashboardRunSummary.from_run(run)],
        limit=limit,
        offset=offset,
        returned=1,
    )


@router.get("/runs/{run_id}", response_model=DashboardRunSummary)
def demo_get_run(run_id: str) -> DashboardRunSummary:
    if run_id != DEMO_RUN_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo run is not available",
        )
    return DashboardRunSummary.from_run(_get_demo_run())


@router.get("/runs/{run_id}/artifacts", response_model=DashboardArtifactListResponse)
def demo_list_artifacts(run_id: str) -> DashboardArtifactListResponse:
    if run_id != DEMO_RUN_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo run is not available",
        )

    _get_demo_run()
    objects = storage.list_objects(f"runs/{DEMO_RUN_ID}")
    artifacts = [
        DashboardArtifact.from_object(stored, DEMO_RUN_ID)
        for stored in objects
        if stored.object_path.startswith(f"runs/{DEMO_RUN_ID}/")
    ]
    return DashboardArtifactListResponse(
        run_id=DEMO_RUN_ID,
        artifacts=artifacts,
        returned=len(artifacts),
    )


@router.get("/runs/{run_id}/artifacts/{artifact_name:path}")
def demo_read_artifact(run_id: str, artifact_name: str) -> Response:
    if run_id != DEMO_RUN_ID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo run is not available",
        )

    if not artifact_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Artifact name must not be empty",
        )

    _get_demo_run()
    object_path = f"runs/{DEMO_RUN_ID}/{artifact_name}"
    try:
        content = storage.read_bytes(object_path)
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


app.include_router(router)
