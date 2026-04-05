# Cross-Project Wiring Guide

Connect all your project repositories to a single central wiki session index.
Every Claude Code session across every project becomes searchable from one place.

---

## The problem this solves

By default, session exports only happen in the repo where your wiki lives.
If you work on 10 different app repos, 10 different sets of sessions are
scattered across your machine — or lost entirely.

This guide wires all your repos to the central wiki so:
- Every session from every project auto-exports to `my-wiki/sessions/exports/`
- One `recall.py` search finds sessions from all projects
- Session exports are tagged with the project name so you know where they came from
- The confidential sentinel works across all projects

---

## How it works

```
any-project/.claude/settings.json
        │
        │  hooks point to →  my-wiki/.claude/scripts/
        │
        ├── PreCompact  →  export-session.py  →  my-wiki/sessions/exports/
        ├── SessionEnd  →  export-session.py  →  my-wiki/sessions/exports/
        └── SessionStart → index-sessions.py
                           recall.py --recent 3
```

Every project's hooks call the scripts that live in the wiki repo.
The wiki repo is the hub. Project repos are the spokes.

---

## Prerequisites

- Wiki repo already set up and working (`bash scripts/setup.sh` completed)
- `WIKI_ROOT` environment variable set, OR edit `scripts/wire-project.py`
  and set `WIKI_ROOT_DEFAULT` to your wiki path

### Setting WIKI_ROOT

**Mac/Linux** — add to `~/.bashrc` or `~/.zshrc`:
```bash
export WIKI_ROOT="$HOME/my-wiki"
```

**Windows** — add to PowerShell profile or System Environment Variables:
```powershell
$env:WIKI_ROOT = "C:\Users\YourName\Documents\GitHub\my-wiki"
```

Or set it permanently via System Properties → Environment Variables.

---

## Wiring a single project

```bash
python /path/to/my-wiki/scripts/wire-project.py /path/to/your-project
```

Examples:
```bash
# Mac/Linux:
python ~/my-wiki/scripts/wire-project.py ~/code/my-app

# Windows:
python C:\Users\you\my-wiki\scripts\wire-project.py C:\Users\you\code\my-app

# Current directory:
cd /path/to/your-project
python ~/my-wiki/scripts/wire-project.py .
```

What it creates/updates:
- `.claude/settings.json` — hook configuration (backed up if it exists)
- `CLAUDE.md` — wiki integration section appended (existing content untouched)

---

## Wiring all existing projects at once

```bash
# Scans auto-detected repos directory (~/Documents/GitHub, ~/code, etc.)
python /path/to/my-wiki/scripts/wire-all-projects.py

# Specify a directory explicitly:
python /path/to/my-wiki/scripts/wire-all-projects.py ~/code

# Dry run first to see what would be wired:
python /path/to/my-wiki/scripts/wire-all-projects.py --dry-run

# Skip specific repos:
python /path/to/my-wiki/scripts/wire-all-projects.py --skip my-old-project archived-stuff
```

The script:
- Finds all git repos in the target directory
- Skips `llm-wiki-template` (public template) and your wiki itself
- Shows you the list before making any changes
- Reports what succeeded, what failed, what was already wired

---

## After wiring

**Commit the changes in each project:**
```bash
cd /path/to/your-project
git add .claude/settings.json CLAUDE.md
git commit -m "wire: connect to central wiki session export"
git push
```

**Restart Claude Code in each project to activate hooks:**
```bash
cd /path/to/your-project
claude
# SessionStart hook fires — shows last 3 sessions from ANY project
```

---

## New project checklist

Wire every new project immediately after creating it:

```bash
# 1. Create the repo
mkdir ~/code/new-project && cd ~/code/new-project
git init

# 2. Wire to the wiki (one command)
python ~/my-wiki/scripts/wire-project.py .

# 3. Let Claude Code document the project
claude
> Read this project and create a complete CLAUDE.md documenting
  the stack, structure, commands, and conventions.
  The wiki integration section is already there — add above it.

# 4. Commit
git add . && git commit -m "init: project scaffold + wiki wiring"
```

That's it. From that point forward, every session is captured.

---

## Using the wiki from a wired project

### Get context before building a feature

Inside any Claude Code session, in any project:
```
> Check my wiki at [WIKI_ROOT] for everything we know about [topic]
```

Claude Code reads the relevant wiki pages and uses that knowledge
to inform what it builds. Your accumulated knowledge travels with you
across every project.

### Update the wiki after a session

At the end of any session where you learned something worth keeping:
```
> Update the wiki at [WIKI_ROOT] with what we learned today.
  Update relevant pages and add to log.md.
```

### Search past sessions across all projects

```bash
# From anywhere:
python [WIKI_ROOT]/.claude/scripts/recall.py "search terms"
python [WIKI_ROOT]/.claude/scripts/recall.py --recent 10
python [WIKI_ROOT]/.claude/scripts/recall.py --date 2026-03

# From inside the wiki directory:
python .claude/scripts/recall.py "audio bridge we built"
```

Results show which project each session came from:
```
📄 2026-04-03 — 2026-04-03_143022_abc123_precompact.md
   Project: dcaa-compliance-training
   >>> The DCAA audit triggers module uses seven defined criteria <<<
```

---

## Confidential sessions

The confidential sentinel works across all wired projects:

```bash
# Before starting a sensitive session in any project:
touch [WIKI_ROOT]/.claude/no-export

# Or say at the first prompt:
> This session is confidential
```

The UserPromptSubmit hook watches for the word "confidential" in any
wired project and activates the sentinel automatically.

---

## Troubleshooting

**Hooks not firing after wiring**

Verify settings.json is valid JSON:
```bash
python -c "import json; json.load(open('.claude/settings.json'))" && echo "valid"
```

Verify the wiki scripts exist at the path in settings.json:
```bash
ls [WIKI_ROOT]/.claude/scripts/
# Should show: export-session.py  index-sessions.py  recall.py  setup.sh
```

**Sessions not appearing in recall**

Check exports are landing in the right place:
```bash
ls [WIKI_ROOT]/sessions/exports/
```

Re-index if files are there but not searchable:
```bash
python [WIKI_ROOT]/.claude/scripts/index-sessions.py
```

**Wire script can't find wiki root**

Set the environment variable:
```bash
export WIKI_ROOT="/absolute/path/to/my-wiki"   # Mac/Linux
$env:WIKI_ROOT = "C:\path\to\my-wiki"          # Windows PowerShell
```

Or edit `scripts/wire-project.py` and set `WIKI_ROOT_DEFAULT`.

---

## What gets committed vs. what stays local

In each wired project repo:

| File | Committed | Why |
|---|---|---|
| `.claude/settings.json` | ✅ Yes | Hook config travels with the repo |
| `CLAUDE.md` (wiki section) | ✅ Yes | Documents the wiki integration |
| Session exports | ❌ No | Local to each machine — add `sessions/` to `.gitignore` |

In the wiki repo — nothing changes. The wiki already handles its own gitignore.

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
