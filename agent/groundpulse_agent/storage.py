from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict


class StoredObject(BaseModel):
    """Immutable object metadata returned by a storage backend."""

    model_config = ConfigDict(extra="forbid")

    object_path: str
    uri: str
    sha256: str
    size_bytes: int
    generation: str | None = None


class ArtifactStorage(Protocol):
    """Contract shared by local and Google Cloud Storage backends."""

    def store_bytes(
        self,
        object_path: str,
        content: bytes,
        *,
        content_type: str,
    ) -> StoredObject:
        """Create an immutable object or reuse an identical existing object."""
        ...

    def store_file(
        self,
        object_path: str,
        source_path: Path,
        *,
        content_type: str,
    ) -> StoredObject:
        """Store one local file as an immutable object."""
        ...

    def store_approved_snapshot(
        self,
        source_id: str,
        source_path: Path,
    ) -> StoredObject:
        """Store an approved source snapshot under its content hash."""
        ...

    def store_directory(
        self,
        prefix: str,
        directory: Path,
    ) -> list[StoredObject]:
        """Store every file in a directory beneath an object prefix."""
        ...
