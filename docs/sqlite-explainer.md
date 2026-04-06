# SQLite FTS5 Session Index — How It Works

The wiki's session search is powered by SQLite's FTS5 (Full-Text Search 5)
extension. No server, no embeddings, no API calls — just a local file
(`sessions.db`) that you can query in milliseconds.

---

## The problem it solves

Claude Code sessions are valuable but ephemeral. After a context compression
or session end, the transcript lives in a raw `.jsonl` file buried in
`~/.claude/projects/`. The export system converts those transcripts to
readable markdown in `sessions/exports/`. But markdown files scattered in
a directory are not searchable. FTS5 makes them searchable.

---

## The database schema

`sessions.db` contains two objects:

### 1. `sessions_raw` — the content table

```sql
CREATE TABLE sessions_raw (
  id           INTEGER PRIMARY KEY,
  filename     TEXT UNIQUE,
  session_id   TEXT,
  export_date  TEXT,
  trigger      TEXT,
  content      TEXT
);
```

One row per exported session file. `content` holds the full markdown text
of the export. `filename` is the basename only (e.g.
`2026-04-05_143022_abc12345_my-wiki_sessionend.md`).

### 2. `sessions_fts` — the FTS5 virtual table

```sql
CREATE VIRTUAL TABLE sessions_fts
  USING fts5(
    filename, session_id, export_date, trigger, content,
    content=sessions_raw,
    content_rowid=id
  );
```

This is the searchable index. `content=sessions_raw` means FTS5 is a
*content table* — it doesn't store its own copy of the text, it reads from
`sessions_raw` at query time. `content_rowid=id` maps FTS5 rows to the
primary key in `sessions_raw`.

### 3. The insert trigger

```sql
CREATE TRIGGER sessions_ai
  AFTER INSERT ON sessions_raw BEGIN
    INSERT INTO sessions_fts(rowid, filename, session_id, export_date, trigger, content)
    VALUES (new.id, new.filename, new.session_id, new.export_date, new.trigger, new.content);
  END;
```

Every time a row is inserted into `sessions_raw`, this trigger automatically
updates the FTS5 index. You never call anything twice — insert once, search
immediately.

---

## How indexing works

`index-sessions.py` (or `.sh`) runs on `SessionStart` and whenever you call
it manually. It:

1. Scans every `.md` file in `sessions/exports/`
2. Checks `.exportignore` — skips files matching any pattern
3. Queries `sessions_raw` — skips files already indexed (`SELECT COUNT(*)
   WHERE filename = ?`)
4. For new files: reads the content, parses the filename for metadata
   (date, session ID, trigger), inserts into `sessions_raw`
5. The trigger fires automatically, updating `sessions_fts`

This is idempotent — safe to run repeatedly. It only processes files it
hasn't seen before.

---

## How search works

`recall.py` issues FTS5 `MATCH` queries:

```sql
SELECT s.export_date, s.filename,
       snippet(sessions_fts, 4, '>>> ', ' <<<', '...', 25) AS excerpt
FROM sessions_fts
JOIN sessions_raw s ON sessions_fts.rowid = s.id
WHERE sessions_fts MATCH 'your search terms'
ORDER BY rank
LIMIT 5;
```

Key FTS5 features in use:

**`MATCH`** — full-text search across all indexed columns. Supports
phrase queries (`"exact phrase"`), prefix queries (`pool*`), and boolean
operators (`pool AND rate NOT overhead`).

**`rank`** — FTS5's built-in BM25 relevance score. `ORDER BY rank`
returns the most relevant results first. BM25 weighs term frequency
against document frequency — common words score lower, rare precise
matches score higher.

**`snippet()`** — extracts a short excerpt around the matched terms,
with configurable highlight markers and context window. The `4` is the
column index (content), `25` is the max tokens in the snippet.

---

## Querying the database directly

You can bypass `recall.py` and query `sessions.db` directly with the
`sqlite3` CLI:

```bash
# Basic keyword search
sqlite3 sessions.db \
  "SELECT filename, snippet(sessions_fts, 4, '>>>', '<<<', '...', 30)
   FROM sessions_fts
   WHERE sessions_fts MATCH 'indirect rate pool'
   ORDER BY rank LIMIT 5;"

# Phrase search (exact sequence of words)
sqlite3 sessions.db \
  "SELECT filename FROM sessions_fts
   WHERE sessions_fts MATCH '\"allowable cost\" AND FAR'
   ORDER BY rank LIMIT 10;"

# List all indexed sessions with dates
sqlite3 sessions.db \
  "SELECT export_date, filename FROM sessions_raw ORDER BY export_date DESC;"

# Count total sessions indexed
sqlite3 sessions.db "SELECT COUNT(*) FROM sessions_raw;"

# Show sessions from a specific date
sqlite3 sessions.db \
  "SELECT filename FROM sessions_raw WHERE export_date LIKE '2026-04%';"
```

---

## The .exportignore control

Before a file is inserted into `sessions_raw`, the indexer checks its
filename against patterns in `.exportignore`. This is a glob match against
the basename only:

```
*_confidential_*.md   → never indexed
*_client_*.md         → never indexed (if uncommented)
```

Files excluded by `.exportignore` remain on disk in `sessions/exports/`
as a plaintext backup but are invisible to all search queries. The index
never knows they exist.

---

## Why FTS5 and not a vector database

| | FTS5 | Vector DB |
|---|---|---|
| Setup | Zero — SQLite ships everywhere | Server, API, embeddings pipeline |
| Search latency | <5ms on 1000 sessions | Varies, often 100ms+ |
| Query model | Keyword + boolean + phrase | Semantic similarity |
| Works offline | Yes | Only if self-hosted |
| Finds exact phrases | Yes | Unreliable |
| Finds conceptual matches | No | Yes |
| Maintenance | None | Re-embed on model change |

For session recall — "find the session where we talked about pool rate
allocation" — keyword search is often more precise than semantic search.
You know the words you used. FTS5 finds them exactly.

---

## Rebuilding the index

The index is always regenerable from the export files. If `sessions.db`
is lost, corrupt, or out of sync:

```bash
rm -f sessions.db
python .claude/scripts/index-sessions.py
# or:
bash .claude/scripts/index-sessions.sh
```

All previously exported sessions are re-indexed. Nothing is lost.
The database is intentionally excluded from git (`.gitignore`) for this
reason — it is local scratch, not source of truth. The markdown files
in `sessions/exports/` are the source of truth.

---

## File locations

| File | Purpose |
|---|---|
| `sessions.db` | The SQLite database (local only, gitignored) |
| `sessions/exports/*.md` | Source of truth for all session content |
| `.claude/scripts/index-sessions.py` | Indexer — reads exports, writes DB |
| `.claude/scripts/recall.py` | Search — queries DB, prints results |
| `.exportignore` | Glob patterns excluded from indexing |

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
