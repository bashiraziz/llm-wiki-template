# Use Case: Multi-Domain Knowledge Base

**Who this is for**: Someone working across 2–4 distinct knowledge domains simultaneously,
wanting a single compounding knowledge base with clear domain separation.

**Example**: A product manager / developer who works in government contracting,
runs an education AI project, and does active research across multiple topics.

**Complexity**: Medium — 3 domains, 3 collaborators, multi-device, confidentiality needed.

---

## Domain configuration

```markdown
| Domain ID  | Name                      | Root folder      |
|------------|---------------------------|------------------|
| `govcon`   | GovCon / FAR / Regulatory | `wiki/govcon/`   |
| `edu`      | Education AI Project      | `wiki/edu/`      |
| `research` | General Research          | `wiki/research/` |
```

## Directory structure additions

```
wiki/
├── govcon/
│   ├── changes/          # active regulatory changes
│   └── regulations/      # one page per FAR/CAS section
├── edu/
│   ├── observations/     # field notes from partner researchers
│   ├── geographies/      # country-specific context pages
│   └── plan/             # phased project plan (living document)
├── research/
│   └── threads/          # active research questions being pursued
└── shared/               # cross-domain concept pages
```

## Cross-domain connections to watch for

```markdown
- AI policy (edu ↔ research)
- Financial controls / cost accounting (govcon ↔ research)
- LLM tooling and workflow (all domains)
- Geopolitical context for partner countries (edu ↔ research)
```

## Confidentiality setup

Three types of sensitive sessions in this setup:

```bash
# Career conversations, job interviews:
touch .claude/no-export

# Client / NDA govcon work:
touch .claude/no-export

# Conversations involving real people's personal data (e.g. children in education project):
touch .claude/no-export
# or: export-session.py --label confidential  (for archival with encryption)
```

.exportignore additions:
```
*_momentus_*.md
*_client_*.md
*_personal_*.md
*_eoj_*.md
```

## Multi-device workflow

Primary machine: MacBook (main development)
Secondary machine: Work Windows PC
Mobile: iPhone (read-only via Obsidian + iCloud)

```bash
# Every session start (all machines):
git pull && claude

# Every session end (all machines):
git add wiki/ && git commit -m "session: [topic]" && git push

# Mobile (iPhone):
# Obsidian iOS opens wiki/ via iCloud symlink — read-only reference
# Quick notes → paste into next desktop session as > update [domain] [page]
```

## edu domain: observation-first philosophy

The education AI project in this configuration follows a strict
observation-first approach: no technology decisions until field research
is complete.

```markdown
### edu — Education AI Project

**Purpose**: Track the design, research, and development of an AI-powered
educational tool for underserved children. Observation-first: understand
what children need before deciding what to build.

**Collaborators**:
- [Partner 1] — field researcher (Uganda), files observation notes
- [Partner 2] — curriculum specialist (Pakistan), files curriculum research

**Domain-specific page types**:

observations/DATE-SLUG.md — field notes from partner researchers:
    ---
    date: YYYY-MM-DD
    observer: [Name]
    location: [Country/Region]
    grade_level: [e.g. P2]
    ---
    ## Setting
    ## What Was Observed
    ## Learning Patterns Noted
    ## Implications for Tool Design
    ## Questions Raised

plan/PROJECT-PLAN.md — living project plan:
    Mark phases [COMPLETE] or [REVISED: reason].
    Never delete history — evolution of the plan is itself knowledge.

**Special rules**:
- File every observation note immediately
- Extract learning patterns and update concepts/ pages
- Check every observation against the project plan
- Track open questions: what do children need vs. what technology can do?
- Current phase always noted in edu/overview.md
```

## Weekly rhythm

```
Monday: git pull, start week's sessions
Throughout week: ingest sources, ask questions, file answers
Friday: digest sessions → wiki pages, lint, git push
```

## Obsidian setup for multi-domain

Open `wiki/` as vault. Use these saved searches:

```
# All govcon pages updated this week:
path:govcon file-mtime:2026-04-01..2026-04-07

# All orphan concept pages (no inbound links):
[[  (empty backlinks panel in graph view shows these)

# All open questions across wiki:
"Open Questions" has:open-questions
```

Graph view filter: show only `wiki/` (exclude `sessions/`, `raw/`).
Color nodes by domain folder for instant visual separation.
