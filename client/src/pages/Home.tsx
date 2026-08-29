/**
 * Design reminder — GroundPulse Product Mission Room:
 * YC-style product clarity on an evidence-first SpaceTech operating surface.
 */
import { useState } from "react";
import {
  ArrowRight,
  ArrowUpRight,
  Check,
  ChevronRight,
  Database,
  FileCheck2,
  Github,
  GitBranch,
  LockKeyhole,
  Menu,
  Play,
  Radar,
  SatelliteDish,
  ScanSearch,
  ShieldCheck,
  X,
} from "lucide-react";
import { toast } from "sonner";
import { journalPosts } from "@/lib/journal";

const mark = "/manus-storage/groundpulse-mark_385613b6.png";
const heroArt = "/manus-storage/groundpulse-hero-orbit_921a6f30.jpg";
const evidenceArt = "/manus-storage/groundpulse-evidence-orbit_e80528b9.jpg";
const packageArt = "/manus-storage/groundpulse-package-artifact_a5613273.jpg";
const operatorArt = "/manus-storage/groundpulse-usecase-satellite-operator_8bc74750.jpg";
const stationArt = "/manus-storage/groundpulse-usecase-ground-station_6fcf41df.jpg";
const researchArt = "/manus-storage/groundpulse-usecase-research-network_36523668.jpg";

const sampleRun = {
  id: "RUN-DEMO-038",
  question: "Ground-station coverage review · Budapest",
  source: "celestrak_gp_25544",
  state: "READY FOR REPLAY",
};

const navItems = [
  ["Product", "#product"],
  ["Proof", "#proof"],
  ["How it works", "#workflow"],
  ["Outputs", "#outputs"],
  ["Use cases", "#use-cases"],
  ["Journal", "#journal"],
];

const workflow = [
  { number: "01", title: "Frame the mission", description: "Normalize the research question, place, window, and intended package.", icon: ScanSearch },
  { number: "02", title: "Discover sources", description: "Query approved adapters for orbital, observation, and space-weather context.", icon: Database },
  { number: "03", title: "Validate evidence", description: "Check coverage, provenance, metadata completeness, and data-use conditions.", icon: ShieldCheck, active: true },
  { number: "04", title: "Build the package", description: "Release a cited brief, claim ledger, gap list, and reproducibility manifest.", icon: FileCheck2 },
];

const labels = [
  ["SOURCE-BACKED", "Directly supported by an approved source.", "green"],
  ["DERIVED", "Calculated from accepted evidence.", "violet"],
  ["UNAVAILABLE", "A gap disclosed instead of invented.", "gray"],
];

