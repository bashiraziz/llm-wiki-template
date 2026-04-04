# OpenAI Codex CLI Adapter

This adapter configures the LLM Wiki Template for **OpenAI Codex CLI**.

Codex reads `AGENTS.md` automatically from the project root — the equivalent of Claude Code's `CLAUDE.md`. The wiki architecture, scripts, and Obsidian setup are identical. The only difference is that session export is a **manual step** rather than automatic, because Codex CLI does not have a native hook system equivalent to Claude Code's `PreCompact`.

---

## Setup

```bash
bash scripts/setup.sh codex
```

---

## The manual export step

Since there's no PreCompact hook, you must export at the end of every session:

```bash
# At the end of every session, before exiting:
python3 scripts/export-session.py --trigger manual
```

Add this shell alias so it's one command:

```bash
# Add to ~/.bashrc or ~/.zshrc:
alias wiki-save='cd ~/my-wiki && python3 scripts/export-session.py --trigger manual && echo "Session saved."'
alias wiki-save-private='cd ~/my-wiki && python3 scripts/export-session.py --trigger manual --label confidential'
```

Then at the end of each session just type `wiki-save`.

---

## Simulating SessionStart context

Since there's no SessionStart hook, run this at the beginning of each session
to get the same context (recent sessions + index update):

```bash
# Add to ~/.bashrc:
alias wiki-start='cd ~/my-wiki && git pull && bash scripts/index-sessions.sh && bash scripts/recall.sh --recent 3'
```

---

## What you get vs Claude Code

| Feature | Codex | Claude Code |
|---|---|---|
| Schema file auto-loaded | ✅ AGENTS.md | ✅ CLAUDE.md |
| Session export | ⚠️ Manual | ✅ Automatic |
| Context-aware recall | ✅ Same scripts | ✅ Same scripts |
| Wiki architecture | ✅ Identical | ✅ Identical |
| Obsidian integration | ✅ Identical | ✅ Identical |
| Multi-device git sync | ✅ Identical | ✅ Identical |

You get ~85% of the value. The only missing piece is automatic export before context compression. As long as you remember to run `wiki-save` before exiting, nothing is lost.

---

## Codex CLI resources

- https://github.com/openai/codex
- AGENTS.md specification: included in Codex documentation
