# GroundPulse P2 Demo Script and Recording Checklist

## Demo objective

Demonstrate that GroundPulse turns an approved satellite-research request into a validated, source-linked, immutable research package. Use the released ISS run `run_p1_55cbb0817ecd` as the primary demonstration record.

## Before recording

Confirm that the local FastAPI server is running on `http://127.0.0.1:8000` with Firestore and GCS enabled, and that the Vite frontend is running on `http://127.0.0.1:3000`. Confirm that `client/.env.local` points to the local API and that the browser opens `/dashboard` without an API error.

Keep the following values available for reference:

| Item | Value |
|---|---|
| Demonstration run | `run_p1_55cbb0817ecd` |
| Object | ISS |
| NORAD ID | `25544` |
| Approved source | `celestrak_gp_25544` |
| Run status | `released` |
| Validation state | `passed` |
| Package objects | `10` |
| Cloud Run revision | `groundpulse-research-api-00020-gqv` |

Do not display `.env` files, API keys, identity tokens, private bucket credentials, or terminal output containing secrets.

## Suggested 3–4 minute walkthrough

### 1. Introduce the problem

Say: “GroundPulse is a controlled satellite research agent. It does not pretend to have live telemetry or spacecraft health data. It answers only what the approved source can support, records what is unavailable, and packages the result as immutable evidence.”

### 2. Show the live mission archive

Open Mission Control and point to the recent-runs archive. Select `run_p1_55cbb0817ecd`. Explain that the dashboard is reading persisted run data from the research API rather than prototype constants.

Say: “This is the verified ISS evidence mission. The run is released, the validation gate passed, and the dashboard is showing the actual backend record.”

### 3. Show the four-stage workflow

Point to Frame request, Discover sources, Validate evidence, and Build package. Highlight that all four stages are complete.

Say: “The workflow makes the control boundary visible. The request is framed first, the approved source is selected, evidence is validated, and only then is the package released.”

### 4. Show mission parameters and evidence state

Point to ISS, NORAD ID `25544`, the UTC window, the research intent, and the passed validation gate.

Say: “The run is about the ISS catalog object, not an unrestricted operational assessment. The evidence state is passed, which is the condition required for claim release.”

### 5. Show the evidence ledger

Open the Evidence tab or source-review section. Point to the approved CelesTrak snapshot, the candidate claim ledger, and the explicit gap list.

Say: “GroundPulse separates supported claims from derived claims and gaps. The gap list is not hidden: unavailable evidence is retained explicitly so users can see what the source does not establish.”

### 6. Show execution events

Point to Request, Source, Validation, and Package events in the run trace.

Say: “The execution trace provides a compact audit path from request acceptance to approved evidence, validation, and immutable package release.”

### 7. Show the package tab

Open the Package tab and show that the run has one immutable package reference and ten package objects. If artifact rows or links are visible, show the names `candidate_ledger.json`, `normalized_result.json`, `source_snapshot.json`, `validation_report.json`, and `manifest.json`.

Say: “The package contains source snapshots, normalized results, claim ledger, gap list, validation report, trace, and manifests. The artifacts are stored in a private GCS bucket and are delivered through an authenticated API boundary.”

### 8. Close with the value proposition

Say: “The result is not just an answer. It is a reproducible research package with provenance, explicit limits, validation state, and immutable evidence. That makes the output auditable and safer to use in downstream decisions.”

## Recording checklist

| Check | Complete |
|---|---|
| FastAPI is running on port 8000 | ☐ |
| Vite is running on port 3000 | ☐ |
| Dashboard loads without API error | ☐ |
| Released run `run_p1_55cbb0817ecd` is selected | ☐ |
| Status shows `released` | ☐ |
| Validation shows `passed` | ☐ |
| Approved source `celestrak_gp_25544` is visible | ☐ |
| Evidence ledger is visible | ☐ |
| Gap list is visible | ☐ |
| Execution trace is visible | ☐ |
| Package tab shows the immutable package | ☐ |
| No secrets or tokens appear on screen | ☐ |
| Final video includes the project name and outcome | ☐ |

## Backup evidence for the submission

Keep the following facts ready if the dashboard view is unavailable during recording: the deployed health endpoint returned `status: ok`; the deployed dashboard API returned the released run; the artifact proxy returned `returned: 10`; and the private GCS bucket remained inaccessible directly while artifacts were available through the authenticated API proxy.

## One-sentence submission description

“GroundPulse is a controlled satellite research agent that transforms approved source data into validated, source-linked, gap-aware, and immutable research packages for auditable decision support.”
