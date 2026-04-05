# Contributing to LLM Wiki Template

Thank you for contributing. This project is a community implementation of
Andrej Karpathy's LLM Wiki pattern — the goal is to make it accessible to
anyone, regardless of which LLM tool they use.

---

## What we most need

### New tool adapters

The highest-value contributions are adapters for LLM tools not yet supported:

- **Gemini CLI** (Google)
- **Aider**
- **Zed AI**
- **Cursor** (beyond the stub in adapters/cursor/)
- **Continue.dev**
- **Any tool with a hook/callback system**

To add an adapter:
1. Create `adapters/YOUR-TOOL/` directory
2. Add the schema file with the tool's expected filename
   (`RULES.md`, `SYSTEM.md`, `CONVENTIONS.md` — whatever your tool reads automatically)
3. Add `README.md` explaining:
   - How to install the schema file
   - Whether automatic session export is possible (and how)
   - Any tool-specific limitations
   - Setup instructions specific to this tool
4. If automatic export is possible, document the hook/trigger mechanism
5. Open a PR

See `adapters/claude-code/` as the reference implementation.

### New domain examples

`examples/domains/` helps people understand how to configure the template
for their specific use case. Good domain examples to add:

- `reading-domain.md` — book-by-book reading with character/theme tracking
- `health-domain.md` — personal health tracking, journal → structured knowledge
- `legal-domain.md` — case law, precedents, regulatory tracking
- `engineering-domain.md` — technical decisions, architecture, runbooks
- `investing-domain.md` — company research, thesis tracking, portfolio notes
- `language-learning-domain.md` — vocabulary, grammar, cultural notes

### New use case examples

`examples/use-cases/` shows complete configurations. Useful additions:

- `team-wiki.md` — shared wiki with human review loop
- `book-deep-dive.md` — reading one book in depth (Tolkien Gateway style)
- `competitive-intel.md` — tracking a market or set of competitors
- `podcast-notes.md` — building a wiki from podcast episode notes

### Script improvements

- **Windows compatibility** for `index-sessions.sh` and `recall.sh`
  (currently bash-only — a PowerShell version or Python rewrite would help)
- **Better deduplication** in `export-session.py` for edge cases
- **Incremental FTS5 rebuild** when content changes
- **Export format support** for non-JSONL transcript formats (Cursor, Aider, etc.)
- **`recall.sh` improvements**: date range search, domain-filtered search

### Cross-platform improvements

- **Windows paths in wire-project.py** — the script handles Windows paths
  but more testing needed. PRs with Windows-specific fixes welcome.
- **wire-all-projects.py for monorepos** — current version scans a flat
  directory of repos. Support for nested repo structures.
- **Shell completion** — bash/zsh completion for wire-project.py arguments.

---

## How to contribute

### For small changes (typos, clarifications)

Open a PR directly. No issue needed.

### For new features or adapters

1. Open an issue first describing what you want to add
2. Wait for a thumbs-up before building (avoids duplicate work)
3. Build on a branch: `git checkout -b adapter/gemini-cli`
4. Open a PR with a clear description

### PR checklist

- [ ] Tested locally (describe what you tested)
- [ ] New files follow existing naming conventions
- [ ] README updated if adding a new adapter or use case
- [ ] No personal/private information included
- [ ] Scripts are executable (`chmod +x`) where applicable

---

## Code style

**Markdown**: Use ATX headers (`##`), fenced code blocks with language tags,
and tables for structured comparisons. Keep line length under ~100 chars for
readability in Obsidian.

**Shell scripts**: `set -euo pipefail` at the top. Comment non-obvious logic.
Provide clear error messages with actionable install instructions.

**Python**: Standard library only (no third-party dependencies). Python 3.6+
compatible. Type hints optional but welcome. Docstrings for all functions.

**Naming**: Filenames use kebab-case (`govcon-domain.md`, `solo-researcher.md`).
Directory names use kebab-case. Script names use kebab-case with extensions.

---

## Questions

Open an issue with the `question` label. No question is too basic —
if something in the setup guide is unclear, that's a documentation bug.

---

*Pattern by Andrej Karpathy · Template by Bashir Aziz · MIT License*
