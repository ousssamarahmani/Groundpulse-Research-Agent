# Implementation Plan

## Delivery philosophy

GroundPulse should progress from a transparent interface prototype into a verifiable, event-driven research system. Every phase must preserve the distinction between local UI state, source-backed evidence, derived analysis, unavailable data, and proposed work. A phase is complete only when its acceptance criteria and non-claim boundary are satisfied—not when the interface merely appears complete.

## Taskmaster delivery path

The Taskmaster path is **trigger → normalize → route → collect → validate → deliver or escalate**. The implementation sequence starts with a narrow user-triggered workflow because it creates a deterministic foundation before external events and streaming data are introduced.

| Phase | Scope | Taskmaster capability | Representative task IDs | Acceptance criteria |
|---|---|---|---|---|
| **P0 — Repository foundation** | Interface, documentation, preview images, limitations, contribution rules, CI. | Makes scope, architecture, and human boundaries inspectable. | `GP-001`–`GP-003` | Prototype values are visibly labeled; no live-data or operational claims are made. |
| **P1 — Request and run model** | Structured request, immutable run ID, event contract, durable status transitions. | Receives and normalizes a bounded trigger. | `GP-010`, `GP-015` | A request moves through explicit states; missing scope is rejected or marked for review. |
| **P2 — Source adapter controls** | Adapter registry, terms review, retry policy, retrieval log, snapshot manifest. | Routes work only to allowed source tools. | `GP-011`, `GP-012`, `GP-016` | Each accepted record retains source reference, timestamps, terms, checksum, and adapter version. |
| **P3 — Evidence gate** | Claim ledger, fitness checks, derivation rules, visible gaps, review queue. | Validates output before it can be released. | `GP-013`, `GP-014`, `GP-017` | Unsupported claims cannot enter a release; unresolved items become review tasks. |
| **P4 — Evidence package** | PDF brief, JSON manifest, citations, artifact storage, access control. | Delivers a reviewable end-to-end artifact. | `GP-020`–`GP-022` | Package has run ID, manifest, source links, gaps, checksum, and permission boundary. |
| **P5 — GCP event routing** | IaC, Cloud Run, Cloud Tasks, Pub/Sub, source freshness, observability. | Receives approved events and routes durable background tasks. | `GP-030`, `GP-031`, `GP-034` | Each route is authenticated, logged, replayable, and exposes freshness. |
| **P6 — Streaming and partner telemetry** | Streaming deduplication, authorized feed contract, end-to-end test. | Handles approved ongoing events without inventing telemetry. | `GP-032`, `GP-033` | No feed enters production without ownership, schema, retention, authorization, and test evidence. |

## Workstream ownership

| Workstream | Accountable scope | Required artifact |
|---|---|---|
| **Product** | Request intake, dashboard status, artifact access, and clear user language. | Typed API contract and UI state map. |
| **Coordinator** | Trigger classification, allowed routing, retry behavior, and task audit trail. | Event contract and routing policy. |
| **Evidence** | Source registry, snapshots, manifest, claim state, evidence gate, and gaps. | Source-policy record and claim ledger. |
| **Platform** | Deployment, identity, queues, storage, observability, and cost controls. | Infrastructure-as-code and runbook. |
| **Verification** | Fixtures, negative paths, replay checks, source-policy review, and acceptance evidence. | Test suite and release checklist. |

## MVP definition

The MVP should not imitate a full mission-control product or integrate every public data source. A credible first release handles **one narrow research-question class**, **two or three approved adapters**, **one durable research-run model**, **one evidence gate**, **one human-review path**, and **one evidence-package format**. The primary success condition is that a reviewer can identify why each released claim exists and why each gap remains visible.

## Release gates

| Gate | Required evidence | Release decision |
|---|---|---|
| **Trigger acceptance** | Event or request schema, authorization state, stable run ID, bounded scope. | Coordinator may create work items. |
| **Source approval** | Provider terms, usage boundary, attribution, test fixture, adapter owner. | Adapter may enter controlled retrieval. |
| **Snapshot acceptance** | Source ID, retrieval timestamp, source timestamp when available, checksum, schema validation. | Record may be evaluated by the evidence gate. |
| **Claim acceptance** | Accepted source links or reproducible derivation inputs. | Claim may enter a Research Brief. |
| **Package release** | Manifest, gap list, citations, rendered PDF, integrity checks, authorization check. | Package may be exposed to the user. |
| **Production telemetry** | Ownership, consent, authentication, retention, monitoring, and end-to-end test. | Feed may receive an operational freshness label. |

For a detailed operating model, see [Taskmaster Operating Model](TASKMASTER_OPERATING_MODEL.md). For the target cloud architecture, see [GCP Real-Time Integration Plan](GCP_REALTIME_INTEGRATION_PLAN.md).
