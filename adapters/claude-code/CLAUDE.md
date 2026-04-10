# CLAUDE.md — LLM Wiki Schema
# [YOUR NAME] Personal Knowledge Base
# Maintained by Claude Code · [YEAR]
#
# CUSTOMIZATION INSTRUCTIONS
# ══════════════════════════
# 1. Replace YOUR_NAME with your name
# 2. Define your domains in the Domain Configuration section below
#    Replace DOMAIN_1, DOMAIN_2, DOMAIN_3 with your actual domain names
#    (e.g. "research", "work", "personal", "reading", "health")
# 3. Fill in domain-specific conventions for each of your domains
# 4. Delete or comment out any page formats you don't need
# 5. Run `> bootstrap` in Claude Code to create the directory structure
#
# See examples/domains/ for fully worked domain configurations.
# See examples/use-cases/ for complete CLAUDE.md configurations.
# ══════════════════════════════════════════════════════════════

---

## Overview

This is a **multi-domain LLM Wiki** — a persistent, compounding knowledge base maintained
entirely by you (the LLM agent). The human sources documents and asks questions.
You do all the writing, filing, cross-referencing, and bookkeeping.

Active domains:

| Domain ID   | Name              | Root folder          |
|-------------|-------------------|----------------------|
| `DOMAIN_1`  | [Domain 1 Name]   | `wiki/DOMAIN_1/`     |
| `DOMAIN_2`  | [Domain 2 Name]   | `wiki/DOMAIN_2/`     |
| `DOMAIN_3`  | [Domain 3 Name]   | `wiki/DOMAIN_3/`     |

Cross-domain connections are valuable. When a concept appears in multiple domains,
note the link explicitly and create a cross-domain page under `wiki/shared/`.

> NOTE: You can have 1 domain or 10. Delete rows you don't need.
> A single-domain setup is perfectly valid — just use one domain ID throughout.

---

## Directory Structure

```
my-wiki/
├── raw/                          # IMMUTABLE. Never modify. Source documents.
│   ├── DOMAIN_1/
│   ├── DOMAIN_2/
│   ├── DOMAIN_3/
│   └── assets/                   # Downloaded images from web clips
│
├── wiki/                         # YOUR DOMAIN. Create, update, cross-reference freely.
│   ├── index.md                  # Master catalog — update on EVERY ingest
│   ├── log.md                    # Append-only chronological record
│   ├── overview.md               # High-level synthesis across all domains
│   ├── DOMAIN_1/
│   │   ├── overview.md
│   │   ├── sources/              # One page per ingested source
│   │   ├── concepts/             # Ideas, frameworks, models
│   │   ├── entities/             # People, orgs, products, places
│   │   └── [DOMAIN_1_SUBDIR]/    # Domain-specific subfolder (see conventions below)
│   ├── DOMAIN_2/
│   │   ├── overview.md
│   │   ├── sources/
│   │   ├── concepts/
│   │   ├── entities/
│   │   └── [DOMAIN_2_SUBDIR]/
│   ├── DOMAIN_3/
│   │   ├── overview.md
│   │   ├── sources/
│   │   ├── concepts/
│   │   ├── entities/
│   │   └── [DOMAIN_3_SUBDIR]/
│   └── shared/                   # Cross-domain pages
│
├── sessions/                     # AUTO-EXPORTED session transcripts (never edit manually)
│   ├── exports/                  # Markdown exports, one per session
│   ├── confidential/             # Encrypted exports — never indexed, never committed
│   └── wiki-digests/             # Sessions digested into wiki (archived)
│
├── .claude/
│   ├── settings.json             # Hook configuration
│   ├── no-export                 # Sentinel: if present, skip export for this session
│   └── scripts/
│       ├── export-session.py
│       ├── index-sessions.sh
│       └── recall.sh
│
├── .exportignore                 # Patterns excluded from FTS5 index
├── .gitignore
├── sessions.db                   # SQLite FTS5 index (local only)
└── CLAUDE.md                     # This file.
```

