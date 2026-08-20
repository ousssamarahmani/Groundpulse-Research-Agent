from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .local_repo import FileRunRepository
from .p1_models import ResearchRun, transition_run


AGENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = AGENT_ROOT.parent
RUNS_ROOT = AGENT_ROOT / "data" / "runs"
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "p0"


def execute_local_run(run_id: str) -> ResearchRun:
    """Execute one queued run through the local ADK/P0 pipeline."""
    repository = FileRunRepository(root=RUNS_ROOT)
    run = repository.get(run_id)

    if run is None:
        raise KeyError(f"Run not found: {run_id}")

    if run.status != "queued":
        raise ValueError(
            f"Run {run_id} is not queued; current status is {run.status}"
        )

    run = transition_run(run, "running")
    repository.save(run)

    try:
        completed = subprocess.run(
            [sys.executable, "-m", "groundpulse_agent.run_p0"],
            cwd=AGENT_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if completed.returncode != 0:
            failed = transition_run(run, "failed").model_copy(
                update={
                    "error_code": "p0_pipeline_failed",
                    "review_reason": (
                        completed.stderr[-2000:]
                        or completed.stdout[-2000:]
                    ),
                }
            )
            repository.save(failed)
            return failed

        if not ARTIFACT_ROOT.exists():
            raise RuntimeError(
                "P0 pipeline completed without an artifact directory"
            )

        artifact_dirs = [
            path for path in ARTIFACT_ROOT.iterdir() if path.is_dir()
        ]

        if not artifact_dirs:
            raise RuntimeError(
                "P0 pipeline completed without a timestamped artifact directory"
            )

        latest_artifact = max(
            artifact_dirs,
            key=lambda path: path.stat().st_mtime,
        )
        report_path = latest_artifact / "validation_report.json"

        if not report_path.exists():
            raise RuntimeError(
                "P0 artifact directory has no validation_report.json"
            )

        report = json.loads(report_path.read_text(encoding="utf-8"))

        run = transition_run(run, "validating")
        repository.save(run)

        if not report.get("passed", False):
            held = transition_run(run, "held_for_review").model_copy(
                update={
                    "validation_state": "review",
                    "review_reason": (
                        "Deterministic evidence validation failed"
                    ),
                    "artifact_ids": [latest_artifact.name],
                }
            )
            repository.save(held)
            return held

        run = transition_run(run, "packaging")
        run = transition_run(run, "released")
        released = run.model_copy(
            update={
                "validation_state": "passed",
                "artifact_ids": [latest_artifact.name],
                "snapshot_ids": ["celestrak_gp_25544"],
            }
        )
        repository.save(released)
        return released

    except Exception as exc:
        failed = transition_run(run, "failed").model_copy(
            update={
                "error_code": "local_worker_exception",
                "review_reason": str(exc),
            }
        )
        repository.save(failed)
        return failed
