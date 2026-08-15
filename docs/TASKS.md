# Task Backlog

The tasks below are written as acceptance-oriented work items. They do not imply that a live dataset, telemetry feed, or cloud deployment already exists.

## Foundation

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-001 | Establish repository documentation and product boundaries. | Complete | README, architecture, limitations, implementation plan, and hackathon narrative agree on the prototype scope. |
| GP-002 | Maintain a self-contained product-interface prototype. | Complete | Local build and type check succeed; embedded preview is clearly marked as a prototype. |
| GP-003 | Define contribution and security expectations. | Complete | Contribution and security files are present and linked from README. |

## Evidence system

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-010 | Define `research_request` and `research_run` schemas. | Planned | Schema includes scope, source constraints, time window, user intent, and immutable run ID. |
| GP-011 | Define the source registry and adapter contract. | Planned | Each adapter has owner, provider terms reference, rate policy, source class, and fixture. |
| GP-012 | Implement immutable snapshot manifests. | Planned | Each snapshot stores source reference, timestamps, checksum, adapter version, and transformation lineage. |
| GP-013 | Implement the claim ledger. | Planned | Claims are classified as source-backed, derived, proposed, or unavailable. |
| GP-014 | Implement the evidence gate. | Planned | Package generation is blocked when required evidence or gaps are missing. |

## Product and package

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-020 | Replace local dashboard state with a typed API contract. | Planned | UI states map to a persisted run model and never imply live data before a connection exists. |
| GP-021 | Produce a Research Brief PDF and JSON manifest. | Planned | Artifact contains citations, claim ledger, gaps, run ID, and package checksum. |
| GP-022 | Add package access control. | Planned | Users can access only authorized runs and artifacts. |

## GCP and streaming

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-030 | Provision target services through infrastructure as code. | Planned | Environments are reproducible, service identities are separate, and no secret is committed. |
| GP-031 | Implement source-freshness analytics. | Planned | UI shows source event time, ingestion time, age, and stale state. |
| GP-032 | Add streaming deduplication and replay tests when a stream is required. | Planned | Replay does not duplicate analytical outputs or creates only idempotent writes. |
| GP-033 | Integrate a partner telemetry feed only after authorization. | Blocked | A written source contract and end-to-end test are approved. |

## Quality and governance

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-040 | Add schema, fixture, and negative-path tests. | Planned | Invalid snapshots and unsupported claims fail predictably. |
| GP-041 | Publish source limitations with every released package. | Planned | Package includes freshness, source terms, and gaps. |
| GP-042 | Run independent review of the first production package. | Planned | Reviewer can reproduce the source trail and identify all limitations. |
