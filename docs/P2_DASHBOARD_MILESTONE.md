# GroundPulse P2 Dashboard Milestone

**Verified:** 2026-08-27  
**Branch:** `feat/p1-cloud-backed-run`  
**Latest deployed revision:** `groundpulse-research-api-00020-gqv`  
**Service:** `groundpulse-research-api`  
**Region:** `europe-west3`

## Dashboard integration verified

Mission Control is now connected to live research API data. The deployed API successfully returns Firestore-backed run history through `GET /dashboard/runs` and exposes immutable artifact metadata through `GET /dashboard/runs/{run_id}/artifacts`.

The primary demonstration run is `run_p1_55cbb0817ecd`. It is released, has passed the evidence validation gate, and is backed by the approved CelesTrak snapshot `celestrak_gp_25544` for the ISS.

| Field | Verified value |
|---|---|
| Run ID | `run_p1_55cbb0817ecd` |
| Object | ISS |
| NORAD catalog ID | `25544` |
| Status | `released` |
| Validation state | `passed` |
| Approved snapshots | `1` |
| Snapshot ID | `celestrak_gp_25544` |
| Immutable package objects | `10` |
| Artifact package ID | `20260827T110302Z` |

## Evidence and package behavior

The dashboard displays the four-stage workflow: frame request, discover sources, validate evidence, and build package. It also displays the source review, canonical candidate claim ledger, explicit gap list, execution events, and recent run archive.

The ten immutable package objects are stored in the private GCS bucket `groundpulse-artifacts-gen-lang-client-0100610229`. Artifact metadata and content are accessed through the authenticated research API proxy; the bucket is not made public.

## Reliability fix

Legacy Firestore documents that do not satisfy the current `ResearchRun` schema are skipped during dashboard listing and logged as compatibility warnings. This prevents malformed historical records from causing a dashboard `500` response while preserving valid run history.

## Deployment fixes

The Buildpacks deployment uses `agent/Procfile` with the following ASGI entrypoint:

```text
web: uvicorn groundpulse_agent.api:app --host 0.0.0.0 --port $PORT
```

The relevant commits are:

```text
c3d7708  feat(dashboard): connect mission control to live backend data
abbc75d  fix(deploy): define Cloud Run ASGI entrypoint
7ca864a  fix(dashboard): skip legacy invalid Firestore run records
```

## P2 demo readiness

The dashboard is ready for recording a demo. Use the released ISS run as the primary path, show the passed validation gate, open the evidence ledger, open the package tab, and demonstrate that the package contains immutable, source-linked artifacts. Keep the local frontend pointed at `http://127.0.0.1:8000` when using the local authenticated API process; do not expose the private GCS bucket or commit `.env` files.
