# GroundPulse Research Agent

> **An evidence-first research agent for satellite and ground-segment questions.**

GroundPulse turns a bounded research question into a reviewable evidence package. It preserves the approved source snapshot, separates source-backed claims from deterministic derivations, records unavailable evidence explicitly, validates the claim ledger, and stores immutable package artifacts for review.

## Judge-facing application

Open the visual React Mission Control dashboard here:

**[GroundPulse Mission Control](https://groundpulse-frontend-1081077557421.europe-west3.run.app/dashboard)**

The public dashboard is configured against a separate read-only demo API. No login, Google identity token, API key, or service-account credential is required.

| Public surface | URL | Purpose |
|---|---|---|
| React Mission Control | [Open dashboard](https://groundpulse-frontend-1081077557421.europe-west3.run.app/dashboard) | Visual judge-facing interface |
| Demo run archive | [Open runs](https://groundpulse-demo-api-1081077557421.europe-west3.run.app/demo/runs) | Lists the approved demonstration run |
| Run details | [Open run](https://groundpulse-demo-api-1081077557421.europe-west3.run.app/demo/runs/run_p1_55cbb0817ecd) | Shows status, validation, source, and package metadata |
| Artifact inventory | [Open artifacts](https://groundpulse-demo-api-1081077557421.europe-west3.run.app/demo/runs/run_p1_55cbb0817ecd/artifacts) | Lists immutable package objects and hashes |
| Research brief | [Open brief](https://groundpulse-demo-api-1081077557421.europe-west3.run.app/demo/runs/run_p1_55cbb0817ecd/artifacts/artifact/brief.md) | Opens the released Markdown brief |

The bare demo API root intentionally returns `404`; use the documented `/demo/...` endpoints above.

## Verified demonstration run

The public demo presents a completed ISS evidence assessment based on one approved CelesTrak GP snapshot.

| Field | Verified value |
|---|---|
| Run ID | `run_p1_55cbb0817ecd` |
| Object | ISS |
| NORAD catalog ID | `25544` |
| Question | Given one approved CelesTrak GP snapshot for the ISS, what is source-backed and what is unavailable? |
| Approved source | `celestrak_gp_25544` |
| Run status | `released` |
| Validation state | `passed` |
| Attempt count | `1` |
| Artifact package ID | `20260827T110302Z` |
| Error | None |

The released package includes a research brief, candidate claim ledger, gap list, normalized result, source snapshot, validation report, request record, package manifest, redacted ADK trace, and immutable manifest metadata.

## What the system does

GroundPulse follows an evidence-first workflow:

```text
Bounded research question
        |
        v
Request and run model
        |
        v
Approved source snapshot
        |
        v
Claim ledger and provenance validation
        |
        v
Explicit gaps and review boundary
        |
        v
Immutable research package in private Cloud Storage
        |
        v
Read-only dashboard and artifact delivery
```

The system is designed so that generated language cannot silently exceed the evidence. A claim may be source-backed, deterministically derived from recorded fields, or marked as an evidence gap. Unsupported operational conclusions remain unavailable and visible.

## Current architecture

The deployed system is separated into private research infrastructure and a public demonstration boundary.

| Component | Deployment boundary | Responsibility |
|---|---|---|
| React frontend | Public Cloud Run service `groundpulse-frontend` | Displays Mission Control and calls only the public demo API |
| Demo API facade | Public Cloud Run service `groundpulse-demo-api` | Exposes only the fixed released run and read-only artifact routes |
| Research API | Private Cloud Run service `groundpulse-research-api` | Handles research submission, worker execution, persistence, and dashboard data |
| Run persistence | Private Firestore collection | Stores run state, validation metadata, and execution information |
| Artifact storage | Private Google Cloud Storage bucket | Stores immutable evidence and package objects |
| Runtime identity | Restricted service accounts | Separates public read-only access from private research operations |

The public facade proxies approved artifact bytes through controlled routes. The frontend never receives bucket credentials, service-account JSON, Google identity tokens, or direct private bucket access.

## Evidence package

The released package demonstrates three evidence categories.

| Category | Example | Meaning |
|---|---|---|
| Supported | Approved CelesTrak source snapshot | Directly present in the approved evidence |
| Derived | Approximate orbital period of 92.93 minutes | Deterministically calculated from recorded `MEAN_MOTION` |
| Gap | Live telemetry and spacecraft health | Not available in the approved GP snapshot and therefore not claimed |

The research brief explicitly states that the package does not provide live telemetry, spacecraft-health assessment, or an operational recommendation.

## Public demo boundary

The judge-facing deployment is intentionally **read-only**. The **New research** panel is a product-surface prototype and does not submit an anonymous cloud job. The public facade does not expose `POST /runs`, queue submission, worker controls, or private research endpoints.

This boundary protects the private pipeline and prevents unauthenticated visitors from creating arbitrary jobs. To demonstrate a new research run, use the authenticated private development or operator workflow rather than the public judge URL.

## Local development

### Prerequisites

Install Node.js 20 or newer, pnpm, Python 3.11 or newer, and Git. Google Cloud commands additionally require the Google Cloud CLI and an authenticated development account.

### Frontend

```powershell
git clone https://github.com/ousssamarahmani/Groundpulse-Research-Agent.git
Set-Location .\Groundpulse-Research-Agent
pnpm install

@"
VITE_GROUNDPULSE_API_URL=https://groundpulse-demo-api-1081077557421.europe-west3.run.app
"@ | Set-Content .\.env.local -Encoding utf8

pnpm exec tsc --noEmit
pnpm dev
```

Open the Vite URL shown in the terminal and navigate to `/dashboard`.

### Private Python API

```powershell
Set-Location .\Groundpulse-Research-Agent

$env:GROUND_PULSE_STORAGE = "firestore"
$env:GROUND_PULSE_ARTIFACT_STORAGE = "gcs"
$env:GROUND_PULSE_ARTIFACT_BUCKET = "groundpulse-artifacts-gen-lang-client-0100610229"
$env:GOOGLE_CLOUD_PROJECT = "gen-lang-client-0100610229"
$env:GROUND_PULSE_QUEUE = "local"

.\agent\.venv\Scripts\python.exe -m uvicorn `
    agent.groundpulse_agent.api:app `
    --host 127.0.0.1 `
    --port 8000
```

The private API requires the appropriate local Google credentials for Firestore and Cloud Storage. Never commit `.env` files, service-account keys, identity tokens, or API secrets.

### Verification commands

```powershell
pnpm exec tsc --noEmit
pnpm build

Set-Location .\agent
.\.venv\Scripts\python.exe -m pytest -q
```

## Deployment notes

The frontend is built from the repository root and served by the Node/Express production server. Its public API base URL is injected at build time using:

```text
VITE_GROUNDPULSE_API_URL=https://groundpulse-demo-api-1081077557421.europe-west3.run.app
```

The public demo API is deployed separately from `.\agent` and uses the restricted `groundpulse-demo-reader` identity. The private research API must not be made publicly invokable merely to support the frontend.

## Repository guide

| Path | Purpose |
|---|---|
| `client/src/pages/Dashboard.tsx` | React Mission Control page |
| `client/src/lib/dashboardApi.ts` | Public demo API client used by the deployed frontend |
| `agent/groundpulse_agent/api.py` | Private research API |
| `agent/groundpulse_agent/demo_api.py` | Public read-only demo facade |
| `agent/groundpulse_agent/` | Run model, repositories, storage, queue, and artifact generation |
| `agent/tests/` | Backend and persistence tests |
| `docs/PROJECT_STATUS.md` | Verified implementation status |
| `docs/P2_DASHBOARD_MILESTONE.md` | Dashboard milestone evidence |
| `docs/P2_DEMO_SCRIPT.md` | Recording walkthrough |
| `docs/ALL_THINGS_AGENTIC_HACKATHON.md` | Hackathon readiness and submission notes |

## Design principles

**Evidence before language** means no statement is stronger than its evidence. **Provenance before aggregation** means source identity, timestamps, and derivation inputs are retained. **Missing means missing** means unavailable information is disclosed rather than silently invented. **Human review before operational decision** means GroundPulse supports specialist review and does not replace engineering or mission authority.

## Limitations and honest scope

The verified demonstration is narrow: one ISS object, one approved CelesTrak GP snapshot, and one released evidence package. CelesTrak GP data provides orbital elements, not live spacecraft telemetry, spacecraft health, mission status, or operational recommendations. The public deployment is a read-only showcase of the verified run; anonymous research submission is intentionally disabled.

## Security

Do not commit Google credentials, service-account JSON, identity tokens, private bucket URLs, API keys, or local `.env` files. The private research service and private artifact bucket must remain protected. Public access is provided only through the restricted read-only facade.

## License

This repository is released under the MIT License. External source data remains subject to its own license, terms, attribution, and permitted-use boundaries.

## Hackathon

GroundPulse is prepared for the All Things Agentic Hackathon under the Taskmaster track. The public demo provides a verifiable visual experience backed by a deployed Google Cloud research pipeline, with explicit evidence, provenance, artifact, and human-review boundaries.
