from __future__ import annotations

from typing import Protocol

from .p1_models import ResearchRequest, ResearchRun


class RunRepository(Protocol):
    """Storage contract shared by local files and Firestore."""

    def create(self, request: ResearchRequest) -> ResearchRun:
        """Create and persist a new run."""
        ...

    def get(self, run_id: str) -> ResearchRun | None:
        """Retrieve a run by ID, or return None if it does not exist."""
        ...

    def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> ResearchRun | None:
        """Retrieve the existing run for an idempotency key."""
        ...

    def save(self, run: ResearchRun) -> ResearchRun:
        """Persist the complete current run state."""
        ...