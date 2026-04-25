# LLM Wiki Template

A personal knowledge base that compounds over time — maintained entirely by an LLM agent.

Inspired by [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (April 2026).  
Implementation by [Bashir Aziz](https://github.com/bashiraziz) · 2026.

---

## The idea in one paragraph

Most people use LLMs like a search engine — ask a question, get an answer, move on. Nothing accumulates. This template gives your LLM agent a persistent wiki: a directory of markdown files it reads, writes, and cross-references across every session. When you add a new source, the agent doesn't just answer a question — it updates entity pages, revises concept summaries, flags contradictions, and files the knowledge permanently. Every session makes the wiki richer. Every question you ask can become a new wiki page. The knowledge compounds instead of evaporating.

---

## How it works

```
┌─────────────────────────────────────────────────────────┐
│                        YOU                              │
│   source documents · questions · direction              │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    LLM AGENT                            │
│   reads · writes · cross-references · maintains        │
└──────────┬────────────────────────────┬─────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────┐        ┌───────────────────────────┐
│   raw/           │        │   wiki/                   │
│   source docs    │        │   index.md  log.md        │
│   (immutable)    │        │   concepts/ entities/     │
│                  │        │   sources/  threads/      │
└──────────────────┘        └───────────────────────────┘
                                        │
                                        ▼
                            ┌───────────────────────────┐
                            │   sessions/               │
                            │   auto-exported transcripts│
                            │   SQLite FTS5 index       │
                            │   (local, never committed)│
                            └───────────────────────────┘
```

Three layers:
- **`raw/`** — your source documents. Immutable. The LLM reads but never modifies.
- **`wiki/`** — LLM-maintained markdown pages. Commits to git. Syncs across devices.
- **`sessions/`** — auto-exported session transcripts. Local only. Indexed for search.

---

## Tool support

| Tool | Schema file | Auto-export hooks | Quality |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` | ✅ Full (PreCompact + SessionEnd + SessionStart) | ⭐⭐⭐⭐⭐ Best experience |
| **OpenAI Codex CLI** | `AGENTS.md` | ⚠️ Partial (manual export step) | ⭐⭐⭐⭐ |
| **Cursor** | System prompt file | ❌ Manual export | ⭐⭐⭐ |
| **Aider** | `CONVENTIONS.md` | ❌ Manual export | ⭐⭐⭐ |
| **Any LLM via API** | Any filename | ❌ Manual export | ⭐⭐⭐ |

Claude Code gets the best experience because it's currently the only tool with a native hook system that makes session export fully automatic. With other tools you get ~80% of the value — the wiki compounding, full-text search, Obsidian interface — but session capture requires a manual step.

> **Windows users**: The SessionEnd hook may not fire reliably on exit.
> See [Part 5 of the Setup Guide](SETUP-GUIDE.md#part-5--closing-sessions-correctly) for the `wikiexit` PowerShell alias that solves this.
> Full Windows-specific notes in [docs/windows-setup.md](docs/windows-setup.md).

---

## Quickstart (Claude Code)

```bash
# 1. Clone the template
git clone https://github.com/bashiraziz/llm-wiki-template.git my-wiki
cd my-wiki

# 2. Run the setup script
bash scripts/setup.sh

# 3. Create your private wiki repo on GitHub, then:
git remote set-url origin git@github.com:bashiraziz/my-wiki.git
git push -u origin main

# 4. Open a Claude Code session and bootstrap
claude
> customize    # walks you through domain setup interactively
> bootstrap    # seeds all directories and wiki structure
```

That's it. Your first ingest:
```
> ingest research raw/research/my-first-article.md
```

> 📋 **New to this?** Start with the **[Quick Reference Card](QUICK-REFERENCE.md)** —
> a one-page cheat sheet covering every daily workflow command.
> Print it and keep it handy until the workflow is muscle memory.

---

## Going further

Once your wiki is running, these guides cover the next level:

| Guide | What it covers |
|---|---|
| [Quick Reference Card](QUICK-REFERENCE.md) | Daily workflow cheat sheet — print this |
| [Cross-project wiring](docs/cross-project-wiring.md) | Connect all your project repos to the central wiki — one search finds sessions from everywhere |
| [Obsidian setup](docs/obsidian-setup.md) | Full Obsidian configuration, Web Clipper, graph view tips, mobile setup, Dataview queries |
| [New project checklist](examples/use-cases/new-project-checklist.md) | 5-minute setup for every new project repo going forward |

---

## Repository structure

```
llm-wiki-template/
│
├── README.md                        ← you are here
├── SETUP-GUIDE.md                   ← complete step-by-step instructions
├── CHANGELOG.md                     ← version history
│
├── scripts/                         ← tool-agnostic shell + python scripts
│   ├── setup.sh                     ← one-time setup script
│   ├── export-session.py            ← session → markdown export
│   ├── index-sessions.sh            ← markdown → SQLite FTS5 indexer
│   ├── recall.sh                    ← search past sessions
│   ├── wire-project.py              ← wire any project to the wiki
│   └── wire-all-projects.py         ← wire all existing projects
│
├── adapters/                        ← tool-specific configuration
│   ├── claude-code/                 ← Claude Code adapter (reference implementation)
│   │   ├── CLAUDE.md                ← schema file (copy to repo root)
│   │   ├── .claude/
│   │   │   └── settings.json        ← hook configuration
│   │   └── README.md                ← Claude Code specific notes
│   ├── codex/
│   │   ├── AGENTS.md                ← schema file for OpenAI Codex
│   │   └── README.md
│   ├── cursor/
│   │   └── README.md
│   └── generic/
│       ├── WIKI-SCHEMA.md           ← tool-agnostic schema template
│       └── README.md
│
├── examples/                        ← filled-in configurations for reference
│   ├── domains/
│   │   ├── govcon-domain.md         ← government contracting domain config
│   │   ├── research-domain.md       ← academic / deep research domain config
│   │   ├── personal-domain.md       ← personal knowledge / journaling domain
│   │   └── business-domain.md       ← business / competitive intelligence domain
│   └── use-cases/
│       ├── solo-researcher.md       ← one person, one domain, simple setup
│       ├── multi-domain.md          ← Bashir's setup: 3 domains, multi-device
│       └── team-wiki.md             ← shared wiki with human review loop
│
├── wiki/                            ← empty wiki structure (ready to populate)
│   ├── index.md
│   └── log.md
│
├── raw/                             ← empty source document directories
│   └── .gitkeep
│
├── sessions/                        ← auto-exported transcripts (gitignored)
│   ├── exports/
│   ├── confidential/
│   └── wiki-digests/
│
├── .gitignore
└── .exportignore
```

---

## Customization in 3 steps

### Step 1 — Choose your adapter

Copy the adapter files for your tool to the repo root:

```bash
# For Claude Code:
cp adapters/claude-code/CLAUDE.md .
cp -r adapters/claude-code/.claude .

# For Codex:
cp adapters/codex/AGENTS.md .

# For others: see adapters/generic/README.md
```

### Step 2 — Define your domains

Edit the schema file (`CLAUDE.md`, `AGENTS.md`, etc.) and replace the domain placeholders:

```
YOUR_DOMAIN_1  →  research
YOUR_DOMAIN_2  →  personal
YOUR_DOMAIN_3  →  work
```

See `examples/domains/` for fully worked examples of different domain types.

### Step 3 — Bootstrap

```bash
claude          # or your tool of choice
> bootstrap     # creates all directories and seed pages for your domains
```

---

## Multi-device workflow

The wiki pages sync via git. Session transcripts stay local.

```bash
# Every session, every device:
git pull && claude

# After every session:
git add wiki/ && git commit -m "session: [topic]" && git push
```

Full instructions in [SETUP-GUIDE.md](./SETUP-GUIDE.md).

---

## Confidentiality

Three layers of protection for sensitive sessions:

```bash
# Layer 1 — Skip export entirely (one command before session):
touch .claude/no-export

# Layer 2 — Export but exclude from search index (.exportignore):
*_client_*.md
*_nda_*.md

# Layer 3 — Encrypt confidential archive (GPG):
# export-session.py --label confidential  →  GPG-encrypted to sessions/confidential/
```

---

## Known issues and workarounds

| Issue | Affects | Workaround |
|---|---|---|
| SessionEnd hook doesn't fire on exit | Windows | Use `wikiexit` PowerShell alias — see [Setup Guide Part 5](SETUP-GUIDE.md#part-5--closing-sessions-correctly) |
| `/compact` blocked: `No such file or directory` | Windows | Use forward slashes in `settings.json` hook paths (`C:/Users/...`), never backslashes — bash mangles them. `wire-project.py` does this automatically. |
| Emoji display as `?` in terminal output | Windows cp1252 | Cosmetic only — exports still work correctly |
| sqlite3 not found in Git Bash | Windows | Copy sqlite3.exe to `C:\Program Files\Git\usr\bin\` as admin |

---

## Contributing

PRs welcome, especially:
- New tool adapters (Gemini CLI, Aider, Zed, etc.)
- New domain examples
- Improvements to the export / indexing scripts
- Windows compatibility fixes

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## License

MIT. Use it, fork it, build on it.

---

*Pattern by Andrej Karpathy · Implementation by Bashir Aziz · Built with Claude (Anthropic) · 2026*
