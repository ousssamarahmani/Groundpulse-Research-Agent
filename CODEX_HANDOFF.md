# Codex Handoff — GroundPulse Research Agent

## Repository location

Open this **folder directly** in Codex; do not use the ZIP archive:

```text
/home/ubuntu/GroundPulse-Research-Agent
```

The intended GitHub remote is:

```text
https://github.com/ousssamarahmani/Groundpulse-Research-Agent.git
```

## What is included

| Area | Location | Notes |
|---|---|---|
| Product landing page | `client/src/pages/Home.tsx` | English SpaceTech product interface with local image assets. |
| Mission Control dashboard | `client/src/pages/Dashboard.tsx` | Interactive local-state prototype, explicitly labeled as non-live. |
| Research Journal | `client/src/pages/JournalArticle.tsx` and `client/src/lib/journal.ts` | Product and methodology content. |
| Product assets | `client/public/assets/` | Self-contained images used by the frontend. |
| Product preview | `assets/previews/groundpulse-landing-page.png` | Current landing-page capture used in the README. |
| Hackathon documentation | `docs/HACKATHON_SUBMISSION.md` | Problem, solution, demo flow, and honest scope. |
| Build roadmap | `docs/IMPLEMENTATION_PLAN.md` and `docs/TASKS.md` | Phased implementation plan and acceptance-oriented backlog. |
| Target architecture | `docs/ARCHITECTURE.md` and `docs/GCP_REALTIME_INTEGRATION_PLAN.md` | Target design only; no live GCP deployment is claimed. |
| Scope controls | `docs/LIMITATIONS.md`, `CONTRIBUTING.md`, and `SECURITY.md` | Prototype, evidence, and source-handling boundaries. |

## Required guardrails

This project is an evidence-first product prototype. Do **not** add claims that a live agent, GCP deployment, telemetry connection, external source ingestion, empirical model result, or operational capability exists unless the implementation and evidence are added in the same change. Dashboard values are intentionally labeled as prototype or illustrative UI content.

Do not commit API keys, GitHub tokens, GCP service-account keys, user data, station logs, or private source payloads. Keep all generated or test data visibly labeled as fixture, prototype, or synthetic where appropriate.

## Verify before pushing

```bash
cd /home/ubuntu/GroundPulse-Research-Agent
git status
pnpm install --frozen-lockfile
pnpm check
pnpm build
```

The repository already contains a clean Git history and an initial commit. If any local modifications are made, review them carefully before committing.

## Push procedure

Use an authenticated GitHub session that has **Contents: Read and write** access to `ousssamarahmani/Groundpulse-Research-Agent`.

```bash
cd /home/ubuntu/GroundPulse-Research-Agent
git remote set-url origin https://github.com/ousssamarahmani/Groundpulse-Research-Agent.git
git branch --show-current
git push -u origin main
```

If Codex changes files first, use a focused commit message and push the resulting commit:

```bash
git add <specific-files>
git commit -m "docs: refine GroundPulse repository handoff"
git push origin main
```

Do **not** force-push and do not replace repository history. If the push is rejected, inspect `git remote -v`, `git status`, and GitHub repository permissions before changing code or retrying.
