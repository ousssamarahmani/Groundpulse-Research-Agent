# Implementation Plan

## Delivery philosophy

The implementation should progress from a transparent prototype into a verifiable research system. Every phase must preserve the distinction between UI demonstration, source-backed evidence, derived analysis, and unavailable data. A phase is complete only when its acceptance criteria are met, not when the interface appears complete.

| Phase | Scope | Acceptance criteria |
|---|---|---|
| **P0 — Repository foundation** | Product interface, README, design captures, implementation plan, limitations, and contribution rules. | All prototype values are clearly labeled; no live-data or operational claims are made. |
| **P1 — Request and job model** | Structured research request, run identifier, durable status model, and immutable artifact metadata. | A request can move through explicit states without data being represented as verified before a validator accepts it. |
| **P2 — Source adapter controls** | Adapter contracts, source register, terms review, retrieval logging, retry policy, and snapshot manifests. | Every accepted source record retains URL/system ID, retrieval time, source time when available, terms, checksum, and adapter version. |
| **P3 — Evidence gate** | Claim ledger, source-fitness checks, derivation rules, and visible gap list. | A report cannot release a source-backed claim without a linked accepted record or a documented derivation. |
| **P4 — Evidence package** | PDF research brief, JSON manifest, citations, and artifact storage. | Generated package has a stable run ID, manifest, source links, gaps, and reproducible build metadata. |
| **P5 — Streaming analytics** | Source freshness, event contract, ingestion pipeline, and time-series analysis. | Each event exposes source time, ingestion time, freshness class, and validation state. |
| **P6 — Partner telemetry** | Authorized event feed, authentication, schema agreement, and end-to-end test harness. | No customer or partner feed enters production without written ownership, schema, retention, and authorization controls. |

## Workstream design

The **product workstream** owns request intake, dashboard state, package access, and user messaging. The **evidence workstream** owns source registration, snapshots, manifests, claim state, and report release gates. The **platform workstream** owns deployment, service identity, queues, artifacts, observability, and cost controls. The **verification workstream** owns fixtures, tests, replay checks, source-policy review, and acceptance evidence.

## MVP definition

The MVP should not aim to integrate every public data source or imitate a full mission-control product. A credible MVP handles one narrow research question class, two or three approved source adapters, one evidence gate, one package format, and a demonstrable end-to-end path. The primary success condition is that a reviewer can see why every released claim exists, not that the dashboard displays the largest number of widgets.

## Release gates

| Gate | Required evidence | Release decision |
|---|---|---|
| **Source approval** | Provider terms, usage boundary, attribution, test fixture, adapter owner. | Adapter can enter controlled retrieval. |
| **Snapshot acceptance** | Source ID, retrieval timestamp, source timestamp, checksum, schema validation. | Record can be considered by the evidence gate. |
| **Claim acceptance** | Accepted source links or reproducible derivation inputs. | Claim may enter a research brief. |
| **Package release** | Manifest, gap list, citations, rendered PDF, integrity checks. | Package may be shown to a user. |
| **Production telemetry** | Ownership, consent, authentication, retention, alerting, and end-to-end test. | Feed may receive an operational freshness label. |
