from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from groundpulse_agent.local_storage import LocalArtifactStorage


def test_store_bytes_is_idempotent_for_identical_content(tmp_path: Path) -> None:
    storage = LocalArtifactStorage(root=tmp_path / "storage")
    content = b"immutable research object"

    first = storage.store_bytes(
        "runs/run-001/manifest.json",
        content,
        content_type="application/json",
    )
    second = storage.store_bytes(
        "runs/run-001/manifest.json",
        content,
        content_type="application/json",
    )

    assert first.object_path == second.object_path
    assert first.sha256 == hashlib.sha256(content).hexdigest()
    assert second.sha256 == first.sha256
    assert second.size_bytes == len(content)


def test_store_bytes_rejects_different_content(tmp_path: Path) -> None:
    storage = LocalArtifactStorage(root=tmp_path / "storage")
    storage.store_bytes(
        "runs/run-001/manifest.json",
        b"first",
        content_type="application/json",
    )

    with pytest.raises(FileExistsError):
        storage.store_bytes(
            "runs/run-001/manifest.json",
            b"different",
            content_type="application/json",
        )


def test_snapshot_path_contains_content_hash(tmp_path: Path) -> None:
    source = tmp_path / "snapshot.json"
    content = b'{"OBJECT_NAME":"ISS (ZARYA)"}'
    source.write_bytes(content)
    storage = LocalArtifactStorage(root=tmp_path / "storage")

    stored = storage.store_approved_snapshot("celestrak_gp_25544", source)

    expected_hash = hashlib.sha256(content).hexdigest()
    assert stored.object_path == (
        f"snapshots/celestrak_gp_25544/{expected_hash}.json"
    )
    assert stored.sha256 == expected_hash


def test_store_directory_preserves_relative_paths(tmp_path: Path) -> None:
    directory = tmp_path / "artifact"
    directory.mkdir()
    (directory / "manifest.json").write_text("{}", encoding="utf-8")
    nested = directory / "nested"
    nested.mkdir()
    (nested / "brief.md").write_text("# Brief", encoding="utf-8")
    storage = LocalArtifactStorage(root=tmp_path / "storage")

    stored = storage.store_directory("runs/run-001/artifact", directory)

    paths = {obj.object_path for obj in stored}
    assert paths == {
        "runs/run-001/artifact/manifest.json",
        "runs/run-001/artifact/nested/brief.md",
    }
