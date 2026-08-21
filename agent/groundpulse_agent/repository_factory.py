from __future__ import annotations

import os
from pathlib import Path

from .firestore_repo import FirestoreRunRepository
from .local_repo import FileRunRepository
from .repository import RunRepository


AGENT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCAL_ROOT = AGENT_ROOT / "data" / "runs"


def get_run_repository() -> RunRepository:
    """Select local or Firestore persistence from environment configuration."""
    backend = os.getenv("GROUND_PULSE_STORAGE", "local").strip().lower()

    if backend == "local":
        return FileRunRepository(root=DEFAULT_LOCAL_ROOT)

    if backend == "firestore":
        return FirestoreRunRepository(
            project=os.getenv(
                "GOOGLE_CLOUD_PROJECT",
                "gen-lang-client-0100610229",
            ),
            collection=os.getenv(
                "GROUND_PULSE_RUN_COLLECTION",
                "research_runs",
            ),
        )

    raise ValueError(
        "GROUND_PULSE_STORAGE must be either 'local' or 'firestore'"
    )
