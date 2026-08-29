/** Design reminder — GroundPulse Editorial System: technical, evidence-led, and calm. */
import { ArrowLeft, ArrowRight, ArrowUpRight, Github, Radar } from "lucide-react";
import { useRoute } from "wouter";
import { journalPosts } from "@/lib/journal";

const mark = "/manus-storage/groundpulse-mark_385613b6.png";

export default function JournalArticle() {
  const [, params] = useRoute("/journal/:slug");
  const post = journalPosts.find((item) => item.slug === params?.slug) ?? journalPosts[0];
  const next = journalPosts[(journalPosts.findIndex((item) => item.slug === post.slug) + 1) % journalPosts.length];

  return (
    <main className="journal-article-shell">
      <header className="journal-nav"><a href="/" className="journal-brand"><img src={mark} alt="GroundPulse mark" /><span><b>GROUNDPULSE</b><small>MISSION NOTES</small></span></a><div><a href="/#journal">Journal</a><a href="/dashboard">Open workspace <ArrowUpRight size={14} /></a></div></header>
      <section className="article-hero"><div className="article-orbit" /><div className="article-frame"><a className="article-back" href="/#journal"><ArrowLeft size={14} /> Back to journal</a><p className="article-meta"><span>{post.category}</span> · {post.date} · {post.readTime}</p><h1>{post.title}</h1><p className="article-deck">{post.deck}</p><div className="article-signal"><Radar size={16} /><span>{post.signal}</span><i /><i /><i /></div></div></section>
      <article className="article-body"><aside><span>{post.number}</span><p>GROUNDPULSE<br />RESEARCH JOURNAL</p></aside><div>{post.body.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}<div className="article-callout"><b>GroundPulse principle</b><p>Evidence is part of the product. A result is not ready until its source trail, derivations, and gaps are visible to the team.</p></div><div className="article-next"><span>NEXT MISSION NOTE</span><a href={`/journal/${next.slug}`}>{next.title} <ArrowRight size={16} /></a></div></div></article>
      <footer className="journal-footer"><a href="/"><ArrowLeft size={14} /> GroundPulse product</a><a href="https://github.com/ousssamarahmani/GroundPulse-Research-Agent" target="_blank" rel="noreferrer"><Github size={15} /> GitHub repository</a></footer>
    </main>
  );
}
