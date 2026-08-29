# All Things Agentic Hackathon — GroundPulse Submission Template

**Project branch:** `feat/p1-cloud-backed-run`  
**Recommended category:** **The Taskmaster**  
**Secondary possibility:** The Fortified Enterprise Fleet, only if the enterprise agent registry, identity, policy enforcement, and observability requirements are demonstrably implemented.  
**Submission deadline shown on Devpost:** August 31, 2026 at 5:00 PM PDT.[1]

## 1. Recommended hackathon positioning

> **GroundPulse is an evidence-first research agent for satellite and ground-segment operations. It takes a mission question, runs an asynchronous source-and-validation workflow, and produces an evidence-linked research package while keeping missing data visible.**

The Taskmaster track is the cleanest fit because GroundPulse is a complete asynchronous workflow rather than a chatbot: it frames a request, dispatches background work, retrieves approved source data, validates claims, generates artifacts, and exposes the result through Mission Control. The demo should prove that the agent **does work after the initial request**, not merely generate a response.

Do not submit the project as a generic “autonomous space operations platform.” For this hackathon, the strongest story is one concrete workflow: **a satellite research question becomes a validated, source-linked package without the operator manually coordinating each step**.

## 2. Hackathon requirement mapping

| Devpost requirement | GroundPulse evidence | Status before submission |
|---|---|---|
| Gemini 3.5 or newer through Gemini API or Vertex AI | Branch documents `gemini-3.5-flash-lite` in the ADK research coordinator | Confirm the deployed model and capture it in the video |
| Google Agent Framework | Google ADK workflow in `agent/groundpulse_agent/` | Implemented; show the ADK path in the README and demo |
| Google Cloud infrastructure | Cloud Run, Cloud Tasks, Firestore, Cloud Storage, Secret Manager | Implemented for the controlled path; show Cloud Run and authenticated task flow |
| Complete asynchronous workflow | Request → dispatch → worker → validation → package | Implemented and tested; demonstrate one real run |
| Hosted project URL | GroundPulse managed domain or deployed frontend URL | Confirm the URL is accessible and does not expose secrets |
| Public or private repository | GitHub feature branch | Ready; provide exact branch and access instructions |
| Architecture diagram | `assets/diagrams/groundpulse-gcp-integration-architecture.png` and related Mermaid/D2 source | Ready; verify it matches the deployed implementation |
| Approximately four-minute demo video | Not complete until recorded | Required |
| Proof backend runs on Google Cloud | Cloud Run revision, logs, authenticated task delivery, or deployed service URL | Required in the video |
| Short written description | Template below | Ready to adapt |

The Devpost page states that every project must use Gemini 3.5 or newer, at least one Google Agent Framework, and at least one Google Cloud infrastructure service. It also requires a demo video, code repository, architecture diagram, and written project description.[1]

## 3. Current branch status

The branch currently has a strong controlled-demo foundation. Its documentation reports a verified ISS/CelesTrak run with a released status, passed validation, a stable Run ID, an approved snapshot, and ten immutable package objects. The branch also includes the live Dashboard API path for run history and artifact metadata, a private Cloud Storage boundary, Cloud Tasks dispatch, Cloud Run worker execution, Firestore persistence, and legacy-record handling.

The local audit completed on August 28, 2026 with Python compilation passing, **21 backend tests passing**, TypeScript validation passing, and a production build passing. The branch is 14 commits ahead of `main` and 2 commits behind it, so synchronize or explicitly freeze the branch before submission.

The following items are not necessary to expand into a full commercial platform for this hackathon submission: broad partner telemetry, every planned source adapter, multi-agent orchestration, a full enterprise agent registry, and production-grade observability across every future workflow. They must instead be described honestly as future work if they are not part of the demonstrated path.

## 4. Remaining hackathon-only work

| Priority | Task | Definition of done |
|---:|---|---|
| P0 | Freeze the submission commit | One branch/commit is named in Devpost; working tree is clean; no secrets or runtime artifacts are committed |
| P0 | Re-run the complete demo path | A fresh Run ID completes from request through released package without manual database edits |
| P0 | Verify the public/hosted frontend | Judges can open Mission Control or a hosted landing page and see the intended route without local-only assumptions |
| P0 | Record the four-minute demo | Video shows problem, value, live agent workflow, GCP proof, and final package |
| P0 | Validate repository instructions | A clean machine can follow README setup instructions; local mode and cloud mode are clearly separated |
| P1 | Match diagram to reality | Every service drawn in the architecture diagram exists in code or is labeled planned |
| P1 | Prepare screenshots and URLs | Include the hosted URL, repository URL, architecture diagram, and relevant Cloud Run/API proof |
| P1 | Write the Devpost entry | Category, description, technologies, data sources, findings, limitations, and demo link are complete |
| P1 | Optional bonus content | Publish a public build article or social post with `#AllThingsAgenticHackathon` if time permits |

