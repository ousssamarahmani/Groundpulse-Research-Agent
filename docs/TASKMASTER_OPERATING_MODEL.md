# Taskmaster Operating Model

## Purpose

This document turns the Taskmaster-track intent into an execution model for GroundPulse. The product is designed to coordinate evidence work after a defined trigger, not to perform unbounded autonomous activity. Each run must have a stable identity, an allowed tool set, an evidence state, and an explicit human-review boundary.

## The six operating stages

| Stage | Coordinator action | Required record | Release boundary |
|---|---|---|---|
| **1. Trigger** | Accept a structured user request or approved event. | `event_id`, `run_id`, source, timestamps, authorization state. | Reject unknown or unauthorized triggers. |
| **2. Normalize** | Convert the input into a constrained research scope. | Object/location, time window, decision intent, source policy. | Do not infer missing scope as fact. |
| **3. Route** | Select the next permitted discovery, validation, or analysis task. | Task ID, worker, allowed adapters, retry policy. | No route may call an unapproved tool or source. |
| **4. Collect** | Retrieve and preserve source snapshots. | Source URL/system ID, timestamps, terms, checksum, adapter version. | Raw data is not yet a released claim. |
| **5. Validate** | Evaluate source fitness and classify claims or gaps. | Claim ledger, derivation inputs, gap state. | Unsupported content cannot pass the evidence gate. |
| **6. Deliver or escalate** | Publish a package or create a human-review task. | PDF, JSON manifest, audit trail, or escalation record. | Consequential or unresolved results remain reviewable. |

## First demonstrable Taskmaster workflow

The first hackathon-grade workflow should be intentionally narrow:

1. A researcher submits one structured ground-segment or space-context question.
2. The coordinator creates `research_run` and routes a small, approved set of source-adapter tasks.
3. Adapters return immutable snapshots and structured metadata.
4. The evidence validator produces source-backed, derived, proposed, or unavailable states.
5. The system releases a Research Evidence Package only when required validation is complete; otherwise it creates a visible review task.

This workflow demonstrates autonomous routing without overstating autonomy. It is not a claim that GroundPulse currently performs the external retrieval or cloud execution shown in the target architecture.

## GCP service mapping

| Concern | Target service | Why it belongs in the workflow | Current repository state |
|---|---|---|---|
| Request and event ingress | Cloud Run | Receives authenticated HTTP requests or approved pushes. | Planned target. |
| Durable asynchronous task dispatch | Cloud Tasks | Separates a user request from slower agent and adapter work. | Planned target. |
| Approved event fan-out | Pub/Sub | Distributes validated events to permitted consumers. | Planned target. |
| Agent implementation | ADK on Cloud Run or Agent Platform Runtime | Supports code-first tool orchestration with managed deployment options. [1] [2] | Planned target. |
| Immutable snapshots and packages | Cloud Storage | Stores raw snapshots, manifests, PDF, and JSON artifacts. | Planned target. |
| Evidence or run state | Firestore or an equivalent operational state store | Holds run transitions and evidence metadata. | Planned target. |
| Streaming analysis when required | BigQuery and/or Dataflow | Supports freshness analytics and event-time processing after a justified need is established. [3] | Planned target. |

## Issue discipline

Use the `Taskmaster work item` issue template for every implementation issue. A work item is incomplete if it cannot answer: **What triggered it? What work may it route? What artifact proves the result? What makes it stop for human review?**

Recommended labels are `track:taskmaster`, `area:trigger`, `area:routing`, `area:adapter`, `area:evidence`, `area:artifact`, `area:gcp`, `risk:source-policy`, and `needs:human-review`.

## References

[1]: [Gemini Enterprise Agent Platform — Agents overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/agents)
[2]: [Google Cloud Run — Build and deploy an AI agent using ADK](https://docs.cloud.google.com/run/docs/ai/build-and-deploy-ai-agents/deploy-adk-agent)
[3]: [Google Cloud Blog — Building event-driven data agents with BigQuery, Pub/Sub, and ADK](https://cloud.google.com/blog/topics/developers-practitioners/building-event-driven-data-agents-with-bigquery-pubsub-and-adk)
