/**
 * Design reminder — GroundPulse Mission Control:
 * An operational SpaceTech research workspace: deep ink, hairline instrumentation,
 * violet only for active state, and every interaction tied to a research artifact.
 */
import { useState } from "react";
import {
  ArrowLeft,
  ArrowUpRight,
  Check,
  ChevronDown,
  CircleDot,
  Clock3,
  Command,
  Database,
  Download,
  FileText,
  Filter,
  Globe2,
  Layers3,
  Menu,
  MoreHorizontal,
  Play,
  Plus,
  Printer,
  Radar,
  Search,
  Send,
  ShieldCheck,
  Signal,
  Sparkles,
  Target,
  X,
} from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { trpc } from "@/lib/trpc";
import { buildResearchPackageHtml } from "@/lib/researchPackage";
import { profileScenarios, type Audience } from "@/lib/researchScenarios";
import { buildOrbitalVisualizationModel } from "@/lib/orbitalVisualization";

const mark = "/manus-storage/groundpulse-mark_385613b6.png";
const CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=JSON";

const nav = [
  { label: "Missions", icon: Radar },
  { label: "Evidence", icon: ShieldCheck },
  { label: "Packages", icon: Layers3 },
  { label: "Sources", icon: Database },
  { label: "Control plane", icon: Command },
];

const demoStages = [
  { label: "Frame request", sub: "Question structured", state: "done" },
  { label: "Discover sources", sub: "3 adapters returned", state: "done" },
  { label: "Validate evidence", sub: "Claim gate in progress", state: "active" },
  { label: "Build package", sub: "Awaiting release", state: "queued" },
];

const demoEvidence = [
  { name: "Approved adapter fixture A", meta: "Interface-only source-review state", type: "Verified", status: "Accepted", tone: "verified" },
  { name: "Approved adapter fixture B", meta: "Interface-only source-review state", type: "Verified", status: "Accepted", tone: "verified" },
  { name: "Example derivation", meta: "Prototype representation of traceable inputs", type: "Derived", status: "Traceable", tone: "derived" },
  { name: "Example data gap", meta: "Prototype representation of unavailable evidence", type: "Gaps", status: "Unavailable", tone: "gap" },
];

const demoTrace: [string, string, string][] = [
  ["DEMO", "Request normalized", "Prototype mission brief parsed with an illustrative time window."],
  ["DEMO", "Adapter search completed", "Illustrative adapter fixtures returned local interface state."],
  ["DEMO", "Coverage validator running", "Prototype representation of provenance and metadata checks."],
  ["DEMO", "Claim gate held", "Illustrative gap remains visible in the prototype package."],
];

