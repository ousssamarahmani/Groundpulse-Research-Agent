# Fix checklist

- [x] Identify all active generated-image references that may resolve to failed placeholders.
- [x] Replace failed generated-image references with reliable managed assets.
- [x] Rebuild and type-check the published project.
- [x] Verify the homepage and public domain no longer show the failure placeholder.
- [x] Save an updated checkpoint and report the result. (Published as version 78486acd.)

## Logo visibility repair

- [x] Inspect header, favicon, and managed logo asset references.
- [x] Repair the logo reference or visibility styling.
- [x] Verify the logo renders on the homepage and save the fix.

## Proof-of-system UI update

- [x] Inspect current landing-page and Workspace components and available interactions.
- [x] Add an honest sample-run proof panel to the landing page.
- [x] Add an interactive sample-run timeline to Workspace.
- [x] Verify both surfaces and save a publishable checkpoint.

## P1 cloud-backed branch audit

- [x] Inspect the feature branch commit, README, task checklist, and source tree.
- [x] Map each P1 task to implementation evidence and mark blockers.
- [x] Run the branch test suite and deployment-readiness checks.
- [x] Summarize completed, incomplete, and blocked tasks.

## Update-version template

- [x] Define the prioritized workstreams for the next version. (Recorded during the prior update-version review.)
- [x] Write acceptance criteria for backend, frontend, evidence, deployment, and customer proof. (Recorded during the prior update-version review.)
- [x] Deliver the reusable template and recommended build order. (Hackathon-only scope retained per user direction.)

## Hackathon-only completion template

- [x] Review the official All Things Agentic Hackathon rules and submission requirements.
- [x] Map the current feature branch to the required demo and submission evidence.
- [x] Define the remaining hackathon-only tasks and the shortest completion order.

## Hackathon deadline status review

- [x] Consolidate completed and incomplete tasks from the latest feature branch.
- [x] Identify the minimum build required for a valid submission.
- [x] Organize the remaining work by deadline priority and go/no-go gates.

## Continue hackathon work

- [x] Check the feature branch state and safely synchronize it with main.
- [x] Rerun backend and frontend validation after synchronization.
- [x] Verify the live workflow and frontend API alignment.
- [x] Prepare the next submission-ready milestone and record remaining blockers.

## No-CLI Cloud deployment preparation

- [x] Audit Dockerfile, Procfile, deployment documentation, and environment variables.
- [x] Validate the backend/frontend builds and container/deployment assumptions locally.
- [x] Prepare a reproducible console-based deployment handoff without exposing secrets.
- [x] Record the remaining Google Cloud authorization steps.

## Continue locally completable tasks

- [x] Audit remaining submission gaps and local validation opportunities.
- [x] Add or improve local preflight and demo reproducibility checks.
- [x] Tighten README/demo documentation for the live-data path.
- [x] Run validation and push the next safe milestone.

## Continue next task

- [x] Inspect the current branch tip and identify the highest-priority locally completable blocker.
- [x] Implement one focused submission-readiness improvement.
- [x] Run validation and push the safe update.

## Replace deterministic Workspace data

- [x] Trace the current public Workspace data source and API configuration.
- [x] Connect the managed Workspace to a real CelesTrak GP/OMM data path.
- [x] Map live source metadata and authoritative Run ID into the UI.
- [x] Preserve a clearly labeled fallback state and verify the updated workflow.

## Browser-safe live CelesTrak connection

- [x] Confirm the direct CelesTrak browser request is blocked by CORS.
- [x] Add a managed backend proxy for CelesTrak GP/OMM.
- [x] Point the Workspace to the proxy and remove the demo state from the live path.
- [x] Verify live source metadata and save a new managed checkpoint. (Live-record contract verified with Vitest; deployed checkpoint 78486acd is published. Local Node egress remains provider-blocked and falls back honestly.)

## Engineering research package expansion

- [x] Audit the current Package tab, run state, and download behavior.
- [x] Define an honest CubeSat/satellite-engineering report contract with source, derivation, and gap sections.
- [x] Add substantive engineering package content to the Workspace using the live orbital record where available.
- [x] Add a client-generated downloadable HTML report artifact with a clear Print → Save as PDF affordance without fabricating operational facts.
- [x] Add Vitest coverage for package generation, browser-verify the Package tab and download confirmation, and validate the Workspace and production build.

## Role-specific CubeSat analyst value

- [x] Define role-specific scenarios for CubeSat analysts, satellite engineers, and space researchers.
- [x] Add structured scenario selection to the New research intake.
- [x] Add dedicated analyst interpretation and next-action outputs without inventing spacecraft telemetry.
- [x] Add role and scenario state to the research package and export.
- [x] Add shared scenario regression tests and browser validation for the role-specific workflow before publishing.

## Workspace layout and analyst usability repair

- [x] Fix Package/Evidence column overflow and card overlap at desktop width.
- [x] Reduce empty vertical space and improve package content density.
- [x] Make workflow state advance to a clearly completed package state after the live source is validated.
- [x] Add an honest orbital-data visualization for mean motion, orbital period, and source freshness.
- [x] Add regression tests and browser screenshots for layout, workflow, and visualization before publishing.

## Backlog audit

- [x] Audit current backlog items against repository implementation and documentation.
- [x] Verify completed items with current tests, build, and published checkpoint evidence.
- [x] Identify remaining implementation tasks, infrastructure blockers, and submission risks.
- [x] Produce a prioritized next-work plan with clear acceptance criteria.
