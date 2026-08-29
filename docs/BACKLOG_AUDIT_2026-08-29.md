# GroundPulse backlog audit — 29 August 2026

## Executive finding

The current managed WebDev project is a polished evidence-first Workspace with a working server-side CelesTrak GP/OMM path, live/fallback states, role-specific intake, an engineering package, download/print actions, and an orbital timing visualization. The latest published checkpoint is `2c14e4e`, and the current working tree is on `main` with only the audit checklist modified before this document was created.

The repository’s hackathon documents describe a broader Google Cloud and Google ADK implementation. The current managed `main` tree does not contain a root README, `agent/groundpulse_agent/`, Cloud Tasks worker code, or the architecture assets referenced by the older submission template. A GitHub API audit confirms that `feat/p1-cloud-backed-run` exists at `b5b0afe089d213e3f4f41398c221f82c0cd73476` and does contain those paths, including ADK agent code, Cloud Tasks/Firestore/Storage modules, tests, and architecture diagrams. Those feature-branch claims are structurally verified but still require a fresh runtime demonstration before they can be claimed as the current hosted path.

## Verified completed work in the current managed project

| Area | Evidence | Status |
|---|---|---|
| Workspace UI | Mission Control route with Overview, Evidence, Package, source ledger, trace, gaps, and role-specific intake | Verified |
| Live orbital source | `celestrak.latest` tRPC procedure with normalized CelesTrak GP/OMM record, epoch, retrieval time, and derived period | Verified by current UI and tests |
| Honest fallback | Explicit unavailable/connecting states; no missing source values presented as live | Verified |
| Engineering package | ADCS/GNC, EPS, communications, thermal/structures, mission operations, gaps, references, HTML download, and Print/Save PDF | Verified |
| Analyst value | CubeSat analyst, satellite engineer, and space researcher profiles with scenarios, interpretations, and next actions | Verified |
| Visualization | Normalized orbital-cycle view with mean motion, period, and source freshness | Verified in browser screenshot and tests |
| Validation | TypeScript check, production build, 11 Vitest tests at the latest published milestone | Verified |
| Hosting | Managed public domain `groundpulse-zx8ga3th.manus.space` | Available; final route smoke test should still be repeated after the audit checkpoint |

## Remaining work, blockers, and risks

| Priority | Task | Why it remains | Acceptance criterion |
|---:|---|---|---|
| P0 | Verify or restore the real Google ADK/Cloud workflow | Current managed tree does not independently prove Gemini, ADK, Cloud Tasks, Firestore, Cloud Storage, or a Cloud Run worker | One fresh run creates a stable Run ID, executes asynchronously, reaches `released`, and exposes the same result in Mission Control |
| P0 | Freeze the exact submission commit | `todo.md` is currently modified by this audit; the submission needs one named clean commit | Clean working tree, exact commit recorded in Devpost and README |
| P0 | Complete the four-minute demo video | No video artifact is present in the current project | Video visibly proves request, Run ID, async execution, Gemini/ADK, Google Cloud, evidence gate, and package |
| P0 | Finalize hosted URL proof | Public domain exists, but the Cloud-backed workflow route must be tested as judges will see it | Incognito/browser smoke test succeeds and URL is recorded in submission materials |
| P1 | Add a current README | No root `README.md` exists in the managed project | Clean-machine setup, local fallback mode, cloud mode, routes, tests, and limitations are documented |
| P1 | Reconcile architecture diagram | The checklist references diagram assets not present in the current tree | Every drawn service exists in the submitted code or is labeled planned |
| P1 | Reconcile submission copy | Existing copy describes a broader cloud path than the current managed tree proves | Devpost text names the exact verified branch/commit and labels unverified items honestly |
| P1 | Add real target selection | Current live source is fixed to ISS/NORAD 25544 | User can select or enter a CubeSat/NORAD ID and the source/package/visualization update together |
| P1 | Add operationally useful analysis | Current visualization is orbital timing, not pass prediction or ground-station visibility | A selected target produces pass windows or a clearly bounded “requires propagation/station inputs” result |
| P2 | Persist packages and runs | Download is currently client-generated HTML and the managed run is not a durable user-created research record | Package metadata and artifact are stored and retrievable by Run ID |
| P2 | Add broader sources | Only CelesTrak is live in the demonstrated path | Additional source adapters have contracts, provenance, tests, and visible failure states |

## Recommended order

First, decide whether the submission will prove the Google ADK/Cloud implementation from `feat/p1-cloud-backed-run` or submit the current managed Workspace as a truthful CelesTrak evidence product. Do not mix claims from the older branch with the current UI without a fresh end-to-end verification.

Second, freeze one reproducible demonstration. The minimum strong demo is an analyst selecting a CubeSat scenario, receiving a Run ID, showing the source record and derived orbital timing, opening the subsystem evidence matrix, assigning a visible data-gap task, and downloading the package. If the Cloud path is available, insert Cloud Tasks, Cloud Run, Gemini/ADK, and Firestore proof into that same run.

Third, create the missing release hygiene: current README, accurate architecture diagram, exact hosted URL, named commit, and four-minute video. Only after those gates should the team add NORAD selection, pass prediction, persistent artifacts, or more source adapters.

## Go/no-go assessment

| Gate | Current assessment |
|---|---|
| Current frontend value | **Go** for a source-backed CubeSat/satellite research Workspace |
| Current managed CelesTrak path | **Go**, with explicit provider-unavailable fallback |
| Google ADK/Cloud proof | **Needs verification** against the feature branch or deployment |
| Clean submission package | **No-go** until README, diagram, exact commit, and video are finalized |
| Broader commercial platform | **Defer**; it is not required for the focused hackathon proof |
