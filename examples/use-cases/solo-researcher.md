# Use Case: Solo Researcher

**Who this is for**: One person going deep on a single topic over weeks or months.
Reading papers, articles, reports, and building a comprehensive wiki with an
evolving thesis.

**Examples**:
- A PhD student tracking literature for a dissertation
- An analyst building competitive intelligence on an industry
- Someone learning a new technical field systematically
- A writer researching a non-fiction book

**Complexity**: Low — 1 domain, 1 person, 1 machine (or simple 2-machine setup).

---

## Minimal domain configuration

```markdown
| Domain ID   | Name         | Root folder    |
|-------------|--------------|----------------|
| `research`  | [Your Topic] | `wiki/research/` |
```

One domain is perfectly valid. Delete the multi-domain complexity from CLAUDE.md.

## Minimal directory structure

```
my-wiki/
├── raw/research/           # papers, articles, notes — immutable
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── overview.md         # your evolving thesis — update every 10 sources
│   └── research/
│       ├── sources/        # one page per paper/article read
│       ├── concepts/       # key ideas, frameworks, models
│       ├── entities/       # people, institutions, theories
│       └── threads/        # active questions you're pursuing
├── sessions/
└── CLAUDE.md
```

## Simplified CLAUDE.md domain block

```markdown
### research — [Your Topic]

**Purpose**: Build a comprehensive, evolving understanding of [topic].
Track sources, concepts, key figures, and the development of my thesis.

**Key concept pages to seed**:
- [Core concept 1 in your field]
- [Core concept 2]
- [Key methodology or framework]

**Special rules**:
- After every 10 sources ingested, update wiki/research/overview.md
  with the current state of the thesis
- Track open questions in wiki/research/threads/
- When a source contradicts the current thesis, flag it prominently
  in both the source page and the relevant concept pages
- The overview.md is the most important page — it's the synthesis
  everything else feeds into

**Output formats for queries**:
- Comparison questions → markdown table
- "What do we know about X?" → concept page update
- "What are the gaps?" → new thread page
- "What should I read next?" → suggest 3 sources based on open questions
```

## Simplified operations

Since there's only one domain, drop the `[domain]` argument from commands:

```
> ingest raw/research/paper-title.md
> what is the relationship between X and Y?
> what are the biggest open questions?
> lint
> digest sessions
```

## Workflow for systematic literature review

```bash
# 1. Clip article with Obsidian Web Clipper → saves to raw/research/
# 2. Start session
claude
# 3. Ingest
> ingest raw/research/article-slug.md
# 4. Ask follow-up questions
> how does this relate to the Smith 2024 paper on X?
> does this change our understanding of Y?
# 5. Update thesis if needed
> update wiki/research/overview.md with new synthesis
# 6. End session
git add wiki/ && git commit -m "session: [paper title]" && git push
```

## What the wiki looks like after 50 sources

```
wiki/research/
├── overview.md              ← your evolving thesis (the crown jewel)
├── sources/                 ← 50 summary pages, each cross-linked
│   ├── smith-2024-x.md
│   ├── jones-2023-y.md
│   └── ...
├── concepts/                ← 20-30 concept pages, deeply cross-referenced
│   ├── core-framework.md    ← linked from 15 source pages
│   ├── contested-claim.md   ← 3 sources agree, 2 disagree — all noted
│   └── ...
├── entities/                ← key people and institutions
│   └── ...
└── threads/                 ← 5-10 open questions still being pursued
    ├── gap-in-evidence.md
    └── ...
```

The graph view in Obsidian will show your intellectual map:
which concepts are hubs (many sources reference them), which are contested
(multiple contradictory sources), which are orphans (mentioned but unexplored).

## Single-machine simplification

If you only use one computer, you can skip the remote git setup entirely
and just use git locally for version history:

```bash
git init
git add wiki/ CLAUDE.md .gitignore
git commit -m "init"
# No push needed — just local history
```

Add remote later if you get a second machine.
