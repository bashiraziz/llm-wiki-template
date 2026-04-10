#!/usr/bin/env python3
"""
sweep-sessions.py — LLM Wiki Template
=======================================
Finds all Claude Code session JSONL files not yet exported to the wiki
and exports them. Safe to run repeatedly — skips already-exported sessions.

Called by wikiexit to catch sessions missed by the PreCompact and
SessionEnd hooks (e.g. sessions that were auto-compacted, or where the
window was closed before hooks fired).

Usage:
    python3 .claude/scripts/sweep-sessions.py
    python3 .claude/scripts/sweep-sessions.py --dry-run
    python3 .claude/scripts/sweep-sessions.py --days 7     # recent only
    python3 .claude/scripts/sweep-sessions.py --days 0     # all time

Requirements:
    Python 3.6+
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# ── Wiki root resolution ───────────────────────────────────────────────────────
# Same priority chain as export-session.py:
# --wiki-dir flag → WIKI_ROOT env var → hardcoded path → cwd

_WIKI_ROOT_HARDCODED = None  # Set to your wiki path, or use WIKI_ROOT env var


def resolve_wiki_root(cli_override: str = "") -> Path:
    if cli_override:
        return Path(cli_override).resolve()
    env_root = os.environ.get("WIKI_ROOT", "")
    if env_root:
        return Path(env_root).resolve()
    if _WIKI_ROOT_HARDCODED and Path(_WIKI_ROOT_HARDCODED).exists():
        return Path(_WIKI_ROOT_HARDCODED)
    return Path(".").resolve()


# ── Already-exported ID detection ─────────────────────────────────────────────

def get_exported_ids(wiki_dir: Path) -> set:
    """Collect 8-char session IDs already present in exports or wiki-digests."""
    exported = set()
    for folder in ("sessions/exports", "sessions/wiki-digests"):
        d = wiki_dir / folder
        if not d.exists():
            continue
        for f in d.iterdir():
            if f.suffix != ".md":
                continue
            parts = f.stem.split("_")
            # Standard format: YYYY-MM-DD_HHMMSS_<8-char-id>_<project>_<trigger>
            # parts[0] = date, parts[1] = time or label, parts[2] = 8-char hex id
            if len(parts) >= 3:
                candidate = parts[2]
                if len(candidate) == 8 and all(c in "0123456789abcdef" for c in candidate):
                    exported.add(candidate)
    return exported


# ── JSONL discovery ────────────────────────────────────────────────────────────

def find_unexported(wiki_dir: Path, max_age_days: int = 0) -> list:
    """
    Return list of (project_slug, jsonl_path) for every JSONL not yet exported.
    Skips files smaller than 512 bytes (empty or stub sessions).
    Sorted by modification time, oldest first.
    """
    exported = get_exported_ids(wiki_dir)
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.exists():
        return []

    cutoff = None
    if max_age_days > 0:
        cutoff = datetime.now().timestamp() - max_age_days * 86400

    results = []
    for project_dir in sorted(claude_projects.iterdir()):
        if not project_dir.is_dir():
            continue
        for jsonl in sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime):
            stat = jsonl.stat()
            if stat.st_size < 512:
                continue
            if cutoff and stat.st_mtime < cutoff:
                continue
            short_id = jsonl.stem[:8]
            if short_id not in exported:
                results.append((project_dir.name, jsonl))

    return results


# ── Output helper ──────────────────────────────────────────────────────────────

def safe_print(msg: str) -> None:
    """Print with emoji fallback for Windows consoles that don't support UTF-8."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export all session JSONLs not yet captured by hooks."
    )
    parser.add_argument(
        "--wiki-dir", default="",
        help="Path to wiki root (overrides WIKI_ROOT env var and hardcoded path)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List what would be exported without exporting anything"
    )
    parser.add_argument(
        "--days", type=int, default=0,
        help="Only sweep sessions from the last N days (default: 0 = all time)"
    )
    args = parser.parse_args()

    wiki_dir = resolve_wiki_root(args.wiki_dir)
    export_script = Path(__file__).parent / "export-session.py"
    index_script = Path(__file__).parent / "index-sessions.py"

    unexported = find_unexported(wiki_dir, args.days)

    if not unexported:
        safe_print("✓ No unexported sessions found.")
        return

    label = f" (last {args.days} days)" if args.days else " (all time)"
    safe_print(f"Found {len(unexported)} unexported session(s){label}:\n")
    for project_slug, jsonl in unexported:
        size_kb = jsonl.stat().st_size // 1024
        mtime = datetime.fromtimestamp(jsonl.stat().st_mtime).strftime("%Y-%m-%d")
        safe_print(f"  {mtime}  {size_kb:>6} KB  {project_slug[:40]}  {jsonl.stem[:8]}")

    if args.dry_run:
        safe_print("\n(dry-run — nothing exported)")
        return

    safe_print("")
    ok = 0
    for project_slug, jsonl in unexported:
        result = subprocess.run(
            [sys.executable, str(export_script),
             "--trigger", "manual",
             "--transcript", str(jsonl),
             "--wiki-dir", str(wiki_dir)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            ok += 1
            if result.stdout.strip():
                safe_print(result.stdout.strip())
        else:
            safe_print(f"  ⚠ Failed: {jsonl.stem[:8]} — {result.stderr.strip()[:100]}")

    safe_print(f"\n✓ Swept {ok}/{len(unexported)} session(s).")

    # Re-index so the new exports are immediately searchable
    if ok:
        index_py = index_script if index_script.exists() else None
        index_sh = Path(__file__).parent / "index-sessions.sh"

        if index_py:
            result = subprocess.run([sys.executable, str(index_py)], capture_output=True, text=True)
        elif index_sh.exists():
            result = subprocess.run(["bash", str(index_sh)], capture_output=True, text=True)
        else:
            result = None

        if result and result.stdout.strip():
            safe_print(result.stdout.strip())


if __name__ == "__main__":
    main()
