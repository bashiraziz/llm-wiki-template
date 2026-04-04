# Example Domain: Research

A fully worked example of a general research domain — going deep on a topic
over weeks or months, building a comprehensive wiki with an evolving thesis.

Works for: academic research, competitive intelligence, industry analysis,
learning a technical field, writing non-fiction, tracking AI/ML developments.

---

## Domain entry for the domain table

```markdown
| `research` | General Research | `wiki/research/` |
```

## Directory additions

```
wiki/research/
├── overview.md        # your evolving thesis — the crown jewel, update every 10 sources
├── sources/           # one page per paper, article, podcast, video
├── concepts/          # key ideas, frameworks, models, theories
├── entities/          # people, institutions, tools, products
└── threads/           # active questions you're currently pursuing
```

## Domain conventions block

```markdown
### research — General Research

**Purpose**: Build a comprehensive, evolving understanding of [your topic].
Track sources, concepts, key figures, and the development of a thesis that
gets sharper with every source ingested.

**Key concept pages to seed early**:
- [Core concept or framework 1 in your field]
- [Core concept or framework 2]
- [Key methodology or approach]
- [Central contested claim in the field]

**Domain-specific page types**:

threads/QUESTION.md — active research questions being pursued:
    ---
    title: "Thread: [Question]"
    status: active | paused | closed
    started: YYYY-MM-DD
    ---
    ## The Question
    ## What We Know So Far
    ## Sources Consulted
    ## Open Sub-Questions
    ## Next Steps

**Special rules**:
- After every 10 sources ingested, update wiki/research/overview.md
  with the current state of the thesis
- When a source contradicts the current thesis, flag it prominently
  in the source page AND the relevant concept pages — contradictions
  are the most valuable things in a research wiki
- Track open questions in threads/ — these drive what to read next
- When a thread closes (question answered), mark status: closed and
  summarize the answer at the top
- overview.md is the most important page — it synthesizes everything.
  Keep it tight: thesis statement, key supporting claims, major contested
  areas, what would change the thesis

**Output formats for queries**:
- "What do we know about X?" → update concept page, then answer
- "What are the biggest open questions?" → review threads/, suggest new ones
- "What should I read next?" → based on open threads and concept gaps
- "How has our thesis evolved?" → compare overview.md versions in git log
- Comparison questions → markdown table filed as a wiki page
```

## Thread lifecycle example

```markdown
## [2026-04-01] thread | research | Thread opened: Does X cause Y?

## [2026-04-08] ingest | research | Smith 2024 — partial evidence for X→Y

## [2026-04-15] ingest | research | Jones 2024 — contradicts Smith, shows Z mediates

## [2026-04-20] query | research | Synthesis: X→Y relationship, Z as mediator — filed

## [2026-04-20] thread | research | Thread closed: X causes Y only when Z > threshold
```

## Cross-domain connections to watch for

If you have other domains alongside research:
- Research ↔ Work: when a research finding has direct practical application
- Research ↔ Personal: when research connects to personal goals or health
- Research ↔ any domain: methodology insights that transfer across contexts

## Suggested Obsidian saved searches for research

```
# All source pages sorted by date:
path:research/sources

# Open threads only:
path:research/threads status:active

# Concepts with high source counts (hubs):
# Use Dataview: TABLE source_count FROM "research/concepts" SORT source_count DESC

# Contested claims (concepts with contradictions noted):
"contradicts" path:research/concepts
```
