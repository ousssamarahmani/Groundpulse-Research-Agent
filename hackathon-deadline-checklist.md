# GroundPulse Hackathon Deadline Checklist

**Project:** GroundPulse Research Agent  
**Branch:** `feat/p1-cloud-backed-run`  
**Hackathon:** All Things Agentic Hackathon  
**Deadline shown on Devpost:** August 31, 2026 at 5:00 PM PDT.[1]

## Executive answer

The project has enough technical work for a credible hackathon submission, but **the submission is not complete yet**. The core agent workflow is implemented and locally validated. The remaining work is mainly proof, release hygiene, and submission packaging—not building the entire future StellarOS platform.

The recommended category is **The Taskmaster**. GroundPulse takes a bounded research question, performs asynchronous multi-step work, validates evidence, and produces a package. Do not spend the remaining time on broad autonomous-space features or every planned telemetry adapter.

## Completed

| Area | Evidence | Status |
|---|---|---|
| Gemini integration | Gemini 3.5 Flash Lite is used in the documented ADK coordinator path | Completed; verify the deployed model name in the demo |
| Google Agent Framework | Google ADK workflow exists in the agent package | Completed |
| Google Cloud usage | Cloud Run, Cloud Tasks, Firestore, Cloud Storage, and Secret Manager are implemented in the controlled path | Completed for the demonstrated path |
| Run model | Durable run state, stable Run ID, idempotent submission, and state transitions | Completed |
| Asynchronous execution | API request dispatches background work through Cloud Tasks to a private Cloud Run worker | Completed |
| Evidence workflow | Source snapshot, candidate ledger, validation report, gaps, and release gate | Completed for the approved fixture path |
| Immutable package | Ten package objects are documented under a private Cloud Storage prefix | Completed for the verified run |
| Dashboard API | Run history and artifact metadata endpoints are documented and implemented | Completed according to the newer P2 milestone |
| Dashboard behavior | Mission Control shows stages, evidence, gaps, events, and package artifacts | Completed for the live API path; verify the hosted frontend is using that API |
| Reliability handling | Legacy malformed Firestore records are skipped rather than causing a Dashboard 500 | Completed |
| Deployment entrypoint | Cloud Run ASGI Procfile is defined | Completed |
| Backend validation | Feature branch audit passed Python compilation and **21 tests** | Completed |
| Frontend validation | TypeScript check and production build passed | Completed |
| Repository documentation | README, architecture, limitations, implementation plan, P1/P2 status, and demo script exist | Mostly completed; final consistency review required |

## Not completed or still blocked

| Area | Status | What is actually needed for the hackathon |
|---|---|---|
| Four-minute demo video | Not completed | Record the problem, live workflow, Gemini/ADK use, Google Cloud proof, and final package |
| Final hosted URL | Needs verification | Provide a URL judges can open, or explain clearly that the video is the primary proof if the service is private |
| README clean-machine test | Needs final verification | Test the exact setup instructions from a clean environment and document local versus cloud mode |
| Branch synchronization | Required | The feature branch is 14 commits ahead and 2 commits behind `main`; merge/rebase deliberately, then rerun tests |
| Architecture diagram accuracy | Needs final verification | Ensure every shown service matches code and the deployed path; label future services as planned |
| Devpost submission fields | Not completed | Fill category, project URL, description, technologies, data sources, findings, repo URL, diagram, and demo video |
| Live partner telemetry | Blocked | Requires authorization, source contract, schema, and end-to-end approval; it is not required if the demo uses the approved fixture honestly |
| Broader source adapters | Planned | Not required for the minimum submission; do not claim them as live |
| Human-review surfaces beyond the demonstrated gate | Planned | Keep the current visible gap and human-authority boundary; do not expand scope unless already working |
| Full observability and budget runbooks | Planned | Not required for a controlled demo; show the deployed Cloud Run/task path instead |
| Independent review | Planned | Valuable but optional if time does not allow it; do not claim it has happened |

## Minimum build required before submission

The minimum acceptable build is one repeatable, truthful end-to-end run. A judge should be able to see a request create a Run ID, background work move through the agent stages, an approved source snapshot enter the evidence path, a validation decision occur, and a final package become available. The package should visibly contain the brief, manifest, source snapshot, claim ledger, gap list, validation report, and redacted trace.

The demo does not need every future feature. It does need to prove that the agent performs work asynchronously and that the result is more than generated text. The CelesTrak ISS fixture is acceptable as a controlled demonstration if the submission clearly labels it as an approved fixture and does not imply that it contains private station telemetry or live RF health measurements.

## Exact order of work before the deadline

| Order | Work | Go condition |
|---:|---|---|
| 1 | Synchronize `feat/p1-cloud-backed-run` with current `main` | No accidental loss of the Run ID fix; branch has one clean submission commit or clearly named HEAD |
| 2 | Run the backend suite and frontend check/build again | All tests pass; TypeScript and production build pass |
| 3 | Execute one fresh cloud-backed demonstration run | A new Run ID reaches `released` with validation `passed` and no manual database repair |
| 4 | Verify the frontend against the live API | Mission Control shows the same Run ID, status, evidence, gaps, and artifacts as the backend |
| 5 | Verify the architecture diagram and README | Instructions and diagram describe the actual submitted commit and deployment |
| 6 | Record the demo | Keep it near four minutes and show Google Cloud proof, not only the frontend |
| 7 | Complete Devpost fields and submit | Category, URLs, code access, description, diagram, video, sources, and limitations are complete |

## Four-minute demo must show

| Time | Required evidence |
|---:|---|
| 0:00–0:30 | The specific research problem and why manual coordination is slow or error-prone |
| 0:30–1:00 | A request creates a stable Run ID |
| 1:00–1:45 | Cloud Tasks dispatch and Cloud Run worker execution |
| 1:45–2:30 | Gemini/ADK performs the research coordination step |
| 2:30–3:10 | Source snapshot, evidence ledger, validation gate, and explicit gap |
| 3:10–3:40 | Immutable package artifacts and manifest |
| 3:40–4:00 | Cloud Run/Google Cloud proof, limitations, and final value proposition |

## Do not build before submission

Do not spend the deadline on autonomous spacecraft control, a large multi-agent architecture, every public-data adapter, a broad partner-telemetry system, a full enterprise agent marketplace, or extra landing-page animations. These features increase risk and are not needed to satisfy the core hackathon proof. A small working Taskmaster workflow with honest boundaries is stronger than a large partially demonstrated platform.

## Final go/no-go gate

Submit when all seven conditions are true: the selected branch is frozen; tests pass; one fresh run completes; the frontend can show the run; the README and diagram are accurate; the demo video proves Gemini/ADK and Google Cloud; and the Devpost form is complete. If live telemetry is not authorized, state that clearly and use the approved fixture path rather than implying production telemetry.

## References

[1]: https://allthingsagentichackathon.devpost.com/ "All Things Agentic Hackathon official Devpost page"

[2]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/tree/feat/p1-cloud-backed-run "GroundPulse feature branch"

[3]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/blob/feat/p1-cloud-backed-run/docs/P2_DASHBOARD_MILESTONE.md "GroundPulse P2 Dashboard Milestone"

[4]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/blob/feat/p1-cloud-backed-run/docs/LIMITATIONS.md "GroundPulse limitations"
