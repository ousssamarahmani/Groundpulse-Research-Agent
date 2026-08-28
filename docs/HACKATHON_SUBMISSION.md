# GroundPulse Research Agent — All Things Agentic Hackathon Submission

**Event:** [All Things Agentic Hackathon](https://allthingsagentichackathon.devpost.com/)
**Selected track:** **Taskmaster**
**Repository status:** The feature branch contains the GroundPulse UI, cloud-backed run API, Google ADK/Gemini worker path, durable run state, immutable artifact handling, Dashboard API integration, and regression coverage. A fresh Google Cloud deployment and recorded end-to-end run still require project authorization and must be demonstrated before submission.

## Event alignment

The event requires every submission to use Gemini 3.5 or newer, at least one Google Agent Framework, and at least one Google Cloud infrastructure service. The selected Taskmaster track additionally requires a complete action-taking workflow rather than a chatbot. [1] GroundPulse now implements the controlled trigger, route, validate, and package path in the feature branch; the remaining compliance proof is a fresh authorized cloud run and a recording that shows it.

## One-line summary

GroundPulse is an evidence-first research-agent prototype that turns a structured satellite or ground-segment question into a reviewable research package rather than an unsupported AI answer.

## Problem

Space-data research often begins across incompatible public catalogs, observation networks, environmental products, internal notes, and engineering assumptions. Teams must determine whether a source fits the question, whether its timestamps and metadata align, and whether a conclusion can be defended. This work is repetitive, difficult to audit, and easy to overstate when research is compressed into a chat-like answer.

## Solution

GroundPulse models research as a controlled workflow: **frame the request → discover sources → validate evidence → build a package**. The target package contains a human-readable research brief, a claim ledger, source snapshots or links, a reproducibility manifest, and a visible list of data gaps. The interface makes validation state and uncertainty part of the product rather than hiding them behind a summary.

## Taskmaster track fit

GroundPulse targets the **Taskmaster** pattern: an approved trigger starts a durable research run; the coordinator routes only permitted source, validation, and package tasks; the evidence gate releases a package or creates a visible human-review task. The full target model is documented in [Taskmaster Track Alignment](TASKMASTER_TRACK.md) and [Taskmaster Operating Model](TASKMASTER_OPERATING_MODEL.md).

> The feature branch implements the product interface, cloud-backed run path, Google ADK/Gemini worker integration, evidence validation, and Dashboard API. A live cloud deployment, partner telemetry, and broader source-adapter coverage remain separate proof or future-scope items.

## Current prototype

The feature branch contains the landing page, Mission Control dashboard, Research Journal, cloud-backed run API, and documentation. Mission Control reads typed run and artifact endpoints and displays mission stages, source review, evidence states, gaps, package status, and immutable artifact metadata. The approved ISS/CelesTrak path is implemented; private partner telemetry and a fresh deployed cloud run still require authorization and proof.

## Intended users and use case

The intended users are satellite operators, ground-station teams, research teams, and technical strategy teams. A representative use case begins with an object, location, time window, and research intent. GroundPulse collects only approved context, evaluates source fitness, and returns an evidence package for specialist review. The product is designed to reduce research operations effort; it does not replace engineering analysis or operational authority.

## Technical direction

The current service path uses a request API, durable job state, asynchronous agent work, approved-source handling, evidence validation, and immutable artifact metadata. The target GCP architecture uses Cloud Run, Cloud Tasks, Firestore, and Cloud Storage; the deployment handoff keeps IAM and secrets in Google Cloud Console. Source freshness remains distinct from private partner telemetry. See [Architecture](ARCHITECTURE.md), the [GCP integration plan](GCP_REALTIME_INTEGRATION_PLAN.md), and [Cloud Console Deployment](CLOUD_CONSOLE_DEPLOYMENT.md).

## Demo path

1. Start from the landing page and frame the structured research request.
2. Open `/dashboard` and show the real Run ID, stage state, validation state, evidence references, and package objects returned by the Research API.
3. Open the Journal to explain the claim-ledger and evidence-gate boundary.
4. Show Cloud Run/Cloud Tasks evidence and the released package, or use the local fallback path if cloud authorization is unavailable.
5. Read the limitations before interpreting any source or telemetry capability beyond what the run proves.

## What is deliberately not claimed

GroundPulse does not claim private live satellite telemetry, operational ground-station authority, empirical alert accuracy, or a broad released dataset. Partner telemetry remains blocked until authorization and schema review are complete. A production GCP deployment must be proven with the deployed revision and an end-to-end run; the Dashboard must not convert a local fallback record into a live operational claim.

## Reference

[1]: [All Things Agentic Hackathon — requirements and submission checklist](https://allthingsagentichackathon.devpost.com/)
