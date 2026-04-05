# LLM Wiki — Quick Reference Card

Print this. Pin it next to your monitor. Build the muscle memory.

---

## Every Session — Every Project

### START
```bash
cd /path/to/your-project    # go to project (Windows: cd C:\...\project-name)
git pull                    # get latest wiki changes
claude                      # start Claude Code
```
*SessionStart hook fires automatically — indexes new exports, shows last 3 sessions*

### WORK
```
> build this feature
> check my wiki for context on [topic]
> what does our wiki say about [topic]?
> update the wiki with what we learned today
> recall: [something from a past session]
```

### END (Mac / Linux)
```bash
exit        # close Claude Code — SessionEnd hook exports automatically
git add wiki/
git commit -m "session: [what you covered today]"
git push
```

### END (Windows)
```
exit        # close Claude Code → back to PowerShell
wikiexit    # export session to wiki (run in PowerShell)
```
```bash
git add wiki/
git commit -m "session: [what you covered today]"
git push
```
*See [Windows Setup Guide](docs/windows-setup.md) for wikiexit one-time setup*

---

## Confidential Session

Before starting Claude Code:
```bash
# Mac/Linux:
touch /path/to/wiki/.claude/no-export

# Windows:
New-Item "C:\path\to\wiki\.claude\no-export" -ItemType File
```
Or just say at the very first prompt inside Claude Code:
```
> This session is confidential
```
Nothing from that session is exported. Sentinel auto-deletes after.

---

## Ingest a Source Document

```bash
# 1. Drop file into raw/[domain]/
# 2. In Claude Code:
> ingest research raw/research/article.md
> ingest govcon raw/govcon/far-part31.md
> ingest edu raw/edu/observation-notes.md
```

---

## Search Past Sessions

```bash
# From your wiki directory:
python .claude/scripts/recall.py "what you're looking for"
python .claude/scripts/recall.py --recent 5
python .claude/scripts/recall.py --date 2026-04
python .claude/scripts/recall.py --list
```

---

## Wire a New Project (every new repo)

```bash
# Run once immediately after git init:
python /path/to/wiki/scripts/wire-project.py .

# Then commit:
git add .claude/settings.json CLAUDE.md
git commit -m "wire: connect to central wiki"
git push
```

---

## Weekly Maintenance

```bash
cd /path/to/wiki
git pull
claude
```
```
> digest sessions     # session exports → permanent wiki pages
> lint                # find orphans, contradictions, gaps
```
```bash
exit                  # Mac/Linux auto-exports
# wikiexit            # Windows — run in PowerShell
git add wiki/
git commit -m "digest + lint: $(date +%Y-%m-%d)"
git push
```

---

## wikiexit Setup (Windows — one time only)

```powershell
notepad $PROFILE
```
Add this (replace YOUR_WIKI_PATH with your actual wiki path):
```powershell
function wikiexit {
    python "YOUR_WIKI_PATH\.claude\scripts\export-session.py" `
           --trigger manual `
           --wiki-dir "YOUR_WIKI_PATH"
}
```
Save, close Notepad, then reload:
```powershell
. $PROFILE
```
From now on type `wikiexit` after every session on Windows.

---

## Key Directories

| What | Where |
|---|---|
| Your wiki pages (Obsidian vault) | `wiki/` |
| Raw source documents | `raw/[domain]/` |
| Session exports | `sessions/exports/` |
| Search index | `sessions.db` |
| Hook scripts | `.claude/scripts/` |
| Schema / conventions | `CLAUDE.md` |

---

## Something Broke?

**Session not exporting?**
```bash
# Run export manually from your project directory:
# Mac/Linux:
python /path/to/wiki/.claude/scripts/export-session.py --trigger manual --wiki-dir /path/to/wiki
# Windows:
python "YOUR_WIKI_PATH\.claude\scripts\export-session.py" --trigger manual --wiki-dir "YOUR_WIKI_PATH"
```

**Search returning nothing?**
```bash
python .claude/scripts/index-sessions.py
```

**Merge conflict after git pull?**
```bash
git status
# Open conflicting file, resolve <<<< markers
git add wiki/resolved-page.md
git commit -m "resolve conflict"
```

Full troubleshooting → [SETUP-GUIDE.md](SETUP-GUIDE.md)
Full Windows guide → [docs/windows-setup.md](docs/windows-setup.md)

---

*LLM Wiki Template · github.com/bashiraziz/llm-wiki-template · MIT License*
*Pattern by Andrej Karpathy · Implementation by Bashir Aziz · Built with Claude (Anthropic)*
