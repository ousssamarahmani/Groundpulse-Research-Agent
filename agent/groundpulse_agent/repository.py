from __future__ import annotations

from typing import Protocol

from .p1_models import ResearchRequest, ResearchRun


class RunRepository(Protocol):
    """Storage contract shared by local files and future Firestore."""

    def create(self, request: ResearchRequest) -> ResearchRun:
        """Create and persist a new run."""
        ...

    def get(self, run_id: str) -> ResearchRun | None:
        """Retrieve a run or return None when it does not exist."""
        ...

    def save(self, run: ResearchRun) -> ResearchRun:
        """Persist the complete current run state."""
        ...
