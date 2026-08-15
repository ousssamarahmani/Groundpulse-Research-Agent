# GroundPulse: September 1 MVP Implementation Plan

**Status:** Deadline-focused implementation plan, not evidence of a deployed agent, live telemetry connection, or completed cloud run.  
**Planning window:** August 16–September 1, 2026.  
**Track:** All Things Agentic Hackathon — **Taskmaster**.  
**Deadline handling:** This schedule uses the September 1 deadline supplied by the project owner. Confirm the Devpost submission timezone and closing hour directly in the event portal before the final upload.

> **MVP principle:** Build one narrow, inspectable research run rather than a broad dashboard simulation. The run must either produce source-linked evidence and explicit gaps, or fail visibly. It must never manufacture a telemetry value, freshness timestamp, or claim.

## 1. Deadline decision

GroundPulse should use **Google AI Studio** to prototype prompts and manage the Gemini API key, then call the **Gemini API** through the current Interactions API for production-shaped experiments. Google documents AI Studio as the place to test prompts, manage API keys, monitor usage, and build prototypes; it recommends the Interactions API for current Gemini API features. [1]

For this deadline, the project should conduct a **time-boxed Antigravity proof** rather than implement several agent frameworks in parallel. Managed Agents in the Gemini API expose an Antigravity-powered agent harness with a remote environment, instructions, tools, and persistent environments; the Antigravity SDK is also documented as a programmatic Python option with lifecycle hooks and safety policies. [2] [3] The existing ADK architecture documentation remains a valid alternative, but **do not build ADK and Antigravity simultaneously before September 1**. The team should keep the framework that completes a source-linked end-to-end run by the Day 4 decision gate.

| Layer | Deadline choice | What must be proven | What must not be claimed before proof |
|---|---|---|---|
| Prompt and model experimentation | Google AI Studio + Gemini API | A saved prompt/test set returns a schema-conformant draft with cited input IDs and gaps. | That the model independently verifies factual claims. |
| Agent runtime spike | Antigravity Managed Agent or Antigravity SDK | One controlled agent can execute the documented research instructions with restricted tools. | A production-grade autonomous fleet or unrestricted web access. |
| Research API | Cloud Run | A deployed HTTPS endpoint creates a `run_id` and returns a status record. [4] | Continuous availability, an SLA, or a live stream. |
| Run state | Firestore | The run state, evidence links, and artifact links survive a request boundary. [5] | Long-term source archive or analytical warehouse behavior. |
| Evidence archive | Cloud Storage | Raw source snapshot and generated package are retained by URI and hash. | That an artifact is authoritative without a validation gate. |
| Telemetry UI | Mission Control | The UI renders only source-provided timestamp, retrieval timestamp, freshness class, and validation state. | Live spacecraft or ground-station telemetry without an owned or contracted feed. |

## 2. Minimum credible demo

The end-to-end demonstration should be deliberately small. A user submits one bounded research question. The API creates a `run_id`; one approved public-source adapter retrieves and stores a source snapshot; the agent receives the approved context; the validator produces a claim ledger with source IDs or explicit gaps; and the system returns a JSON manifest plus a short research brief. The Mission Control interface may display the run only after the backend provides its real timestamps and state.

The proof should start with **one source type**. CelesTrak GP/OMM context is a reasonable first candidate if the team can honor the provider's published access expectations and preserve source epoch/retrieval time; SatNOGS or NOAA SWPC can be added only after the first path works. [6] [7] [8]

| Required proof | Acceptance test | Evidence to retain for the demo |
|---|---|---|
| Request creation | `POST /runs` returns a generated `run_id`. | API response and Firestore record. |
| Approved source snapshot | Adapter writes raw response, source URL, source timestamp where present, retrieval time, and hash. | Cloud Storage URI and manifest record. |
| Agent invocation | Antigravity or Gemini interaction receives only the bounded prompt plus approved source context. | Interaction ID/log with secret values redacted. |
| Evidence gate | Every output claim has source IDs, derivation inputs, or an explicit `gap` status. | Claim ledger JSON. |
| Artifact package | Brief and manifest point to the same `run_id` and source snapshot IDs. | Downloadable files plus their hashes. |
| Honest UI | Dashboard shows actual backend values for the demo run or remains labeled `Not connected`. | Screen recording of both states. |