function Brand() {
  return <a href="#top" className="brand" aria-label="GroundPulse home"><img src={mark} alt="GroundPulse satellite dish mark" /><span><b>GROUNDPULSE</b><small>RESEARCH AGENT</small></span></a>;
}

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const notifyWorkspace = () => toast("Sample run ready", { description: "Open Mission Control to replay the evidence-first workflow." });
  const requestAccess = () => toast("Early access is opening soon", { description: "GroundPulse is currently being prepared for initial research teams." });

  return (
    <main id="top" className="site-shell">
      <header className="site-header">
        <div className="header-inner">
          <Brand />
          <nav className="desktop-nav" aria-label="Primary navigation">{navItems.map(([label, href]) => <a key={label} href={href}>{label}</a>)}</nav>
          <div className="header-actions">
            <a className="github-link" href="https://github.com/ousssamarahmani/GroundPulse-Research-Agent" target="_blank" rel="noreferrer"><Github size={16} /> <span>GitHub</span></a>
            <a className="header-cta" href="/dashboard">Open workspace <ArrowUpRight size={15} /></a>
            <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">{menuOpen ? <X size={20} /> : <Menu size={20} />}</button>
          </div>
        </div>
        {menuOpen && <nav className="mobile-nav" aria-label="Mobile navigation">{navItems.map(([label, href]) => <a key={label} href={href} onClick={() => setMenuOpen(false)}>{label}</a>)}<button onClick={requestAccess}>Request early access <ArrowUpRight size={15} /></button></nav>}
      </header>

      <section className="hero-section" aria-labelledby="hero-title">
        <div className="hero-art" style={{ backgroundImage: `url(${heroArt})` }} /><div className="hero-grid" />
        <div className="hero-content container">
          <div className="hero-copy reveal">
            <p className="eyebrow"><span className="pulse-dot" /> THE RESEARCH AGENT FOR SPACE OPERATIONS</p>
            <h1 id="hero-title">Your space data research team—<em>in one agent.</em></h1>
            <p className="hero-text">Ask a mission question. GroundPulse maps the source landscape, validates the evidence, and delivers an audit-ready research package your team can act on.</p>
            <div className="hero-buttons"><button className="button primary" onClick={requestAccess}>Request early access <ArrowRight size={17} /></button><a className="button quiet" href="#outputs">See what you receive <ArrowUpRight size={16} /></a></div>
          </div>
          <aside className="hero-console reveal delay-2" aria-label="Live workflow preview">
            <div className="console-topline"><span>SAMPLE RUN / TRACEABLE PATH</span><span className="console-live">DEMO READY</span></div>
            <div className="console-title"><SatelliteDish size={19} /><div><strong>Coverage review / Budapest</strong><small>Ground-station research request</small></div></div>
            <div className="mini-flow"><div className="done"><Check size={13} /><span>Plan request</span><b>Complete</b></div><div className="done"><Check size={13} /><span>Discover sources</span><b>3 adapters</b></div><div className="current"><Radar size={14} /><span>Validate evidence</span><b>In progress</b></div><div><span className="empty-node" /><span>Build package</span><b>Queued</b></div></div>
            <div className="console-footer"><LockKeyhole size={14} /> Demo state only · evidence gate is visible.</div>
          </aside>
        </div>
        <div className="hero-status container"><div><span>01</span><p><b>Ask the question</b><small>Mission, place, time window</small></p></div><div><span>02</span><p><b>Validate the sources</b><small>Coverage and provenance checked</small></p></div><div><span>03</span><p><b>Review the packet</b><small>Claims, citations, gaps</small></p></div><a href="#request-access">REQUEST ACCESS <ArrowRight size={15} /></a></div>
      </section>

      <section id="proof" data-path="01 · PROOF OF SYSTEM" className="proof-section section">
        <div className="container proof-layout">
          <div className="proof-copy reveal">
            <p className="eyebrow"><span className="pulse-dot" /> PROOF OF SYSTEM</p>
            <h2>See the run,<br /><em>not just the promise.</em></h2>
            <p>Replay a complete sample mission in Mission Control: a structured request, approved source, evidence gate, visible gap, and package-ready state.</p>
            <a className="button primary" href="/dashboard"><Play size={16} fill="currentColor" /> Replay sample run <ArrowUpRight size={16} /></a>
            <small className="proof-disclaimer">Deterministic demo state · no live services connected</small>
          </div>
          <div className="proof-run-card reveal delay-1">
            <div className="proof-run-head"><span><span className="live-dot" /> SAMPLE MISSION REPLAY</span><b>{sampleRun.state}</b></div>
            <div className="proof-run-title"><div className="proof-run-icon"><Radar size={19} /></div><div><span>{sampleRun.id}</span><strong>{sampleRun.question}</strong></div></div>
            <div className="proof-run-steps"><div className="proof-step done"><Check size={14} /><span>Request framed</span><b>01</b></div><div className="proof-step done"><Check size={14} /><span>Source approved</span><b>{sampleRun.source}</b></div><div className="proof-step active"><Radar size={14} /><span>Evidence gate</span><b>READY</b></div><div className="proof-step"><span className="empty-node" /><span>Package release</span><b>QUEUED</b></div></div>
            <div className="proof-run-foot"><span>Claims · citations · gaps</span><a href="/dashboard">Open Mission Control <ArrowUpRight size={14} /></a></div>
          </div>
        </div>
      </section>

      <section id="product" data-path="02 · THE PRODUCT" className="mission-section section container">
        <div className="mission-number">01</div>
        <div className="mission-heading reveal"><p className="eyebrow">RESEARCH WITHOUT THE CONTEXT TAX</p><h2>Move from scattered sources to a <em>defensible decision.</em></h2></div>
        <div className="mission-copy reveal delay-1"><p>Satellite and ground-segment teams lose time gathering context across portals, PDFs, datasets, and operational assumptions before the actual analysis even begins.</p><p>GroundPulse compresses that work into an inspectable agent run: a clear question, validated sources, and a packet that states exactly what is supported—and what is still missing.</p><a className="inline-link" href="#outputs">Inspect the product outputs <ArrowUpRight size={15} /></a></div>
      </section>

      <section id="workflow" data-path="03 · AGENT WORKFLOW" className="workflow-section section">
        <div className="container">
          <div className="section-intro"><div className="reveal"><p className="eyebrow">HOW GROUNDPULSE WORKS</p><h2>One question in.<br /><em>A research-ready packet out.</em></h2></div><p className="reveal delay-1">GroundPulse does not jump from prompt to prose. It works through a controlled workflow where evidence is assessed before a research claim is written.</p></div>
          <div className="workflow-rail">{workflow.map(({ number, title, description, icon: Icon, active }, index) => <article className={`workflow-card ${active ? "active" : ""} reveal`} style={{ transitionDelay: `${index * 65}ms` }} key={number}><div className="workflow-card-top"><span>{number}</span><Icon size={21} strokeWidth={1.4} /></div><h3>{title}</h3><p>{description}</p><div className="workflow-card-footer">{active ? <><span className="active-dot" /> Evidence gate active</> : <><ChevronRight size={14} /> Structured state</>}</div></article>)}</div>
          <div className="workflow-note reveal"><ShieldCheck size={20} /><p><b>Validation before synthesis.</b> The final package contains accepted evidence, explicit derivations, proposals, or documented gaps—never an invented operational claim.</p><a href="#outputs">See the product outputs <ArrowRight size={16} /></a></div>
        </div>
      </section>

      <section id="outputs" data-path="04 · PRODUCT OUTPUTS" className="evidence-section section">
        <div className="container evidence-grid">
          <div className="evidence-image reveal"><img src={evidenceArt} alt="Abstract orbital evidence visualization" /><div className="instrument-readout"><span>RECEIVER TRACE / 03</span><b>Provenance vector stabilized</b><i><em /> <em /> <em /> <em /> <em /></i></div><div className="image-caption"><span>PROVENANCE VECTOR</span><span>RETRIEVAL → VALIDATION → PACKAGE</span></div></div>
          <div className="evidence-content"><p className="eyebrow reveal">WHAT YOUR TEAM RECEIVES</p><h2 className="reveal delay-1">Not chat history.<br /><em>Deliverables you can inspect.</em></h2><p className="evidence-lede reveal delay-1">Every GroundPulse run returns a research brief, claim ledger, cited source trail, and an explicit gap list for the question at hand.</p><div className="label-stack">{labels.map(([name, description, color], index) => <div className={`evidence-label ${color} reveal`} style={{ transitionDelay: `${index * 80}ms` }} key={name}><span className="label-code">{name}</span><p>{description}</p><ChevronRight size={17} /></div>)}</div><button className="text-button reveal" onClick={notifyWorkspace}>Preview a product run <ArrowUpRight size={16} /></button></div>
        </div>
      </section>

      <section id="architecture" data-path="04 · PRODUCT INFRASTRUCTURE" className="architecture-section section">
        <div className="container"><div className="architecture-heading"><div className="reveal"><p className="eyebrow">BUILT FOR TRUSTED AGENT RUNS</p><h2>Product infrastructure,<br /><em>not a prompt wrapper.</em></h2></div><p className="reveal delay-1">The system separates intake, durable job state, agent execution, validation, and immutable research artifacts so every run can be inspected and replayed.</p></div><div className="architecture-board reveal"><div className="arch-row request"><span className="arch-index">A</span><div><b>Researcher request</b><small>React experience · structured intake</small></div><ArrowRight size={17} /></div><div className="arch-row api"><span className="arch-index">B</span><div><b>API & durable job state</b><small>Cloud Run · Firestore · Cloud Tasks</small></div><ArrowRight size={17} /></div><div className="arch-row agent"><span className="arch-index">C</span><div><b>Agent + source tools</b><small>Planning · discovery · provenance validation</small></div><ArrowRight size={17} /></div><div className="arch-row package"><span className="arch-index">D</span><div><b>Evidence package</b><small>Report · claim ledger · JSON manifest</small></div><FileCheck2 size={18} /></div><div className="arch-side"><GitBranch size={22} /><span>Every transition is logged.<br />Every retry is idempotent.</span></div></div><div className="architecture-foot"><span>STACK / FASTAPI · CLOUD RUN · ADK · CLOUD TASKS · FIRESTORE · CLOUD STORAGE</span><a href="https://github.com/ousssamarahmani/GroundPulse-Research-Agent" target="_blank" rel="noreferrer">Read the technical guide <ArrowUpRight size={15} /></a></div></div>
      </section>

      <section data-path="05 · RESEARCH PACKAGE" className="package-section section container">
        <div className="package-copy reveal"><p className="eyebrow">ONE RUN, FOUR ARTIFACTS</p><h2>A research packet your team can <em>inspect, reuse, and defend.</em></h2><p>GroundPulse returns more than an answer: a research brief with citations, an evidence ledger, a versioned manifest, and a visible account of every unresolved data gap.</p><button className="button primary" onClick={notifyWorkspace}>Preview a research packet <ArrowRight size={17} /></button></div>
        <div className="package-visual reveal delay-1"><img src={packageArt} alt="Research package artifact floating in space" /><div className="package-badge"><FileCheck2 size={16} /><span><b>PACKAGE STATUS</b><small>Traceable by design</small></span></div></div>
      </section>

      <section id="use-cases" data-path="06 · WHO IT IS FOR" className="use-cases-section section">
        <div className="container"><div className="section-intro use-case-intro"><div className="reveal"><p className="eyebrow">FOR THE TEAMS WHO NEED TO KNOW</p><h2>Research that meets your <em>operational context.</em></h2></div><p className="reveal delay-1">GroundPulse is built for teams that need a transparent answer to a space-data question before they make the next technical, operational, or investment decision.</p></div><div className="use-case-grid"><article className="use-case-card reveal"><div className="case-image-wrap"><img className="case-image" src={operatorArt} alt="Satellite coverage analysis in low Earth orbit" /><span>ORBITAL COVERAGE</span></div><div className="case-content"><SatelliteDish size={23} /><p className="case-kicker">SATELLITE OPERATORS</p><h3>Validate the context around your next coverage question.</h3><p>Move from a mission question to a cited view of sources, availability, and unresolved gaps.</p><button onClick={requestAccess}>Explore operator workflows <ArrowUpRight size={15} /></button></div></article><article className="use-case-card reveal delay-1"><div className="case-image-wrap"><img className="case-image" src={stationArt} alt="Ground-station antenna network at blue hour" /><span>SITE CONTEXT</span></div><div className="case-content"><Radar size={23} /><p className="case-kicker">GROUND-STATION TEAMS</p><h3>Build a research baseline before deployment work starts.</h3><p>Bring source coverage, metadata conditions, and operational assumptions into one reviewable packet.</p><button onClick={requestAccess}>Explore station workflows <ArrowUpRight size={15} /></button></div></article><article className="use-case-card reveal delay-2"><div className="case-image-wrap"><img className="case-image" src={researchArt} alt="Orbital research network over Earth horizon" /><span>SOURCE MAP</span></div><div className="case-content"><GitBranch size={23} /><p className="case-kicker">RESEARCH & STRATEGY</p><h3>Keep every technical narrative connected to the evidence.</h3><p>Give decision-makers research briefs that expose sources, derivations, and uncertainty instead of masking them.</p><button onClick={requestAccess}>Explore research workflows <ArrowUpRight size={15} /></button></div></article></div></div>
      </section>

      <section id="journal" data-path="07 · MISSION NOTES" className="journal-section section">
        <div className="container"><div className="journal-section-head"><div className="reveal"><p className="eyebrow">GROUNDPULSE RESEARCH JOURNAL</p><h2>Notes for the teams<br /><em>building from evidence.</em></h2></div><div className="reveal delay-1"><p>Method notes, product decisions, and field guides for making space-data research more traceable, repeatable, and useful.</p><a className="inline-link" href={`/journal/${journalPosts[0].slug}`}>Read the latest mission note <ArrowUpRight size={15} /></a></div></div><div className="journal-grid">{journalPosts.map((post, index) => <article className={`journal-card reveal ${index === 0 ? "featured" : ""}`} key={post.slug}><div className="journal-card-top"><span>{post.number}</span><p>{post.category}</p><i>{post.signal}</i></div><div className="journal-geometry"><span /><span /><span /><span /></div><div className="journal-copy"><h3>{post.title}</h3><p>{post.deck}</p></div><div className="journal-card-foot"><span>{post.readTime}</span><a href={`/journal/${post.slug}`}>Read note <ArrowRight size={15} /></a></div></article>)}</div></div>
      </section>

      <section id="request-access" className="closing-section"><div className="container closing-inner reveal"><p className="eyebrow">GROUNDPULSE RESEARCH AGENT</p><h2>Get the evidence.<br /><em>Keep the uncertainty visible.</em></h2><p className="closing-copy">Join the early group of teams shaping an evidence-first research workflow for satellite and ground-segment decisions.</p><div><button className="button primary" onClick={requestAccess}>Request early access <ArrowUpRight size={17} /></button><a className="button quiet" href="https://github.com/ousssamarahmani/GroundPulse-Research-Agent" target="_blank" rel="noreferrer">Explore GitHub <Github size={17} /></a></div></div></section>
      <footer className="site-footer container"><Brand /><p>GroundPulse Research Agent turns satellite and ground-segment questions into inspectable, evidence-backed research packets.</p><span>© 2026 GROUNDPULSE AI</span></footer>
    </main>
  );
}
