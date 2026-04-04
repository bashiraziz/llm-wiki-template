#!/bin/bash
# recall.sh — LLM Wiki Template
# ================================
# Search past session exports by keyword.
# The "remember that thing we built?" command.
#
# Usage:
#   bash scripts/recall.sh "search terms"
#   bash scripts/recall.sh --recent [N]        # last N sessions (default 5)
#   bash scripts/recall.sh --date YYYY-MM      # sessions from a specific month
#   bash scripts/recall.sh --date YYYY-MM-DD   # sessions from a specific day
#   bash scripts/recall.sh --list              # list all indexed sessions
#   bash scripts/recall.sh --stats             # show index statistics
#
# Uses SQLite FTS5 for ranked full-text search.
# Falls back to grep if SQLite returns no results.
#
# Requirements:
#   sqlite3

DB="sessions.db"
EXPORT_DIR="sessions/exports"

# ── Helpers ────────────────────────────────────────────────────────────────────

check_db() {
  if [ ! -f "$DB" ]; then
    echo "⚠️  sessions.db not found. Run: bash scripts/index-sessions.sh"
    exit 1
  fi
}

print_result() {
  local date="$1"
  local fname="$2"
  local excerpt="$3"
  echo "📄 $date — $fname"
  if [ -n "$excerpt" ]; then
    # Indent excerpt lines for readability
    echo "$excerpt" | sed 's/^/   /'
  fi
  echo ""
}

# ── Commands ───────────────────────────────────────────────────────────────────

if [ "$1" = "--recent" ]; then
  COUNT="${2:-5}"
  check_db
  echo "📋 Last $COUNT session(s):"
  echo ""
  sqlite3 "$DB" \
    "SELECT export_date, filename FROM sessions_raw
     ORDER BY export_date DESC, id DESC
     LIMIT $COUNT;" \
  | while IFS='|' read -r date fname; do
      echo "  📄 $date — $fname"
    done
  echo ""
  exit 0
fi

if [ "$1" = "--date" ]; then
  DATE_FILTER="${2:-}"
  if [ -z "$DATE_FILTER" ]; then
    echo "Usage: recall.sh --date YYYY-MM or YYYY-MM-DD"
    exit 1
  fi
  check_db
  echo "📅 Sessions from $DATE_FILTER:"
  echo ""
  sqlite3 "$DB" \
    "SELECT export_date, filename FROM sessions_raw
     WHERE export_date LIKE '$DATE_FILTER%'
     ORDER BY export_date DESC;" \
  | while IFS='|' read -r date fname; do
      echo "  📄 $date — $fname"
    done
  echo ""
  exit 0
fi

if [ "$1" = "--list" ]; then
  check_db
  TOTAL=$(sqlite3 "$DB" "SELECT COUNT(*) FROM sessions_raw;")
  echo "📋 All indexed sessions ($TOTAL total):"
  echo ""
  sqlite3 "$DB" \
    "SELECT export_date, trigger, filename FROM sessions_raw
     ORDER BY export_date DESC, id DESC;" \
  | while IFS='|' read -r date trigger fname; do
      echo "  [$date] ($trigger) $fname"
    done
  echo ""
  exit 0
fi

if [ "$1" = "--stats" ]; then
  check_db
  echo "📊 Session index statistics:"
  echo ""
  sqlite3 "$DB" "SELECT COUNT(*) || ' total sessions indexed' FROM sessions_raw;"
  sqlite3 "$DB" \
    "SELECT export_date || ': ' || COUNT(*) || ' session(s)'
     FROM sessions_raw
     GROUP BY export_date
     ORDER BY export_date DESC
     LIMIT 10;"
  echo ""
  DBSIZE=$(du -sh "$DB" 2>/dev/null | cut -f1 || echo "unknown")
  echo "  Database size: $DBSIZE"
  echo ""
  exit 0
fi

# ── Keyword search ─────────────────────────────────────────────────────────────

QUERY="$*"

if [ -z "$QUERY" ]; then
  echo "LLM Wiki — Session Recall"
  echo ""
  echo "Usage:"
  echo "  recall.sh <search terms>            — keyword search"
  echo "  recall.sh --recent [N]              — last N sessions"
  echo "  recall.sh --date YYYY-MM            — sessions from month"
  echo "  recall.sh --date YYYY-MM-DD         — sessions from day"
  echo "  recall.sh --list                    — all indexed sessions"
  echo "  recall.sh --stats                   — index statistics"
  exit 0
fi

check_db

echo "🔍 Searching sessions for: \"$QUERY\""
echo ""

# SQLite FTS5 search with BM25 ranking and snippet extraction
RESULTS=$(sqlite3 "$DB" \
  "SELECT
     s.export_date,
     s.filename,
     snippet(sessions_fts, 4, '>>> ', ' <<<', '...', 30) as excerpt
   FROM sessions_fts
   JOIN sessions_raw s ON sessions_fts.rowid = s.id
   WHERE sessions_fts MATCH '$QUERY'
   ORDER BY rank
   LIMIT 8;" 2>/dev/null)

FTS_COUNT=$(sqlite3 "$DB" \
  "SELECT COUNT(*) FROM sessions_fts WHERE sessions_fts MATCH '$QUERY';" 2>/dev/null || echo "0")

if [ -n "$RESULTS" ] && [ "$FTS_COUNT" -gt "0" ]; then
  echo "$RESULTS" | while IFS='|' read -r date fname excerpt; do
    print_result "$date" "$fname" "$excerpt"
  done
  [ "$FTS_COUNT" -gt "8" ] && echo "  (showing top 8 of $FTS_COUNT matches)"
else
  echo "  No FTS results. Falling back to grep..."
  echo ""

  GREP_RESULTS=$(grep -ril "$QUERY" "$EXPORT_DIR/" 2>/dev/null)

  if [ -n "$GREP_RESULTS" ]; then
    echo "$GREP_RESULTS" | head -8 | while read -r f; do
      BNAME=$(basename "$f")
      DATE=$(echo "$BNAME" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || echo "unknown")
      EXCERPT=$(grep -m 2 -i "$QUERY" "$f" | head -c 200)
      print_result "$DATE" "$BNAME" "$EXCERPT"
    done
  else
    echo "  No results found for \"$QUERY\""
    echo ""
    echo "  Tips:"
    echo "    • Try broader terms (e.g. 'pool rates' instead of 'pool rate allocation base')"
    echo "    • Check if sessions are indexed: bash scripts/index-sessions.sh"
    echo "    • List all sessions: bash scripts/recall.sh --list"
  fi
fi

exit 0
