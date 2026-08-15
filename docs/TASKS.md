# Task Backlog

The backlog is acceptance-oriented. It does not imply that a live dataset, telemetry feed, external adapter, GCP deployment, or production agent already exists. Tasks marked **Complete** describe repository or local prototype work; tasks marked **Planned** or **Blocked** describe target implementation.

## Taskmaster conventions

Every task must state a **trigger**, **allowed routing/tools**, **output artifact**, **human-review boundary**, and **acceptance evidence**. Use the [Taskmaster issue template](../.github/ISSUE_TEMPLATE/taskmaster-work-item.md) when opening a GitHub issue.

| GitHub label | Use it for |
|---|---|
| `track:taskmaster` | Any event-driven coordination work item. |
| `area:trigger` | Request/event schemas and authorization intake. |
| `area:routing` | Queueing, worker selection, retry, and idempotency. |
| `area:adapter` | Approved external source adapters and policy controls. |
| `area:evidence` | Snapshots, claims, validation, and gaps. |
| `area:artifact` | PDF, JSON manifests, and release integrity. |
| `area:gcp` | Cloud infrastructure, identity, monitoring, and operations. |
| `needs:human-review` | A condition that cannot be released autonomously. |

## Foundation

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-001 | Establish repository documentation and product boundaries. | Complete | README, architecture, limitations, implementation plan, Taskmaster docs, and hackathon narrative agree on prototype scope. |
| GP-002 | Maintain a self-contained product-interface prototype. | Complete | Local build and type check succeed; dashboard values and preview are clearly marked as non-live. |
| GP-003 | Define contribution, security, and issue expectations. | Complete | Contribution and security files are present; Taskmaster issue template is available. |

## Taskmaster coordination and evidence system

| ID | Trigger and task | Status | Definition of done |
|---|---|---|---|
| GP-010 | **User request:** define `research_request` and `research_run` schemas. | Planned | Schema includes bounded scope, source constraints, time window, decision intent, authorization state, immutable run ID, and status transitions. |
| GP-011 | **Coordinator route:** define the source registry and adapter contract. | Planned | Each adapter has owner, provider terms reference, rate policy, source class, fixture, and allowed output schema. |
| GP-012 | **Adapter completion:** implement immutable snapshot manifests. | Planned | Each snapshot stores source reference, timestamps, checksum, adapter version, transformation lineage, and freshness class. |
| GP-013 | **Validation trigger:** implement the claim ledger. | Planned | Claims are classified as source-backed, derived, proposed, or unavailable, with linked evidence. |
| GP-014 | **Release trigger:** implement the evidence gate. | Planned | Package generation is blocked when required evidence is absent, stale, unsupported, or requires review. |
| GP-015 | **Approved event:** define `source_freshness` and `partner_event` contracts. | Planned | Every event has stable ID, source event time, ingestion time, source policy, run reference, and idempotency behavior. |
| GP-016 | **Route decision:** implement deterministic worker routing. | Planned | Router records why a task selected a worker, source adapter, retry policy, or review path. |
| GP-017 | **Validation failure:** implement visible human-review tasks. | Planned | Unsupported or consequential items create a reviewable task rather than a hidden fallback. |
| GP-018 | **Audit requirement:** persist run and routing audit records. | Planned | A reviewer can reconstruct trigger, route, tool outputs, validator decision, and final artifact. |

## Product and package

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-020 | Replace local dashboard state with a typed API contract. | Planned | UI states map to persisted runs and never imply live data before a connection exists. |
| GP-021 | Produce a Research Brief PDF and JSON manifest. | Planned | Artifact contains citations, claim ledger, gaps, run ID, package checksum, and source references. |
| GP-022 | Add package access control. | Planned | Users can access only authorized runs and artifacts. |
| GP-023 | Add an explicit package release view. | Planned | UI shows why a package is released, held, or routed to review. |

## GCP and streaming target

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-030 | Provision target services through infrastructure as code. | Planned | Environments are reproducible, service identities are separate, and no secret is committed. |
| GP-031 | Implement source-freshness analytics. | Planned | UI shows source event time, ingestion time, age, and stale state. |
| GP-032 | Add streaming deduplication and replay tests when a stream is required. | Planned | Replay does not duplicate analytical outputs, or writes are proven idempotent. |
| GP-033 | Integrate a partner telemetry feed only after authorization. | Blocked | A written source contract and end-to-end test are approved. |
| GP-034 | Add Cloud Run, Cloud Tasks, and Pub/Sub task orchestration. | Planned | Trigger, route, worker invocation, retry, and audit event are observable without exposing secrets. |
| GP-035 | Add observability and budget safeguards. | Planned | Lag, worker failure, package failure, request volume, and cost alerts have a documented runbook. |

## Quality and governance

| ID | Task | Status | Definition of done |
|---|---|---|---|
| GP-040 | Add schema, fixture, and negative-path tests. | Planned | Invalid snapshots, invalid events, and unsupported claims fail predictably. |
| GP-041 | Publish source limitations with every released package. | Planned | Package includes freshness, source terms, transformation notes, and gaps. |
| GP-042 | Run independent review of the first production package. | Planned | Reviewer can reproduce the source trail and identify every limitation. |
| GP-043 | Define a policy test for every allowed tool route. | Planned | A failing authorization, source policy, or human-review condition is observable and blocks release. |

## Suggested GitHub Project columns

Use a GitHub Project with these columns: **Backlog**, **Trigger defined**, **In implementation**, **Evidence/test review**, **Human review**, **Released**, and **Blocked**. A task moves to **Released** only when its definition of done is satisfied and no prototype or operational claim is left ambiguous.
