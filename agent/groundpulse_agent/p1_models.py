from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


RunStatus = Literal[
    "created",
    "queued",
    "running",
    "validating",
    "packaging",
    "released",
    "held_for_review",
    "failed",
]

ValidationState = Literal["pending", "passed", "failed", "review"]
AuthorizationState = Literal[
    "approved_public_source",
    "review_required",
    "partner_authorized",
]


class RequestObject(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    norad_catalog_id: str | None = None


class TimeWindow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: datetime | None = None
    end: datetime | None = None
    timezone: str = "UTC"


class ResearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["research-request.v1"] = "research-request.v1"
    question: str = Field(min_length=20, max_length=2000)
    decision_intent: str = Field(min_length=3, max_length=500)
    object: RequestObject
    time_window: TimeWindow = Field(default_factory=TimeWindow)
    allowed_source_ids: list[str] = Field(min_length=1)
    authorization_state: AuthorizationState
    non_claims: list[str] = Field(default_factory=list)


class ResearchRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["research-run.v1"] = "research-run.v1"
    run_id: str = Field(min_length=8)
    request: ResearchRequest
    status: RunStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    attempt_count: int = Field(default=0, ge=0)
    snapshot_ids: list[str] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)
    validation_state: ValidationState = "pending"
    error_code: str | None = None
    review_reason: str | None = None


ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "created": {"queued", "failed"},
    "queued": {"running", "failed"},
    "running": {"validating", "failed"},
    "validating": {"packaging", "held_for_review", "failed"},
    "packaging": {"released", "held_for_review", "failed"},
    "released": set(),
    "held_for_review": {"running", "failed"},
    "failed": {"queued"},
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def transition_run(
    run: ResearchRun,
    new_status: RunStatus,
    *,
    now: datetime | None = None,
) -> ResearchRun:
    """Apply one explicit, validated run-state transition."""
    if new_status not in ALLOWED_TRANSITIONS[run.status]:
        raise ValueError(
            f"Invalid run transition: {run.status} -> {new_status}"
        )

    timestamp = now or utc_now()
    updates: dict[str, object] = {"status": new_status}

    if new_status == "running":
        updates["started_at"] = timestamp
        updates["attempt_count"] = run.attempt_count + 1

    if new_status in {"released", "held_for_review", "failed"}:
        updates["completed_at"] = timestamp

    return run.model_copy(update=updates)
