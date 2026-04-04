# Claude Code Adapter

This is the reference implementation of the LLM Wiki Template for **Claude Code** (Anthropic's CLI coding agent).

Claude Code gets the best experience because it's currently the only LLM tool with a native hook system that makes session export **fully automatic**. No manual steps required.

---

## Files in this adapter

| File | Purpose | Where it goes |
|---|---|---|
| `CLAUDE.md` | Wiki schema — Claude Code reads this automatically at session start | Repo root |
| `.claude/settings.json` | Hook configuration — wires auto-export | `.claude/settings.json` in repo root |

The scripts (`export-session.py`, `index-sessions.sh`, `recall.sh`) are in the shared `scripts/` directory and get copied to `.claude/scripts/` during setup.

---

## How the hooks work

```
Session starts
     │
     ▼
SessionStart hook fires
  → bash .claude/scripts/index-sessions.sh   (index any new exports)
  → bash .claude/scripts/recall.sh --recent 3  (show last 3 sessions)
     │
     ▼
[You work normally]
     │
     ▼
Context fills up / you run /compact
     │
     ▼
PreCompact hook fires  ← THE CRITICAL ONE
  → python3 .claude/scripts/export-session.py --trigger precompact
  → Full session exported to sessions/exports/ BEFORE anything is summarized
     │
     ▼
Session ends normally
     │
     ▼
SessionEnd hook fires
  → python3 .claude/scripts/export-session.py --trigger sessionend
  → Exports if PreCompact didn't already run (short sessions)
```

---

## Setup

Run the shared setup script from the repo root:

```bash
bash scripts/setup.sh claude-code
```

Or manually:
```bash
cp adapters/claude-code/CLAUDE.md .
mkdir -p .claude
cp adapters/claude-code/.claude/settings.json .claude/settings.json
cp scripts/export-session.py scripts/index-sessions.sh scripts/recall.sh .claude/scripts/
chmod +x .claude/scripts/*.py .claude/scripts/*.sh
```

---

## Claude Code version requirements

Hooks require Claude Code **v1.x or later**. Verify:
```bash
claude --version
```

The `PreCompact` hook specifically requires a version that supports it. If you're on an older version and PreCompact isn't firing, update Claude Code:
```bash
npm update -g @anthropic-ai/claude-code
```

---

## Confidential sessions

```bash
# Before starting a confidential session:
touch .claude/no-export

# Or just say at the start of the session:
# "This session is confidential"
# (The UserPromptSubmit hook will create the sentinel automatically)
```

---

## Multi-computer setup

See the main [SETUP-GUIDE.md](../../SETUP-GUIDE.md) for full multi-device instructions.

The short version: each computer clones the repo and runs `bash scripts/setup.sh`. The wiki pages sync via git. Session exports stay local to each machine.

---

## Hook reference

Full Claude Code hook documentation: https://code.claude.com/docs/en/hooks
