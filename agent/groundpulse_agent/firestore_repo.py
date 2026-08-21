from __future__ import annotations

import os

from google.cloud import firestore

from .p1_models import ResearchRequest, ResearchRun, utc_now
from .repository import RunRepository


class FirestoreRunRepository(RunRepository):
    """Firestore implementation of the shared run repository contract."""

    def __init__(
        self,
        *,
        project: str | None = None,
        collection: str = "research_runs",
        client: firestore.Client | None = None,
    ) -> None:
        self.project = project or os.getenv(
            "GOOGLE_CLOUD_PROJECT",
            "gen-lang-client-0100610229",
        )
        self.collection = collection
        self.client = client or firestore.Client(project=self.project)

    def create(self, request: ResearchRequest) -> ResearchRun:
        from uuid import uuid4

        run = ResearchRun(
            run_id=f"run_p1_{uuid4().hex[:12]}",
            request=request,
            status="created",
            created_at=utc_now(),
        )
        self.save(run)
        return run

    def get(self, run_id: str) -> ResearchRun | None:
        snapshot = self._document(run_id).get()
        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        if data is None:
            return None

        return ResearchRun.model_validate(data)

    def save(self, run: ResearchRun) -> ResearchRun:
        payload = run.model_dump(mode="python")
        self._document(run.run_id).set(payload)
        return run

    def _document(self, run_id: str):
        return self.client.collection(self.collection).document(run_id)
