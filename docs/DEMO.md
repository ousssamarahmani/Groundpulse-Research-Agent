# Demo Guide

## Purpose

This guide demonstrates the current GroundPulse Taskmaster workflow honestly. The preferred path is the verified cloud-backed run. The local path remains available for UI review when Google Cloud authorization or service access is unavailable.

## Preferred cloud-backed demo

Use the synchronized `feat/p1-cloud-backed-run` branch and the deployed Research API. Confirm that the frontend build variable `VITE_GROUNDPULSE_API_URL` points to the authorized API origin. Do not place API keys, service-account files, or private bucket URLs in the frontend.

| Step | Screen or action | What to show |
|---|---|---|
| 1 | Landing page | The problem: coordinating source discovery, validation, and package creation is repetitive and error-prone |
| 2 | Mission Control | A real Run ID, current status, validation state, and stage timeline |
| 3 | Evidence tab | Approved source snapshots, claim classifications, evidence references, and explicit gaps |
| 4 | Package tab | Immutable artifact metadata and the package manifest |
| 5 | Google Cloud Console | Cloud Run revision, Cloud Tasks delivery, or relevant service logs proving the backend path |
| 6 | Final result | The released package and the limitation that human specialists retain operational authority |

The preferred demonstration run is the approved ISS/CelesTrak path documented in `docs/P2_DASHBOARD_MILESTONE.md`. Use the exact Run ID shown by the API at demo time rather than hard-coding a stale value.

## Local development path

Start the frontend from the repository root:

```bash
pnpm install
pnpm dev
```

To run the local API in a second terminal:

```bash
cd agent
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn groundpulse_agent.api:app --host 127.0.0.1 --port 8000
```

Set `VITE_GROUNDPULSE_API_URL=http://127.0.0.1:8000` before starting the frontend when testing the local API. The local API can use the repository’s local persistence and storage fallbacks. Cloud-only features require the corresponding Google Cloud services and credentials.

## What the agent proves

The demo should make the asynchronous behavior visible: a bounded request creates a stable Run ID, background work is dispatched, approved evidence is preserved, the validator decides what can be released, and the final artifacts remain inspectable. The model call is one part of this workflow; it is not presented as an opaque answer generator.

## Failure-path moment

Show one unavailable telemetry or calibration field as a visible `gap`. Explain that GroundPulse does not turn missing evidence into a confident operational claim. This is a core product behavior, not an error to hide.

## Demonstration boundary

The cloud-backed path demonstrates a controlled research workflow using the approved CelesTrak fixture and the documented services. Do not claim that the fixture contains private RF metrics, modem health, station incidents, live telemetry, or spacecraft readiness unless an authorized source actually provides those measurements. Do not present future partner adapters, independent review, or broader autonomous spacecraft operations as complete.

## Hackathon recording checklist

Before recording, verify the current commit, API base URL, Run ID, service revision, and package artifacts. Record a screen that includes Gemini/ADK usage and a Google Cloud proof point. The video should stay near four minutes and end on the released package, its evidence trail, and its limitations.
