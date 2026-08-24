from __future__ import annotations

import os
from pathlib import Path

from .cloud_tasks_queue import CloudTasksQueue
from .local_queue import LocalTaskQueue
from .queue import TaskQueue


AGENT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCAL_TASK_ROOT = AGENT_ROOT / "data" / "tasks"
DEFAULT_PROJECT = "gen-lang-client-0100610229"
DEFAULT_LOCATION = "europe-west3"
DEFAULT_QUEUE_NAME = "groundpulse-research"


def get_task_queue() -> TaskQueue:
    """Select local or Cloud Tasks queueing from environment configuration."""
    backend = os.getenv("GROUND_PULSE_QUEUE", "local").strip().lower()

    if backend == "local":
        return LocalTaskQueue(root=DEFAULT_LOCAL_TASK_ROOT)

    if backend == "cloudtasks":
        worker_url = os.getenv("GROUND_PULSE_WORKER_URL", "").strip()
        service_account = os.getenv(
            "GROUND_PULSE_TASK_SERVICE_ACCOUNT_EMAIL",
            "",
        ).strip()

        if not worker_url:
            raise ValueError(
                "GROUND_PULSE_WORKER_URL is required when "
                "GROUND_PULSE_QUEUE=cloudtasks"
            )

        if not service_account:
            raise ValueError(
                "GROUND_PULSE_TASK_SERVICE_ACCOUNT_EMAIL is required when "
                "GROUND_PULSE_QUEUE=cloudtasks"
            )

        return CloudTasksQueue(
            project=os.getenv(
                "GOOGLE_CLOUD_PROJECT",
                DEFAULT_PROJECT,
            ),
            location=os.getenv(
                "GROUND_PULSE_CLOUD_TASKS_LOCATION",
                DEFAULT_LOCATION,
            ),
            queue_name=os.getenv(
                "GROUND_PULSE_CLOUD_TASKS_QUEUE",
                DEFAULT_QUEUE_NAME,
            ),
            worker_url=worker_url,
            oidc_service_account_email=service_account,
        )

    raise ValueError(
        "GROUND_PULSE_QUEUE must be either 'local' or 'cloudtasks'"
    )
