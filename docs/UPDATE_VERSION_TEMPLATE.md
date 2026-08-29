# GroundPulse Update-Version Template

This template records the next implementation layer after the hackathon prototype. It is intentionally scoped to the evidence-first research workflow and keeps every claim tied to a source, timestamp, and run identifier.

## Prioritized workstreams

| Priority | Workstream | Outcome | Hackathon relevance |
|---|---|---|---|
| P0 | Cloud-backed research execution | Replace the demo replay with an asynchronous Google ADK / Gemini run coordinated by Cloud Run, Cloud Tasks, and Firestore. | Demonstrates autonomous, action-taking behavior. |
| P0 | Evidence and provenance | Persist raw source payloads, retrieval time, published epoch, validation decisions, and authoritative Run ID. | Makes the four-minute demo auditable. |
| P1 | Source adapters | Add SatNOGS and NOAA SWPC only after the CelesTrak path is stable, with one adapter contract and explicit source health states. | Expands the visible research surface without hiding gaps. |
| P1 | Operator experience | Add run status, retry, evidence assignment, and package release controls with accessible loading and error states. | Makes the workflow understandable to judges and operators. |
| P2 | Submission and customer proof | Maintain the hosted URL, demo script, architecture diagram, and a small set of reproducible evaluation scenarios. | Supports judging and future customer discovery. |

## Acceptance criteria

| Area | Acceptance criteria |
|---|---|
| Backend | A research request creates a stable Run ID; asynchronous workers update Firestore state; retries are bounded and observable; provider failures return an explicit gap rather than fabricated data. |
| Frontend | Workspace renders loading, live, error, and fallback states; live records show source name, object identifier, published epoch, retrieval time, and derived-value labels; keyboard navigation and visible focus states remain intact. |
| Evidence | Every accepted claim links to a source record and validation decision; raw payload and normalized fields are distinguishable; unsupported fields remain visible as gaps. |
| Deployment | Production build passes; hosted URL serves the same routes as the local preview; required environment variables are documented without exposing values; logs identify failed external calls and Run IDs. |
| Customer proof | A reviewer can start or replay a research scenario, inspect its evidence trail, and understand what the agent did, what it derived, and what it could not establish without requiring internal credentials. |

## Recommended build order

1. Stabilize the CelesTrak adapter and verify the deployed network path.
2. Add Firestore run-state persistence and Cloud Tasks orchestration.
3. Connect the Google ADK / Gemini worker to the persisted run contract.
4. Replace the replay-only status surface with live asynchronous run updates while retaining an honest fallback.
5. Add evidence-package export and a judge-facing reproducibility scenario.
6. Add secondary source adapters only after the first source passes the complete acceptance table.

## Current boundary

The current hackathon checkpoint implements the P0 browser-safe CelesTrak path and its explicit fallback. The local sandbox cannot establish Node outbound TLS to CelesTrak even though direct command-line retrieval succeeds; this limitation is recorded rather than represented as live evidence. End-to-end live-network verification must be confirmed in the deployed runtime.
