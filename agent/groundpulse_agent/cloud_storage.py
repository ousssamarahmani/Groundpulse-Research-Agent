from __future__ import annotations

import hashlib
from pathlib import Path

from google.api_core.exceptions import PreconditionFailed
from google.cloud import storage

from .storage import StoredObject


class CloudStorageArtifactStorage:
    """Private Google Cloud Storage backend for immutable research objects."""

    def __init__(
        self,
        *,
        bucket_name: str,
        project: str | None = None,
        client: storage.Client | None = None,
    ) -> None:
        if not bucket_name.strip():
            raise ValueError("Cloud Storage bucket name must not be empty")

        self.bucket_name = bucket_name
        self.client = client or storage.Client(project=project)
        self.bucket = self.client.bucket(bucket_name)

    def store_bytes(
        self,
        object_path: str,
        content: bytes,
        *,
        content_type: str,
    ) -> StoredObject:
        normalized_path = self._normalize_object_path(object_path)
        digest = hashlib.sha256(content).hexdigest()
        blob = self.bucket.blob(normalized_path)
        blob.metadata = {"sha256": digest}

        try:
            blob.upload_from_string(
                content,
                content_type=content_type,
                if_generation_match=0,
            )
        except PreconditionFailed:
            blob.reload()
            existing_sha256 = (blob.metadata or {}).get("sha256")
            if existing_sha256 != digest:
                raise FileExistsError(
                    "Immutable Cloud Storage object already exists with "
                    f"different content: {normalized_path}"
                )

        return StoredObject(
            object_path=normalized_path,
            uri=f"gs://{self.bucket_name}/{normalized_path}",
            sha256=digest,
            size_bytes=len(content),
            generation=str(blob.generation) if blob.generation else None,
        )

    def store_file(
        self,
        object_path: str,
        source_path: Path,
        *,
        content_type: str,
    ) -> StoredObject:
        return self.store_bytes(
            object_path,
            source_path.read_bytes(),
            content_type=content_type,
        )

    def store_approved_snapshot(
        self,
        source_id: str,
        source_path: Path,
    ) -> StoredObject:
        content = source_path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        object_path = f"snapshots/{source_id}/{digest}.json"
        return self.store_bytes(
            object_path,
            content,
            content_type="application/json",
        )

    def store_directory(
        self,
        prefix: str,
        directory: Path,
    ) -> list[StoredObject]:
        stored: list[StoredObject] = []
        for source_path in sorted(path for path in directory.rglob("*") if path.is_file()):
            relative_path = source_path.relative_to(directory).as_posix()
            object_path = f"{prefix.rstrip('/')}/{relative_path}"
            stored.append(
                self.store_file(
                    object_path,
                    source_path,
                    content_type=self._content_type(source_path),
                )
            )
        return stored

    @staticmethod
    def _normalize_object_path(object_path: str) -> str:
        normalized = object_path.strip().replace("\\", "/").lstrip("/")
        if not normalized or normalized in {".", ".."}:
            raise ValueError("Object path must not be empty")
        parts = normalized.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError(f"Unsafe object path: {object_path}")
        return "/".join(parts)

    @staticmethod
    def _content_type(path: Path) -> str:
        suffix = path.suffix.lower()
        return {
            ".json": "application/json",
            ".md": "text/markdown; charset=utf-8",
            ".txt": "text/plain; charset=utf-8",
        }.get(suffix, "application/octet-stream")
