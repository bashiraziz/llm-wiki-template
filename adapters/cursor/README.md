# Cursor Adapter

> **Status**: Stub — full adapter coming in v1.1.0.

Cursor does not currently have an equivalent to Claude Code's `CLAUDE.md`
auto-loading or the `PreCompact` hook system. This limits automation.

## Workaround for Cursor

1. Copy `adapters/generic/WIKI-SCHEMA.md` to your repo root
2. Add it to Cursor's "Always include in context" setting if available,
   or paste its contents into your system prompt
3. Use manual session export at the end of each session:
   ```bash
   python3 scripts/export-session.py --trigger manual
   ```
4. The wiki architecture, SQLite search, and Obsidian setup work identically

## Contributing

If you use Cursor and figure out a better integration, please open a PR.
The most valuable thing would be: a way to auto-load the schema file and
a hook or script that fires automatically when Cursor ends a session.

See `adapters/claude-code/` for the reference implementation to adapt from.