## 3. Daily execution plan

Each day ends with a small artifact committed to GitHub or an explicit recorded blocker. Do not postpone testing until the last days.

| Date | Primary task | Concrete deliverable by end of day | Validation gate |
|---|---|---|---|
| **Aug 16** | Freeze the smallest demo question and select **one** approved public source. Create a GCP project, billing budget alert, and separate development environment. | One-page scope; source license/access note; GitHub issue board. | The scope has a decision intent, time window, expected source, and a statement of what GroundPulse cannot conclude. |
| **Aug 17** | In Google AI Studio, build three prompt variants for source-context extraction and claim-ledger JSON. Define the output schema. | Prompt test set, rubric, and JSON schema committed under `evals/`. | Each response either names source IDs/gaps or is rejected; no free-text “facts” are accepted. |
| **Aug 18** | Create the first Gemini API smoke test using the Interactions API. Load the key through a secret mechanism—not client code or Git. | CLI/server smoke test plus redacted result. | A schema-valid response is reproduced from the committed test fixture. |
| **Aug 19** | Build the Antigravity spike: use a single inline instruction or versioned `.agents/AGENTS.md` plus one source-policy skill. Keep tools allowlisted. [2] [3] | One successful Antigravity interaction and a short failure log. | **Decision gate:** continue only if the agent can run the test fixture with bounded tools and produce the required schema. |
| **Aug 20** | If the Antigravity spike passes, create a managed agent configuration or SDK wrapper. If it fails because access, preview availability, or tool controls block the MVP, switch immediately to the documented ADK fallback and record the decision. | Architecture decision record (ADR) with an actual invocation result. | One framework only is selected for the deadline path. |
| **Aug 21** | Implement the first source adapter and immutable snapshot contract. Store `source_url`, `source_event_at` when supplied, `retrieved_at`, payload hash, and freshness class. | Adapter test and example manifest. | The same source fixture replays without changing its snapshot hash. |
| **Aug 22** | Create Firestore collections for `runs`, `evidence_refs`, and `artifacts`; write and read a run state through the backend. [5] | Firestore schema note and integration test. | A `run_id` can recover its state and links after process restart. |
| **Aug 23** | Implement the Cloud Run Research API with `POST /runs` and `GET /runs/{id}`. Keep the service private or authenticated where possible. [4] | Local container and Cloud Run deployment proof. | A request returns a `run_id`; unauthenticated behavior is intentionally tested and documented. |
| **Aug 24** | Connect the API to Cloud Tasks or an equivalent bounded background worker so source retrieval and agent execution do not block the user request. [9] | Queued run with retry/idempotency note. | Re-running the same request does not create duplicate source snapshots or duplicate claim IDs. |
| **Aug 25** | Connect the selected agent runtime to the approved snapshot. Add system instructions that prohibit unsupported operational conclusions and require gaps. | Agent worker test against one stored snapshot. | Validator rejects a claim with no source ID or derivation record. |
| **Aug 26** | Generate the first research package: claim ledger JSON, manifest JSON, and a minimal human-readable brief. | One package under a single `run_id`. | Every artifact references identical snapshot IDs and timestamps. |
| **Aug 27** | Replace one Mission Control illustrative telemetry panel with backend-backed run state **only for the verified demo run**. Keep other panels marked illustrative. | UI integration branch and screen capture. | The UI labels freshness from backend fields; it does not show invented numerical telemetry. |
| **Aug 28** | Add guardrails: source allowlist, request size limits, secret review, structured logs, error state, and cost caps. | Short security/cost checklist and error-path capture. | A failed adapter or agent call produces a visible `failed`/`gap` state rather than fabricated output. |
| **Aug 29** | Perform a recorded dry run from fresh request to package. Capture cold-start and retry behavior. | Unedited local or Cloud Run screen recording; run manifest. | A second reviewer can inspect the source snapshot, state record, and ledger. |
| **Aug 30** | Produce the final demo video and update README, architecture, implementation status, and Devpost draft. | Video draft, screenshots, command list, and known-limitations section. | Every spoken claim maps to a visible proof or is reframed as a target. |
| **Aug 31** | Run regression tests, rotate/review keys if needed, record a clean final run, and create a release tag. | Final release candidate and reproducible setup note. | Another person can repeat the basic run using the documented environment variables. |
| **Sep 1** | Verify the event cutoff time, submit the final video/repository links, and preserve the demo environment until submission confirmation. | Submission receipt or screenshot, final commit SHA, and release notes. | Do not claim submission success until the event portal confirms it. |

