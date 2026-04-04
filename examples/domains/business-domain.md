# Example Domain: Business / Competitive Intelligence

A fully worked example of a business domain — tracking competitors, market
landscape, customer insights, product decisions, and strategic context.

Works for: competitive intelligence, market research, product strategy,
due diligence, startup research, industry analysis, investor tracking.

---

## Domain entry for the domain table

```markdown
| `business` | Business / Competitive Intelligence | `wiki/business/` |
```

## Directory additions

```
wiki/business/
├── overview.md          # current market map and strategic thesis
├── sources/             # reports, articles, earnings calls, interviews
├── concepts/            # business models, market dynamics, frameworks
├── entities/            # companies, people, products, markets
├── competitors/         # one page per competitor — living documents
└── signals/             # notable market signals and what they mean
```

## Domain conventions block

```markdown
### business — Business / Competitive Intelligence

**Purpose**: Build a structured, always-current picture of a market, set of
competitors, or strategic landscape. Every source ingested updates the picture.
Every signal gets filed and cross-referenced.

**Key concept pages to seed early**:
- [Your market definition — who are the buyers, what do they buy, why]
- [Key value drivers in this market]
- [Main competitive dynamics — where do players compete, where don't they]
- [Technology shifts affecting the market]

**Domain-specific page types**:

competitors/COMPANY.md — living competitor profile:
    ---
    title: "Company Name"
    entity_type: competitor | adjacent | potential
    status: active | acquired | defunct
    last_updated: YYYY-MM-DD
    ---
    ## What They Do
    ## Business Model
    ## Strengths
    ## Weaknesses / Gaps
    ## Recent Moves
    ## What to Watch
    ## Source History (append on each update)

signals/YYYY-MM-DD-SLUG.md — notable market signals:
    ---
    date: YYYY-MM-DD
    signal_type: product_launch | funding | acquisition | partnership |
                 executive_move | regulatory | customer_behavior | technology
    entities: [Company, Person]
    ---
    ## What Happened
    ## Why It Matters
    ## Implications for [Your Position / Thesis]
    ## Questions Raised

**Special rules**:
- Competitor pages are living documents — always update, never replace.
  Mark outdated sections [AS OF YYYY-MM-DD] rather than deleting.
- After every ingest, check: does this source change the overview.md
  market map or strategic thesis? If yes, update it.
- Signal pages should always end with "Implications for [your position]" —
  raw observation without interpretation doesn't compound.
- Flag when the same signal is confirmed by multiple sources — convergence
  is stronger evidence than a single data point.
- Entity pages for companies should link to all relevant signal pages.

**Confidentiality note**:
If this wiki contains NDA'd information, client research, or proprietary
competitive analysis:
    touch .claude/no-export     (before sessions with sensitive material)
And add to .exportignore:
    *_client_*.md
    *_nda_*.md
    *_confidential_*.md

**Output formats for queries**:
- "What are [Company]'s weaknesses?" → read competitors/company.md, synthesize
- "What happened in [market] last month?" → review signals/ by date
- "What should we be worried about?" → lint for signals pointing the same direction
- "Compare [Company A] vs [Company B]" → markdown table filed as wiki page
- "What's changed in our thesis?" → compare overview.md git history
```

## Seed entities immediately

After bootstrapping, create entity pages for:
- Your own company / position (the anchor for "implications for us")
- Your top 3–5 competitors
- The 2–3 most important customers or customer segments

These become the hub pages everything else links to.

## Cross-domain connections to watch for

- Business ↔ Research: academic or technical research that creates market shifts
- Business ↔ Personal: leadership or communication patterns that affect strategy
- Business ↔ any domain: regulatory changes that affect the market
