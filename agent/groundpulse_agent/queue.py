from __future__ import annotations

from datetime import datetime
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field


QueueTaskStatus = Literal[
    "queued",
    "claimed",
    "completed",
    "failed",
]


class QueueTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["queue-task.v1"] = "queue-task.v1"
    task_id: str = Field(min_length=8)
    run_id: str = Field(min_length=8)
    idempotency_key: str = Field(min_length=8)
    status: QueueTaskStatus = "queued"
    attempt_count: int = Field(default=0, ge=0)
    created_at: datetime
    claimed_at: datetime | None = None
    completed_at: datetime | None = None
    error_code: str | None = None


class TaskQueue(Protocol):
    """Queue contract shared by local and future Cloud Tasks adapters."""

    def enqueue_for_run(self, run_id: str) -> QueueTask:
        """Enqueue one task per run using run_id as the idempotency key."""
        ...

    def get(self, task_id: str) -> QueueTask | None:
        """Retrieve a task by ID."""
        ...

    def get_for_run(self, run_id: str) -> QueueTask | None:
        """Retrieve the task associated with a run."""
        ...
