# WIKI-SCHEMA.md — LLM Wiki Schema (Generic / Tool-Agnostic)
# [YOUR NAME] Personal Knowledge Base
# [YEAR]
#
# This is the tool-agnostic version of the LLM Wiki schema.
# Use this if your LLM tool isn't Claude Code or Codex CLI.
#
# Load this file into your LLM session manually:
# - Paste it as a system prompt
# - Include it in your tool's context file (whatever filename it expects)
# - Reference it at the start of each session: "Read WIKI-SCHEMA.md first"
#
# SESSION EXPORT NOTE:
# Without a hook system, export sessions manually at the end of each session:
#   python3 scripts/export-session.py --trigger manual
# See scripts/export-session.py for details.
#
# CUSTOMIZATION: Replace DOMAIN_1, DOMAIN_2, DOMAIN_3 with your domain names.

---

## Overview

This is a **multi-domain LLM Wiki** — a persistent, compounding knowledge base
maintained entirely by you (the LLM agent). The human sources documents and asks
questions. You do all the writing, filing, cross-referencing, and bookkeeping.

Active domains:

| Domain ID   | Name              | Root folder          |
|-------------|-------------------|----------------------|
| `DOMAIN_1`  | [Domain 1 Name]   | `wiki/DOMAIN_1/`     |
| `DOMAIN_2`  | [Domain 2 Name]   | `wiki/DOMAIN_2/`     |
| `DOMAIN_3`  | [Domain 3 Name]   | `wiki/DOMAIN_3/`     |

---

## Directory Structure

```
my-wiki/
├── raw/                 # IMMUTABLE. Source documents. Never modify.
├── wiki/                # YOUR DOMAIN. Create, update, cross-reference.
│   ├── index.md         # Master catalog — update on every ingest
│   ├── log.md           # Append-only record — never edit past entries
│   ├── overview.md      # Evolving synthesis across all domains
│   ├── DOMAIN_1/{sources,concepts,entities}/
│   ├── DOMAIN_2/{sources,concepts,entities}/
│   ├── DOMAIN_3/{sources,concepts,entities}/
│   └── shared/
├── sessions/            # Exported session transcripts
│   ├── exports/
│   └── wiki-digests/
├── scripts/             # export-session.py, index-sessions.sh, recall.sh
├── sessions.db          # SQLite FTS5 index
└── WIKI-SCHEMA.md       # This file.
```

---

## Page Formats

### sources/SLUG.md
```markdown
---
title: "Full Title"
domain: DOMAIN_1 | DOMAIN_2 | DOMAIN_3
date_ingested: YYYY-MM-DD
source_type: article | paper | book_chapter | podcast | memo | report | other
tags: []
raw_path: raw/DOMAIN/filename.md
---
# [Title]
## Summary
## Key Claims
## Key Entities Mentioned
## Contradictions / Open Questions
## Wiki Pages Updated
```

### concepts/NAME.md
```markdown
---
title: "Concept Name"
domain: DOMAIN_1 | shared
tags: []
source_count: N
last_updated: YYYY-MM-DD
---
# [Concept Name]
## Definition
## Why It Matters
## Key Sources
## Related Concepts
## Open Questions
```

### entities/NAME.md
```markdown
---
title: "Entity Name"
entity_type: person | org | product | place | tool
domain: DOMAIN_1 | shared
---
# [Entity Name]
## What / Who
## Relevance
## Key Facts
## Connections
```

---

## Special Files

**wiki/index.md** — master catalog, updated on every ingest:
```
| [[path/to/page]] | One-line description | domain | YYYY-MM-DD |
```

**wiki/log.md** — append-only, never edit past entries:
```
## [YYYY-MM-DD] ingest | DOMAIN | Source Title
## [YYYY-MM-DD] query | DOMAIN | Question filed as page
## [YYYY-MM-DD] digest | sessions | N sessions → M wiki pages
```

---

## Operations

**INGEST** — `> ingest [domain] raw/path/to/file.md`
1. Read source · 2. Brief takeaway discussion · 3. Create sources/SLUG.md
4. Update index.md · 5. Update entity + concept pages · 6. Check cross-domain
7. Append to log.md · 8. Report files created/modified

**QUERY** — just ask a question
1. Check sessions: `bash scripts/recall.sh "[keywords]"`
2. Read index.md · 3. Synthesize with citations · 4. Offer to file as wiki page

**RECALL** — `> recall: [what you're looking for]`
```bash
bash scripts/recall.sh "search terms"
bash scripts/recall.sh --recent 5
```

**DIGEST** — `> digest sessions`
Session exports → wiki pages → archive to sessions/wiki-digests/

**LINT** — `> lint`
Orphan pages · contradictions · stale claims · concept gaps · missing links

**UPDATE** — `> update [domain] [path]`
Update a page from information in the current chat (no raw file needed)

---

## Domain Conventions

### DOMAIN_1 — [Name]
**Purpose**: [Description]
**Key concepts to seed**: [List]
**Special rules**: [Domain-specific LLM behavior]

### DOMAIN_2 — [Name]
**Purpose**: [Description]
**Key concepts to seed**: [List]
**Special rules**: [Instructions]

### DOMAIN_3 — [Name]
**Purpose**: [Description]
**Key concepts to seed**: [List]
**Special rules**: [Instructions]

---

## Tone and Judgment

Write for the human who owns this wiki. Match their expertise. Don't over-explain
what they know. Surface contradictions — don't smooth them over. Prefer specificity.
Short pages with good links beat long sprawling pages. Never edit history.

---

## Bootstrap

```
> customize    # replace placeholders with real domain names
> bootstrap    # create directories, seed pages, initialize sessions.db
```

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
