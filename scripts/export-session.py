#!/usr/bin/env python3
"""
export-session.py — LLM Wiki Template
======================================
Exports a Claude Code session transcript (JSONL) to a readable markdown file.

Triggered automatically by Claude Code hooks (PreCompact, SessionEnd).
Can also be run manually for other LLM tools.

Usage:
  # Automatic (Claude Code hook — reads payload from stdin):
  echo '<hook_json>' | python3 export-session.py --trigger precompact

  # Manual (other tools — uses latest session from ~/.claude/projects/):
  python3 export-session.py --trigger manual

  # Manual with confidential label (GPG-encrypted output):
  python3 export-session.py --trigger manual --label confidential

  # Explicit transcript path:
  python3 export-session.py --trigger manual --transcript /path/to/session.jsonl

Output:
  sessions/exports/YYYY-MM-DD_HHMMSS_<session_id>_<project>_<trigger>.md
  sessions/confidential/YYYY-MM-DD_HHMMSS_<session_id>_<project>_confidential.md.gpg  (if confidential)

Requirements:
  Python 3.6+
  GPG (optional, for confidential exports): brew install gnupg / apt install gnupg
"""

import json
import os
import sys
import argparse
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# ── Wiki root resolution ───────────────────────────────────────────────────────
# Exports always land in the central wiki, not in whichever project cwd triggered
# the hook. Priority: --wiki-dir flag → WIKI_ROOT env var → hardcoded path → cwd.

_WIKI_ROOT_HARDCODED = None  # Set to your wiki path, or use WIKI_ROOT env var


def resolve_wiki_root(cwd: Path, cli_override: str = "") -> Path:
    """Return the canonical wiki root for session export output."""
    if cli_override:
        return Path(cli_override).resolve()
    env_root = os.environ.get("WIKI_ROOT", "")
    if env_root:
        return Path(env_root).resolve()
    if _WIKI_ROOT_HARDCODED and Path(_WIKI_ROOT_HARDCODED).exists():
        return Path(_WIKI_ROOT_HARDCODED)
    return cwd


# ── Markdown conversion ────────────────────────────────────────────────────────

def parse_jsonl_to_markdown(jsonl_path: Path, session_id: str, trigger: str, project_name: str = "", project_path: str = "") -> str:
    """Convert a Claude Code JSONL transcript to readable markdown."""
    lines = []
    lines.append("# Session Export")
    lines.append(f"- **Session ID**: `{session_id}`")
    lines.append(f"- **Exported**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **Trigger**: {trigger}")
    if project_name:
        lines.append(f"- **Project**: {project_name}")
    if project_path:
        lines.append(f"- **Project Path**: `{project_path}`")
    lines.append(f"- **Source**: {jsonl_path}")
    lines.append("")
    lines.append("---")
    lines.append("")

    try:
        with open(jsonl_path, encoding="utf-8") as f:
            for raw_line in f:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    entry = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                # Support both formats:
                # New (Claude Code 2.x): {"type":"user","message":{"role":"user","content":...}}
                # Old: {"role":"human","content":...}
                message = entry.get("message", {})
                if message:
                    role = message.get("role", "")
                    content = message.get("content", "")
                else:
                    role = entry.get("role", "")
                    content = entry.get("content", "")
                # Normalize role names
                if role == "user":
                    role = "human"

                if role == "human":
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text = block.get("text", "").strip()
                                if text:
                                    lines.append("## 👤 Human")
                                    lines.append(text)
                                    lines.append("")
                    elif isinstance(content, str) and content.strip():
                        lines.append("## 👤 Human")
                        lines.append(content.strip())
                        lines.append("")

                elif role == "assistant":
                    if isinstance(content, list):
                        for block in content:
                            if not isinstance(block, dict):
                                continue
                            if block.get("type") == "text":
                                text = block.get("text", "").strip()
                                if text:
                                    lines.append("## 🤖 Assistant")
                                    lines.append(text)
                                    lines.append("")
                            elif block.get("type") == "tool_use":
                                tool = block.get("name", "unknown")
                                inp = json.dumps(block.get("input", {}), indent=2)
                                lines.append(f"## 🔧 Tool: `{tool}`")
                                lines.append(f"```json\n{inp}\n```")
                                lines.append("")
                    elif isinstance(content, str) and content.strip():
                        lines.append("## 🤖 Assistant")
                        lines.append(content.strip())
                        lines.append("")

    except FileNotFoundError:
        lines.append(f"⚠️ Transcript file not found: {jsonl_path}")
    except Exception as e:
        lines.append(f"⚠️ Parse error: {e}")

    return "\n".join(lines)


# ── Find latest session transcript (manual mode) ───────────────────────────────

def find_latest_transcript(cwd: Path) -> tuple[str, str]:
    """
    Find the most recently modified .jsonl session file in ~/.claude/projects/.
    Returns (session_id, transcript_path) or ("unknown", "") if not found.
    """
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.exists():
        return "unknown", ""

    # Find the project directory matching cwd
    cwd_slug = str(cwd).replace("/", "-").lstrip("-")
    matching = list(claude_projects.glob(f"*{cwd.name}*"))

    search_dirs = matching if matching else list(claude_projects.iterdir())

    latest_file = None
    latest_mtime = 0

    for project_dir in search_dirs:
        if not project_dir.is_dir():
            continue
        for jsonl in project_dir.glob("*.jsonl"):
            mtime = jsonl.stat().st_mtime
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_file = jsonl

    if latest_file:
        return latest_file.stem[:8], str(latest_file)

    return "unknown", ""


# ── GPG encryption ─────────────────────────────────────────────────────────────

