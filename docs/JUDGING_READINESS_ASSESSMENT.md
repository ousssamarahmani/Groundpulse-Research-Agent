# Taskmaster Judging Readiness Assessment

**Event:** [All Things Agentic Hackathon](https://allthingsagentichackathon.devpost.com/)  
**Selected track:** Taskmaster  
**Assessment type:** Directional project-readiness review, **not** a prediction of judge scores.

## Current fit

GroundPulse has a strong Taskmaster narrative because it treats a research request as a durable, controlled workflow rather than as a chat interaction. Its differentiator is the evidence gate: the intended system must route a request through approved source work, validation, an explicit claim ledger, and a visible gap or human-review route. That is a meaningful operational workflow if it is implemented and demonstrated.

| Judging criterion | Current strength | Current limitation | Readiness assessment |
|---|---|---|---|
| **Innovation & Operational Utility — 40%** | The evidence-first research package and gap-aware routing solve a concrete research-operations problem. | The repository does not yet execute a real agent workflow or adapter action. | **Promising concept; proof required.** |
| **Architectural Discipline & Tech Stack — 30%** | The repository has a clear GCP target architecture, state model, source boundaries, task backlog, security guidance, and explicit non-claims. | Cloud services, credentials, durable state, failures, and tool policies are documented rather than deployed. | **Strong blueprint; runtime evidence required.** |
| **Demo & Production Readiness — 30%** | Product UI, dashboard, README, architecture diagram, and local spin-up instructions are present. | There is no live Google Cloud backend proof, no generated research package, and no unedited demo video. | **UI/repository ready; submission proof incomplete.** |

## Smallest credible Taskmaster proof-of-work

The winning move is not a broad multi-source system. It is one working, narrow loop that removes real research friction without asking a user to manually perform every step.

| Step | Demonstrable behavior | Evidence to show in the demo |
|---|---|---|
| **1. Trigger** | A structured research request creates a `run_id`. | Request in the UI and persisted run state. |
| **2. Autonomous routing** | The coordinator selects the permitted source/validation task from the request scope. | Worker log or event trace showing the route decision. |
| **3. Tool action** | The worker calls one approved source adapter or a documented public-data tool. | Source URL, retrieval timestamp, raw snapshot reference, and tool result. |
| **4. Evidence gate** | The system writes an accepted claim or a visible unavailable-data gap. | Claim Ledger with source state, or a human-review task. |
| **5. Package** | The system produces a small Research Evidence Package. | Downloadable JSON and/or PDF with run ID, source references, and limitations. |
| **6. Cloud proof** | The agent code executes on Google Cloud using required services. | Cloud Run or job details, logs, and an unedited end-to-end video. |

## Priority sequence

1. Build a narrow ADK- or other approved Google Agent Framework-based worker that uses Gemini 3.5+ and performs one approved tool call.
2. Deploy that worker to one real Google Cloud service, preferably Cloud Run for a small first deployment, and persist run state in Firestore or another chosen managed store.
3. Connect the existing Dashboard to real `run_id`, stage, ledger, and gap data. Preserve the current prototype content only as a clearly labelled fallback.
4. Produce a minimal JSON/PDF research package; do not wait for a feature-complete reporting system.
5. Record a short, unedited demo: UI request → background agent execution → Cloud Run/Google Cloud proof → returned evidence package and limitation.

## Submission boundary

The event requires Gemini 3.5 or newer, at least one Google Agent Framework, and at least one Google Cloud infrastructure service. [1] Until those parts are implemented and demonstrated, GroundPulse should be presented as a polished Taskmaster **prototype and implementation blueprint**, not as a fully compliant deployed hackathon submission.

## Reference

[1]: [All Things Agentic Hackathon — requirements, tracks, and submission checklist](https://allthingsagentichackathon.devpost.com/)
