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
  FileText,
  Filter,
  Globe2,
  Layers3,
  Menu,
  MoreHorizontal,
  Plus,
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

const mark = "/assets/groundpulse-mark.png";

const nav = [
  { label: "Missions", icon: Radar },
  { label: "Evidence", icon: ShieldCheck },
  { label: "Packages", icon: Layers3 },
  { label: "Sources", icon: Database },
  { label: "Control plane", icon: Command },
];

const stages = [
  { label: "Frame request", sub: "Question structured", state: "done" },
  { label: "Discover sources", sub: "3 adapters returned", state: "done" },
  { label: "Validate evidence", sub: "Claim gate in progress", state: "active" },
  { label: "Build package", sub: "Awaiting release", state: "queued" },
];

const evidence = [
  { name: "Approved adapter fixture A", meta: "Interface-only source-review state", type: "Verified", status: "Accepted", tone: "verified" },
  { name: "Approved adapter fixture B", meta: "Interface-only source-review state", type: "Verified", status: "Accepted", tone: "verified" },
  { name: "Example derivation", meta: "Prototype representation of traceable inputs", type: "Derived", status: "Traceable", tone: "derived" },
  { name: "Example data gap", meta: "Prototype representation of unavailable evidence", type: "Gaps", status: "Unavailable", tone: "gap" },
];

const trace = [
  ["DEMO", "Request normalized", "Prototype mission brief parsed with an illustrative time window."],
  ["DEMO", "Adapter search completed", "Illustrative adapter fixtures returned local interface state."],
  ["DEMO", "Coverage validator running", "Prototype representation of provenance and metadata checks."],
  ["DEMO", "Claim gate held", "Illustrative gap remains visible in the prototype package."],
];

