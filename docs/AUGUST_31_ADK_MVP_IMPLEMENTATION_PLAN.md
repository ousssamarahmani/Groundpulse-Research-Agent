# GroundPulse: August 31 ADK MVP Implementation Plan

**Status:** Deadline-focused target plan. It is not evidence of a deployed agent, a live telemetry connection, or a completed cloud run.
**Planning window:** August 16–August 31, 2026.
**Track:** All Things Agentic Hackathon — **Taskmaster**.

> **MVP principle:** Build one narrow, inspectable research run with **Google ADK**, Gemini API, and Google AI Studio. The run must either return source-linked evidence with explicit gaps or fail visibly; it must never invent a telemetry value, freshness timestamp, or operational claim.

## 1. Locked framework path

GroundPulse will use **Google AI Studio** for prompt tests, API-key management, and early model experimentation, and the **Gemini API** for model calls. Google identifies AI Studio as a workspace for testing prompts, managing keys, monitoring usage, and prototyping; its Gemini API documentation recommends the Interactions API for the latest features. [1] [2]

**Google ADK is the sole primary agent framework for this MVP.** ADK is an open-source framework for building, evaluating, and deploying agents, with documented support for tools, structured workflows, Cloud Run deployment, and multi-agent composition. [3] [4] The first deadline run stays **single-agent plus deterministic validation**. A multi-agent team is a target expansion only after that baseline passes its evidence gates.

| Layer | August 31 choice | What must be proven | What must not be claimed before proof |
|---|---|---|---|
| Prompt and model experimentation | Google AI Studio + Gemini API | A versioned prompt/test set returns schema-conformant claim entries and gaps. | That the model independently verifies factual claims. |
| Agent implementation | Google ADK | A bounded ADK research coordinator can invoke approved tools and return the required structure. | An autonomous multi-agent fleet or unrestricted web research. |
| Run orchestration | ADK workflow plus deterministic validator | The agent hands a candidate ledger to a non-generative evidence gate. | That model output is automatically accepted as evidence. |
| Research API | Cloud Run | A deployed HTTPS endpoint creates a `run_id` and returns state. [5] | Continuous availability, an SLA, or a live stream. |
| Run state | Firestore | Run status, evidence links, and artifact links survive a request boundary. [6] | A raw source archive or analytical warehouse. |
| Telemetry UI | Mission Control | The UI displays only source-provided time/state fields after a verified run. | Live spacecraft or ground-station telemetry without an owned or contracted feed. |

## 2. Minimum credible demo

The demonstration should be deliberately small. A user submits one bounded research question; the API creates a `run_id`; one approved public-source adapter stores a source snapshot; the ADK coordinator receives only the approved context; the validator emits a claim ledger with source IDs or explicit gaps; and the system returns a JSON manifest plus a short research brief. Mission Control may display values only after the backend provides real timestamps and state.

Start with **one source type**. CelesTrak GP/OMM context is a reasonable first candidate if the team preserves the published epoch and retrieval time while respecting provider expectations. SatNOGS or NOAA SWPC should be added only after the first path works. [7] [8] [9]

| Required proof | Acceptance test | Evidence retained for the demo |
|---|---|---|
| Request creation | `POST /runs` returns a generated `run_id`. | API response and Firestore record. |
| Approved source snapshot | Adapter saves raw response, source URL, source timestamp where present, retrieval time, and hash. | Storage URI and manifest record. |
| ADK invocation | Coordinator receives only the bounded question and approved context. | Redacted ADK trace and structured result. |
| Evidence gate | Every output claim has source IDs, derivation inputs, or explicit `gap` status. | Claim ledger JSON. |
| Artifact package | Brief and manifest point to the same `run_id` and snapshot IDs. | Downloadable files and hashes. |
| Honest UI | Dashboard shows verified backend values or `Not connected`. | Recording of both states. |

## 3. Daily execution plan

Each day ends with a small artifact committed to GitHub or an explicit recorded blocker. Do not postpone testing until the last days.

