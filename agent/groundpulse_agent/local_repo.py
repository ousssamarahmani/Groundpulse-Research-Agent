from __future__ import annotations

from pathlib import Path
from threading import Lock
from uuid import uuid4

from .p1_models import ResearchRequest, ResearchRun, utc_now


class FileRunRepository:
    """Small local repository used before Firestore is introduced."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path("data/runs")
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def create(self, request: ResearchRequest) -> ResearchRun:
        run_id = f"run_p1_{uuid4().hex[:12]}"
        run = ResearchRun(
            run_id=run_id,
            request=request,
            status="created",
            created_at=utc_now(),
        )
        self.save(run)
        return run

    def get(self, run_id: str) -> ResearchRun | None:
        path = self._path(run_id)
        if not path.exists():
            return None
        return ResearchRun.model_validate_json(path.read_text(encoding="utf-8"))

    def save(self, run: ResearchRun) -> ResearchRun:
        path = self._path(run.run_id)
        temporary = path.with_suffix(".tmp")
        with self._lock:
            temporary.write_text(run.model_dump_json(indent=2), encoding="utf-8")
            temporary.replace(path)
        return run

    def _path(self, run_id: str) -> Path:
        safe_run_id = "".join(
            character for character in run_id if character.isalnum() or character in "-_"
        )
        return self.root / f"{safe_run_id}.json"
