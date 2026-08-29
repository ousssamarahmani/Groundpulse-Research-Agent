export type ResearchPackageRecord = {
  objectName: string;
  epoch: string;
  orbitalPeriodMinutes: number;
};

export function buildResearchPackageHtml({
  runId,
  record,
  audience,
  scenario,
  generatedAt = new Date().toISOString(),
}: {
  runId: string;
  record?: ResearchPackageRecord;
  audience?: string;
  scenario?: string;
  generatedAt?: string;
}) {
  const objectName = record?.objectName ?? "Selected satellite (awaiting source)";
  const role = audience ?? "Satellite analyst";
  const scenarioName = scenario ?? "Evidence-first engineering review";
  const epoch = record?.epoch ?? "Not available until CelesTrak responds";
  const orbitalPeriod = record ? `${record.orbitalPeriodMinutes.toFixed(2)} minutes` : "Not available until mean motion is retrieved";
  const evidence = record ? "Supported by CelesTrak GP/OMM" : "Unavailable";
  const derived = record ? "Derived: 1440 / mean motion" : "Unavailable";

  return `<!doctype html><html><head><meta charset="utf-8"><title>GroundPulse Research Package</title><style>body{font:15px Arial,sans-serif;max-width:900px;margin:40px auto;color:#18202d;line-height:1.55}h1,h2{font-family:Arial}h1{border-bottom:3px solid #7650db;padding-bottom:12px}table{width:100%;border-collapse:collapse;margin:18px 0}th,td{border:1px solid #ccd2dc;padding:9px;text-align:left;vertical-align:top}th{background:#f0edff}.meta{color:#556070}.gap{background:#fff4e7;padding:14px;border-left:4px solid #d7892e}.source{font-size:13px}</style></head><body><h1>GroundPulse Satellite Engineering Research Package</h1><p class="meta">Run ${runId} · ${role} · ${scenarioName} · Generated ${generatedAt} · Evidence-first review</p><h2>Executive brief</h2><p>This package separates observed orbital evidence, engineering interpretation, and unresolved mission evidence. It is not a spacecraft health certification or a substitute for mission documentation.</p><h2>Orbital context</h2><table><tr><th>Field</th><th>Value</th><th>Evidence class</th></tr><tr><td>Object</td><td>${objectName}</td><td>${evidence}</td></tr><tr><td>Published epoch</td><td>${epoch}</td><td>${record ? "Supported" : "Unavailable"}</td></tr><tr><td>Orbital period</td><td>${orbitalPeriod}</td><td>${derived}</td></tr></table><h2>Engineering review map</h2><table><tr><th>Subsystem</th><th>What this review can establish</th><th>Required evidence still missing</th></tr><tr><td>ADCS / GNC</td><td>Orbit context can support propagation and pass-planning inputs.</td><td>Attitude mode, pointing error, sensors, actuators, and control logs.</td></tr><tr><td>EPS</td><td>No EPS conclusion is supported by GP/OMM.</td><td>Power budget, battery state, eclipse model, and solar-array telemetry.</td></tr><tr><td>Communications</td><td>Orbit context can inform contact-window analysis.</td><td>Frequency coordination, link budget, modem configuration, and ground-station availability.</td></tr><tr><td>Thermal / structures</td><td>No thermal or structural conclusion is supported by GP/OMM.</td><td>Thermal model, materials, load cases, qualification, and flight telemetry.</td></tr><tr><td>Mission operations</td><td>Source freshness and provenance can be audited.</td><td>Operations concept, command history, anomaly log, and operator-approved constraints.</td></tr></table><div class="gap"><strong>Visible gap:</strong> CelesTrak GP/OMM provides orbital elements, not spacecraft health, subsystem performance, or ground-station telemetry.</div><h2>References</h2><p class="source">[1] CelesTrak GP data formats: https://celestrak.org/NORAD/documentation/gp-data-formats.php</p><p class="source">[2] NASA CubeSat Launch Initiative resources: https://www.nasa.gov/kennedy/launch-services-program/cubesat-launch-initiative/cubesat-launch-initiative-resources/</p><p class="source">[3] NASA State-of-the-Art Small Spacecraft Technology: https://www.nasa.gov/smallsat-institute/sst-soa/</p></body></html>`;
}
