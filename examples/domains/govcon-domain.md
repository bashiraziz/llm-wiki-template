# Example Domain: Government Contracting (GovCon)

This is a fully worked example of a GovCon domain configuration.
Copy the relevant sections into your `CLAUDE.md` domain conventions.

Used in: [Bashir Aziz's multi-domain setup](../use-cases/multi-domain.md)

---

## Domain entry for the domain table

```markdown
| `govcon` | GovCon / FAR / Regulatory | `wiki/govcon/` |
```

## Directory additions

```
wiki/govcon/
├── overview.md
├── sources/
├── regulations/          # FAR parts, CAS standards, DFARS clauses — one page each
├── concepts/             # Cost principles, indirect rates, EVM, etc.
├── entities/             # Agencies (DCAA, DoD, GSA), contractors, tools
└── changes/              # Active regulatory changes — track status over time
```

## Domain conventions block

```markdown
### GovCon — Government Contracting / FAR / Regulatory

**Purpose**: Track FAR regulations, cost accounting standards, DCAA compliance
requirements, and regulatory changes relevant to government contracting work.
Build a permanent reference that compounds with every new regulation read,
memo reviewed, or training module built.

**Key concept pages to seed early**:
- FAR Part 31 cost principles (each 31.205-x clause is a candidate for its own page)
- Indirect cost rates (fringe benefits, overhead, G&A, facilities capital cost of money)
- Cost Accounting Standards (CAS 401–420 — each standard gets its own page)
- DCAA audit process and Incurred Cost Submission (ICS)
- Truth in Negotiations Act (TINA)
- Earned Value Management (EVM)
- Unallowable costs and expressly unallowable costs
- Pool rates and allocation bases

**Domain-specific page types**:

changes/TOPIC.md — track active regulatory changes:
    ---
    title: "Change Title"
    status: proposed | final | effective | superseded
    effective_date: YYYY-MM-DD or TBD
    regulation: FAR | CAS | DFARS | EO | NDAA
    ---
    ## What Changed
    ## Current Status
    ## Practical Impact
    ## Source References

**Special rules**:
- After every govcon ingest, check wiki/govcon/changes/ — does this source
  update the status of any tracked regulatory change?
- Note training app impact in every source page (if applicable):
  Which deployed tools or modules does this change affect?
- Flag expressly unallowable costs explicitly — DCAA treats these differently
  from merely unallowable costs and the distinction matters.
- CAS-covered contracts have additional disclosure requirements — always note
  when a source is relevant to CAS-covered vs. non-CAS work.
```

## Seed pages for changes/

Pre-populate these pages immediately after bootstrapping:

### changes/rfo-part31.md
```markdown
---
title: "Revolutionary FAR Overhaul (RFO) — Part 31 Changes"
status: proposed
effective_date: TBD
regulation: FAR
---
# RFO Part 31 Changes
## What Changed
## Current Status
## Practical Impact
## Source References
```

### changes/ndaa-fy2026-cas-thresholds.md
```markdown
---
title: "FY2026 NDAA — CAS Coverage Threshold Changes"
status: final
effective_date: 2026-06-30
regulation: CAS | NDAA
---
# FY2026 NDAA CAS Threshold Changes
## What Changed
Full CAS coverage: $50M → $100M
Per-contract threshold: $2.5M → $35M
TINA threshold: $2.5M → $10M
## Current Status
Enacted. Effective June 30, 2026.
## Practical Impact
## Source References
```

### changes/cas-gaap-harmonization.md
```markdown
---
title: "CAS-GAAP Harmonization — Elimination of CAS 404, 408, 409, 411"
status: proposed
effective_date: TBD
regulation: CAS
---
# CAS-GAAP Harmonization
## What Changed
Proposed elimination of: CAS 404, CAS 408, CAS 409, CAS 411
(standards where CAS and GAAP treatment have converged)
## Current Status
## Practical Impact
## Source References
```

## Cross-domain connections for GovCon

- GovCon ↔ Research: GRC (Governance, Risk, Compliance) space — cost accounting
  principles overlap with broader financial controls research
- GovCon ↔ Research: AI transformation of audit and compliance workflows
