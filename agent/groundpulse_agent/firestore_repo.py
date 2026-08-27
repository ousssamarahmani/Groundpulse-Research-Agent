from __future__ import annotations

import logging
import os
from uuid import uuid4

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import ValidationError

from .p1_models import ResearchRequest, ResearchRun, utc_now
from .repository import RunRepository


logger = logging.getLogger(__name__)


class FirestoreRunRepository(RunRepository):
    """Firestore implementation of the shared run repository contract."""

    def __init__(
        self,
        *,
        project: str | None = None,
        collection: str = "research_runs",
        database: str | None = None,
        client: firestore.Client | None = None,
    ) -> None:
        self.project = project or os.getenv(
            "GOOGLE_CLOUD_PROJECT",
            "gen-lang-client-0100610229",
        )
        self.collection = collection
        self.database = self._normalize_database_name(
            database
            if database is not None
            else os.getenv("GOOGLE_CLOUD_FIRESTORE_DATABASE")
        )

        if client is not None:
            self.client = client
        elif self.database is None:
            # Omitting database selects the normal Firestore default database.
            # Passing the literal string "(default)" is rejected by some
            # google-cloud-firestore client versions.
            self.client = firestore.Client(project=self.project)
        else:
            self.client = firestore.Client(
                project=self.project,
                database=self.database,
            )

    def create(self, request: ResearchRequest) -> ResearchRun:
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

        try:
            return ResearchRun.model_validate(data)
        except ValidationError:
            # A direct lookup of a malformed legacy record must behave as
            # "not found" rather than turning a dashboard request into 500.
            logger.warning(
                "Skipping invalid Firestore run document during get: %s",
                run_id,
            )
            return None

    def list_runs(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[ResearchRun]:
        if limit < 1 or offset < 0:
            raise ValueError("limit must be positive and offset must be non-negative")

        # Fetch a wider page because old documents may not satisfy the current
        # ResearchRun schema. Invalid legacy records are skipped below while
        # valid records remain visible in newest-first order.
        query = (
            self.client
            .collection(self.collection)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .offset(offset)
            .limit(max(limit * 3, limit))
        )

        runs: list[ResearchRun] = []
        for snapshot in query.stream():
            data = snapshot.to_dict()
            if data is None:
                continue

            try:
                runs.append(ResearchRun.model_validate(data))
            except ValidationError as exc:
                logger.warning(
                    "Skipping invalid Firestore run document %s: %s",
                    snapshot.id,
                    exc.errors(include_url=False),
                )

            if len(runs) >= limit:
                break

        return runs

    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> ResearchRun | None:
        query = (
            self.client
            .collection(self.collection)
            .where(
                filter=FieldFilter(
                    "request.idempotency_key",
                    "==",
                    idempotency_key,
                )
            )
            .limit(1)
        )

        for snapshot in query.stream():
            data = snapshot.to_dict()
            if data is None:
                continue

            try:
                return ResearchRun.model_validate(data)
            except ValidationError:
                logger.warning(
                    "Skipping invalid Firestore run document during idempotency lookup: %s",
                    snapshot.id,
                )

        return None

    def save(self, run: ResearchRun) -> ResearchRun:
        payload = run.model_dump(mode="python")
        self._document(run.run_id).set(payload)
        return run

    def _document(self, run_id: str):
        return self.client.collection(self.collection).document(run_id)

    @staticmethod
    def _normalize_database_name(database: str | None) -> str | None:
        normalized = (database or "").strip()
        if not normalized or normalized == "(default)":
            return None
        return normalized


__all__ = ["FirestoreRunRepository"]


def get_run_repository() -> FirestoreRunRepository:
    """Return a Firestore repository using the active environment settings."""
    return FirestoreRunRepository()