---

## SESSION EXPORT SYSTEM
## The layer that makes memory survive context compression

Every Claude Code session is automatically exported to markdown before the context
compresses. Exports are indexed in SQLite FTS5 — full-text searchable with no API
calls, no embeddings, no vector database. Just markdown and SQL.

### Three hooks

**PreCompact** — fires before context compression triggered by manual `/compact`.
**Does not fire for automatic context compression** (when the context limit is hit
mid-session). For auto-compacted sessions, SessionEnd is the only automatic safety net.

**SessionEnd** — fires when the session exits normally.
Catches short sessions that never triggered PreCompact.

**SessionStart** — fires when a new session begins.
Indexes any unindexed exports, prints last 3 sessions so you know where you left off.

### Manual recovery — when a session wasn't captured

The JSONL transcript stays on disk in `~/.claude/projects/` indefinitely.
If a session was auto-compacted or the window was closed before hooks ran:

```bash
# 1. Find the session JSONL
ls ~/.claude/projects/   # look for your project slug directory

# 2. Export it manually
python3 .claude/scripts/export-session.py \
  --trigger manual \
  --transcript ~/.claude/projects/<project-slug>/<session-id>.jsonl

# 3. Index it
bash .claude/scripts/index-sessions.sh
```

Check `.claude/hooks.log` for a timestamped record of when hooks ran and
what failed — useful for diagnosing why a session went missing.

### Windows note — wikiexit alias

On Windows, the SessionEnd hook may not fire reliably when you type
`exit` to close Claude Code. Add this function to your PowerShell
profile as a reliable alternative:

```powershell
# Run once in PowerShell to open your profile:
notepad $PROFILE

# Add this function to the file, save, and close:
function wikiexit {
    python "YOUR_WIKI_PATH\.claude\scripts\export-session.py" `
           --trigger manual `
           --wiki-dir "YOUR_WIKI_PATH"
}

# Reload the profile in the current terminal:
. $PROFILE
```

Replace `YOUR_WIKI_PATH` with your actual wiki path.

After setup, your session closing ritual is:
```
exit        ← close Claude Code
wikiexit    ← export the session to your wiki
```

`wikiexit` works from any project directory. It detects the current
project and exports the latest session transcript automatically.

---

### Confidentiality controls

**Control 1 — Sentinel file** (skip export entirely):
```bash
touch .claude/no-export   # before starting a sensitive session
# or say "This session is confidential" at the first prompt
```
The sentinel auto-deletes after the session so the next session exports normally.

> **Important**: Do NOT customize the UserPromptSubmit trigger to a single
> common word like "confidential", "private", or "secret". These words appear
> naturally in work content and will silently block ALL session exports. Use
> the exact phrase `"this session is confidential"` or another unambiguous
> deliberate phrase.

**Control 2 — .exportignore** (export to disk but exclude from search index):
Add filename patterns to `.exportignore`. Files exist as backup but are never searchable.

**Control 3 — GPG encryption** (archive but lock):
```bash
# Export with confidential label → GPG-encrypted to sessions/confidential/
python3 .claude/scripts/export-session.py --trigger manual --label confidential
```

### Hook configuration — .claude/settings.json

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/scripts/export-session.py --trigger precompact"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/scripts/export-session.py --trigger sessionend"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/scripts/index-sessions.sh && echo '---' && bash .claude/scripts/recall.sh --recent 3"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json,sys,pathlib; d=json.load(sys.stdin); pathlib.Path('.claude/no-export').touch() if 'this session is confidential' in d.get('prompt','').lower() else None\""
          }
        ]
      }
    ]
  }
}
```

---

## Page Formats

### sources/SLUG.md — one per ingested document
```markdown
---
title: "Full Title of Source"
domain: DOMAIN_1 | DOMAIN_2 | DOMAIN_3
date_ingested: YYYY-MM-DD
source_type: article | paper | book_chapter | podcast | video | memo | report | other
tags: []
raw_path: raw/DOMAIN/filename.md
---

