from __future__ import annotations

from groundpulse_agent.local_queue import LocalTaskQueue


def test_duplicate_enqueue_returns_same_task(tmp_path) -> None:
    queue = LocalTaskQueue(root=tmp_path / "tasks")
    run_id = "run_p1_idempotency_test"

    first = queue.enqueue_for_run(run_id)
    second = queue.enqueue_for_run(run_id)

    assert first.task_id == second.task_id
    assert first.run_id == run_id
    assert second.idempotency_key == run_id
    assert second.status == "queued"
    assert len(list((tmp_path / "tasks").glob("*.json"))) == 1


def test_task_survives_queue_restart(tmp_path) -> None:
    storage = tmp_path / "tasks"
    run_id = "run_p1_restart_test"

    first_queue = LocalTaskQueue(root=storage)
    created = first_queue.enqueue_for_run(run_id)

    second_queue = LocalTaskQueue(root=storage)
    recovered = second_queue.get_for_run(run_id)
    recovered_by_id = second_queue.get(created.task_id)

    assert recovered is not None
    assert recovered_by_id is not None
    assert recovered.task_id == created.task_id
    assert recovered.run_id == run_id
    assert recovered.status == "queued"


def test_different_runs_get_different_tasks(tmp_path) -> None:
    queue = LocalTaskQueue(root=tmp_path / "tasks")

    first = queue.enqueue_for_run("run_p1_first_test")
    second = queue.enqueue_for_run("run_p1_second_test")

    assert first.task_id != second.task_id
    assert first.run_id != second.run_id
    assert len(list((tmp_path / "tasks").glob("*.json"))) == 2
