# All Things Agentic Hackathon Readiness

**Event:** [All Things Agentic Hackathon](https://allthingsagentichackathon.devpost.com/)  
**Selected track:** **Taskmaster**  
**Project:** GroundPulse Research Agent

This document distinguishes what is implemented in the feature branch from what still must be proven in an authorized Google Cloud environment before the final Devpost submission. It prevents the project from overstating repository code as a deployed production service.

## Why GroundPulse is submitted as Taskmaster

The Taskmaster track asks for a complete workflow in which an agent takes action beyond a standard chat loop. [1] GroundPulse’s target loop is **structured request or approved event → permitted task routing → source discovery → evidence validation → reviewable package or human-review task**. The workflow, evidence gate, human-review boundary, diagram, and task contracts are documented in [Taskmaster Track Alignment](TASKMASTER_TRACK.md), [Taskmaster Operating Model](TASKMASTER_OPERATING_MODEL.md), and the [task backlog](TASKS.md).

## Readiness checklist

| Submission expectation | Repository evidence now | Remaining work before claiming compliance |
|---|---|---|
| Select one official track | **Taskmaster** is named in the README, submission document, metadata, and operating model. | Select Taskmaster in Devpost. |
| Show an autonomous, action-taking workflow | The feature branch implements the request, durable run, worker, approved-source, validation, and package path. | Execute one fresh authorized run and record the full loop. |
| Use Gemini 3.5 or newer | The worker integrates the Gemini API and records the selected model path. | Verify the deployed model version in the cloud run evidence and video. |
| Use a Google Agent Framework | The worker path uses the Google ADK integration. | Show the ADK/Gemini execution in a verified cloud-backed run. |
| Use Google Cloud infrastructure | Cloud Run, Cloud Tasks, Firestore, and Cloud Storage deployment configuration and Console instructions are present. | Deploy from Cloud Console and capture service, task, and artifact evidence. |
| Provide a code repository and architecture diagram | The repository, synchronized feature branch, implementation plan, task system, GCP plan, architecture diagram, and deployment guide are present. | Confirm the README and diagram match the exact deployed commit. |
| Provide a demo video | UI/UX is externally accessible; no video is included. | Record a concise, unedited demonstration showing the backend running on Google Cloud and the end-to-end Taskmaster loop. |

## Recommended minimum compliant MVP

The recommended minimum compliant MVP is implemented in the feature branch for the approved ISS/CelesTrak path: accept a structured request, create a durable Run ID, route background work, call the approved Gemini/ADK path, validate source metadata, create a Claim Ledger entry or explicit gap, and render the result in Mission Control. Remaining work is operational proof: deploy the container, deliver one Cloud Task, capture the cloud-backed result, and record the evidence in the demo video. This is smaller and more defensible than claiming broad real-time telemetry.

## Reference

[1]: [All Things Agentic Hackathon — event requirements, tracks, and submissions](https://allthingsagentichackathon.devpost.com/)
