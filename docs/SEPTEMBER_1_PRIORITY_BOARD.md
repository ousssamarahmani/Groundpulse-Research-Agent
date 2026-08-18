# GroundPulse: September 1 Priority Board

**Status:** Deadline-focused delivery board. This is a plan, not evidence that any cloud service, ADK agent, multi-agent team, or telemetry source is currently deployed.  
**Primary objective:** Prove one narrow, source-linked **Google ADK** research run before September 1.

> **Scope-control rule:** Do not spend implementation time on additional dashboard styling, additional public sources, multi-agent orchestration, Dataflow, BigQuery, or partner telemetry until the P0 evidence path has completed one reproducible run.

## P0 — Required proof of the core idea

P0 tasks establish the smallest credible Taskmaster demonstration. All P0 work must be complete before the team describes GroundPulse as an implemented agent workflow.

| ID | Priority task | Why it is critical | Definition of done |
|---|---|---|---|
| **P0.1** | Freeze one demo question and one approved source | Limits the MVP to a testable research problem. | A committed scope includes decision intent, object/location, time window, source policy, and explicit non-claims. |
| **P0.2** | Create Google AI Studio prompt fixtures and JSON schema | Makes model behavior repeatable rather than prompt-only. | Test input and expected `claim`, `source_id`, `derivation`, and `gap` fields are versioned under `evals/`. |
| **P0.3** | Create Gemini API smoke test | Proves model access before backend complexity is introduced. | Server-side request returns a schema-valid result from a committed fixture; no key appears in Git or client code. |
| **P0.4** | Build one Google ADK research coordinator | Supplies the selected Google agent-framework evidence. | A local coordinator processes a bounded fixture using only approved function tools/context and returns the required schema. |
| **P0.5** | Add deterministic evidence validator | Protects the core evidence-first innovation. | A claim without a source ID, named derivation inputs, or a `gap` state is rejected. |
| **P0.6** | Implement one source adapter and immutable snapshot | Replaces illustrative records with a traceable evidence input. | Raw response, source URL, timestamps, content hash, and freshness class are retained under one `run_id`. |

## P1 — Complete a cloud-backed research run

P1 turns the validated core into a Google Cloud-backed Taskmaster path. It begins only when P0.1–P0.6 have passed locally.

| ID | Priority task | Why it follows P0 | Definition of done |
|---|---|---|---|
| **P1.1** | Add Firestore run state | Makes the run and evidence links recoverable. | `runs`, `evidence_refs`, and `artifacts` records can be read after a service restart. |
| **P1.2** | Deploy the Research API on Cloud Run | Provides demonstrable Google Cloud infrastructure. | Authenticated or intentionally scoped `POST /runs` and `GET /runs/{id}` endpoints create/read a `run_id`. |
| **P1.3** | Queue the background research path | Keeps adapter and ADK work outside the request-response path. | Retry behavior is idempotent: it does not duplicate source snapshots or claim IDs. |
| **P1.4** | Connect ADK → validator → artifact package | Produces the Taskmaster outcome, not only a model response. | One request generates a claim ledger, gap list, JSON manifest, and minimal readable brief. |
| **P1.5** | Bind one verified run to Mission Control | Proves that the dashboard can display an actual run without false telemetry. | UI shows backend `run_id`, source/retrieval times, freshness class, and validation state; unconnected panels stay labeled illustrative. |

## P2 — Submission evidence and release readiness

P2 converts a working path into a clear, honest hackathon submission.

| ID | Priority task | Definition of done |
|---|---|---|
| **P2.1** | Record an unedited end-to-end demo | Video shows request, approved source snapshot, ADK execution, validation/gap result, artifact package, and Google Cloud evidence. |
| **P2.2** | Update README, architecture, and Devpost draft | Every claim maps to a visible proof; target design and implementation status remain separate. |
| **P2.3** | Complete error-path and security review | Failed adapter/agent calls produce a visible `failed` or `gap` state; secret handling and access scope are documented. |
| **P2.4** | Create release candidate | Final commit SHA, reproducible setup steps, limitation notes, and submission links are ready before the deadline. |

## P3 — Post-core expansion

P3 items are valuable only after the P0–P2 workflow is recorded successfully. They must not delay the first credible demo.

| ID | Future expansion | Entry condition |
|---|---|---|
| **P3.1** | ADK multi-agent team: coordinator, source specialist, evidence validator, and artifact assembler | The single-agent coordinator and deterministic validator have produced a reproducible source-linked run. |
| **P3.2** | Additional approved public sources | The first source adapter has stable provenance, freshness, and replay behavior. |
| **P3.3** | Pub/Sub, BigQuery, and Dataflow analytics | The product has a demonstrated need for event windows, deduplication, joins, or historical analysis. |
| **P3.4** | Partner telemetry ingestion | An owned/contracted feed has an explicit authentication, schema, ownership, and retention contract. |

## First five tasks to execute

1. Select one demo question and one approved public source.
2. Create the Google AI Studio prompt fixture and claim-ledger schema.
3. Implement the Google ADK coordinator locally against a saved source fixture.
4. Write the deterministic validator that blocks unsupported claims.
5. Implement the first real source adapter and snapshot manifest.

## Completion gate

GroundPulse may move from P0 to P1 only when a reviewer can inspect one source snapshot, reproduce the ADK result from its bounded input, and see each proposed conclusion classified as **source-backed**, **derived**, or **gap**. A polished dashboard without that chain is not completion.
