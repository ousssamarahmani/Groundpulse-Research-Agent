import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  ArrowUpRight,
  Check,
  ChevronDown,
  CircleDot,
  Clock3,
  Command,
  Database,
  FileText,
  Filter,
  Layers3,
  Menu,
  MoreHorizontal,
  Plus,
  Radar,
  Search,
  ShieldCheck,
  Signal,
  Sparkles,
  Target,
  X,
} from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  DashboardApiError,
  DashboardArtifact,
  DashboardRunSummary,
  artifactUrl,
  listDashboardArtifacts,
  listDashboardRuns,
} from "@/lib/dashboardApi";

const mark = "/assets/groundpulse-mark.png";

const nav = [
  { label: "Missions", icon: Radar },
  { label: "Evidence", icon: ShieldCheck },
  { label: "Packages", icon: Layers3 },
  { label: "Sources", icon: Database },
  { label: "Control plane", icon: Command },
];

type StageState = "done" | "active" | "queued";
type DashboardStage = { label: string; sub: string; state: StageState };

type EvidenceItem = {
  name: string;
  meta: string;
  type: "Verified" | "Derived" | "Gaps";
  status: string;
  tone: "verified" | "derived" | "gap";
};

function formatTime(value: string | null) {
  if (!value) return "—";
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function relativeTime(value: string | null) {
  if (!value) return "—";
  const seconds = Math.max(0, Math.round((Date.now() - new Date(value).getTime()) / 1000));
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.round(hours / 24)}d ago`;
}

function stagesForRun(run: DashboardRunSummary): DashboardStage[] {
  const hasSource = run.snapshot_ids.length > 0;
  const validated = run.validation_state === "passed";
  const released = run.status === "released";
  return [
    { label: "Frame request", sub: "Question structured", state: "done" },
    { label: "Discover sources", sub: hasSource ? `${run.snapshot_ids.length} approved snapshot${run.snapshot_ids.length === 1 ? "" : "s"}` : "Awaiting source snapshot", state: hasSource ? "done" : "active" },
    { label: "Validate evidence", sub: validated ? "Claim gate passed" : run.validation_state, state: validated ? "done" : "active" },
    { label: "Build package", sub: released ? `${run.artifact_ids.length} immutable package reference${run.artifact_ids.length === 1 ? "" : "s"}` : "Awaiting release", state: released ? "done" : "queued" },
  ];
}

function evidenceForRun(run: DashboardRunSummary, artifacts: DashboardArtifact[]): EvidenceItem[] {
  const sourceCount = run.snapshot_ids.length;
  const items: EvidenceItem[] = [];
  if (sourceCount > 0) {
    items.push({
      name: run.snapshot_ids[0],
      meta: `${sourceCount} approved source snapshot${sourceCount === 1 ? "" : "s"}`,
      type: "Verified",
      status: "Accepted",
      tone: "verified",
    });
  }
  if (artifacts.some((artifact) => artifact.name.endsWith("candidate_ledger.json"))) {
    items.push({ name: "Candidate claim ledger", meta: "Canonical claims with provenance fields", type: "Derived", status: "Traceable", tone: "derived" });
  }
  if (artifacts.some((artifact) => artifact.name.endsWith("gap_list.json"))) {
    items.push({ name: "Gap list", meta: "Unavailable evidence retained explicitly", type: "Gaps", status: "Disclosed", tone: "gap" });
  }
  return items;
}

export default function Dashboard() {
  const [activeNav, setActiveNav] = useState("Missions");
  const [activeTab, setActiveTab] = useState("Overview");
  const [filter, setFilter] = useState("All");
  const [menuOpen, setMenuOpen] = useState(false);
  const [requestOpen, setRequestOpen] = useState(false);
  const [requestTitle, setRequestTitle] = useState("Ground station coverage review");
  const [runs, setRuns] = useState<DashboardRunSummary[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [artifacts, setArtifacts] = useState<DashboardArtifact[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const selectedRun = runs.find((run) => run.run_id === selectedRunId) ?? runs[0] ?? null;

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    listDashboardRuns()
      .then((response) => {
        if (cancelled) return;
        setRuns(response.runs);
        setSelectedRunId((current) => current ?? response.runs[0]?.run_id ?? null);
        setError(null);
      })
      .catch((cause: unknown) => {
        if (cancelled) return;
        const message = cause instanceof DashboardApiError ? cause.message : "Dashboard API is unavailable";
        setError(message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!selectedRun) {
      setArtifacts([]);
      return;
    }
    let cancelled = false;
    listDashboardArtifacts(selectedRun.run_id)
      .then((response) => { if (!cancelled) setArtifacts(response.artifacts); })
      .catch(() => { if (!cancelled) setArtifacts([]); });
    return () => { cancelled = true; };
  }, [selectedRun?.run_id]);

  const stages = selectedRun ? stagesForRun(selectedRun) : [];
  const evidence = selectedRun ? evidenceForRun(selectedRun, artifacts) : [];
  const shownEvidence = filter === "All" ? evidence : evidence.filter((item) => item.type === filter);
  const packageArtifacts = useMemo(() => artifacts.filter((artifact) => artifact.name.includes("artifact/")).slice(0, 6), [artifacts]);

  const chooseNav = (label: string) => {
    setActiveNav(label);
    if (label !== "Missions") toast(`${label} module`, { description: "This module will use the same dashboard API contract." });
  };

  const submitRequest = () => {
    setRequestOpen(false);
    toast("Research request form", { description: `“${requestTitle || "Untitled request"}” submission will be connected to POST /runs next.` });
  };

  return (
    <div className="dash-shell">
      <aside className={`dash-sidebar ${menuOpen ? "open" : ""}`} aria-label="Research workspace navigation">
        <div className="dash-brand"><img src={mark} alt="GroundPulse mark" /><span><b>GROUNDPULSE</b><small>RESEARCH CONTROL</small></span><button className="dash-close" onClick={() => setMenuOpen(false)} aria-label="Close dashboard menu"><X size={18} /></button></div>
        <div className="workspace-chip"><span className="live-dot" /> WORKSPACE / CLOUD-RUN <ChevronDown size={14} /></div>
        <nav className="dash-nav">{nav.map(({ label, icon: Icon }) => <button className={activeNav === label ? "active" : ""} onClick={() => chooseNav(label)} key={label}><Icon size={17} /><span>{label}</span>{label === "Missions" && <b>{String(runs.length).padStart(2, "0")}</b>}</button>)}</nav>
        <div className="sidebar-bottom"><div className="control-status"><Signal size={15} /><span><b>{error ? "Dashboard API error" : "Cloud control plane"}</b><small>{error ?? "Live run data connected"}</small></span></div><a href="/"><ArrowLeft size={15} /> Product site</a></div>
      </aside>

      <main className="dash-main">
        <header className="dash-header"><div className="dash-heading"><button className="dash-menu" onClick={() => setMenuOpen(true)} aria-label="Open dashboard menu"><Menu size={20} /></button><div><p className="dash-eyebrow">RESEARCH WORKSPACE / LIVE RUN ARCHIVE</p><h1>Mission control</h1></div></div><div className="dash-actions"><button className="search-control" onClick={() => toast("Search", { description: "Run search will use the dashboard archive." })}><Search size={16} /><span>Search records</span><kbd>⌘ K</kbd></button><Button className="new-run" onClick={() => setRequestOpen(true)}><Plus size={16} /> New research</Button></div></header>

        {loading && <div className="dash-card" style={{ marginBottom: 18, padding: 18 }}>Loading live research runs…</div>}
        {error && <div className="dash-card" style={{ marginBottom: 18, padding: 18 }}>Dashboard API unavailable: {error}</div>}
        {!loading && !error && !selectedRun && <div className="dash-card" style={{ marginBottom: 18, padding: 18 }}>No research runs are available yet.</div>}

        {selectedRun && <>
          <section className="brief-bar"><div className="brief-mainline"><div className="brief-title"><div className="brief-signal"><Radar size={20} /><i /></div><div><p>GROUNDPULSE / RESEARCH EVIDENCE MISSION <span>{selectedRun.run_id}</span></p><h2>{selectedRun.object_name} evidence assessment</h2><small>{selectedRun.question}</small></div></div><div className="brief-metrics"><div><b>{String(selectedRun.snapshot_ids.length).padStart(2, "0")}</b><span>Approved snapshots</span></div><div><b>{String(artifacts.length).padStart(2, "02")}</b><span>Package objects</span></div><div className="mission-state"><span className="live-dot" /> {selectedRun.status}</div><button onClick={() => toast("Run metadata", { description: `Created ${formatTime(selectedRun.created_at)}` })} aria-label="Run metadata"><MoreHorizontal size={19} /></button></div></div><div className="brief-path" aria-label="Evidence mission path">{stages.map((stage, index) => <div className={stage.state} key={stage.label}><span>{String(index + 1).padStart(2, "0")}</span><b>{stage.label.replace(" ", " ")}</b><small>{stage.sub}</small></div>)}</div></section>

          <div className="dashboard-tabs"><div>{["Overview", "Evidence", "Package"].map((tab) => <button key={tab} className={activeTab === tab ? "active" : ""} onClick={() => setActiveTab(tab)}>{tab}</button>)}</div><p><Clock3 size={14} /> Last update {relativeTime(selectedRun.completed_at ?? selectedRun.started_at ?? selectedRun.created_at)}</p></div>

          <section className="dash-grid-primary">
            <article className="dash-card stage-card"><div className="card-label"><span>MISSION PATH / AGENT WORKFLOW</span><b>04 stages</b></div><div className="stage-list">{stages.map((stage, index) => <div className={`stage-row ${stage.state}`} key={stage.label}><div className="stage-index">{stage.state === "done" ? <Check size={14} /> : index + 1}</div><div><b>{stage.label}</b><small>{stage.sub}</small></div><span className="stage-state">{stage.state === "done" ? "Complete" : stage.state === "active" ? "Running" : "Queued"}</span></div>)}</div><div className="stage-footer"><ShieldCheck size={15} /> Claim release is gated by evidence validation.</div></article>

            <article className="dash-card brief-detail"><div className="card-label"><span>{activeTab === "Overview" ? "MISSION PARAMETERS" : activeTab === "Evidence" ? "CLAIM AUDIT" : "PACKAGE MANIFEST"}</span><button onClick={() => toast("Run details", { description: selectedRun.decision_intent })}><MoreHorizontal size={18} /></button></div>{activeTab === "Overview" ? <div className="parameter-grid"><div><span>OBJECT</span><b>{selectedRun.object_name}</b></div><div><span>NORAD ID</span><b>{selectedRun.norad_catalog_id ?? "Not supplied"}</b></div><div><span>WINDOW</span><b>UTC · {formatTime(selectedRun.created_at)}</b></div><div><span>INTENT</span><b>{selectedRun.decision_intent}</b></div></div> : activeTab === "Evidence" ? <div className="audit-panel"><div><ShieldCheck size={22} /><p><b>{selectedRun.validation_state === "passed" ? "Validation passed" : selectedRun.validation_state}</b><span>Canonical ledger and evidence rules are applied by the worker.</span></p></div><div><CircleDot size={22} /><p><b>{selectedRun.snapshot_ids.length} approved source snapshot{selectedRun.snapshot_ids.length === 1 ? "" : "s"}</b><span>{selectedRun.allowed_source_ids.join(", ") || "No source IDs"}</span></p></div><div><Target size={22} /><p><b>{selectedRun.artifact_ids.length} artifact reference{selectedRun.artifact_ids.length === 1 ? "" : "s"}</b><span>Immutable package metadata is available below.</span></p></div></div> : <div className="manifest-panel"><div><span>RUN ID</span><b>{selectedRun.run_id}</b></div><div><span>ARTIFACTS</span><b>{artifacts.length} immutable objects</b></div><div><span>RELEASE</span><b>{selectedRun.status}</b></div><button onClick={() => setActiveTab("Package")}>Preview package <ArrowUpRight size={14} /></button></div>}</article>

            <article className="dash-card confidence-card"><div className="card-label"><span>EVIDENCE STATE</span><b className={selectedRun.validation_state === "passed" ? "violet-text" : ""}>{selectedRun.validation_state}</b></div><div className="confidence-gauge"><div><strong>{selectedRun.validation_state === "passed" ? "OK" : "—"}</strong><span>validation gate</span></div></div><p>{selectedRun.error_code ? `${selectedRun.error_code}: ${selectedRun.review_reason ?? "review required"}` : "Run state and validation metadata are sourced from the research API."}</p><div className="confidence-legend"><span><i className="legend-verified" /> Supported</span><span><i className="legend-derived" /> Derived</span><span><i className="legend-gap" /> Gap</span></div></article>
          </section>

          <section className="dash-grid-secondary"><article className="dash-card ledger-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / EVIDENCE LEDGER</span></p><h2>Source review</h2></div><button className="filter-button" onClick={() => setFilter(filter === "All" ? "Verified" : "All")}><Filter size={14} /> {filter === "All" ? "Filter" : filter}</button></div><div className="ledger-tabs">{["All", "Verified", "Derived", "Gaps"].map((item) => <button className={filter === item ? "active" : ""} key={item} onClick={() => setFilter(item)}>{item}</button>)}</div><div className="ledger-list">{shownEvidence.length ? shownEvidence.map((item) => <button className="ledger-row" key={item.name} onClick={() => toast(item.name, { description: item.meta })}><span className={`ledger-dot ${item.tone}`} /><span className="ledger-copy"><b>{item.name}</b><small>{item.meta}</small></span><span className={`ledger-status ${item.tone}`}>{item.status}</span><ArrowUpRight size={14} /></button>) : <div className="ledger-row"><span className="ledger-copy"><b>No evidence records</b><small>The API returned no matching ledger entries.</small></span></div>}</div></article><article className="dash-card trace-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / RUN TRACE</span></p><h2>Execution events</h2></div><button onClick={() => toast("Trace refreshed", { description: "Run metadata is current." })}><span className="live-dot" /> Live</button></div><div className="trace-list">{[["REQUEST", "Request accepted", selectedRun.question], ["SOURCE", "Approved evidence selected", selectedRun.snapshot_ids.join(", ") || "Awaiting snapshot"], ["VALIDATION", "Claim gate evaluated", selectedRun.validation_state], ["PACKAGE", "Immutable package stored", selectedRun.status]].map(([time, title, description], index, rows) => <div className="trace-row" key={time}><div className="trace-time">{time}</div><div className="trace-line"><span className={index === rows.length - 1 ? "current" : ""} /></div><div><b>{title}</b><p>{description}</p></div></div>)}</div></article></section>

          <section className="dash-bottom-grid"><article className="dash-card packages-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / RECENT RUNS</span></p><h2>Research archive</h2></div><button onClick={() => setSelectedRunId(null)}>View all <ArrowUpRight size={14} /></button></div><div className="packages-table"><div className="packages-head"><span>RUN</span><span>STATE</span><span>UPDATED</span></div>{runs.slice(0, 4).map((run) => <button key={run.run_id} onClick={() => setSelectedRunId(run.run_id)}><FileText size={16} /><span><b>{run.run_id}</b><small>{run.object_name} · {run.validation_state}</small></span><em>{run.status}</em><time>{relativeTime(run.completed_at ?? run.created_at)}</time></button>)}</div></article><article className="dash-card gap-card"><div className="gap-icon"><Sparkles size={20} /></div><p className="card-label"><span>MISSION PATH / IMMUTABLE PACKAGE</span></p><h2>{packageArtifacts.length ? `${packageArtifacts.length} package objects available.` : "No package objects listed yet."}</h2><p>{packageArtifacts.length ? "Open an artifact through the authenticated Dashboard API boundary." : "Artifacts will appear after the run reaches released."}</p>{packageArtifacts[0] && <a href={artifactUrl(selectedRun.run_id, packageArtifacts[0].name)} target="_blank" rel="noreferrer">Open package artifact <ArrowUpRight size={14} /></a>}</article></section>
        </>}
      </main>

      {requestOpen && <div className="request-overlay" role="dialog" aria-modal="true" aria-label="New research request"><div className="request-panel"><div className="request-panel-head"><div><p className="dash-eyebrow">NEW AGENT RUN</p><h2>Frame a research request</h2></div><button onClick={() => setRequestOpen(false)} aria-label="Close request panel"><X size={19} /></button></div><label>Research title<input value={requestTitle} onChange={(event) => setRequestTitle(event.target.value)} /></label><div className="request-form-grid"><label>Target system<select defaultValue="Satellite / ground station"><option>Satellite / ground station</option><option>Space-weather context</option><option>Source landscape</option></select></label><label>Analysis window<select defaultValue="48 hours"><option>48 hours</option><option>7 days</option><option>Custom window</option></select></label></div><label>Question<textarea defaultValue="Assess available evidence for orbital coverage and ground-station context." /></label><div className="request-panel-foot"><span><Sparkles size={15} /> Validation rules enabled</span><Button onClick={submitRequest}>Stage research run <ArrowUpRight size={15} /></Button></div></div></div>}
    </div>
  );
}