def encrypt_with_gpg(plaintext_path: Path) -> bool:
    """
    Encrypt a file with GPG using the default recipient key.
    Returns True if successful, False if GPG is unavailable or fails.
    """
    if not shutil.which("gpg"):
        print("⚠️  GPG not found. Install with: brew install gnupg (Mac) or apt install gnupg (Linux)",
              file=sys.stderr)
        print("    Confidential session saved as plaintext (move it to a secure location).",
              file=sys.stderr)
        return False

    encrypted_path = Path(str(plaintext_path) + ".gpg")
    result = subprocess.run(
        ["gpg", "--batch", "--yes", "--encrypt",
         "--default-recipient-self",
         "--output", str(encrypted_path),
         str(plaintext_path)],
        capture_output=True
    )

    if result.returncode == 0:
        plaintext_path.unlink()  # remove plaintext after successful encryption
        return True
    else:
        print(f"⚠️  GPG encryption failed: {result.stderr.decode()}", file=sys.stderr)
        print(f"    Plaintext file kept at: {plaintext_path}", file=sys.stderr)
        return False


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Export an LLM session transcript to markdown."
    )
    parser.add_argument(
        "--trigger",
        default="manual",
        choices=["precompact", "sessionend", "manual"],
        help="What triggered this export"
    )
    parser.add_argument(
        "--label",
        default="",
        help="Optional label appended to filename. Use 'confidential' to enable GPG encryption."
    )
    parser.add_argument(
        "--transcript",
        default="",
        help="Explicit path to JSONL transcript file (overrides auto-detection)"
    )
    parser.add_argument(
        "--wiki-dir",
        default="",
        help="Explicit path to wiki root for session output (overrides cwd from hook payload)"
    )
    args = parser.parse_args()

    # ── Read hook payload from stdin (Claude Code hook mode) ──────────────────
    hook_data = {}
    if not sys.stdin.isatty():
        try:
            hook_data = json.load(sys.stdin)
        except Exception:
            pass

    session_id = hook_data.get("session_id", "unknown")
    transcript_path_str = args.transcript or hook_data.get("transcript_path", "")
    cwd = Path(hook_data.get("cwd", ".")).resolve()
    # wiki_dir is where sessions are written — always resolves to the central wiki,
    # never the project cwd that triggered the hook.
    wiki_dir = resolve_wiki_root(cwd, args.wiki_dir)

    # ── Control 1: Sentinel file check ────────────────────────────────────────
    # Check both the project cwd (where the user may have placed the sentinel)
    # and the wiki dir (canonical location).
    sentinel = cwd / ".claude" / "no-export"
    wiki_sentinel = wiki_dir / ".claude" / "no-export"
    for s in {sentinel, wiki_sentinel}:
        if s.exists():
            s.unlink()
            print("🔒 Export skipped — confidential sentinel was active. Sentinel removed.",
                  file=sys.stderr)
            sys.exit(0)

    # ── Find transcript (manual mode fallback) ────────────────────────────────
    if not transcript_path_str:
        session_id, transcript_path_str = find_latest_transcript(cwd)
        if not transcript_path_str:
            print("⚠️  No transcript found. Run from your wiki root, or pass --transcript.",
                  file=sys.stderr)
            sys.exit(0)

    transcript_path = Path(transcript_path_str)
    if not transcript_path.exists():
        print(f"⚠️  Transcript not found: {transcript_path}", file=sys.stderr)
        sys.exit(0)

    short_id = session_id[:8] if session_id != "unknown" else "manual"
    is_confidential = args.label.lower() == "confidential"

    # ── Route to correct output directory ─────────────────────────────────────
    if is_confidential:
        export_dir = wiki_dir / "sessions" / "confidential"
    else:
        export_dir = wiki_dir / "sessions" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    # ── Sanitize project name for use in filename ─────────────────────────────
    project_slug = cwd.name.lower()
    project_slug = "".join(c if c.isalnum() or c == "-" else "-" for c in project_slug)
    project_slug = project_slug.strip("-")

    # ── Deduplication: skip SessionEnd if PreCompact already ran ──────────────
    if args.trigger == "sessionend" and not is_confidential:
        existing = list(export_dir.glob(f"*_{short_id}_*_precompact*.md"))
        if existing:
            print(f"Session {short_id} already captured by PreCompact — skipping SessionEnd.",
                  file=sys.stderr)
            sys.exit(0)

    # ── Build output filename ──────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    label_suffix = f"_{args.label}" if args.label else ""
    export_filename = f"{timestamp}_{short_id}_{project_slug}_{args.trigger}{label_suffix}.md"
    export_path = export_dir / export_filename

    # ── Convert and write ──────────────────────────────────────────────────────
    markdown = parse_jsonl_to_markdown(
        transcript_path, session_id, args.trigger,
        project_name=cwd.name,
        project_path=str(cwd)
    )
    export_path.write_text(markdown, encoding="utf-8")

    # ── GPG encryption for confidential sessions ───────────────────────────────
    def safe_print(msg: str) -> None:
        """Print with emoji fallback for Windows consoles that don't support UTF-8."""
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode("ascii", errors="replace").decode("ascii"))

    if is_confidential:
        success = encrypt_with_gpg(export_path)
        if success:
            safe_print(f"🔒 Encrypted → sessions/confidential/{export_filename}.gpg")
        else:
            safe_print(f"Saved (unencrypted) → sessions/confidential/{export_filename}")
    else:
        safe_print(f"✅ Session exported → sessions/exports/{export_filename}")

    sys.exit(0)


if __name__ == "__main__":
    main()
