# Changelog

All notable changes to LLM Wiki Template will be documented here.

Format: [Semantic Versioning](https://semver.org).
Each release notes what was added, changed, fixed, or removed.

---

## [1.1.2] — 2026-04-10

### Fixed

- `export-session.py` — Hook failures were silent. Added `.claude/hooks.log`:
  every hook invocation (trigger, session ID, transcript path, wiki dir) is
  timestamped and appended. Parse errors and missing-transcript errors are
  logged with detail. Success is logged with the output filename.
  Check this file whenever exports go missing.
- `export-session.py` — stdin read changed from `json.load()` to `read()` +
  `json.loads()` so parse failures can log the raw input for diagnosis.
- `adapters/claude-code/CLAUDE.md` — Corrected PreCompact description:
  the hook fires for manual `/compact` only, **not** for automatic context
  compression. Previous docs said "manual /compact or automatic" — that was wrong.
  SessionEnd is the only automatic safety net for auto-compacted sessions.
- `adapters/claude-code/CLAUDE.md` — Added manual recovery procedure:
  how to export a missed session from the JSONL on disk and re-index it.
- `.gitignore` — Added `.claude/hooks.log` (local debug log, not for commits).

---

## [1.1.1] — 2026-04-05

### Fixed

**Critical bug fixes found during Windows testing**

- `export-session.py` — Parse new Claude Code 2.x JSONL message format
  (`{"type": "user", "message": {...}}` wrapper). Old format still supported.
- `export-session.py` — Always route exports to central wiki (WIKI_ROOT)
  regardless of which project directory Claude Code is running from.
  Previously wrote to cwd, scattering exports across project directories.
- `export-session.py` — Include project name in export filename.
  New format: `YYYY-MM-DD_HHMMSS_<sessionid>_<project>_<trigger>.md`
- `adapters/claude-code/.claude/settings.json` — Tighten UserPromptSubmit
  sentinel trigger from bare word `"confidential"` to exact phrase
  `"this session is confidential"`. The bare word match silently blocked
  ALL exports in domains where "confidential" appears in normal work
  content (DCAA compliance, legal, medical, HR, etc.).
- `scripts/wire-project.py` — Same sentinel trigger fix applied to
  template for future projects.
- `export-session.py` — Windows console encoding: use safe_print()
  to avoid cp1252 emoji encoding errors.

### Added

- Setup Guide Part 5: Windows session closing with `wikiexit` alias
- README: Windows callout and Known Issues table
- `docs/windows-setup.md`: Dedicated Windows setup guide
- `.exportignore`: Better commented template with domain-specific examples
- Warning in CLAUDE.md about UserPromptSubmit trigger customization

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
