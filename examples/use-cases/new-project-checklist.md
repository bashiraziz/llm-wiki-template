# New Project Checklist

Steps to follow every time you create a new project repository.
Wire it to the central wiki before writing a single line of code.

---

## The 5-minute setup

```bash
# 1. Create the repo
mkdir ~/code/new-project-name
cd ~/code/new-project-name
git init

# 2. Wire to the wiki (ONE command)
python ~/my-wiki/scripts/wire-project.py .

# 3. Open Claude Code
claude
```

Inside the Claude Code session:
```
> Read this project directory and create a complete CLAUDE.md
  documenting the stack, directory structure, key commands,
  and conventions. The wiki integration section is already
  there — add your documentation above it.
```

```bash
# 4. Commit
git add .
git commit -m "init: project scaffold + wiki wiring"

# 5. Push to GitHub (private repo)
gh repo create new-project-name --private --source=. --push
# or manually: git remote add origin ... && git push -u origin main
```

**Done.** Every Claude Code session in this project now auto-exports
to your central wiki session index.

---

## What wire-project.py does

Running `python ~/my-wiki/scripts/wire-project.py .` creates or updates:

**`.claude/settings.json`** — installs four Claude Code hooks:
- `PreCompact` → exports session before context compression
- `SessionEnd` → exports session on normal exit
- `SessionStart` → indexes new exports, shows last 3 sessions
- `UserPromptSubmit` → watches for "confidential" to block export

All hooks point to the scripts in your central wiki repo.

**`CLAUDE.md`** — appends a Wiki Integration section that documents:
- Where sessions are exported
- How to query the wiki from this project
- How to update the wiki after a session
- How to search past sessions
- How to mark a session confidential

---

## After the first Claude Code session

The first session generates a session export automatically.
Verify it landed in the wiki:

```bash
ls ~/my-wiki/sessions/exports/
# Should show a new .md file from today
```

Search for it:
```bash
python ~/my-wiki/.claude/scripts/recall.py --recent 1
# Should show your new session tagged with the project name
```

---

## The ongoing workflow

**Every session:**
```bash
cd ~/code/new-project-name
git pull          # if collaborating
claude            # SessionStart shows last 3 sessions automatically
```

**End of session — update the wiki with what you learned:**
```
> Update the wiki at [WIKI_ROOT] with anything worth keeping
  from this session — decisions made, things discovered,
  problems solved. Update relevant pages and log.md.
```

**Then commit:**
```bash
git add .
git commit -m "session: [brief description of what was covered]"
git push
```

---

## When to create a wiki thread for a new project

For significant projects (more than a few sessions of work), create
a research thread in the wiki to track the project's evolution:

In a wiki session:
```
> Create a research thread for my new project [name]:
  wiki/research/threads/[project-name].md
  Document: what it is, why building it, key technical decisions,
  domain it relates to, open questions.
```

This becomes the permanent record of the project's reasoning — separate
from the session transcripts, always in the wiki, always searchable.

---

## Confidential projects

If the project itself is sensitive (client work, NDA, etc.):

```bash
# Add to the project's .gitignore:
echo "sessions/" >> .gitignore
echo ".claude/no-export" >> .gitignore
```

Before every session in this project:
```bash
touch ~/my-wiki/.claude/no-export
claude
```

Or just say at the first prompt of every session:
```
> This session is confidential
```

---

## Checklist summary

```
□ mkdir + git init
□ python wire-project.py .
□ claude → document the project in CLAUDE.md
□ git add . && git commit -m "init"
□ git push (private repo)
□ Verify first session exports to my-wiki/sessions/exports/
□ Create wiki/research/threads/[project].md (for significant projects)
□ Add to .gitignore if project is confidential
```

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
