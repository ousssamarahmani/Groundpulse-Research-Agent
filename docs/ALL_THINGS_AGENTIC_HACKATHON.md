# All Things Agentic Hackathon Readiness

**Event:** [All Things Agentic Hackathon](https://allthingsagentichackathon.devpost.com/)  
**Selected track:** **Taskmaster**  
**Project:** GroundPulse Research Agent

This document distinguishes what is present in the repository from what must be implemented before a final Devpost submission. It prevents the project from overstating prototype UI or architecture documentation as a deployed agent.

## Why GroundPulse is submitted as Taskmaster

The Taskmaster track asks for a complete workflow in which an agent takes action beyond a standard chat loop. [1] GroundPulse’s target loop is **structured request or approved event → permitted task routing → source discovery → evidence validation → reviewable package or human-review task**. The workflow, evidence gate, human-review boundary, diagram, and task contracts are documented in [Taskmaster Track Alignment](TASKMASTER_TRACK.md), [Taskmaster Operating Model](TASKMASTER_OPERATING_MODEL.md), and the [task backlog](TASKS.md).

## Readiness checklist

| Submission expectation | Repository evidence now | Remaining work before claiming compliance |
|---|---|---|
| Select one official track | **Taskmaster** is named in the README, submission document, metadata, and operating model. | Select Taskmaster in Devpost. |
| Show an autonomous, action-taking workflow | Event routing, evidence gates, acceptance criteria, and UI flows are documented; the UI is interactive local state. | Implement and demonstrate a real trigger, worker route, adapter action, and output package. |
| Use Gemini 3.5 or newer | No current runtime claim. | Integrate Gemini 3.5+ through Gemini API or Vertex AI and record the integration. |
| Use a Google Agent Framework | No current runtime claim. | Implement at least one approved framework, such as ADK, GenAI SDK, Antigravity SDK, or Genkit. |
| Use Google Cloud infrastructure | Target GCP architecture and integration plan are documented. | Deploy and demonstrate at least one Google Cloud service, such as Cloud Run, Pub/Sub, or Firestore. |
| Provide a code repository and architecture diagram | This repository, implementation plan, task system, GCP plan, and architecture diagram are present. | Keep the repository reproducible and align code with the deployment used in the demo. |
| Provide a demo video | UI/UX is externally accessible; no video is included. | Record a concise, unedited demonstration showing the backend running on Google Cloud and the end-to-end Taskmaster loop. |

## Recommended minimum compliant MVP

Implement one narrow task end-to-end: accept a structured research request, create a durable run, route one source-adapter action through an approved Google Agent Framework, validate the returned source metadata, create either a Claim Ledger entry or an explicit gap, and render the outcome in the Dashboard. Deploy the worker to one Google Cloud service and capture the deployed service or console evidence in the demo video. This is smaller, clearer, and more defensible than claiming real-time multi-source analytics before the core loop works.

## Reference

[1]: [All Things Agentic Hackathon — event requirements, tracks, and submissions](https://allthingsagentichackathon.devpost.com/)