## 5. Four-minute demo script

| Time | Screen/action | Message |
|---:|---|---|
| 0:00–0:25 | Show the problem and GroundPulse landing page | Satellite research requires coordinating sources, validation, and reporting across disconnected workflows |
| 0:25–0:45 | Open Mission Control and enter or select the sample request | GroundPulse accepts a bounded mission question and creates a durable Run ID |
| 0:45–1:25 | Show the request, Cloud Tasks dispatch, and Cloud Run worker path | The agent works asynchronously in the background rather than waiting in a chat loop |
| 1:25–2:10 | Show source discovery and the approved CelesTrak snapshot | The workflow preserves source identity, timestamps, and snapshot lineage |
| 2:10–2:55 | Open the evidence ledger and validation gate | Claims are source-backed, derived, proposed, or unavailable; unsupported claims do not silently pass |
| 2:55–3:25 | Open the artifact/package tab | The system produces an immutable package with manifest, brief, ledger, gaps, validation report, and trace |
| 3:25–3:45 | Show Cloud Run revision, task delivery, or relevant logs | The backend is deployed on Google Cloud and the asynchronous path is real |
| 3:45–4:00 | End on the released package and limitations | GroundPulse removes coordination work while keeping uncertainty and human review visible |

## 6. Copy-ready Devpost description

### What we built

GroundPulse is an evidence-first agent for satellite and ground-segment research. A user provides a structured question, object or location, time window, source constraints, and decision intent. GroundPulse creates a durable run, dispatches asynchronous work, retrieves approved source snapshots, validates the resulting claim ledger, and generates a source-linked research package.

### Why it matters

Operational and satellite research often requires manually coordinating discovery, source checking, provenance, gaps, and reporting. GroundPulse handles that repetitive workflow in the background while keeping the evidence trail visible to a specialist. It is designed to make research faster without turning an unsupported model output into an operational fact.

### Technologies used

GroundPulse uses Gemini through the Google Agent Development Kit, with Google Cloud Run for the API and worker runtime, Cloud Tasks for asynchronous dispatch, Firestore for run state, Cloud Storage for immutable artifacts, and Secret Manager for controlled credentials. The frontend exposes Mission Control views for run status, source review, evidence validation, gaps, execution events, and package artifacts.

### Data sources

The demonstrated path uses an approved CelesTrak snapshot for ISS/NORAD 25544. The snapshot is used as a controlled public orbital-context fixture. The demo must not imply that public orbital data provides private RF metrics, modem health, station incidents, or operational readiness unless those measurements are actually present in an authorized source.

### Findings and learnings

The most important design finding was that an agentic workflow needs durable state, idempotent submission, explicit evidence gates, immutable artifacts, and visible gaps. A model call alone is not enough: the system must preserve what was requested, what sources were used, what was derived, what could not be found, and why a package was released or held.

### Limitations

The submission demonstrates a controlled research workflow and does not claim that every future telemetry adapter, partner feed, autonomous spacecraft operation, or enterprise governance surface is complete. The demo uses approved fixtures and a bounded evidence path. Human specialists retain final operational authority.

## 7. Repository and release checklist

Before submitting, confirm that the README contains the exact branch/commit, prerequisites, local startup commands, cloud deployment commands, environment-variable names without secret values, API routes, test commands, and a clear distinction between local fallback mode and cloud mode. Confirm that `.env` files, credentials, virtual environments, generated runtime artifacts, private bucket contents, and customer data are absent from Git.

Use one named demonstration Run ID consistently across the video, README, screenshots, and Devpost description. The Run ID should appear in the request, Dashboard, artifact manifest, and final package so judges can follow the complete trace.

## 8. Final go/no-go gate

| Gate | Go condition |
|---|---|
| Agentic behavior | The agent performs multi-step asynchronous work after the initial request |
| Gemini/ADK proof | The code and video show where Gemini and ADK are used |
| Google Cloud proof | The video shows a real Cloud Run/task/backend path |
| Evidence quality | The final output contains source references, validation state, and explicit gaps |
| Reproducibility | README setup is accurate and tested from a clean environment |
| Demo reliability | The same sample run can be repeated without manual repair |
| Truthfulness | Planned features and controlled fixtures are labeled honestly |

If any P0 gate fails, submit only after fixing it or narrow the demo to the verified controlled path. A smaller truthful workflow is stronger than a larger claim that the video cannot prove.

## References

[1]: https://allthingsagentichackathon.devpost.com/ "All Things Agentic Hackathon — official Devpost page"

[2]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/tree/feat/p1-cloud-backed-run "GroundPulse feature branch"

[3]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/blob/feat/p1-cloud-backed-run/docs/P2_DASHBOARD_MILESTONE.md "GroundPulse P2 Dashboard Milestone"

[4]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/blob/feat/p1-cloud-backed-run/docs/LIMITATIONS.md "GroundPulse limitations"
