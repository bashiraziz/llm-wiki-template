# Generic Adapter

Use this adapter if your LLM tool isn't Claude Code or Codex CLI, or if you're
building your own LLM interface.

---

## What's tool-agnostic vs. tool-specific

**Tool-agnostic (works with anything):**
- The wiki architecture (markdown files, index.md, log.md, cross-references)
- The SQLite FTS5 session index
- The recall search system
- The Obsidian integration
- The git multi-device workflow
- The confidentiality controls
- All three scripts (export-session.py, index-sessions.sh, recall.sh)

**Tool-specific (needs adaptation):**
- The schema filename (`CLAUDE.md` for Claude Code, `AGENTS.md` for Codex)
- Automatic session export hooks (currently Claude Code only)
- How the schema file is loaded into context

---

## Setup for any tool

```bash
bash scripts/setup.sh generic
```

This copies `WIKI-SCHEMA.md` to your repo root and sets up all scripts.
Rename it to whatever your tool expects, or load it manually into your system prompt.

---

## Making export automatic for your tool

If your tool supports hooks or callbacks, wire `export-session.py` to fire
before context compression. The script reads a JSON payload from stdin:

```json
{
  "session_id": "abc12345",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/path/to/my-wiki"
}
```

If your tool writes transcripts in a different format, modify the
`parse_jsonl_to_markdown()` function in `scripts/export-session.py` to match
your tool's output format.

---

## Contributing a new adapter

If you build an adapter for a new tool, please contribute it back:

1. Create `adapters/YOUR-TOOL/` directory
2. Add the schema file with tool-specific naming (`SCHEMA.md`, `RULES.md`, etc.)
3. Add a `README.md` explaining tool-specific setup and limitations
4. Open a PR

See `adapters/claude-code/` as the reference implementation.
