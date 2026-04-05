# Changelog

All notable changes to LLM Wiki Template will be documented here.

Format: [Semantic Versioning](https://semver.org).
Each release notes what was added, changed, fixed, or removed.

---

## [1.1.0] — 2026-04-04

### Added

**Cross-project wiring**
- `scripts/wire-project.py` — wire any project repo to the central wiki
  with one command. Installs hooks and appends wiki integration section
  to CLAUDE.md. Auto-detects wiki root via WIKI_ROOT env var.
- `scripts/wire-all-projects.py` — wire all existing repos at once.
  Scans a directory, skips already-wired repos, shows list before
  making changes. Supports --dry-run and --skip flags.

**Documentation**
- `docs/cross-project-wiring.md` — complete guide to connecting all
  project repos to the central session index
- `docs/obsidian-setup.md` — full Obsidian configuration reference
  including Web Clipper, graph view, mobile setup, Dataview queries
- `examples/use-cases/new-project-checklist.md` — 5-minute checklist
  for wiring every new project from day one

---

## [1.0.0] — 2026-04-04

Initial public release.

### Added

**Core system**
- `scripts/export-session.py` — session transcript → markdown export
  - Claude Code hook mode (reads JSON from stdin)
  - Manual mode (auto-detects latest session from `~/.claude/projects/`)
  - Confidential label → GPG encryption + routing to `sessions/confidential/`
  - Sentinel file check (`.claude/no-export`) for skipping sensitive sessions
  - Deduplication logic (PreCompact + SessionEnd don't double-export)
- `scripts/index-sessions.sh` — SQLite FTS5 indexer
  - `.exportignore` pattern matching
  - Idempotent (safe to run repeatedly)
  - Clear progress reporting
- `scripts/recall.sh` — session search
  - FTS5 keyword search with BM25 ranking and snippet extraction
  - `--recent N`, `--date YYYY-MM`, `--list`, `--stats` modes
  - Grep fallback when FTS returns no results
- `scripts/setup.sh` — one-time setup script
  - Adapter selection (claude-code / codex / generic)
  - Prerequisite checking with install instructions
  - Directory creation, script installation, DB initialization

**Adapters**
- `adapters/claude-code/` — Claude Code reference implementation
  - `CLAUDE.md` — generic wiki schema with domain placeholders
  - `.claude/settings.json` — PreCompact, SessionEnd, SessionStart, UserPromptSubmit hooks
  - Full automatic session export via hook system
- `adapters/codex/` — OpenAI Codex CLI adapter
  - `AGENTS.md` — equivalent schema for Codex
  - Manual export workflow with shell aliases
- `adapters/generic/` — tool-agnostic adapter stub

**Examples**
- `examples/domains/govcon-domain.md` — government contracting domain config
- `examples/use-cases/multi-domain.md` — 3-domain, multi-device, collaborators
- `examples/use-cases/solo-researcher.md` — single domain, one person

**Documentation**
- `README.md` — project overview, tool support matrix, quickstart
- `SETUP-GUIDE.md` — complete step-by-step instructions (7 parts)
- `CONTRIBUTING.md` — contribution guide, what we need most
- `adapters/claude-code/README.md` — Claude Code specific notes
- `adapters/codex/README.md` — Codex specific notes

**Configuration templates**
- `.gitignore` — keeps sessions, db, sentinel out of version control
- `.exportignore` — template for index exclusion patterns
- `wiki/index.md` — master catalog template
- `wiki/log.md` — append-only log template

### Credits

- Pattern conceived by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (April 4, 2026)
- Independent parallel implementation described by a welder / drag racing shop developer
  (same day, Karpathy gist comments) — validated the pattern works at scale
- Template implementation by Bashir Aziz with Claude (Anthropic)

---

## Roadmap

### [1.1.0] — planned

- `adapters/cursor/` — Cursor adapter with manual export workflow
- `adapters/aider/` — Aider adapter
- `examples/domains/research-domain.md` — academic research domain
- `examples/domains/personal-domain.md` — personal knowledge / journaling
- `examples/use-cases/team-wiki.md` — shared team wiki with review loop
- PowerShell versions of `index-sessions.sh` and `recall.sh` for Windows

### [1.2.0] — planned

- `scripts/wiki-health.py` — standalone lint / health check script
- `scripts/digest.py` — automated session → wiki page extraction
- Dataview query examples for Obsidian frontmatter
- GitHub Actions workflow: auto-lint wiki on push

### Future

- Gemini CLI adapter (when hook system matures)
- MCP server for recall (search sessions from within Claude Code natively)
- Export format support for non-JSONL transcript formats
