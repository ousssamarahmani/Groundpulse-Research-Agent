export type Audience = "CubeSat analyst" | "Satellite engineer" | "Space researcher";

export type ResearchScenario = {
  id: string;
  label: string;
  title: string;
  target: string;
  question: string;
  output: string;
  nextAction: string;
  interpretation: string;
};

export const profileScenarios: Record<Audience, ResearchScenario[]> = {
  "CubeSat analyst": [
    { id: "orbit-readiness", label: "Orbit readiness check", title: "CubeSat orbit readiness review", target: "CubeSat / small satellite", question: "Assess whether the latest public orbital record is fresh enough for preliminary pass planning. Show epoch, mean motion, derived period, and the evidence needed before scheduling operations.", output: "Orbit freshness, derived period, planning inputs, and a safe-to-use boundary.", nextAction: "Request a pass-planning propagation run.", interpretation: "Use the orbital record for preliminary propagation and pass planning only; confirm freshness and mission-specific tolerances before scheduling commands." },
    { id: "launch-object", label: "Launch catalog review", title: "New launch object identification", target: "CubeSat / small satellite", question: "Identify the public orbital record for a newly launched CubeSat and separate catalog evidence from assumptions about mission identity or operational status.", output: "Candidate records, identity confidence, and unresolved attribution gaps.", nextAction: "Assign a human object-identity review.", interpretation: "Treat catalog identity as a research finding, not proof of mission ownership or operational status; require an independent identity source." },
  ],
  "Satellite engineer": [
    { id: "subsystem-evidence", label: "Subsystem evidence map", title: "Satellite subsystem evidence review", target: "Satellite / ground station", question: "Map which ADCS, EPS, communications, thermal, and operations conclusions are supported by public sources, and list the telemetry or design evidence still required.", output: "Subsystem evidence matrix with engineering gaps and next evidence tasks.", nextAction: "Attach design documents or telemetry for validation.", interpretation: "The public orbit record is an input to systems analysis, not a health report; close subsystem claims with design documents, test results, or telemetry." },
    { id: "ground-link", label: "Ground-link readiness", title: "Ground segment readiness review", target: "Satellite / ground station", question: "Assess public evidence relevant to a small-satellite ground link, including orbit context, station visibility, frequency considerations, and the missing link-budget inputs.", output: "Ground-segment checklist, source trail, and link-budget evidence gaps.", nextAction: "Start a link-budget evidence task.", interpretation: "Orbit context can inform visibility and contact planning, while frequency licensing, antenna performance, and link margin require mission-specific evidence." },
  ],
  "Space researcher": [
    { id: "source-landscape", label: "Source landscape", title: "CubeSat source landscape review", target: "Research source landscape", question: "Build a reproducible source landscape for CubeSat mission analysis. Rank primary sources, preserve retrieval times, and distinguish supported, derived, and unavailable claims.", output: "Cited source ledger, reproducibility manifest, and claim classifications.", nextAction: "Export the evidence package for peer review.", interpretation: "A reproducible result preserves the source URL, retrieval time, published epoch, transformation, and uncertainty boundary for every claim." },
    { id: "literature-gap", label: "Literature and evidence gap", title: "Small-spacecraft evidence gap review", target: "Research source landscape", question: "Identify what can be established from public orbital data and NASA small-spacecraft guidance, and what requires mission-specific documentation or operator telemetry.", output: "Research brief, references, and an explicit gap register.", nextAction: "Invite a subject-matter reviewer to fill gaps.", interpretation: "Use public guidance to frame the investigation, but do not generalize subsystem or mission performance from a reference document alone." },
  ],
};
