# GroundPulse Project Status

**Last verified:** 2026-08-27  
**Active branch:** `feat/p1-cloud-backed-run`  
**Latest verified code commit:** `1ffde96`  
**Latest verified runtime revision:** `groundpulse-research-api-00017-hz4`

## Completed P1 baseline

GroundPulse has a verified controlled satellite-research path using the approved CelesTrak GP snapshot `celestrak_gp_25544` for the ISS. The system persists research runs with Firestore or local JSON fallback, supports idempotent submissions, dispatches asynchronous work through Cloud Tasks, executes a private Cloud Run worker, validates the canonical claim ledger, generates deterministic research-package artifacts, and stores immutable evidence in Google Cloud Storage.

The deployed runtime uses Firestore, Cloud Tasks, private Cloud Run, Cloud Storage, Secret Manager, and `gemini-3.5-flash-lite`. The service is configured for authenticated Cloud Tasks delivery and retains local-first development support.

The final end-to-end verification run was:

| Field | Value |
|---|---|
| Run ID | `run_p1_55cbb0817ecd` |
| Idempotency key | `artifact-package-e2e-006` |
| Status | `released` |
| Validation state | `passed` |
| Attempt count | `1` |
| Snapshot ID | `celestrak_gp_25544` |
| Artifact ID | `20260827T110302Z` |
| Error code | None |

The run produced `manifest.json`, `brief.md`, `candidate_ledger.json`, `gap_list.json`, `normalized_result.json`, `package_manifest.json`, `request.json`, `source_snapshot.json`, `validation_report.json`, and `adk_trace.redacted.json` under its immutable Cloud Storage prefix.

The focused backend regression suite passed with **17 tests passing**, covering the authoritative run ID contract, deterministic artifact generation, immutable storage behavior, persistence, and the local task queue.

## Current milestone: Dashboard API integration

The Mission Control page exists as a visual prototype but still contains hard-coded mission, evidence, trace, confidence, and package values. Dashboard API integration is now **in progress**.

The planned live-data contract is:

| Endpoint | Purpose |
|---|---|
| `GET /dashboard/runs` | Paginated recent run summaries |
| `GET /dashboard/runs/{run_id}` | One dashboard-safe run summary |
| `GET /dashboard/runs/{run_id}/artifacts` | Immutable artifact metadata |
| `GET /dashboard/runs/{run_id}/artifacts/{artifact_name}` | Authenticated artifact read through the private API boundary |

The frontend must retain explicit loading, empty, and error states. The private bucket must not be made public, and no secrets, `.env` files, virtual environments, or runtime artifact objects belong in Git.

## Remaining roadmap items

Broader live-source adapters, live telemetry, richer event and human-review surfaces, independent review, demonstration recording, and hackathon submission materials remain future or finalization work. Multi-agent orchestration is optional and should not delay completion of the controlled MVP dashboard path.
