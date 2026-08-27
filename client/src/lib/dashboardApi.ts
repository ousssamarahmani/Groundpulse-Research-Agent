export type DashboardRunSummary = {
  run_id: string;
  status: string;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  attempt_count: number;
  validation_state: string;
  error_code: string | null;
  review_reason: string | null;
  question: string;
  decision_intent: string;
  object_name: string;
  norad_catalog_id: string | null;
  allowed_source_ids: string[];
  snapshot_ids: string[];
  artifact_ids: string[];
};

export type DashboardRunListResponse = {
  runs: DashboardRunSummary[];
  limit: number;
  offset: number;
  returned: number;
};

export type DashboardArtifact = {
  name: string;
  object_path: string;
  uri: string;
  sha256: string;
  size_bytes: number;
  generation: string | null;
  download_url: string;
};

export type DashboardArtifactListResponse = {
  run_id: string;
  artifacts: DashboardArtifact[];
  returned: number;
};

const apiBaseUrl = (import.meta.env.VITE_GROUNDPULSE_API_URL ?? "").replace(/\/$/, "");

export class DashboardApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "DashboardApiError";
    this.status = status;
  }
}

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: { Accept: "application/json" },
    credentials: "include",
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const payload = (await response.json()) as { detail?: string };
      detail = payload.detail ?? detail;
    } catch {
      // Preserve the HTTP status when the response is not JSON.
    }
    throw new DashboardApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

export function listDashboardRuns(limit = 20, offset = 0) {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });
  return requestJson<DashboardRunListResponse>(`/dashboard/runs?${params}`);
}

export function getDashboardRun(runId: string) {
  return requestJson<DashboardRunSummary>(
    `/dashboard/runs/${encodeURIComponent(runId)}`,
  );
}

export function listDashboardArtifacts(runId: string) {
  return requestJson<DashboardArtifactListResponse>(
    `/dashboard/runs/${encodeURIComponent(runId)}/artifacts`,
  );
}

export function artifactUrl(runId: string, artifactName: string) {
  const encodedName = artifactName
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");
  return `${apiBaseUrl}/dashboard/runs/${encodeURIComponent(runId)}/artifacts/${encodedName}`;
}
