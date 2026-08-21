from __future__ import annotations

from datetime import datetime, timezone

import pytest

from groundpulse_agent.local_repo import FileRunRepository
from groundpulse_agent.p1_models import (
    ResearchRequest,
    ResearchRun,
    transition_run,
)


def make_request() -> ResearchRequest:
    return ResearchRequest.model_validate(
        {
            "idempotency_key": "p1-test-iss-request-001",
            "question": (
                "Given one approved CelesTrak GP snapshot for the ISS, "
                "what is source-backed and what is unavailable?"
            ),
            "decision_intent": "Evidence preparation for research review",
            "object": {
                "name": "ISS",
                "norad_catalog_id": "25544",
            },
            "allowed_source_ids": ["celestrak_gp_25544"],
            "authorization_state": "approved_public_source",
            "non_claims": ["No live telemetry"],
        }
    )


def test_create_and_restart_recovery(tmp_path) -> None:
    storage = tmp_path / "runs"

    first_repository = FileRunRepository(root=storage)
    created = first_repository.create(make_request())
    queued = transition_run(created, "queued")
    first_repository.save(queued)

    second_repository = FileRunRepository(root=storage)
    recovered = second_repository.get(created.run_id)

    assert recovered is not None
    assert recovered.run_id == created.run_id
    assert recovered.status == "queued"
    assert recovered.request.idempotency_key == "p1-test-iss-request-001"
    assert recovered.request.object.name == "ISS"
    assert recovered.request.allowed_source_ids == ["celestrak_gp_25544"]


def test_running_transition_increments_attempt_count(tmp_path) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    created = repository.create(make_request())
    queued = transition_run(created, "queued")
    running = transition_run(queued, "running")
    repository.save(running)

    assert running.status == "running"
    assert running.attempt_count == 1
    assert running.started_at is not None

    recovered = repository.get(running.run_id)
    assert recovered is not None
    assert recovered.attempt_count == 1
    assert recovered.status == "running"


def test_failed_run_can_be_requeued(tmp_path) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    created = repository.create(make_request())
    queued = transition_run(created, "queued")
    running = transition_run(queued, "running")
    failed = transition_run(running, "failed")
    retried = transition_run(failed, "queued")
    repository.save(retried)

    assert failed.status == "failed"
    assert failed.completed_at is not None
    assert retried.status == "queued"
    assert retried.attempt_count == 1


def test_terminal_released_run_cannot_restart(tmp_path) -> None:
    repository = FileRunRepository(root=tmp_path / "runs")
    request = make_request()
    run = ResearchRun(
        run_id="run_p1_terminal_test",
        request=request,
        status="released",
        created_at=datetime.now(timezone.utc),
    )

    repository.save(run)

    with pytest.raises(ValueError, match="Invalid run transition"):
        transition_run(run, "running")


def test_repositories_are_isolated(tmp_path) -> None:
    first = FileRunRepository(root=tmp_path / "first")
    second = FileRunRepository(root=tmp_path / "second")

    created = first.create(make_request())

    assert first.get(created.run_id) is not None
    assert second.get(created.run_id) is None
