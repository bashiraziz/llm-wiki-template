# LLM Wiki Template — Setup Guide

Complete step-by-step instructions for setting up your personal LLM wiki.

---

## Prerequisites

Install these before starting:

| Tool | Install | Purpose |
|---|---|---|
| Claude Code | `npm install -g @anthropic-ai/claude-code` | LLM agent (reference implementation) |
| Git | pre-installed Mac/Linux · git-scm.com Windows | Version control + multi-device sync |
| Python 3 | pre-installed Mac/Linux · python.org Windows | Session export script |
| SQLite 3 | `brew install sqlite3` Mac · pre-installed Linux · see Windows note below | Session search index |
| GPG | `brew install gnupg` Mac · `apt install gnupg` Linux | Encrypted confidential sessions (optional) |
| Obsidian | obsidian.md | Reading and navigating the wiki |
| Obsidian Web Clipper | obsidian.md/clipper (browser extension) | Clipping web articles to raw/ |

Verify installs:
```bash
claude --version
git --version
python3 --version    # Mac/Linux
python --version     # Windows (use whichever works)
sqlite3 --version
gpg --version        # optional
```

**Windows — SQLite not pre-installed:**
Download `sqlite-tools-win-x64-*.zip` from sqlite.org/download.html, extract
`sqlite3.exe`, and copy it to `C:\Windows\System32\` (requires admin).
See [docs/windows-setup.md](docs/windows-setup.md) for more details.

---

## Part 1 — Initial setup (primary machine)

Do this once on your main machine. All other devices clone from the result.

### Step 1.1 — Clone the template

```bash
git clone https://github.com/bashiraziz/llm-wiki-template.git my-wiki
cd my-wiki
```

### Step 1.2 — Run the setup script

```bash
bash scripts/setup.sh
# Default adapter: claude-code
# For Codex: bash scripts/setup.sh codex
# For other tools: bash scripts/setup.sh generic
```

The setup script:
- Checks prerequisites
- Creates `raw/`, `sessions/`, and `wiki/` directories
- Copies the adapter files (`CLAUDE.md`, `.claude/settings.json`) to the repo root
- Installs scripts to `.claude/scripts/` and makes them executable
- Creates `.gitignore` and `.exportignore`
- Initializes the SQLite database

### Step 1.3 — Customize your domains

Open `CLAUDE.md` and replace the placeholder domain names:

```
DOMAIN_1  →  research       (or whatever your first domain is)
DOMAIN_2  →  work
DOMAIN_3  →  personal
```

See `examples/domains/` for fully worked domain configurations.
See `examples/use-cases/` for complete setups you can copy from.

You can have 1 domain or 10. Delete rows you don't need from the domain table.
A single-domain setup is perfectly valid.

### Step 1.4 — Push to a private remote

Create a **private** repository on GitHub (github.com → New → Private).
Do not initialize it with a README. Then:

```bash
git remote set-url origin git@github.com:YourName/my-wiki.git
git add wiki/ CLAUDE.md .gitignore .exportignore .claude/
git commit -m "init: wiki structure and schema"
git push -u origin main
```

The repo must be **private**. Your wiki will contain personal knowledge,
research notes, and potentially sensitive material.

### Step 1.5 — Bootstrap the wiki structure

Start Claude Code from the wiki root:

```bash
cd my-wiki
claude
```

Inside the session, run:

```
> customize
```

Claude Code walks you through replacing all placeholders interactively —
domain names, conventions, page formats. Takes about 5 minutes.

Then:

```
> bootstrap
```

This creates all domain directories, seeds skeleton overview pages,
initializes `wiki/index.md` and `wiki/log.md`, and confirms the hook
scripts are in place.

Exit the session. Commit:

```bash
git add wiki/ CLAUDE.md
git commit -m "bootstrap: domain structure seeded"
git push
```

### Step 1.6 — Your first ingest

Drop a source document into `raw/[domain]/`:

```bash
cp ~/Downloads/some-article.md raw/research/
```

Then in Claude Code:

```
> ingest research raw/research/some-article.md
```

Watch 8–15 wiki pages get created or updated in real time. Open Obsidian
to see the results immediately.

---

## Part 2 — Obsidian setup

Obsidian is your reading interface. Claude Code writes the wiki.
You read, navigate, and use graph view to see the shape of your knowledge.

### Step 2.1 — Open the vault

- Open Obsidian → "Open folder as vault"
- Select `my-wiki/wiki/` — the `wiki/` subdirectory, **not** the repo root
- This keeps Obsidian focused on curated knowledge pages only

### Step 2.2 — Configure file settings

In Obsidian → Settings → Files and links:

| Setting | Value |
|---|---|
| Default location for new notes | `research/` (or your most-used domain) |
| Attachment folder path | `../raw/assets/` |
| Automatically update internal links | On |
| Use `[[Wikilinks]]` | On |

### Step 2.3 — Bind the image download hotkey

Settings → Hotkeys → search "Download attachments for current file" → bind to `Ctrl+Shift+D`.

After clipping a web article, one keystroke downloads all images locally so
Claude Code can reference them directly.

### Step 2.4 — Install Obsidian Web Clipper

Install from obsidian.md/clipper (Chrome, Firefox, Safari).

Configure:
- Default save location: `../raw/research/` (adjust to your domain)
- Format: Markdown
- Include front matter: Yes

This is how web articles enter your `raw/` folder ready for ingestion.

### Step 2.5 — Enable core plugins

Settings → Core plugins → enable:
- **Graph view** — see your wiki as a network. Hub pages have many connections.
  Orphan pages have none. This is the best way to find gaps.
- **Backlinks** — every page that links to the current one
- **Outline** — navigate long concept pages
- **Search** — full-text search across all wiki pages

### Step 2.6 — Optional community plugins

Settings → Community plugins → Browse:

| Plugin | Why |
|---|---|
| **Dataview** | Query wiki frontmatter dynamically. Works because every page has YAML frontmatter (domain, tags, date, source_count). Example: table of all concepts updated this month. |
| **Marp** | Renders Markdown as slide decks. Useful when Claude Code generates presentations from wiki content. |

---

## Part 3 — Multi-device setup

### Step 3.1 — Clone on each additional machine

```bash
git clone git@github.com:YourName/my-wiki.git ~/my-wiki
cd ~/my-wiki
chmod +x .claude/scripts/*.sh .claude/scripts/*.py
bash .claude/scripts/index-sessions.sh
```

Open `~/my-wiki/wiki/` as a vault in Obsidian on that machine.

### Step 3.2 — The pull-before-you-start habit

**Every session, every device:**

```bash
cd ~/my-wiki
git pull
claude
```

Two commands. Make it one motion. The `SessionStart` hook runs automatically
after this — indexing new exports and showing your last 3 sessions.

### Step 3.3 — The commit-after-you-finish habit

**After every session, every device:**

```bash
git add wiki/
git commit -m "session: [what you covered]"
git push
```

Only `wiki/` is committed. Session exports, the SQLite database, and
confidential files stay local to each machine by design.

### Step 3.4 — Phone access

Three options ranked by capability:

**Option A — Obsidian Mobile (best for reading)**

iOS:
```bash
# On your Mac — symlink wiki/ into iCloud:
ln -s ~/my-wiki/wiki \
  ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/my-wiki
```
Open that folder as a vault in Obsidian iOS. Full read access, graph view,
search — everything. Changes sync automatically via iCloud.

Android: Use Obsidian + Dropsync or a git client (MGit) for sync.

**Option B — Mobile git client**

iOS: Working Copy · Android: MGit

Pull the repo, read any file, add quick notes to `raw/` (voice transcription
→ paste → save as .md), commit and push. The note will be there for
ingestion on your next desktop session.

**Option C — Think on mobile, file on desktop**

Use your LLM app on mobile for thinking. At the start of your next desktop
session, tell Claude Code what was decided:
```
> update research wiki/research/threads/my-thread.md
  [paste decisions from mobile]
```

---

## Part 4 — Daily workflow

### Starting a session
```bash
cd ~/my-wiki && git pull
claude
# SessionStart hook fires automatically:
# → indexes new session exports
# → shows last 3 sessions
```

### Ingesting a source
```bash
# Drop file into raw/[domain]/
> ingest research raw/research/article.md
```

### Asking a question
```
> what is the relationship between X and Y?
```
Claude Code checks past sessions first, then the wiki index, then synthesizes
with citations. Non-trivial answers can be filed as wiki pages:
```
> file this answer as a wiki page
```

### Searching past sessions
```
> recall: audio bridge we built last month
> bash .claude/scripts/recall.sh --recent 5
> bash .claude/scripts/recall.sh --date 2026-03
```

### Before a confidential session
```bash
touch .claude/no-export
claude
# or just say "This session is confidential" at the first prompt
```
Nothing from that session touches disk. Sentinel auto-deletes.

### Ending a session (Mac / Linux)
```bash
# SessionEnd hook fires automatically → exports if PreCompact didn't
git add wiki/
git commit -m "session: [topic]"
git push
```

### Ending a session (Windows)
```
exit        ← close Claude Code
wikiexit    ← export session to wiki (see Part 5)
```
Then commit as normal.

### Weekly maintenance
```bash
cd ~/my-wiki && git pull
claude
> digest sessions   # session exports → wiki pages → archive
> lint              # orphan check, contradictions, stale claims
git add wiki/
git commit -m "digest + lint: $(date +%Y-%m-%d)"
git push
```

---

## Part 5 — Closing sessions correctly

How you close a Claude Code session determines whether it gets exported.

### Mac / Linux

The SessionEnd hook fires reliably on `exit`. Your closing ritual:
```bash
exit        # closes Claude Code, triggers export automatically
```

### Windows

The SessionEnd hook does not always fire on Windows. Use the
`wikiexit` PowerShell alias instead.

**One-time setup:**
```powershell
notepad $PROFILE
```
Add this to the file:
```powershell
function wikiexit {
    python "YOUR_WIKI_PATH\.claude\scripts\export-session.py" `
           --trigger manual `
           --wiki-dir "YOUR_WIKI_PATH"
}
```
Replace `YOUR_WIKI_PATH` with your actual wiki path. Save, close Notepad, then run:
```powershell
. $PROFILE
```

**Every session closing ritual (Windows):**
```
exit        ← closes Claude Code, back to PowerShell
wikiexit    ← exports session to wiki
```

`wikiexit` is a PowerShell function that:
- Works from any project directory
- Auto-detects the latest session transcript
- Exports with the project name in the filename
- Routes to your central wiki regardless of which project you're in

### Verifying export worked

After `wikiexit` (or on Mac/Linux after `exit`), check:
```bash
# Mac/Linux:
ls sessions/exports/

# Windows:
dir YOUR_WIKI_PATH\sessions\exports\
```

You should see a new file named:
```
YYYY-MM-DD_HHMMSS_sessionid_projectname_manual.md
```

The project name in the filename confirms which project it came from.

---

## Part 6 — Confidentiality

| Situation | What to do |
|---|---|
| Sensitive negotiation / job interview | `touch .claude/no-export` |
| Client / NDA work | `touch .claude/no-export` |
| Personal health / finance | `touch .claude/no-export` |
| Want archived but not searchable | Add pattern to `.exportignore` |
| Archive encrypted, not plaintext | `export-session.py --label confidential` |
| Routine work | Default — export and index normally |

**Sentinel on Windows (PowerShell):**
```powershell
echo $null > .claude\no-export
# or say "This session is confidential" at the first prompt
```

---

## Part 7 — Multi-project wiring

Wire all your existing project repos to the central wiki so every
session from every project exports to one searchable index.

### Wire a single project

```bash
# Mac/Linux:
python /path/to/wiki/scripts/wire-project.py /path/to/project

# Windows:
python C:\path\to\wiki\scripts\wire-project.py C:\path\to\project

# Current directory:
python C:\path\to\wiki\scripts\wire-project.py .
```

### Wire all existing projects at once

```bash
python /path/to/wiki/scripts/wire-all-projects.py
```

Shows you the list of repos it found before making any changes.
Skips `llm-wiki-template` and the wiki itself.

### Wire new projects (every time)

Make this a habit for every new repo you create:
```bash
# After git init:
python /path/to/wiki/scripts/wire-project.py .
```

See [examples/use-cases/new-project-checklist.md](examples/use-cases/new-project-checklist.md)
for the full new project setup sequence.

### After wiring — commit in each project

```bash
cd /path/to/project
git add .claude/settings.json CLAUDE.md
git commit -m "wire: connect to central wiki session export"
git push
```

### Verifying a project is wired correctly

```bash
cat .claude/settings.json | grep "export-session"
# Should show the absolute path to your wiki's export-session.py
```

---

## Part 8 — Troubleshooting

**Hooks not firing**

Verify `settings.json` is valid JSON:
```bash
python3 -c "import json; json.load(open('.claude/settings.json'))" && echo "valid"
```

Check scripts are executable (Mac/Linux):
```bash
ls -la .claude/scripts/
# Should show -rwxr-xr-x for each file
# Fix: chmod +x .claude/scripts/*.sh .claude/scripts/*.py
```

**SQLite database missing or corrupt**

Rebuild from existing exports (non-destructive):
```bash
rm -f sessions.db
bash .claude/scripts/index-sessions.sh
```

**Recall returns no results**

```bash
# Check how many sessions are indexed:
sqlite3 sessions.db "SELECT COUNT(*) FROM sessions_raw;"

# Re-index:
bash .claude/scripts/index-sessions.sh

# Grep fallback:
grep -rl "your search terms" sessions/exports/
```

**Merge conflict after git pull**

Wiki pages are plain text — conflicts are easy to resolve:
```bash
git status                          # see conflicting files
# Open file, find <<<<<<< markers, resolve
git add wiki/resolved-page.md
git commit -m "resolve merge conflict"
```

**GPG not found (confidential export)**
```bash
# Mac:
brew install gnupg

# Linux:
sudo apt install gnupg

# Generate a key if you don't have one:
gpg --gen-key
```

**SessionEnd hook exports but PreCompact doesn't**

This is normal for short sessions that never fill the context window.
`SessionEnd` is the fallback for exactly this case. Both hooks produce
identical output — the deduplication logic prevents double-export.

**Windows: emoji shows as `?` in terminal**

Cosmetic only. Exports work correctly. The scripts use `safe_print()` internally.

**Windows: `wikiexit` says "No transcript found"**

Check that `~\.claude\projects\` exists and contains session files:
```powershell
dir $HOME\.claude\projects\
```
If empty, run at least one Claude Code session first.

---

## What commits vs. what stays local

| Path | Committed | Reason |
|---|---|---|
| `wiki/` | ✅ Yes | Curated knowledge — syncs across devices |
| `CLAUDE.md` | ✅ Yes | Schema — must be consistent everywhere |
| `.claude/settings.json` | ✅ Yes | Hook config — reproducible anywhere |
| `.claude/scripts/` | ✅ Yes | Scripts — reproducible anywhere |
| `.gitignore` | ✅ Yes | Exclusion rules travel with repo |
| `.exportignore` | ✅ Yes | Index exclusion rules travel with repo |
| `raw/` | ✅ Usually | Source docs — your raw inputs |
| `raw/[sensitive]/` | ⚠️ Consider | Add to .gitignore if sensitive |
| `sessions/exports/` | ❌ No | Raw transcripts — local to each device |
| `sessions/confidential/` | ❌ No | Encrypted — never leave the machine |
| `sessions/wiki-digests/` | ❌ No | Archived after digesting — local only |
| `sessions.db` | ❌ No | Regenerable SQLite index — local |
| `.claude/no-export` | ❌ No | Transient sentinel |

---

## Quick reference card

```
FIRST TIME:
  git clone → bash scripts/setup.sh → customize CLAUDE.md
  → git push to private repo → claude → customize → bootstrap

EACH NEW DEVICE:
  git clone → chmod +x scripts → bash index-sessions.sh → Obsidian

EVERY SESSION (Mac/Linux):
  git pull → claude → [work] → exit → git add wiki/ → git commit → git push

EVERY SESSION (Windows):
  git pull → claude → [work] → exit → wikiexit → git add wiki/ → git commit → git push

CONFIDENTIAL SESSION:
  touch .claude/no-export → claude → [nothing recorded]
  Windows: echo $null > .claude\no-export

WIRE A NEW PROJECT:
  python /path/to/wiki/scripts/wire-project.py /path/to/project

WEEKLY:
  claude → digest sessions → lint → git commit → git push

RECALL:
  bash .claude/scripts/recall.sh "what you're looking for"
  bash .claude/scripts/recall.sh --recent 5
```

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