| Date | Primary task | Concrete deliverable by end of day | Validation gate |
|---|---|---|---|
| **Aug 16** | Freeze one demo question and select **one** approved public source. Create GCP project, budget alert, and source-use note. | One-page scope and GitHub issue board. | Scope has decision intent, time window, source, and non-claims. |
| **Aug 17** | In Google AI Studio, create three extraction/claim-ledger prompt variants and a strict JSON schema. | Prompt fixtures, rubric, and schema in `evals/`. | Each response cites an input ID or emits a gap. |
| **Aug 18** | Create the Gemini API smoke test through the Interactions API. Load the key only from a server-side secret mechanism. | Server/CLI smoke test and redacted result. | A schema-valid response reproduces from a committed fixture. |
| **Aug 19** | Create the first **ADK research coordinator** with no external source access beyond a local fixture or approved function tool. | `research_coordinator` module and local run result. | The coordinator returns the schema and never creates unsourced claims. |
| **Aug 20** | Add deterministic claim validation: source IDs, provenance fields, derivation inputs, and gaps are checked outside the model. | Validator unit tests and rejection examples. | A claim without evidence is blocked. |
| **Aug 21** | Implement one source adapter and the immutable snapshot contract. | Adapter test and example manifest. | The same fixture replays with the same snapshot hash. |
| **Aug 22** | Create Firestore collections for `runs`, `evidence_refs`, and `artifacts`; read and write state through backend code. [6] | Schema note and integration test. | A `run_id` recovers its state and links after restart. |
| **Aug 23** | Implement Cloud Run `POST /runs` and `GET /runs/{id}` endpoints. Keep them private or authenticated where practical. [5] | Local container and Cloud Run deployment proof. | A request returns `run_id`; access behavior is documented. |
| **Aug 24** | Add Cloud Tasks or a bounded background worker for source retrieval and ADK execution. [10] | Queued run and idempotency note. | Retrying does not duplicate snapshots or claim IDs. |
| **Aug 25** | Connect the ADK coordinator to one approved stored snapshot and the deterministic validator. | Worker integration test. | Validator rejects a claim with no source ID or derivation record. |
| **Aug 26** | Generate the first research package: claim ledger JSON, manifest JSON, and minimal human-readable brief. | One package under one `run_id`. | Artifacts reference identical snapshot IDs and timestamps. |
| **Aug 27** | Replace one Mission Control illustrative panel with backend-backed state for the verified demo run only. | UI integration branch and recording. | UI shows backend freshness fields; no invented numerical telemetry. |
| **Aug 28** | Record the **multi-agent target design**: coordinator, source specialist, evidence validator, and artifact assembler. Implement it only if the single-agent path has passed all gates. | ADR and component contracts. | No public claim that multi-agent execution exists without a recorded run. |
| **Aug 29** | Add source allowlist, request limits, structured logs, error states, and cost caps. | Security/cost checklist and failure-path capture. | Failure produces `failed` or `gap`, never a fabricated result. |
| **Aug 30** | Perform and record the final dry run; finish the demo video, README/Devpost draft, secret review, and release candidate. | Unedited screen recording, run manifest, video draft, and release commit. | A second reviewer can inspect snapshot, state, ledger, and every public claim. |
| **Aug 31** | Confirm the event cutoff time, submit final links early, and retain the demo environment until submission confirmation. | Receipt/screenshot, final SHA, and release notes. | Do not claim submission success until the portal confirms it. |

## 4. Future ADK multi-agent target

The execution order and scope-control rule for this plan are maintained in the companion [August 31 Priority Board](AUGUST_31_PRIORITY_BOARD.md). P0 must be completed before the project begins multi-agent or streaming expansion.

ADK supports multi-agent and multi-node workflows, including deterministic graph workflows, collaborative coordinator patterns, and template sequence/parallel flows. [3] This capability should improve specialization—not add novelty without evidence. GroundPulse's target team is therefore deliberately small:

| Future ADK role | Responsibility | Non-negotiable boundary |
|---|---|---|
| **Research coordinator** | Owns the bounded question, selects the approved workflow path, and assembles the run. | Cannot accept a claim directly. |
| **Source specialist** | Calls an approved adapter and records source URL, timestamps, license, and snapshot hash. | Cannot infer a mission condition from incomplete context. |
| **Evidence validator** | Applies deterministic admission rules and classifies each entry as source-backed, derived, or gap. | Must block unsupported synthesis. |
| **Artifact assembler** | Creates the brief and JSON manifest from already accepted ledger entries. | Cannot introduce new factual content. |

The MVP should remain a coordinator plus deterministic validator until a full source-linked run is reproducible. If the multi-agent expansion is implemented after that point, use an ADK graph or controlled sequence so that the evidence validator remains a mandatory gate rather than an optional conversational handoff. [3] [4]

## 5. Stop conditions

Stop adding scope when a source adapter cannot retain provenance, the ADK coordinator cannot be constrained to source-linked output, Firestore/Cloud Run deployment is not reproducible, or the UI begins to imply live telemetry without a feed. In these cases, preserve the single-agent research package and surface a visible `gap` or `not connected` state.

## References

[1]: [Google AI Studio](https://aistudio.google.com)
[2]: [Gemini API documentation](https://ai.google.dev/gemini-api/docs)
[3]: [Google ADK workflows](https://adk.dev/workflows/)
[4]: [Google ADK overview](https://adk.dev/)
[5]: [Cloud Run documentation](https://docs.cloud.google.com/run/docs)
[6]: [Cloud Firestore documentation](https://firebase.google.com/docs/firestore)
[7]: [CelesTrak GP data formats and queries](https://celestrak.org/NORAD/documentation/gp-data-formats.php)
[8]: [SatNOGS Network API](https://docs.satnogs.org/projects/satnogs-network/en/latest/api.html)
[9]: [NOAA SWPC data access](https://www.spaceweather.gov/content/data-access)
[10]: [Cloud Run: executing asynchronous tasks](https://docs.cloud.google.com/run/docs/triggering/using-tasks)