# [Title]

## Summary
2–4 sentence plain-English summary.

## Key Claims
- Claim 1
- Claim 2 (note contradictions with [[existing pages]])

## Key Entities Mentioned
- [[Entity Name]] — role in this source

## Contradictions / Open Questions

## Wiki Pages Updated
List every wiki page touched during this ingest.
```

### concepts/NAME.md — ideas, frameworks, models
```markdown
---
title: "Concept Name"
domain: DOMAIN_1 | DOMAIN_2 | DOMAIN_3 | shared
tags: []
source_count: N
last_updated: YYYY-MM-DD
---

# [Concept Name]

## Definition
Plain-English definition.

## Why It Matters (in this domain)

## Key Sources
- [[sources/slug]] — how this source relates

## Related Concepts
- [[concepts/related-concept]] — how they connect

## Open Questions
```

### entities/NAME.md — people, orgs, products, places
```markdown
---
title: "Entity Name"
entity_type: person | org | product | place | regulation | tool
domain: DOMAIN_1 | DOMAIN_2 | DOMAIN_3 | shared
---

# [Entity Name]

## What / Who

## Relevance

## Key Facts
- Fact (source: [[sources/slug]])

## Connections
- Related to [[Entity or Concept]]
```

### research/threads/THREAD.md — active research questions
```markdown
---
title: "Thread: [Question Being Pursued]"
status: active | paused | closed
started: YYYY-MM-DD
---

# Thread: [Question]

## The Question

## What We Know So Far

## Sources Consulted
- [[sources/slug]]

## Open Sub-Questions

