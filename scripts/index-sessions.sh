#!/bin/bash
# index-sessions.sh — LLM Wiki Template
# ========================================
# Indexes session export markdown files into a SQLite FTS5 database.
# Safe to run repeatedly — skips already-indexed files.
# Respects .exportignore patterns.
#
# Usage:
#   bash scripts/index-sessions.sh
#
# Run automatically at SessionStart (Claude Code) or manually before searching.
#
# Requirements:
#   sqlite3 (brew install sqlite3 / apt install sqlite3)
#   python3 (for JSON escaping)

set -euo pipefail

DB="sessions.db"
EXPORT_DIR="sessions/exports"

# ── Must run from wiki root ────────────────────────────────────────────────────
if [ ! -f "CLAUDE.md" ] && [ ! -f "AGENTS.md" ] && [ ! -f "WIKI-SCHEMA.md" ]; then
  echo "⚠️  Run from your wiki root directory (where CLAUDE.md / AGENTS.md lives)."
  exit 1
fi

# ── Verify sqlite3 is available ───────────────────────────────────────────────
if ! command -v sqlite3 &> /dev/null; then
  echo "⚠️  sqlite3 not found."
  echo "    Mac:   brew install sqlite3"
  echo "    Linux: sudo apt install sqlite3"
  exit 1
fi

# ── Create database schema if it doesn't exist ────────────────────────────────
sqlite3 "$DB" <<'SQL'
CREATE TABLE IF NOT EXISTS sessions_raw (
  id           INTEGER PRIMARY KEY,
  filename     TEXT UNIQUE,
  session_id   TEXT,
  export_date  TEXT,
  trigger      TEXT,
  content      TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts
  USING fts5(
    filename,
    session_id,
    export_date,
    trigger,
    content,
    content=sessions_raw,
    content_rowid=id
  );

CREATE TRIGGER IF NOT EXISTS sessions_ai
  AFTER INSERT ON sessions_raw BEGIN
    INSERT INTO sessions_fts(rowid, filename, session_id, export_date, trigger, content)
    VALUES (new.id, new.filename, new.session_id, new.export_date, new.trigger, new.content);
  END;
SQL

# ── Index new files ────────────────────────────────────────────────────────────
INDEXED=0
SKIPPED=0
ERRORS=0

# Create export dir if it doesn't exist yet
mkdir -p "$EXPORT_DIR"

for f in "$EXPORT_DIR"/*.md; do
  # Handle empty directory
  [ -f "$f" ] || continue

  BASENAME=$(basename "$f")

  # ── Control 2: .exportignore check ──────────────────────────────────────────
  IGNORED=0
  if [ -f ".exportignore" ]; then
    while IFS= read -r pattern || [ -n "$pattern" ]; do
      # Skip blank lines and comments
      [[ "$pattern" =~ ^[[:space:]]*$ ]] && continue
      [[ "$pattern" =~ ^# ]] && continue
      # shellcheck disable=SC2254
      case "$BASENAME" in
        $pattern) IGNORED=1; break ;;
      esac
    done < ".exportignore"
  fi

  if [ "$IGNORED" = "1" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  # Skip already-indexed files
  ALREADY=$(sqlite3 "$DB" "SELECT COUNT(*) FROM sessions_raw WHERE filename='$BASENAME';")
  [ "$ALREADY" = "0" ] || continue

  # Extract metadata from filename (format: YYYY-MM-DD_HHMMSS_sessionid_trigger.md)
  SESSION_ID=$(echo "$BASENAME" | grep -oE '[a-f0-9]{8}' | head -1 || echo "unknown")
  EXPORT_DATE=$(echo "$BASENAME" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || echo "unknown")
  TRIGGER=$(echo "$BASENAME" | grep -oE '(precompact|sessionend|manual)' | head -1 || echo "unknown")

  # JSON-escape the content for safe insertion
  CONTENT=$(cat "$f")
  ESCAPED=$(python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' <<< "$CONTENT" 2>/dev/null)

  if [ -z "$ESCAPED" ]; then
    echo "⚠️  Failed to process: $BASENAME" >&2
    ERRORS=$((ERRORS + 1))
    continue
  fi

  sqlite3 "$DB" "
    INSERT OR IGNORE INTO sessions_raw (filename, session_id, export_date, trigger, content)
    VALUES ('$BASENAME', '$SESSION_ID', '$EXPORT_DATE', '$TRIGGER', $ESCAPED);
  " 2>/dev/null && INDEXED=$((INDEXED + 1)) || ERRORS=$((ERRORS + 1))

done

# ── Report ─────────────────────────────────────────────────────────────────────
TOTAL=$(sqlite3 "$DB" "SELECT COUNT(*) FROM sessions_raw;" 2>/dev/null || echo "?")

[ "$INDEXED" -gt 0 ] && echo "📚 Indexed $INDEXED new session(s) → sessions.db (total: $TOTAL)"
[ "$SKIPPED" -gt 0 ] && echo "🔒 Skipped $SKIPPED session(s) excluded by .exportignore"
[ "$ERRORS"  -gt 0 ] && echo "⚠️  $ERRORS error(s) during indexing — check file encoding"
[ "$INDEXED" -eq 0 ] && [ "$SKIPPED" -eq 0 ] && [ "$ERRORS" -eq 0 ] && \
  echo "✓  sessions.db up to date ($TOTAL session(s) indexed)"

exit 0
