from __future__ import annotations

from datetime import datetime
from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field

from .p1_models import ResearchRun
from .storage import StoredObject


class DashboardRunSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    status: str
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    attempt_count: int
    validation_state: str
    error_code: str | None = None
    review_reason: str | None = None
    question: str
    decision_intent: str
    object_name: str
    norad_catalog_id: str | None = None
    allowed_source_ids: list[str]
    snapshot_ids: list[str]
    artifact_ids: list[str]

    @classmethod
    def from_run(cls, run: ResearchRun) -> "DashboardRunSummary":
        return cls(
            run_id=run.run_id,
            status=run.status,
            created_at=run.created_at,
            started_at=run.started_at,
            completed_at=run.completed_at,
            attempt_count=run.attempt_count,
            validation_state=run.validation_state,
            error_code=run.error_code,
            review_reason=run.review_reason,
            question=run.request.question,
            decision_intent=run.request.decision_intent,
            object_name=run.request.object.name,
            norad_catalog_id=run.request.object.norad_catalog_id,
            allowed_source_ids=list(run.request.allowed_source_ids),
            snapshot_ids=list(run.snapshot_ids),
            artifact_ids=list(run.artifact_ids),
        )


class DashboardRunListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runs: list[DashboardRunSummary]
    limit: int
    offset: int
    returned: int


class DashboardArtifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    object_path: str
    uri: str
    sha256: str
    size_bytes: int
    generation: str | None = None
    download_url: str

    @classmethod
    def from_object(cls, stored: StoredObject, run_id: str) -> "DashboardArtifact":
        expected_prefix = f"runs/{run_id}/"
        if not stored.object_path.startswith(expected_prefix):
            raise ValueError("Stored object is outside the requested run prefix")
        name = str(PurePosixPath(stored.object_path).relative_to(expected_prefix))
        return cls(
            name=name,
            object_path=stored.object_path,
            uri=stored.uri,
            sha256=stored.sha256,
            size_bytes=stored.size_bytes,
            generation=stored.generation,
            download_url=f"/dashboard/runs/{run_id}/artifacts/{name}",
        )


class DashboardArtifactListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    artifacts: list[DashboardArtifact]
    returned: int
