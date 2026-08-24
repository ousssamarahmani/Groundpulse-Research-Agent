from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud import tasks_v2

from .p1_models import utc_now
from .queue import QueueTask, TaskQueue


class CloudTasksQueue(TaskQueue):
    """Google Cloud Tasks HTTP queue with idempotent active-task reuse."""

    def __init__(
        self,
        *,
        project: str,
        location: str,
        queue_name: str,
        worker_url: str,
        oidc_service_account_email: str,
        oidc_audience: str | None = None,
        client: tasks_v2.CloudTasksClient | None = None,
    ) -> None:
        if not project.strip():
            raise ValueError("Cloud Tasks project must not be empty")
        if not location.strip():
            raise ValueError("Cloud Tasks location must not be empty")
        if not queue_name.strip():
            raise ValueError("Cloud Tasks queue name must not be empty")
        if not worker_url.startswith("https://"):
            raise ValueError(
                "Cloud Tasks worker URL must be an HTTPS URL"
            )
        if not oidc_service_account_email.strip():
            raise ValueError(
                "Cloud Tasks OIDC service account email must not be empty"
            )

        self.project = project
        self.location = location
        self.queue_name = queue_name
        self.worker_url = worker_url.rstrip("/")
        self.oidc_service_account_email = oidc_service_account_email
        self.oidc_audience = (oidc_audience or self.worker_url).rstrip("/")
        self.client = client or tasks_v2.CloudTasksClient()
        self.queue_path = self.client.queue_path(
            project,
            location,
            queue_name,
        )

    def enqueue_for_run(self, run_id: str) -> QueueTask:
        """Create a task, reuse an active task, or use a retry-safe name."""
        deterministic_task_id = self._deterministic_task_id(run_id)

        existing = self._get_by_task_id(deterministic_task_id)
        if existing is not None:
            return existing

        try:
            return self._create_task(
                run_id=run_id,
                task_id=deterministic_task_id,
            )
        except AlreadyExists:
            # Cloud Tasks can retain a recently completed named task for a
            # deduplication window even though get_task no longer returns it.
            # A retry must receive a fresh name rather than being reported as
            # queued without an active task.
            retry_task_id = self._retry_task_id(run_id)
            return self._create_task(
                run_id=run_id,
                task_id=retry_task_id,
            )

    def get(self, task_id: str) -> QueueTask | None:
        """Retrieve a named Cloud Task when it still exists."""
        return self._get_by_task_id(task_id)

    def get_for_run(self, run_id: str) -> QueueTask | None:
        """Retrieve the deterministic active task associated with a run."""
        return self.get(self._deterministic_task_id(run_id))

    def _create_task(self, run_id: str, task_id: str) -> QueueTask:
        task_name = self.client.task_path(
            self.project,
            self.location,
            self.queue_name,
            task_id,
        )
        created_at = utc_now()
        body = json.dumps(
            {"run_id": run_id},
            separators=(",", ":"),
        ).encode("utf-8")

        task = tasks_v2.Task(
            name=task_name,
            http_request=tasks_v2.HttpRequest(
                http_method=tasks_v2.HttpMethod.POST,
                url=self.worker_url,
                headers={
                    "Content-Type": "application/json",
                },
                body=body,
                oidc_token=tasks_v2.OidcToken(
                    service_account_email=self.oidc_service_account_email,
                    audience=self.oidc_audience,
                ),
            ),
        )

        response = self.client.create_task(
            request={
                "parent": self.queue_path,
                "task": task,
            }
        )
        response_created_at = self._task_create_time(response)
        if response_created_at is not None:
            created_at = response_created_at

        return QueueTask(
            task_id=task_id,
            run_id=run_id,
            idempotency_key=run_id,
            status="queued",
            created_at=created_at,
        )

    def _get_by_task_id(self, task_id: str) -> QueueTask | None:
        task_name = self.client.task_path(
            self.project,
            self.location,
            self.queue_name,
            task_id,
        )

        try:
            task = self.client.get_task(name=task_name)
        except NotFound:
            return None

        run_id = self._run_id_from_task(task_id, task)
        created_at = self._task_create_time(task) or utc_now()

        return QueueTask(
            task_id=task_id,
            run_id=run_id,
            idempotency_key=run_id,
            status="queued",
            created_at=created_at,
        )

    @staticmethod
    def _deterministic_task_id(run_id: str) -> str:
        safe_run_id = CloudTasksQueue._safe_run_id(run_id)
        return f"task-{safe_run_id}"

    @staticmethod
    def _retry_task_id(run_id: str) -> str:
        safe_run_id = CloudTasksQueue._safe_run_id(run_id)
        return f"task-{safe_run_id}-retry-{uuid4().hex[:8]}"

    @staticmethod
    def _safe_run_id(run_id: str) -> str:
        safe_run_id = "".join(
            character
            for character in run_id
            if character.isalnum() or character in "-_"
        )
        if not safe_run_id:
            raise ValueError("run_id must contain at least one safe character")
        return safe_run_id

    @staticmethod
    def _run_id_from_task(task_id: str, task: object) -> str:
        http_request = getattr(task, "http_request", None)
        body = getattr(http_request, "body", b"")
        if body:
            try:
                payload = json.loads(body.decode("utf-8"))
                run_id = payload.get("run_id")
                if isinstance(run_id, str) and run_id:
                    return run_id
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass

        if task_id.startswith("task-"):
            return task_id[5:]
        return task_id

    @staticmethod
    def _task_create_time(task: object) -> datetime | None:
        create_time = getattr(task, "create_time", None)
        if create_time is None:
            return None

        if isinstance(create_time, datetime):
            return create_time

        to_datetime = getattr(create_time, "ToDatetime", None)
        if callable(to_datetime):
            return to_datetime(tzinfo=timezone.utc)

        return None
