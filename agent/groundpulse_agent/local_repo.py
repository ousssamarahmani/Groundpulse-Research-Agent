from __future__ import annotations

from pathlib import Path
from threading import Lock
from uuid import uuid4

from pydantic import ValidationError

from .p1_models import ResearchRequest, ResearchRun, utc_now
from .repository import RunRepository


class FileRunRepository(RunRepository):
    """Local JSON implementation of the shared run repository contract."""

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

        try:
            return ResearchRun.model_validate_json(
                path.read_text(encoding="utf-8")
            )
        except ValidationError:
            # Legacy files created before idempotency_key was required are
            # intentionally ignored by the current P1 contract.
            return None

    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> ResearchRun | None:
        for path in self.root.glob("*.json"):
            try:
                run = ResearchRun.model_validate_json(
                    path.read_text(encoding="utf-8")
                )
            except ValidationError:
                # Skip pre-idempotency local records instead of failing the
                # entire POST /runs request with HTTP 500.
                continue

            if run.request.idempotency_key == idempotency_key:
                return run

        return None

    def save(self, run: ResearchRun) -> ResearchRun:
        path = self._path(run.run_id)
        temporary = path.with_suffix(".tmp")

        with self._lock:
            temporary.write_text(
                run.model_dump_json(indent=2),
                encoding="utf-8",
            )
            temporary.replace(path)

        return run

    def _path(self, run_id: str) -> Path:
        safe_run_id = "".join(
            character
            for character in run_id
            if character.isalnum() or character in "-_"
        )
        return self.root / f"{safe_run_id}.json"
