# Example Domain: Personal Knowledge

A fully worked example of a personal domain — tracking goals, health,
psychology, self-improvement. Filing journal entries, articles, podcast notes,
and building a structured picture of yourself over time.

Works for: personal development, health tracking, journaling with structure,
goal tracking, habit analysis, reflection practice.

---

## Domain entry for the domain table

```markdown
| `personal` | Personal Knowledge | `wiki/personal/` |
```

## Directory additions

```
wiki/personal/
├── overview.md        # current self-model — where you are, where you're going
├── sources/           # books, articles, podcasts that shaped your thinking
├── concepts/          # frameworks you use to understand yourself and the world
├── goals/             # active and archived goals — one page each
├── journals/          # structured summaries of journal entries (not raw journals)
└── patterns/          # recurring observations about yourself
```

## Domain conventions block

```markdown
### personal — Personal Knowledge

**Purpose**: Build a structured, evolving understanding of yourself — your
patterns, goals, values, psychology, and how you're changing over time.
The LLM files and cross-references; you do the living and reflecting.

**IMPORTANT — Privacy**: Personal domain sessions are almost always
confidential. Default to using the sentinel before personal sessions:
    touch .claude/no-export
Or say "This session is personal" at the first prompt.

**Key concept pages to seed early**:
- [Your core values — what you've identified as non-negotiable]
- [Your working style / how you do your best work]
- [Recurring challenges or patterns you've noticed]
- [Your decision-making framework]

**Domain-specific page types**:

goals/GOAL-NAME.md — active and archived goals:
    ---
    title: "Goal Name"
    status: active | paused | achieved | abandoned
    started: YYYY-MM-DD
    target_date: YYYY-MM-DD or ongoing
    domain: health | work | learning | relationship | financial | other
    ---
    ## What and Why
    ## Current Status
    ## Key Actions
    ## What's Working / Not Working
    ## History (append, never delete)

journals/YYYY-MM.md — monthly structured journal summaries:
    NOT raw journal entries — structured summaries of themes and patterns.
    Raw journals stay in raw/personal/ if you keep them.
    ---
    month: YYYY-MM
    themes: []
    ---
    ## Key Themes This Month
    ## Progress on Goals
    ## Patterns Observed
    ## What Changed in My Thinking

patterns/PATTERN-NAME.md — recurring observations:
    ---
    title: "Pattern: [Name]"
    first_observed: YYYY-MM-DD
    frequency: always | often | sometimes
    ---
    ## What the Pattern Is
    ## When It Shows Up
    ## Root Cause Hypothesis
    ## What Helps
    ## Evidence (sources + journal entries that confirm/refute)

**Special rules**:
- Never store raw sensitive personal data (health numbers, financial details,
  relationship specifics) in wiki pages — these belong in dedicated apps
  with proper security. Wiki pages store patterns, observations, frameworks.
- When filing a journal summary, extract the patterns — don't summarize events.
  "Noticed I procrastinate most on tasks with unclear success criteria" is
  more valuable than "Had a hard week at work."
- Goals get updated, never replaced — mark old status [REVISED: reason].
  The history of how a goal evolved is itself valuable.
- overview.md is your current self-model: where you are, what matters,
  what you're working on. Update it quarterly or when something significant shifts.

**Output formats for queries**:
- "How am I doing on X goal?" → read goals/X.md and recent journals
- "What patterns keep coming up?" → review patterns/ and synthesize
- "What's changed in my thinking about Y?" → compare overview.md + journal summaries
- "What should I focus on?" → review active goals + current patterns + overview
```

## Privacy configuration for personal domain

Add to `.exportignore`:
```
*_personal_*.md
*_journal_*.md
*_health_*.md
```

Always use `touch .claude/no-export` before personal sessions, or say
"This session is personal" at the first prompt.

## What NOT to put in the wiki

The wiki is for structured knowledge — patterns, frameworks, observations.
Not for:
- Raw journal entries (keep those in raw/personal/ or a dedicated journal app)
- Medical records or precise health metrics (use a health app)
- Financial account details (use a password manager or financial app)
- Anything you'd be uncomfortable with someone else reading

The wiki is searchable and lives in a git repo. Design it accordingly.

## Cross-domain connections to watch for

- Personal ↔ Work: working style patterns that affect professional output
- Personal ↔ Research: research findings that directly apply to personal goals
- Personal ↔ any domain: values and decision frameworks that cross contexts