## 4. Antigravity operating model for GroundPulse

The Antigravity proof should not start with a free-form autonomous researcher. Start with a single **Evidence Package Agent** that receives only: (1) the bounded question, (2) approved source records already saved by the adapter, (3) a strict JSON output schema, and (4) a small allowlist of tools. Google documents that a managed Antigravity agent can be customized at interaction time with system instructions, tools, and environment sources, then saved as a managed agent once the configuration is stable. [2]

| Agent input | Agent responsibility | Hard boundary |
|---|---|---|
| `question` | Restate scope and identify the requested decision context. | It cannot silently broaden the question. |
| `approved_evidence[]` | Extract only what the stored records support. | It cannot call unapproved sources or present memory as evidence. |
| `source_policy` | Apply source type, timestamp, license, and freshness rules. | It must write a gap when the record is missing or stale. |
| `artifact_schema` | Return claim ledger entries, citations, derivations, and gaps. | It cannot return a final operational recommendation without review. |

> **Implementation note:** Google’s current examples use the managed-agent identifier `antigravity-preview-05-2026`. Preview product availability, agent identifiers, limits, and pricing can change; validate the exact model/agent entry in Google AI Studio on the day of implementation rather than hard-coding a promise into public materials. [2]

## 5. Stop conditions and fallback rule

The deadline plan must protect the demo. Stop adding scope when any of the following occurs: a real source adapter does not provide retainable provenance, the agent cannot be constrained to source-linked output, Firestore/Cloud Run deployment is not reproducible, or the UI begins to imply live telemetry without a feed. In those cases, preserve the research package workflow and show a visible `gap` or `not connected` state.

If Antigravity cannot complete the Day 19–20 spike due to access or preview constraints, do **not** continue spending days on integration workarounds. Switch to the existing documented ADK path only after running a minimal local agent test and updating the architecture decision record. The submission should name the framework that actually produced the demo evidence—not every framework considered.

## References

[1]: [Gemini API documentation](https://ai.google.dev/gemini-api/docs)  
[2]: [Building Managed Agents with Gemini API](https://ai.google.dev/gemini-api/docs/custom-agents)  
[3]: [Google Antigravity documentation](https://antigravity.google/docs/home)  
[4]: [Cloud Run documentation](https://docs.cloud.google.com/run/docs)  
[5]: [Cloud Firestore documentation](https://firebase.google.com/docs/firestore)  
[6]: [CelesTrak GP data formats and queries](https://celestrak.org/NORAD/documentation/gp-data-formats.php)  
[7]: [SatNOGS Network API](https://docs.satnogs.org/projects/satnogs-network/en/latest/api.html)  
[8]: [NOAA SWPC data access](https://www.spaceweather.gov/content/data-access)  
[9]: [Cloud Run: executing asynchronous tasks](https://docs.cloud.google.com/run/docs/triggering/using-tasks)
