# GroundPulse Cloud Console Deployment

This guide deploys the current `feat/p1-cloud-backed-run` backend without requiring the Google Cloud CLI. It uses Cloud Build and the Google Cloud Console. The container starts `groundpulse_agent.api:app` on port `8080`; the existing `Dockerfile` and `agent/Procfile` are the deployment source of truth.

## Deployment target

| Setting | Recommended value |
|---|---|
| Region | `europe-west3` |
| Cloud Run service | `groundpulse-research-api` |
| Artifact Registry repository | `groundpulse` |
| Container image | `research-api` |
| Runtime | Python 3.11 container from the repository Dockerfile |
| Ingress | Internal and Cloud Load Balancing, or the narrowest setting compatible with the frontend |
| Authentication | Do not allow unauthenticated access for the research API unless a deliberate public proxy is added |

## One-time project setup in the Console

1. Open Google Cloud Console and select the intended project.
2. Enable Cloud Run, Cloud Build, Artifact Registry, Firestore, Cloud Tasks, Cloud Storage, Secret Manager, and Vertex AI or the Gemini API according to the selected model access path.
3. Create an Artifact Registry Docker repository named `groundpulse` in `europe-west3`.
4. Create or confirm a Firestore database in the intended mode and region.
5. Create a private Cloud Storage bucket for immutable research artifacts. Do not make the bucket public.
6. Create a Cloud Tasks queue named `groundpulse-research` in the same region.
7. Create separate service accounts for the API/worker runtime and Cloud Build where possible. Grant only the required Firestore, Cloud Tasks, Storage, Secret Manager, and model permissions.
8. Store `GOOGLE_API_KEY` or the chosen model credential in Secret Manager. Never place the secret in Git, a Dockerfile, a frontend environment variable, or a screenshot.

## Build from GitHub without the CLI

1. In Cloud Build, open **Triggers** and create a GitHub trigger for `feat/p1-cloud-backed-run`.
2. Select the repository and configure the trigger to use the checked-in `cloudbuild.yaml`.
3. Set the substitution values in the trigger if the project uses names different from the defaults: `_REGION`, `_REPOSITORY`, and `_IMAGE`.
4. Run the trigger manually once. Confirm that the Docker image is created in Artifact Registry and that the build log contains no secret values.

The checked-in `cloudbuild.yaml` builds and pushes the image only. This keeps deployment configuration and secrets visible in the Cloud Console rather than embedding credentials in source control.

## Deploy the image in Cloud Run

1. Open **Cloud Run → Create service** or **Edit and deploy new revision** for `groundpulse-research-api`.
2. Choose the Artifact Registry image produced by the Cloud Build trigger.
3. Set the region to `europe-west3` and keep the container port at `8080`.
4. Keep authentication restricted. If the frontend is hosted separately, use an authenticated backend proxy or a deliberate Cloud Run ingress and IAM design; do not expose the private artifact bucket.
5. Attach the runtime service account.
6. Add the non-secret environment variables in the revision configuration:

```text
GEMINI_MODEL=gemini-3.5-flash-lite
GOOGLE_CLOUD_PROJECT=<project-id>
GOOGLE_CLOUD_FIRESTORE_DATABASE=<database-name>
GROUND_PULSE_ARTIFACT_BUCKET=<private-bucket-name>
GROUND_PULSE_QUEUE=groundpulse-research
GROUND_PULSE_STORAGE=gcs
GROUND_PULSE_ARTIFACT_STORAGE=gcs
GROUND_PULSE_WORKER_URL=<cloud-run-service-url>
GROUND_PULSE_CORS_ORIGINS=<authorized-frontend-origin>
```

7. Add the model credential through the **Secrets** section, mapped to `GOOGLE_API_KEY` if that is the selected authentication method.
8. Deploy the revision and record the revision name, service URL, region, and timestamp in the hackathon notes.

## Cloud Tasks delivery

Configure the queue target to call the worker endpoint exposed by the API. Use an OIDC token issued for the runtime or worker service account. The caller needs permission to invoke the private Cloud Run service. The task payload must include the API-created `run_id`; the worker must preserve that ID in every artifact.

Do not mark the deployment complete until a task is delivered through the queue and the worker reaches a terminal state. A successful HTTP response from the API alone is not enough.

## Verification checklist

| Check | Required evidence |
|---|---|
| Container starts | Cloud Run revision becomes healthy and listens on port `8080` |
| API health | The documented health endpoint or a safe read-only API request succeeds |
| Task delivery | Cloud Tasks log shows delivery to the private service with successful response |
| Model call | Cloud Run logs show the selected Gemini model without exposing prompts or secrets |
| Run persistence | Firestore contains the created run with the authoritative Run ID |
| Run ID integrity | `request.json`, `normalized_result.json`, and package metadata contain the same Run ID |
| Artifact privacy | Artifact metadata is readable through the authenticated API; the bucket remains private |
| Dashboard | Frontend reads `/dashboard/runs` and artifact metadata from the configured API base URL |
| Failure path | A missing or unsupported source becomes a visible gap and does not become an invented claim |
| Reproducibility | README setup works from a clean checkout and identifies the exact branch/commit |

## Frontend connection

Set the frontend build-time variable to the authorized API origin:

```text
VITE_GROUNDPULSE_API_URL=https://<authorized-api-origin>
```

The frontend client already calls:

```text
GET /dashboard/runs
GET /dashboard/runs/{run_id}
GET /dashboard/runs/{run_id}/artifacts
GET /dashboard/runs/{run_id}/artifacts/{artifact_name}
```

If the API is private, the public frontend cannot call it directly without an authenticated proxy or an approved identity flow. Do not solve this by making Cloud Storage public or by placing service credentials in the frontend.

## Hackathon evidence to capture

For the four-minute demo, capture the Cloud Run service/revision, Cloud Tasks delivery, Gemini/ADK execution, Mission Control Run ID, evidence gate, and immutable package. The official hackathon requires proof that the backend was built and deployed on Google Cloud, not merely a local UI.[1]

## Current limitation

The deployment files and Console handoff can be prepared without the CLI, but the actual Cloud Run deployment still requires an authorized Google Cloud project, billing/credits where applicable, IAM permissions, and secrets configured in the Console. This repository does not contain those credentials.

## References

[1]: https://allthingsagentichackathon.devpost.com/ "All Things Agentic Hackathon official Devpost page"

[2]: https://github.com/ousssamarahmani/Groundpulse-Research-Agent/tree/feat/p1-cloud-backed-run "GroundPulse feature branch"