export default function Dashboard() {
  const [activeNav, setActiveNav] = useState("Missions");
  const [activeTab, setActiveTab] = useState("Overview");
  const [filter, setFilter] = useState("All");
  const [menuOpen, setMenuOpen] = useState(false);
  const [requestOpen, setRequestOpen] = useState(false);
  const [requestTitle, setRequestTitle] = useState("Ground station coverage review");

  const shownEvidence = filter === "All" ? evidence : evidence.filter((item) => item.type === filter);
  const chooseNav = (label: string) => {
    setActiveNav(label);
    if (label !== "Missions") toast(`${label} module selected`, { description: "This interactive product view uses a local presentation state." });
  };
  const submitRequest = () => {
    setRequestOpen(false);
    toast("Research run staged", { description: `“${requestTitle || "Untitled request"}” is ready for source discovery.` });
  };

  return (
    <div className="dash-shell">
      <aside className={`dash-sidebar ${menuOpen ? "open" : ""}`} aria-label="Research workspace navigation">
        <div className="dash-brand"><img src={mark} alt="GroundPulse mark" /><span><b>GROUNDPULSE</b><small>RESEARCH CONTROL</small></span><button className="dash-close" onClick={() => setMenuOpen(false)} aria-label="Close dashboard menu"><X size={18} /></button></div>
        <div className="workspace-chip"><span className="live-dot" /> WORKSPACE / PROTOTYPE-01 <ChevronDown size={14} /></div>
        <nav className="dash-nav">{nav.map(({ label, icon: Icon }) => <button className={activeNav === label ? "active" : ""} onClick={() => chooseNav(label)} key={label}><Icon size={17} /><span>{label}</span>{label === "Missions" && <b>04</b>}</button>)}</nav>
        <div className="sidebar-bottom"><div className="control-status"><Signal size={15} /><span><b>Prototype control plane</b><small>No live services connected</small></span></div><a href="/"><ArrowLeft size={15} /> Product site</a></div>
      </aside>

      <main className="dash-main">
        <header className="dash-header"><div className="dash-heading"><button className="dash-menu" onClick={() => setMenuOpen(true)} aria-label="Open dashboard menu"><Menu size={20} /></button><div><p className="dash-eyebrow">RESEARCH WORKSPACE / PROTOTYPE MISSION</p><h1>Mission control</h1></div></div><div className="dash-actions"><button className="search-control" onClick={() => toast("Search index ready", { description: "Source and package search will connect to the research archive when a backend is implemented." })}><Search size={16} /><span>Search records</span><kbd>⌘ K</kbd></button><Button className="new-run" onClick={() => setRequestOpen(true)}><Plus size={16} /> New research</Button></div></header>

        <section className="brief-bar"><div className="brief-mainline"><div className="brief-title"><div className="brief-signal"><Radar size={20} /><i /></div><div><p>GROUNDPULSE / PROTOTYPE EVIDENCE MISSION <span>RUN-DEMO</span></p><h2>Coverage assessment demo</h2><small>Illustrative request · no live source connection</small></div></div><div className="brief-metrics"><div><b>03</b><span>Example source states</span></div><div><b>01</b><span>Visible data gap</span></div><div className="mission-state"><span className="live-dot" /> Prototype</div><button onClick={() => toast("Mission menu", { description: "Run actions will be available in the connected control plane." })} aria-label="Mission options"><MoreHorizontal size={19} /></button></div></div><div className="brief-path" aria-label="Evidence mission path"><div className="complete"><span>01</span><b>Question</b><small>Framed</small></div><div className="complete"><span>02</span><b>Sources</b><small>Selected</small></div><div className="running"><span>03</span><b>Validation</b><small>Active gate</small></div><div><span>04</span><b>Package</b><small>Held for release</small></div></div></section>

        <div className="dashboard-tabs"><div>{["Overview", "Evidence", "Package"].map((tab) => <button key={tab} className={activeTab === tab ? "active" : ""} onClick={() => setActiveTab(tab)}>{tab}</button>)}</div><p><Clock3 size={14} /> Last agent event 14s ago</p></div>

        <section className="dash-grid-primary">
          <article className="dash-card stage-card"><div className="card-label"><span>MISSION PATH / AGENT WORKFLOW</span><b>04 stages</b></div><div className="stage-list">{stages.map((stage, index) => <div className={`stage-row ${stage.state}`} key={stage.label}><div className="stage-index">{stage.state === "done" ? <Check size={14} /> : index + 1}</div><div><b>{stage.label}</b><small>{stage.sub}</small></div><span className="stage-state">{stage.state === "done" ? "Complete" : stage.state === "active" ? "Running" : "Queued"}</span></div>)}</div><div className="stage-footer"><ShieldCheck size={15} /> Claim release is gated by evidence validation.</div></article>

          <article className="dash-card brief-detail"><div className="card-label"><span>{activeTab === "Overview" ? "MISSION PARAMETERS" : activeTab === "Evidence" ? "CLAIM AUDIT" : "PACKAGE MANIFEST"}</span><button onClick={() => toast("Brief editor", { description: "Mission parameters will be editable in the connected product." })}><MoreHorizontal size={18} /></button></div>{activeTab === "Overview" ? <div className="parameter-grid"><div><span>OBJECT</span><b>DEMO OBJECT</b></div><div><span>LOCATION</span><b>Illustrative coordinate</b></div><div><span>WINDOW</span><b>Illustrative time window</b></div><div><span>INTENT</span><b>Coverage context</b></div></div> : activeTab === "Evidence" ? <div className="audit-panel"><div><ShieldCheck size={22} /><p><b>2 fixture states accepted</b><span>Prototype representation only; no source records are connected.</span></p></div><div><CircleDot size={22} /><p><b>1 derivation traceable</b><span>Example state linked to illustrative inputs.</span></p></div><div><Target size={22} /><p><b>1 gap retained</b><span>Example of how unavailable evidence remains visible.</span></p></div></div> : <div className="manifest-panel"><div><span>PACKAGE ID</span><b>DEMO-PACKAGE</b></div><div><span>ARTIFACTS</span><b>Brief · Ledger · Manifest · Gaps</b></div><div><span>RELEASE</span><b>Held at evidence gate</b></div><button onClick={() => toast("Package preview", { description: "The generated package will appear here once the evidence gate clears." })}>Preview package <ArrowUpRight size={14} /></button></div>}</article>

          <article className="dash-card confidence-card"><div className="card-label"><span>EVIDENCE STATE</span><b className="violet-text">Updating</b></div><div className="confidence-gauge"><div><strong>78</strong><span>coverage score</span></div></div><p>Source coverage is sufficient for a research brief. One hardware calibration gap remains disclosed.</p><div className="confidence-legend"><span><i className="legend-verified" /> Supported</span><span><i className="legend-derived" /> Derived</span><span><i className="legend-gap" /> Gap</span></div></article>
        </section>

        <section className="dash-grid-secondary">
          <article className="dash-card ledger-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / EVIDENCE LEDGER</span></p><h2>Source review</h2></div><button className="filter-button" onClick={() => setFilter(filter === "All" ? "Verified" : "All")}><Filter size={14} /> {filter === "All" ? "Filter" : filter}</button></div><div className="ledger-tabs">{["All", "Verified", "Derived", "Gaps"].map((item) => <button className={filter === item ? "active" : ""} key={item} onClick={() => setFilter(item)}>{item}</button>)}</div><div className="ledger-list">{shownEvidence.map((item) => <button className="ledger-row" key={item.name} onClick={() => toast(item.name, { description: item.meta })}><span className={`ledger-dot ${item.tone}`} /><span className="ledger-copy"><b>{item.name}</b><small>{item.meta}</small></span><span className={`ledger-status ${item.tone}`}>{item.status}</span><ArrowUpRight size={14} /></button>)}</div></article>

          <article className="dash-card trace-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / AGENT TRACE</span></p><h2>Execution events</h2></div><button onClick={() => toast("Trace refreshed", { description: "Latest run events are already displayed." })}><span className="live-dot" /> Live</button></div><div className="trace-list">{trace.map(([time, title, description], index) => <div className="trace-row" key={time}><div className="trace-time">{time}</div><div className="trace-line"><span className={index === trace.length - 1 ? "current" : ""} /></div><div><b>{title}</b><p>{description}</p></div></div>)}</div></article>
        </section>

        <section className="dash-bottom-grid"><article className="dash-card packages-card"><div className="ledger-head"><div><p className="card-label"><span>MISSION PATH / RECENT PACKAGES</span></p><h2>Research artifacts</h2></div><a href="/">View all <ArrowUpRight size={14} /></a></div><div className="packages-table"><div className="packages-head"><span>PACKAGE</span><span>STATE</span><span>UPDATED</span></div><div><FileText size={16} /><span><b>GP-RUN-038</b><small>Ground station landscape</small></span><em>Released</em><time>2h ago</time></div><div><FileText size={16} /><span><b>GP-RUN-041</b><small>Space-weather context</small></span><em>Review</em><time>Yesterday</time></div></div></article><article className="dash-card gap-card"><div className="gap-icon"><Globe2 size={20} /></div><p className="card-label"><span>MISSION PATH / VISIBLE DATA GAP</span></p><h2>Receiver gain record not found.</h2><p>GroundPulse keeps the missing calibration source in the final brief rather than extending a claim beyond the evidence.</p><button onClick={() => toast("Gap task created", { description: "A human evidence request has been added to the mission backlog." })}>Assign evidence task <Send size={14} /></button></article></section>
      </main>

      {requestOpen && <div className="request-overlay" role="dialog" aria-modal="true" aria-label="New research request"><div className="request-panel"><div className="request-panel-head"><div><p className="dash-eyebrow">NEW AGENT RUN</p><h2>Frame a research request</h2></div><button onClick={() => setRequestOpen(false)} aria-label="Close request panel"><X size={19} /></button></div><label>Research title<input value={requestTitle} onChange={(event) => setRequestTitle(event.target.value)} /></label><div className="request-form-grid"><label>Target system<select defaultValue="Satellite / ground station"><option>Satellite / ground station</option><option>Space-weather context</option><option>Source landscape</option></select></label><label>Analysis window<select defaultValue="48 hours"><option>48 hours</option><option>7 days</option><option>Custom window</option></select></label></div><label>Question<textarea defaultValue="Assess available evidence for orbital coverage and ground-station context." /></label><div className="request-panel-foot"><span><Sparkles size={15} /> Validation rules enabled</span><Button onClick={submitRequest}>Stage research run <ArrowUpRight size={15} /></Button></div></div></div>}
    </div>
  );
}
