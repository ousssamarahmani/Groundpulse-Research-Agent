from __future__ import annotations

import hashlib
from pathlib import Path

from .storage import StoredObject


class LocalArtifactStorage:
    """Filesystem artifact storage used for local development and tests."""

    def __init__(self, root: Path | str | None = None) -> None:
        self.root = Path(root or Path("data") / "storage")
        self.root.mkdir(parents=True, exist_ok=True)

    def store_bytes(
        self,
        object_path: str,
        content: bytes,
        *,
        content_type: str,
    ) -> StoredObject:
        del content_type
        normalized_path = self._normalize_object_path(object_path)
        destination = self.root / normalized_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(content).hexdigest()

        if destination.exists():
            existing = destination.read_bytes()
            existing_digest = hashlib.sha256(existing).hexdigest()
            if existing_digest != digest:
                raise FileExistsError(
                    f"Immutable object already exists with different content: "
                    f"{normalized_path}"
                )
        else:
            destination.write_bytes(content)

        return StoredObject(
            object_path=normalized_path,
            uri=destination.resolve().as_uri(),
            sha256=digest,
            size_bytes=len(content),
            generation=None,
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

    def list_objects(self, prefix: str) -> list[StoredObject]:
        normalized_prefix = self._normalize_object_path(prefix).rstrip("/")
        prefix_root = self.root / normalized_prefix
        if not prefix_root.exists():
            return []

        objects: list[StoredObject] = []
        for path in sorted(path for path in prefix_root.rglob("*") if path.is_file()):
            content = path.read_bytes()
            object_path = path.relative_to(self.root).as_posix()
            objects.append(
                StoredObject(
                    object_path=object_path,
                    uri=path.resolve().as_uri(),
                    sha256=hashlib.sha256(content).hexdigest(),
                    size_bytes=len(content),
                    generation=None,
                )
            )
        return objects

    def read_bytes(self, object_path: str) -> bytes:
        normalized_path = self._normalize_object_path(object_path)
        path = self.root / normalized_path
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(normalized_path)
        return path.read_bytes()

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