export default function Dashboard() {
  const [activeNav, setActiveNav] = useState("Missions");
  const [activeTab, setActiveTab] = useState(() => new URLSearchParams(window.location.search).get("tab") === "package" ? "Package" : "Overview");
  const [filter, setFilter] = useState("All");
  const [menuOpen, setMenuOpen] = useState(false);
  const [requestOpen, setRequestOpen] = useState(false);
  const [requestTitle, setRequestTitle] = useState("CubeSat orbit readiness review");
  const [audience, setAudience] = useState<Audience>("CubeSat analyst");
  const [scenarioId, setScenarioId] = useState("orbit-readiness");
  const activeScenario = profileScenarios[audience].find((scenario) => scenario.id === scenarioId) ?? profileScenarios[audience][0];
  const [sampleRunState, setSampleRunState] = useState<"ready" | "running" | "released">("ready");
  const { data: liveRecord, isLoading: sourceLoading } = trpc.celestrak.latest.useQuery({ noradId: 25544 }, { retry: 1, staleTime: 300_000 });
  const liveStatus = sourceLoading ? "loading" : liveRecord ? "live" : "fallback";
  const usingLive = liveRecord !== undefined;
  const orbitalVisual = buildOrbitalVisualizationModel(usingLive ? liveRecord : undefined);
  const displayRunId = usingLive ? `LIVE-CELESTRAK-${liveRecord.noradId}` : "RUN-DEMO";
  const sourceStatus = usingLive ? "Live CelesTrak GP/OMM" : liveStatus === "loading" ? "Connecting to CelesTrak…" : "Fallback fixture · source unavailable";
  const stages = usingLive ? [
    { label: "Frame request", sub: "Question structured", state: "done" },
    { label: "Read GP/OMM", sub: `Epoch ${liveRecord.epoch.slice(0, 10)}`, state: "done" },
    { label: "Validate evidence", sub: "Source metadata checked", state: "done" },
    { label: "Build package", sub: "Research package ready", state: "done" },
  ] : sampleRunState === "released" ? [
    { label: "Frame request", sub: "Question structured", state: "done" },
    { label: "Discover sources", sub: "3 adapters returned", state: "done" },
    { label: "Validate evidence", sub: "Claim gate passed with gaps", state: "done" },
    { label: "Build package", sub: "Research package ready", state: "done" },
  ] : demoStages;
  const evidence = usingLive ? [
    { name: "CelesTrak GP/OMM snapshot", meta: `${liveRecord.objectName} · retrieved ${new Date(liveRecord.retrievedAt).toLocaleTimeString()}`, type: "Verified", status: "Accepted", tone: "verified" },
    { name: "Published orbital epoch", meta: `${liveRecord.epoch} · NORAD ${liveRecord.noradId}`, type: "Verified", status: "Traceable", tone: "verified" },
    { name: "Derived orbital period", meta: `1440 / ${liveRecord.meanMotion.toFixed(5)} = ${liveRecord.orbitalPeriodMinutes.toFixed(2)} minutes`, type: "Derived", status: "Traceable", tone: "derived" },
    { name: "Live telemetry gap", meta: "CelesTrak GP/OMM does not provide spacecraft health or station telemetry.", type: "Gaps", status: "Unavailable", tone: "gap" },
  ] : demoEvidence;
  const trace = usingLive ? [
    ["NOW", "CelesTrak GP/OMM retrieved", `${liveRecord.objectName} · live server proxy · ${liveRecord.retrievedAt}`],
    ["SOURCE", "Published epoch preserved", `${liveRecord.epoch} · NORAD ${liveRecord.noradId}`],
    ["DERIVE", "Orbital period calculated", `1440 / mean motion = ${liveRecord.orbitalPeriodMinutes.toFixed(2)} minutes`],
    ["GAP", "Operational telemetry unavailable", "The missing evidence remains visible rather than inferred."],
  ] as [string, string, string][] : demoTrace;
  const shownEvidence = filter === "All" ? evidence : evidence.filter((item) => item.type === filter);
  const chooseNav = (label: string) => {
    setActiveNav(label);
    if (label !== "Missions") toast(`${label} module selected`, { description: "This interactive product view uses a local presentation state." });
  };
  const submitRequest = () => {
    setRequestOpen(false);
    toast("Research run staged", { description: `“${requestTitle || "Untitled request"}” is ready for source discovery.` });
  };
  const downloadResearchPackage = () => {
    const blob = new Blob([buildResearchPackageHtml({ runId: displayRunId, record: usingLive ? liveRecord : undefined, audience, scenario: activeScenario.label })], { type: "text/html;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `groundpulse-${displayRunId.toLowerCase()}-research-package.html`;
    anchor.click();
    URL.revokeObjectURL(url);
    toast("Research package downloaded", { description: "Open the HTML file and choose Print → Save as PDF for a shareable PDF." });
  };
  const printResearchPackage = () => {
    const reportWindow = window.open("", "_blank", "noopener,noreferrer");
    if (!reportWindow) {
      toast("Pop-up blocked", { description: "Allow pop-ups to print the research package." });
      return;
    }
    reportWindow.document.write(buildResearchPackageHtml({ runId: displayRunId, record: usingLive ? liveRecord : undefined, audience, scenario: activeScenario.label }));
    reportWindow.document.close();
    reportWindow.focus();
    reportWindow.print();
  };
  const replaySampleRun = () => {
    if (sampleRunState === "running") return;
    setSampleRunState("running");
    window.setTimeout(() => setSampleRunState("released"), 900);
    toast("Sample run replay started", { description: "The deterministic workflow is moving through its evidence gate." });
  };

  return (
    <div className="dash-shell">
      <aside className={`dash-sidebar ${menuOpen ? "open" : ""}`} aria-label="Research workspace navigation">
        <div className="dash-brand"><img src={mark} alt="GroundPulse mark" /><span><b>GROUNDPULSE</b><small>RESEARCH CONTROL</small></span><button className="dash-close" onClick={() => setMenuOpen(false)} aria-label="Close dashboard menu"><X size={18} /></button></div>
        <div className="workspace-chip"><span className={`live-dot ${usingLive ? "live" : ""}`} /> WORKSPACE / {usingLive ? "CELESTRAK-LIVE" : "PROTOTYPE-01"} <ChevronDown size={14} /></div>
        <nav className="dash-nav">{nav.map(({ label, icon: Icon }) => <button className={activeNav === label ? "active" : ""} onClick={() => chooseNav(label)} key={label}><Icon size={17} /><span>{label}</span>{label === "Missions" && <b>04</b>}</button>)}</nav>
        <div className="sidebar-bottom"><div className="control-status"><Signal size={15} /><span><b>{usingLive ? "CelesTrak source link" : "Source connection"}</b><small>{sourceStatus}</small></span></div><a href="/"><ArrowLeft size={15} /> Product site</a></div>
      </aside>

      <main className="dash-main">
        <header className="dash-header"><div className="dash-heading"><button className="dash-menu" onClick={() => setMenuOpen(true)} aria-label="Open dashboard menu"><Menu size={20} /></button><div><p className="dash-eyebrow">RESEARCH WORKSPACE / {usingLive ? "LIVE SOURCE SESSION" : "SOURCE SESSION"}</p><h1>Mission control</h1></div></div><div className="dash-actions"><button className="search-control" onClick={() => toast("Search index ready", { description: usingLive ? "CelesTrak GP/OMM source session is available." : "Live source is unavailable; showing the explicit fallback fixture." })}><Search size={16} /><span>Search records</span><kbd>⌘ K</kbd></button><Button className="new-run" onClick={() => setRequestOpen(true)}><Plus size={16} /> New research</Button></div></header>

        <section className="brief-bar"><div className="brief-mainline"><div className="brief-title"><div className="brief-signal"><Radar size={20} /><i /></div><div><p>GROUNDPULSE / {usingLive ? "CELESTRAK GP/OMM MISSION" : "SOURCE SESSION"} <span>{displayRunId}</span></p><h2>{usingLive ? `${liveRecord.objectName} orbital context` : liveStatus === "loading" ? "Connecting to CelesTrak" : "Source unavailable · fallback view"}</h2><small>{usingLive ? `Live source retrieved · epoch ${liveRecord.epoch}` : sourceStatus}</small></div></div><div className="brief-metrics"><div><b>{usingLive ? "01" : "00"}</b><span>{usingLive ? "Live source" : "Source states"}</span></div><div><b>01</b><span>Visible data gap</span></div><div className="mission-state"><span className={`live-dot ${usingLive ? "live" : ""}`} /> {usingLive ? "Live source" : liveStatus === "loading" ? "Connecting" : "Fallback"}</div><button onClick={() => toast("Mission menu", { description: "Run actions will be available in the connected control plane." })} aria-label="Mission options"><MoreHorizontal size={19} /></button></div></div><div className="brief-path" aria-label="Evidence mission path"><div className="complete"><span>01</span><b>Question</b><small>Framed</small></div><div className="complete"><span>02</span><b>{usingLive ? "CelesTrak" : "Sources"}</b><small>{usingLive ? "GP/OMM retrieved" : "Awaiting source"}</small></div><div className={usingLive || sampleRunState === "released" ? "complete" : "running"}><span>03</span><b>Validation</b><small>{usingLive ? "Metadata checked" : sampleRunState === "released" ? "Claim gate passed" : "Active gate"}</small></div><div className={usingLive || sampleRunState === "released" ? "complete" : ""}><span>04</span><b>Package</b><small>{usingLive || sampleRunState === "released" ? "Ready for review" : "Held for release"}</small></div></div></section>

        <div className="dashboard-tabs"><div>{["Overview", "Evidence", "Package"].map((tab) => <button key={tab} className={activeTab === tab ? "active" : ""} onClick={() => setActiveTab(tab)}>{tab}</button>)}</div><p><Clock3 size={14} /> {sampleRunState === "ready" ? "Replay ready" : sampleRunState === "running" ? "Agent event now" : "Released 2s ago"}</p></div>

        <section className={`proof-console ${sampleRunState} ${usingLive ? "live-source" : "fallback-source"}`} aria-label="Live source proof">
          <div className="proof-console-copy"><p className="card-label"><span>{usingLive ? "PROOF OF SOURCE / CELESTRAK GP/OMM" : "SOURCE STATUS / FALLBACK"}</span><b>{usingLive ? "LIVE" : liveStatus === "loading" ? "CONNECTING" : "UNAVAILABLE"}</b></p><h2>{usingLive ? "A real orbital record is in the workspace." : "The live source is not available."}</h2><p>{usingLive ? "The Workspace is using a fresh CelesTrak GP/OMM response with its published epoch preserved." : "No source values are presented as live until CelesTrak responds."}</p></div>
          <button className="proof-replay-button" onClick={replaySampleRun} disabled={usingLive || sampleRunState === "running"}><Play size={15} fill="currentColor" /> {usingLive ? "Source loaded" : sampleRunState === "running" ? "Replaying fallback" : "Replay fallback"}</button>
          <div className="proof-console-path"><div className="proof-node complete"><Check size={13} /><span>Request</span></div><i /><div className={`proof-node ${usingLive ? "complete" : sampleRunState === "ready" ? "active" : "complete"}`}>{usingLive || sampleRunState !== "ready" ? <Check size={13} /> : <Radar size={13} />}<span>{usingLive ? "Source read" : "Evidence gate"}</span></div><i /><div className={`proof-node ${usingLive || sampleRunState === "released" ? "complete" : "queued"}`}>{usingLive || sampleRunState === "released" ? <Check size={13} /> : <span className="empty-node" />}<span>{usingLive ? "Package ready" : "Package"}</span></div></div>
          <span className="proof-console-note">{usingLive ? `${displayRunId} · live source session` : `${displayRunId} · ${sourceStatus}`}</span>
        </section>

        <section className="dash-grid-primary">
          <article className="dash-card stage-card"><div className="card-label"><span>MISSION PATH / AGENT WORKFLOW</span><b>04 stages</b></div><div className="stage-list">{stages.map((stage, index) => <div className={`stage-row ${stage.state}`} key={stage.label}><div className="stage-index">{stage.state === "done" ? <Check size={14} /> : index + 1}</div><div><b>{stage.label}</b><small>{stage.sub}</small></div><span className="stage-state">{stage.state === "done" ? "Complete" : stage.state === "active" ? "Running" : "Queued"}</span></div>)}</div><div className="stage-footer"><ShieldCheck size={15} /> Claim release is gated by evidence validation.</div></article>

          <article className="dash-card brief-detail"><div className="card-label"><span>{activeTab === "Overview" ? "MISSION PARAMETERS" : activeTab === "Evidence" ? "CLAIM AUDIT" : "PACKAGE MANIFEST"}</span><button onClick={() => toast("Brief editor", { description: "Mission parameters will be editable in the connected product." })}><MoreHorizontal size={18} /></button></div>{activeTab === "Overview" ? <div className="parameter-grid"><div><span>OBJECT</span><b>{usingLive ? liveRecord.objectName : "Awaiting source"}</b></div><div><span>OBJECT ID</span><b>{usingLive ? liveRecord.objectId : "Not available"}</b></div><div><span>EPOCH</span><b>{usingLive ? liveRecord.epoch : "Not available"}</b></div><div><span>MEAN MOTION</span><b>{usingLive ? `${liveRecord.meanMotion.toFixed(5)} rev/day` : "Not available"}</b></div></div> : activeTab === "Evidence" ? <div className="audit-panel"><div><ShieldCheck size={22} /><p><b>{usingLive ? "1 live source accepted" : "Source not connected"}</b><span>{usingLive ? "CelesTrak GP/OMM response validated in the browser." : "Showing the explicit fallback while CelesTrak is unavailable."}</span></p></div><div><CircleDot size={22} /><p><b>{usingLive ? "1 derivation traceable" : "No live derivation"}</b><span>{usingLive ? `Orbital period = ${liveRecord.orbitalPeriodMinutes.toFixed(2)} minutes.` : "No source values are being represented as live."}</span></p></div><div><Target size={22} /><p><b>1 gap retained</b><span>Health and station telemetry are not provided by GP/OMM.</span></p></div></div> : <div className="research-package"><div className="package-actions"><div><span className="package-kicker">ENGINEERING RESEARCH PACKAGE / {usingLive ? "SOURCE-BACKED" : "DRAFT WITH GAPS"}</span><span className="package-audience">{audience} · {activeScenario.label}</span><h2>{usingLive ? `${liveRecord.objectName} mission engineering brief` : "Satellite mission engineering brief"}</h2><p>Structured for {audience.toLowerCase()}s: {activeScenario.output} The package keeps unsupported operational claims visible as gaps.</p></div><div className="package-buttons"><Button variant="outline" onClick={downloadResearchPackage}><Download size={14} /> Download package</Button><Button onClick={printResearchPackage}><Printer size={14} /> Print / Save PDF</Button></div></div><div className="package-summary-grid"><div><span>RUN</span><b>{displayRunId}</b></div><div><span>SOURCE</span><b>{usingLive ? "CelesTrak GP/OMM" : "Awaiting source"}</b></div><div><span>EPOCH</span><b>{usingLive ? liveRecord.epoch : "Not available"}</b></div><div><span>DERIVED</span><b>{usingLive ? `${liveRecord.orbitalPeriodMinutes.toFixed(2)} min period` : "No derivation"}</b></div></div><div className="orbital-visual"><div><span className="package-kicker">ORBITAL TIMING / DERIVED VIEW</span><b>{usingLive ? "One normalized orbital cycle" : "Waiting for orbital record"}</b><p>{usingLive ? "A timing visualization derived from mean motion; it is not a ground-track or spacecraft-health prediction." : "The cycle view will appear when mean motion is retrieved."}</p><small className="orbit-freshness">SOURCE FRESHNESS · {orbitalVisual.freshnessLabel}</small></div><div className="orbit-plot" aria-label="Normalized orbital cycle timing visualization"><svg viewBox="0 0 420 112" role="img"><path d="M10 82 C48 18 86 18 124 82 S200 146 238 82 S314 18 352 82 S390 146 410 82" /><line x1="10" y1="92" x2="410" y2="92" /><circle cx="124" cy="82" r="4" /><circle cx="238" cy="82" r="4" /><circle cx="352" cy="82" r="4" /></svg><div className="orbit-scale"><span>0 min</span><b>{orbitalVisual.periodLabel}</b><span>{orbitalVisual.meanMotionLabel}</span></div></div></div><div className="package-section"><div className="package-section-head"><span>01 / EXECUTIVE BRIEF</span><b>{activeScenario.nextAction}</b></div><p>{activeScenario.question} This review distinguishes observed orbital evidence from engineering interpretation. It is not a spacecraft health certification or a substitute for mission documentation.</p><div className="analyst-interpretation"><span>ANALYST INTERPRETATION</span><b>{activeScenario.interpretation}</b></div></div><div className="package-section"><div className="package-section-head"><span>02 / SUBSYSTEM REVIEW</span><b>What an engineer can act on</b></div><div className="engineering-table"><div><b>ADCS / GNC</b><span>Orbit context supports propagation and pass-planning inputs.</span><em>Needs attitude mode, pointing error, sensors, actuators, and control logs.</em></div><div><b>EPS</b><span>GP/OMM does not support an EPS conclusion.</span><em>Needs power budget, battery state, eclipse model, and solar-array telemetry.</em></div><div><b>Communications</b><span>Orbit context can inform contact-window analysis.</span><em>Needs frequency coordination, link budget, modem configuration, and station availability.</em></div><div><b>Thermal / structures</b><span>GP/OMM does not support thermal or structural conclusions.</span><em>Needs thermal model, materials, load cases, qualification, and flight telemetry.</em></div></div></div><div className="package-section package-gap"><div className="package-section-head"><span>03 / VISIBLE DATA GAP</span><b>Human evidence task required</b></div><p>CelesTrak GP/OMM provides orbital elements, not spacecraft health, subsystem performance, or ground-station telemetry. GroundPulse retains this gap instead of inferring a mission conclusion.</p></div><div className="package-section package-references"><div className="package-section-head"><span>04 / REFERENCES</span><b>Public sources</b></div><a href="https://celestrak.org/NORAD/documentation/gp-data-formats.php" target="_blank" rel="noreferrer">[1] CelesTrak GP data formats and OMM fields <ArrowUpRight size={13} /></a><a href="https://www.nasa.gov/kennedy/launch-services-program/cubesat-launch-initiative/cubesat-launch-initiative-resources/" target="_blank" rel="noreferrer">[2] NASA CubeSat Launch Initiative resources <ArrowUpRight size={13} /></a><a href="https://www.nasa.gov/smallsat-institute/sst-soa/" target="_blank" rel="noreferrer">[3] NASA State-of-the-Art Small Spacecraft Technology <ArrowUpRight size={13} /></a></div></div>}</article>

          <article className="dash-card confidence-card"><div className="card-label"><span>EVIDENCE STATE</span><b className="violet-text">{usingLive ? "Verified" : "Updating"}</b></div><div className="confidence-gauge"><div><strong>{usingLive ? "01" : "—"}</strong><span>{usingLive ? "source verified" : "coverage"}</span></div></div><p>{usingLive ? "CelesTrak GP/OMM is available with epoch and retrieval metadata; operational telemetry remains a documented gap." : "A source-backed view will appear when CelesTrak responds."}</p><div className="confidence-legend"><span><i className="legend-verified" /> Supported</span><span><i className="legend-derived" /> Derived</span><span><i className="legend-gap" /> Gap</span></div></article>
        </section>

        <section className="dash-grid-secondary">
          <article className="dash-card ledger-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / EVIDENCE LEDGER</span></p><h2>Source review</h2></div><button className="filter-button" onClick={() => setFilter(filter === "All" ? "Verified" : "All")}><Filter size={14} /> {filter === "All" ? "Filter" : filter}</button></div><div className="ledger-tabs">{["All", "Verified", "Derived", "Gaps"].map((item) => <button className={filter === item ? "active" : ""} key={item} onClick={() => setFilter(item)}>{item}</button>)}</div><div className="ledger-list">{shownEvidence.map((item) => <button className="ledger-row" key={item.name} onClick={() => toast(item.name, { description: item.meta })}><span className={`ledger-dot ${item.tone}`} /><span className="ledger-copy"><b>{item.name}</b><small>{item.meta}</small></span><span className={`ledger-status ${item.tone}`}>{item.status}</span><ArrowUpRight size={14} /></button>)}</div></article>

          <article className="dash-card trace-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / AGENT TRACE</span></p><h2>Execution events</h2></div><button onClick={() => toast("Trace refreshed", { description: "Latest run events are already displayed." })}><span className="live-dot" /> Live</button></div><div className="trace-list">{trace.map(([time, title, description], index) => <div className="trace-row" key={time}><div className="trace-time">{time}</div><div className="trace-line"><span className={index === trace.length - 1 ? "current" : ""} /></div><div><b>{title}</b><p>{description}</p></div></div>)}</div></article>
        </section>

        <section className="dash-bottom-grid"><article className="dash-card packages-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / SOURCE RECORDS</span></p><h2>{usingLive ? "CelesTrak record" : "Source records"}</h2></div><a href={CELESTRAK_URL} target="_blank" rel="noreferrer">Open source <ArrowUpRight size={14} /></a></div><div className="packages-table"><div className="packages-head"><span>RECORD</span><span>STATE</span><span>UPDATED</span></div><div><FileText size={16} /><span><b>{usingLive ? displayRunId : "No live record"}</b><small>{usingLive ? `${liveRecord.objectName} · NORAD ${liveRecord.noradId}` : sourceStatus}</small></span><em>{usingLive ? "Verified" : "Waiting"}</em><time>{usingLive ? new Date(liveRecord.retrievedAt).toLocaleTimeString() : "—"}</time></div></div></article><article className="dash-card gap-card"><div className="gap-icon"><Globe2 size={20} /></div><p className="card-label"><span>MISSION PATH / VISIBLE DATA GAP</span></p><h2>{usingLive ? "Operational telemetry not provided." : "Live source unavailable."}</h2><p>{usingLive ? "CelesTrak GP/OMM provides orbital elements, not spacecraft health, receiver gain, or ground-station telemetry." : "GroundPulse keeps missing evidence visible instead of replacing it with generated values."}</p><button onClick={() => toast("Gap task created", { description: "A human evidence request has been added to the mission backlog." })}>Assign evidence task <Send size={14} /></button></article></section>
      </main>

      {requestOpen && <div className="request-overlay" role="dialog" aria-modal="true" aria-label="New research request"><div className="request-panel"><div className="request-panel-head"><div><p className="dash-eyebrow">NEW AGENT RUN</p><h2>Frame a research request</h2></div><button onClick={() => setRequestOpen(false)} aria-label="Close request panel"><X size={19} /></button></div><label>Research role<select value={audience} onChange={(event) => { const nextAudience = event.target.value as Audience; setAudience(nextAudience); setScenarioId(profileScenarios[nextAudience][0].id); setRequestTitle(profileScenarios[nextAudience][0].title); }}><option>CubeSat analyst</option><option>Satellite engineer</option><option>Space researcher</option></select></label><label>Research scenario<select value={activeScenario.id} onChange={(event) => { const next = profileScenarios[audience].find((scenario) => scenario.id === event.target.value) ?? activeScenario; setScenarioId(next.id); setRequestTitle(next.title); }} >{profileScenarios[audience].map((scenario) => <option key={scenario.id} value={scenario.id}>{scenario.label}</option>)}</select></label><label>Research title<input value={requestTitle} onChange={(event) => setRequestTitle(event.target.value)} /></label><div className="request-form-grid"><label>Target system<select defaultValue={activeScenario.target}><option>CubeSat / small satellite</option><option>Satellite / ground station</option><option>Research source landscape</option></select></label><label>Analysis window<select defaultValue="48 hours"><option>48 hours</option><option>7 days</option><option>30 days</option></select></label></div><label>Question<textarea value={activeScenario.question} readOnly /></label><div className="scenario-output"><span>EXPECTED OUTPUT</span><b>{activeScenario.output}</b></div><div className="request-panel-foot"><span><Sparkles size={15} /> Validation rules enabled</span><Button onClick={submitRequest}>Stage research run <ArrowUpRight size={15} /></Button></div></div></div>}
    </div>
  );
}