## Next Steps
```

> Add domain-specific page formats below. See examples/domains/ for reference.
> For example, a "reading" domain might add a "books/TITLE.md" format.
> A "health" domain might add a "logs/DATE.md" format for daily tracking.

---

## Special Files

### wiki/index.md
Master catalog. **Update on every ingest — no exceptions.**
```
| [[path/to/page]] | One-line description | domain | date |
```
Organized by domain, then page type. The LLM reads this first on every query.

### wiki/log.md
Append-only. **Never edit past entries.**
```
## [YYYY-MM-DD] ingest | DOMAIN_1 | Source Title
## [YYYY-MM-DD] query | DOMAIN_2 | Question answered + filed
## [YYYY-MM-DD] lint | all | Orphan check + contradiction scan
## [YYYY-MM-DD] digest | sessions | N sessions → M wiki pages
## [YYYY-MM-DD] update | DOMAIN_3 | Page updated from chat
```
Parseable: `grep "^## \[" wiki/log.md | tail -10`

---

## Operations

### INGEST — `> ingest [domain] raw/path/to/file.md`
1. Read the source from `raw/`
2. Brief 2–3 sentence takeaway discussion
3. Create `wiki/[domain]/sources/SLUG.md`
4. Update `wiki/index.md`
5. Update or create entity and concept pages touched by this source
6. Check for domain-specific implications (see Domain Conventions below)
7. Check for cross-domain connections → `wiki/shared/`
8. Append to `wiki/log.md`
9. Report: files created/modified, contradictions found

A single ingest typically touches 8–15 wiki pages. That is expected and good.

### QUERY — `> [question]`
1. Check past sessions: `bash .claude/scripts/recall.sh "[keywords]"`
2. Read `wiki/index.md` to find relevant pages
3. Read those pages, drill into linked pages as needed
4. Synthesize answer with inline citations: `[[wiki/domain/path]]`
5. Ask: *"Should I file this answer as a wiki page?"*

Good answers are knowledge — they should compound in the wiki, not disappear.

### RECALL — `> recall: [what you're looking for]`
```bash
bash .claude/scripts/recall.sh "your search terms"
bash .claude/scripts/recall.sh --recent 5
bash .claude/scripts/recall.sh --date 2026-03
```
Searches all indexed session exports. Falls back to grep if SQLite returns nothing.

### DIGEST — `> digest sessions`
Scan `sessions/exports/` for undigested sessions. Extract structured knowledge.
File as wiki pages. Move processed files to `sessions/wiki-digests/`.
Log: `## [YYYY-MM-DD] digest | sessions | N sessions → M wiki pages`

During digest, look for:
- Architecture decisions → concept pages
- Dead ends (what didn't work and why) → open questions on concept pages
- Discoveries → new source or concept pages
- Decisions made in conversation → update relevant domain pages

### LINT — `> lint` or `> lint [domain]`
Check for:
- Orphan pages (no inbound links)
- Contradictions between pages
- Stale claims superseded by newer sources
- Concepts mentioned but lacking their own page
- Missing cross-references between related pages
- Sessions older than 7 days not yet digested

Suggest: new sources to find, new questions worth pursuing.

### UPDATE — `> update [domain] [path]`
Update a specific wiki page from information provided in chat (no raw file needed).
Use for: quick corrections, meeting notes, decisions from conversations.

### CUSTOMIZE — `> customize`
Interactive walkthrough: replace DOMAIN_1/2/3 placeholders with real domain names,
configure domain-specific conventions, create domain-specific page formats.
Run this once when setting up a new wiki from this template.

### BOOTSTRAP — `> bootstrap`
After customization, create all directory structures, seed skeleton pages,
write the three hook scripts to `.claude/scripts/`, initialize `sessions.db`.

---

## Domain Conventions

> CUSTOMIZE THIS SECTION for each of your domains.
> Delete placeholder text and replace with domain-specific instructions.
> See examples/domains/ for worked examples.

### DOMAIN_1 — [Domain 1 Name]

**Purpose**: [What this domain covers]

**Key concept pages to seed early**:
- [Concept 1]
- [Concept 2]

**Domain-specific page types**: [Any custom page formats beyond sources/concepts/entities]

**Special rules**: [Anything the LLM should always check or update for this domain]

---

### DOMAIN_2 — [Domain 2 Name]

**Purpose**: [What this domain covers]

**Key concept pages to seed early**:
- [Concept 1]
- [Concept 2]

**Domain-specific page types**: [Any custom page formats]

**Special rules**: [Domain-specific LLM behavior]

---

### DOMAIN_3 — [Domain 3 Name]

**Purpose**: [What this domain covers]

**Key concept pages to seed early**:
- [Concept 1]
- [Concept 2]

**Domain-specific page types**: [Any custom page formats]

**Special rules**: [Domain-specific LLM behavior]

---

## Cross-Domain Connections

> List concept pairs that naturally bridge your domains.
> The LLM will watch for these and create wiki/shared/ pages when found.

Examples:
- [Concept A] (DOMAIN_1 ↔ DOMAIN_2)
- [Person or Org] (DOMAIN_2 ↔ DOMAIN_3)

---

## Tone and Judgment

- Write for the human who owns this wiki. Match their expertise level. Don't
  over-explain things they already know. Do flag things that are new or contradictory.
- Be direct about uncertainty. Surface contradictions — don't smooth them over.
- Prefer specificity over generality. Precise claims age better than vague ones.
- Short pages with good links beat long sprawling pages no one re-reads.
- The log and session exports are sacred — never edit history.

---

## Bootstrapping Sequence

```
> customize          # replace placeholders with your domain names and conventions
> bootstrap          # create directory structure, seed pages, write scripts
> bootstrap privacy  # create .gitignore, .exportignore, sessions/confidential/
> git init && git add wiki/ CLAUDE.md .exportignore .gitignore .claude/ && git commit -m "init wiki"
```

---

## Co-Evolution Note

This schema is a starting point, not a final spec. As your wiki grows, update this
file. If a convention isn't working, change it here and note the change in
`wiki/log.md`. If a new domain emerges, add it. The schema is code — keep it
maintained just like a codebase.

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
