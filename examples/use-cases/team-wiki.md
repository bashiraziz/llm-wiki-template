# Use Case: Team Wiki

**Who this is for**: A small team (2–10 people) who want a shared knowledge
base maintained by LLMs, fed by Slack threads, meeting transcripts, project
documents, and customer calls.

**Complexity**: High — multiple contributors, human review loop, shared remote,
merge discipline required.

**Key challenge**: Balancing LLM automation with human judgment on what goes into
the shared wiki. Individual wikis can be fully automated. Team wikis benefit from
a human-in-the-loop review step before changes are committed.

---

## Architecture

```
                    ┌─────────────────────────────────┐
                    │         Shared GitHub Repo       │
                    │     (private, team access)       │
                    └──────┬──────────┬──────────┬─────┘
                           │          │          │
                    ┌──────┘    ┌─────┘    ┌─────┘
                    │           │          │
              ┌─────┴──┐  ┌────┴───┐  ┌───┴────┐
              │ Person 1│  │Person 2│  │Person 3│
              │  (PM)   │  │ (Eng)  │  │ (Sales)│
              └─────────┘  └────────┘  └────────┘
              Each runs Claude Code locally.
              Each has their own sessions/ (local).
              All push wiki/ changes to shared repo.
```

## Recommended workflow for teams

### Option A — Branch + PR (most controlled)

Each contributor works on a branch:
```bash
git checkout -b wiki/session-2026-04-04-meeting-notes
claude
> ingest work raw/work/q2-planning-meeting.md
git add wiki/
git commit -m "ingest: Q2 planning meeting notes"
git push origin wiki/session-2026-04-04-meeting-notes
# Open PR for team review before merging to main
```

The PR review is the human-in-the-loop step. Team members check:
- Is the synthesis accurate?
- Are the cross-references correct?
- Is anything sensitive that shouldn't be in the shared wiki?

### Option B — Direct push (faster, less control)

Everyone pushes directly to `main`. Simpler but requires trust and discipline.
Works well for small teams (2–3 people) who communicate frequently.

```bash
git pull && claude
> ingest work raw/work/customer-call-acme.md
git add wiki/ && git commit -m "ingest: Acme customer call" && git push
```

### Option C — Designated wiki maintainer

One person (the "wiki lead") owns all ingestion. Others file raw sources into
`raw/` and the wiki lead processes them on a schedule (daily or weekly).

Best for: teams where LLM tool adoption is uneven, or where quality control
is critical.

---

## Domain configuration for teams

Add a `shared` or `team` domain for cross-functional knowledge:

```markdown
| `product`    | Product & Roadmap        | `wiki/product/`    |
| `engineering`| Engineering & Systems    | `wiki/engineering/`|
| `customers`  | Customer Intelligence    | `wiki/customers/`  |
| `shared`     | Cross-functional         | `wiki/shared/`     |
```

## Confidentiality in a team wiki

Team wikis require extra care because multiple people access the repo.

Add a `wiki/internal/` directory with a README:
```markdown
# Internal — Access Restricted
Pages in this directory contain information that should not be shared
outside the team. Do not link these pages from public documentation.
```

For NDA'd customer information — either keep it out of the shared wiki entirely,
or use a separate private repo with restricted access.

Add to the team's `.exportignore`:
```
*_confidential_*.md
*_nda_*.md
*_customer-name_*.md    # customer-specific sessions
```

## Feeding the wiki automatically

For teams, the richest sources are:
- **Meeting transcripts** (record → transcribe → drop in raw/) 
- **Slack threads** (export key threads → raw/)
- **Customer call notes** (Gong, Chorus, or manual notes → raw/)
- **Project documents** (PRDs, specs, postmortems → raw/)

Create a shared `raw/incoming/` directory where anyone can drop files.
The wiki maintainer (or each person) ingests from there:
```
> ingest product raw/incoming/q2-prd-draft.md
```

## Git discipline for teams

```bash
# Before every session:
git pull --rebase

# After every session:
git add wiki/
git commit -m "session: [name] [topic]"   # include your name
git push

# If there's a conflict:
git pull --rebase   # rebase your changes on top of new remote changes
# Resolve any conflicts in wiki/ (markdown is easy to merge)
git add wiki/
git rebase --continue
git push
```

## CLAUDE.md additions for team wikis

Add to the Tone and Judgment section:

```markdown
**Team wiki additions**:
- Every wiki page is read by multiple people with different contexts.
  Write entity and concept pages as if the reader hasn't been in recent meetings.
- Flag when a page reflects a single contributor's perspective vs. team consensus.
  Use "According to [source]" not "We believe" unless it's genuinely agreed.
- When ingesting meeting notes, distinguish between:
  - Decisions made (mark clearly)
  - Options discussed (mark as open)
  - Action items (note owner and date)
- Customer intelligence pages should note data source and date prominently.
  Customer needs change — old observations can mislead.
```

## What doesn't work well for team wikis

- **Real-time collaboration**: The git workflow is async. If two people ingest
  sources simultaneously, one will need to resolve a merge conflict. Not a
  blocker, but requires communication.
- **Access control within the repo**: Git repos are all-or-nothing. If you need
  some pages accessible only to certain team members, use separate repos.
- **Automatic ingestion of Slack/email**: Requires building a pipeline from
  those tools to `raw/`. Doable, but out of scope for this template.
