# Run ID Fix Notes

## Root cause

The updated P1 worker creates an authoritative `run_id` in the Research API and passes it to `execute_local_run`, but both worker subprocess calls launched `groundpulse_agent.run_p0` without passing that ID. The P0 pipeline then wrote `normalized_result.json` without a `run_id` field. `artifact_generator.generate_research_package` requires `envelope["run_id"]`, so the worker failed after the Gemini call and before package artifacts were stored.

## Fix

`run_p0.py` now requires `--run-id`, receives the API-created ID, normalizes the model ledger to that ID, writes it into `request.json`, `candidate_ledger.json`, and `normalized_result.json`, and uses it for package generation. Both `local_worker.py` and `local_worker_package.py` pass `--run-id run_id` to the subprocess. A regression test checks this contract.

## Verification

`PYTHONPATH=agent python3 -m pytest -q agent/tests` passes: 17 tests passed. Python bytecode compilation and `git diff --check` also pass.

## Repository state

The local clone was fast-forwarded from `514ae42` to the updated remote `db574ce` before the fix. The fix is currently in the local working tree and has not been pushed to GitHub.
