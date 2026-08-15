export type JournalPost = {
  slug: string;
  number: string;
  category: string;
  title: string;
  deck: string;
  readTime: string;
  date: string;
  signal: string;
  body: string[];
};

export const journalPosts: JournalPost[] = [
  {
    slug: "claim-ledger",
    number: "01",
    category: "METHOD NOTE",
    title: "Why research agents need a claim ledger.",
    deck: "The difference between a useful research answer and a defensible one is a record of what each claim can actually support.",
    readTime: "4 min read",
    date: "Mission Note 001",
    signal: "PROVENANCE / ACTIVE",
    body: [
      "Research systems routinely encounter a difficult boundary: sources are partial, time windows disagree, and operational context is not always public. A useful agent must preserve that boundary rather than smooth it away.",
      "A claim ledger gives every output sentence a status. It can be source-backed, derived from accepted inputs, proposed for further work, or unavailable. This makes the research package inspectable by the people who have to rely on it.",
      "The goal is not to make an agent sound more cautious. The goal is to make its reasoning reviewable, so that a team can move quickly without losing the record of what still needs a human measurement.",
    ],
  },
  {
    slug: "evidence-gate",
    number: "02",
    category: "PRODUCT NOTE",
    title: "The evidence gate between discovery and synthesis.",
    deck: "A controlled validation step keeps an agent from turning a convenient source list into an unsupported conclusion.",
    readTime: "3 min read",
    date: "Mission Note 002",
    signal: "VALIDATION / IN PROGRESS",
    body: [
      "Discovery is an input to research, not a conclusion. A result may be relevant to the question and still fail because its coverage, provenance, terms of use, or metadata are not fit for the decision being made.",
      "GroundPulse treats validation as a distinct mission stage. The agent compares each source with the structured request before it can become part of a released research package.",
      "The result is a clearer handoff: teams receive accepted evidence, explicit derivations, and visible gaps. The package can be scrutinized or repeated without reverse-engineering a chat transcript.",
    ],
  },
  {
    slug: "coverage-brief",
    number: "03",
    category: "FIELD GUIDE",
    title: "Designing a reproducible coverage brief.",
    deck: "A strong ground-station research brief connects mission intent, location, time window, source trace, and unresolved constraints.",
    readTime: "5 min read",
    date: "Mission Note 003",
    signal: "PACKAGE / READY",
    body: [
      "Coverage questions look simple until they meet the real operating environment. A useful brief starts by identifying the target system, station location, time window, and the intended decision before retrieval begins.",
      "The source trail then becomes part of the deliverable. Each candidate is checked for temporal fit and metadata completeness, and the resulting derivations remain linked to their inputs.",
      "This is how a research brief becomes a reusable team artifact: not an answer in isolation, but a package with context, evidence, known gaps, and an honest boundary around what it can establish.",
    ],
  },
];
