from __future__ import annotations

import os
from pathlib import Path

from .cloud_storage import CloudStorageArtifactStorage
from .local_storage import LocalArtifactStorage
from .storage import ArtifactStorage


def get_artifact_storage() -> ArtifactStorage:
    """Return the configured artifact storage backend.

    Local storage is the safe default for development. Cloud Storage requires
    an explicit backend selection and bucket name.
    """
    backend = os.getenv("GROUND_PULSE_ARTIFACT_STORAGE", "local").strip().lower()

    if backend == "local":
        root = os.getenv("GROUND_PULSE_LOCAL_STORAGE_ROOT", "")
        return LocalArtifactStorage(root=Path(root) if root else None)

    if backend in {"gcs", "cloudstorage", "cloud_storage"}:
        bucket_name = os.getenv("GROUND_PULSE_ARTIFACT_BUCKET", "").strip()
        if not bucket_name:
            raise RuntimeError(
                "GROUND_PULSE_ARTIFACT_BUCKET is required when "
                "GROUND_PULSE_ARTIFACT_STORAGE=gcs"
            )
        return CloudStorageArtifactStorage(
            bucket_name=bucket_name,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        )

    raise RuntimeError(
        "Unsupported GROUND_PULSE_ARTIFACT_STORAGE: "
        f"{backend!r}; expected 'local' or 'gcs'"
    )
