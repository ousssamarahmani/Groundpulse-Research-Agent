from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_workers_pass_authoritative_run_id_to_p0_pipeline() -> None:
    expected_invocation = '"--run-id", run_id'

    for worker_name in ("local_worker.py", "local_worker_package.py"):
        worker_source = (
            REPO_ROOT / "agent" / "groundpulse_agent" / worker_name
        ).read_text(encoding="utf-8")
        assert expected_invocation in worker_source


def test_p0_pipeline_writes_authoritative_run_id_to_normalized_result() -> None:
    pipeline_source = (
        REPO_ROOT / "agent" / "groundpulse_agent" / "run_p0.py"
    ).read_text(encoding="utf-8")

    assert '"run_id": run_id' in pipeline_source
    assert 'ledger = ledger.model_copy(update={"run_id": run_id})' in pipeline_source
