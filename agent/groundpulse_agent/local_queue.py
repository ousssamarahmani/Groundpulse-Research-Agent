from __future__ import annotations

from pathlib import Path
from threading import Lock
from uuid import uuid4

from .p1_models import utc_now
from .queue import QueueTask, TaskQueue


class LocalTaskQueue(TaskQueue):
    """JSON-backed local queue with one task per run ID."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path("data/tasks")
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def enqueue_for_run(self, run_id: str) -> QueueTask:
        path = self._run_path(run_id)

        with self._lock:
            if path.exists():
                return self._read(path)

            task = QueueTask(
                task_id=f"task_{uuid4().hex[:12]}",
                run_id=run_id,
                idempotency_key=run_id,
                status="queued",
                created_at=utc_now(),
            )

            temporary = path.with_suffix(".tmp")
            temporary.write_text(
                task.model_dump_json(indent=2),
                encoding="utf-8",
            )
            temporary.replace(path)
            return task

    def get(self, task_id: str) -> QueueTask | None:
        for path in self.root.glob("*.json"):
            task = self._read(path)
            if task.task_id == task_id:
                return task
        return None

    def get_for_run(self, run_id: str) -> QueueTask | None:
        path = self._run_path(run_id)
        if not path.exists():
            return None
        return self._read(path)

    def _run_path(self, run_id: str) -> Path:
        safe_run_id = "".join(
            character
            for character in run_id
            if character.isalnum() or character in "-_"
        )
        return self.root / f"{safe_run_id}.json"

    @staticmethod
    def _read(path: Path) -> QueueTask:
        return QueueTask.model_validate_json(
            path.read_text(encoding="utf-8")
        )
