from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from groundpulse_agent.dashboard_api import (
    dashboard_get_run,
    dashboard_list_artifacts,
    dashboard_list_runs,
    dashboard_read_artifact,
)
from groundpulse_agent.dashboard_models import (
    DashboardArtifactListResponse,
    DashboardRunListResponse,
)
from groundpulse_agent.local_repo import FileRunRepository
from groundpulse_agent.local_storage import LocalArtifactStorage
from groundpulse_agent.p1_models import ResearchRequest, transition_run
import groundpulse_agent.dashboard_api as dashboard_module


def make_request(key: str = "dashboard-test-request-001") -> ResearchRequest:
    return ResearchRequest(
        idempotency_key=key,
        question="Which evidence is source-backed and which is unavailable?",
        decision_intent="Dashboard integration test",
        object={"name": "ISS", "norad_catalog_id": "25544"},
        allowed_source_ids=["celestrak_gp_25544"],
        authorization_state="approved_public_source",
        non_claims=["No live telemetry"],
    )


def make_released_run(repository: FileRunRepository):
    run = repository.create(make_request())
    run = transition_run(run, "queued")
    run = transition_run(run, "running")
    run = transition_run(run, "validating")
    run = transition_run(run, "packaging")
    run = transition_run(run, "released")
    run = run.model_copy(
        update={
            "validation_state": "passed",
            "snapshot_ids": ["celestrak_gp_25544"],
            "artifact_ids": ["20260827T110302Z"],
        }
    )
    repository.save(run)
    return run


def test_dashboard_lists_runs_newest_first(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    first = make_released_run(repository)
    second = repository.create(make_request("dashboard-test-request-002"))
    repository.save(transition_run(second, "queued"))
    monkeypatch.setattr(dashboard_module, "_dashboard_repository", repository)

    response = dashboard_list_runs(limit=20, offset=0)

    assert isinstance(response, DashboardRunListResponse)
    assert response.returned == 2
    assert {item.run_id for item in response.runs} == {first.run_id, second.run_id}
    assert response.runs[0].created_at >= response.runs[1].created_at


def test_dashboard_returns_single_run_summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    run = make_released_run(repository)
    monkeypatch.setattr(dashboard_module, "_dashboard_repository", repository)

    summary = dashboard_get_run(run.run_id)

    assert summary.run_id == run.run_id
    assert summary.object_name == "ISS"
    assert summary.validation_state == "passed"
    assert summary.snapshot_ids == ["celestrak_gp_25544"]


def test_dashboard_lists_and_reads_artifacts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    storage = LocalArtifactStorage(root=tmp_path / "objects")
    run = make_released_run(repository)
    storage.store_bytes(
        f"runs/{run.run_id}/artifact/package_manifest.json",
        json.dumps({"run_id": run.run_id}).encode("utf-8"),
        content_type="application/json",
    )
    monkeypatch.setattr(dashboard_module, "_dashboard_repository", repository)
    monkeypatch.setattr(dashboard_module, "_dashboard_storage", storage)

    listing = dashboard_list_artifacts(run.run_id)
    response = dashboard_read_artifact(run.run_id, "artifact/package_manifest.json")

    assert isinstance(listing, DashboardArtifactListResponse)
    assert listing.returned == 1
    assert listing.artifacts[0].name == "artifact/package_manifest.json"
    assert listing.artifacts[0].download_url.endswith("artifact/package_manifest.json")
    assert response.body == json.dumps({"run_id": run.run_id}).encode("utf-8")
    assert response.media_type == "application/json"


def test_dashboard_rejects_artifact_path_traversal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    storage = LocalArtifactStorage(root=tmp_path / "objects")
    run = make_released_run(repository)
    monkeypatch.setattr(dashboard_module, "_dashboard_repository", repository)
    monkeypatch.setattr(dashboard_module, "_dashboard_storage", storage)

    with pytest.raises(Exception):
        dashboard_read_artifact(run.run_id, "../secrets.txt")
