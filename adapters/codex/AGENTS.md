# AGENTS.md — LLM Wiki Schema
# [YOUR NAME] Personal Knowledge Base
# Maintained by OpenAI Codex CLI · [YEAR]
#
# This is the Codex CLI adapter for the LLM Wiki Template.
# It is functionally identical to CLAUDE.md but uses Codex naming conventions.
# Codex reads AGENTS.md automatically from the project root.
#
# DIFFERENCES FROM CLAUDE CODE ADAPTER:
# - No native hook system — session export is a manual step (see Manual Export below)
# - Use `codex` slash commands instead of `claude` slash commands
# - Bootstrap commands work the same way
#
# See adapters/claude-code/CLAUDE.md for the full reference implementation.
# See examples/domains/ for domain configuration examples.

---

## Overview

This is a **multi-domain LLM Wiki** — a persistent, compounding knowledge base
maintained entirely by you (the LLM agent). The human sources documents and
asks questions. You do all the writing, filing, cross-referencing, and bookkeeping.

Active domains:

| Domain ID   | Name              | Root folder          |
|-------------|-------------------|----------------------|
| `DOMAIN_1`  | [Domain 1 Name]   | `wiki/DOMAIN_1/`     |
| `DOMAIN_2`  | [Domain 2 Name]   | `wiki/DOMAIN_2/`     |
| `DOMAIN_3`  | [Domain 3 Name]   | `wiki/DOMAIN_3/`     |

---

## Manual Session Export

Codex CLI does not have a native hook system for automatic export. Run this
at the end of every session before exiting:

```bash
# Export current session manually
python3 scripts/export-session.py --trigger manual

# If the session is confidential:
python3 scripts/export-session.py --trigger manual --label confidential
```

**Important**: Make this a habit. The session export is where memory lives.
Without it, context that isn't digested into the wiki is lost when the session ends.

To make it easier, add this alias to your shell:

```bash
# Add to ~/.bashrc or ~/.zshrc:
alias wiki-save="cd ~/my-wiki && python3 scripts/export-session.py --trigger manual"
alias wiki-save-private="cd ~/my-wiki && python3 scripts/export-session.py --trigger manual --label confidential"
```

### Simulating SessionStart behavior

Since there's no hook, run this at the start of each session to get the same
context that Claude Code's SessionStart hook provides automatically:

```bash
bash scripts/index-sessions.sh && bash scripts/recall.sh --recent 3
```

Or add to your shell as:
```bash
alias wiki-start="cd ~/my-wiki && git pull && bash scripts/index-sessions.sh && bash scripts/recall.sh --recent 3"
```

---

## Directory Structure

```
my-wiki/
├── raw/                          # IMMUTABLE. Never modify.
│   ├── DOMAIN_1/
│   ├── DOMAIN_2/
│   ├── DOMAIN_3/
│   └── assets/
│
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── overview.md
│   ├── DOMAIN_1/{sources,concepts,entities}/
│   ├── DOMAIN_2/{sources,concepts,entities}/
│   ├── DOMAIN_3/{sources,concepts,entities}/
│   └── shared/
│
├── sessions/
│   ├── exports/
│   ├── confidential/
│   └── wiki-digests/
│
├── scripts/                      # Note: scripts/ not .claude/scripts/ for Codex
│   ├── export-session.py
│   ├── index-sessions.sh
│   └── recall.sh
│
├── .exportignore
├── .gitignore
├── sessions.db
└── AGENTS.md                     # This file.
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
- Claim 1
- Claim 2 (note contradictions with [[existing pages]])

## Key Entities Mentioned
- [[Entity]] — role

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

### wiki/index.md
Master catalog. Update on every ingest.
```
| [[path/to/page]] | One-line description | domain | date |
```

### wiki/log.md
Append-only. Never edit past entries.
```
## [YYYY-MM-DD] ingest | DOMAIN | Source Title
## [YYYY-MM-DD] export | manual | session saved before exit
## [YYYY-MM-DD] digest | sessions | N sessions → M wiki pages
```

---

## Operations

### INGEST — `> ingest [domain] raw/path/to/file.md`
1. Read source from `raw/`
2. Brief takeaway discussion
3. Create `wiki/[domain]/sources/SLUG.md`
4. Update `wiki/index.md`
5. Update entity and concept pages
6. Check cross-domain connections → `wiki/shared/`
7. Append to `wiki/log.md`

### QUERY — `> [question]`
1. Read `wiki/index.md` for relevant pages
2. Synthesize with citations: `[[wiki/domain/path]]`
3. Offer to file the answer as a wiki page

### RECALL — `> recall: [terms]`
```bash
bash scripts/recall.sh "your search terms"
bash scripts/recall.sh --recent 5
```

### DIGEST — `> digest sessions`
Extract knowledge from session exports → wiki pages → archive to wiki-digests/.

### LINT — `> lint`
Check orphans, contradictions, stale claims, concept gaps.

---

## Domain Conventions

### DOMAIN_1 — [Name]
**Purpose**: [Description]
**Key concepts**: [List]
**Special rules**: [Instructions]

### DOMAIN_2 — [Name]
**Purpose**: [Description]
**Key concepts**: [List]
**Special rules**: [Instructions]

### DOMAIN_3 — [Name]
**Purpose**: [Description]
**Key concepts**: [List]
**Special rules**: [Instructions]

---

## Bootstrapping

```
> customize     # replace placeholders with real domain names
> bootstrap     # create structure, seed pages, initialize sessions.db
```

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
