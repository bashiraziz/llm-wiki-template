#!/usr/bin/env python3
"""
wire-all-projects.py — LLM Wiki Template
==========================================
Wire ALL git repos in a directory to the central wiki session export system.

Runs wire-project.py on every git repo found in the target directory,
skipping repos listed in SKIP_REPOS.

Usage:
    python wire-all-projects.py                     (scans ~/Documents/GitHub/)
    python wire-all-projects.py ~/code              (scans ~/code/)
    python wire-all-projects.py --dry-run           (shows what would be wired)

Skips:
    - The wiki repo itself (already configured)
    - llm-wiki-template (public template)
    - Non-git directories
    - Repos listed in SKIP_REPOS

Configuration:
    Set WIKI_ROOT environment variable or edit wire-project.py.
    Set REPOS_DIR_DEFAULT to your repos directory, or pass it as an argument.
"""

import sys
import os
import argparse
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
from wire_project import wire_project, get_wiki_root


# ── CONFIGURATION ──────────────────────────────────────────────────────────────

# Default directory to scan for repos. Override with command-line argument.
# Examples:
#   Mac/Linux:  Path.home() / "code"
#   Windows:    Path.home() / "Documents" / "GitHub"
REPOS_DIR_DEFAULT = None  # auto-detected if None


# Repos to always skip (names, not full paths)
SKIP_REPOS = {
    "llm-wiki-template",    # public template — don't wire to personal wiki
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def find_repos_dir() -> Path:
    """Auto-detect the repos directory."""
    if REPOS_DIR_DEFAULT:
        return Path(REPOS_DIR_DEFAULT).resolve()

    candidates = [
        Path.home() / "Documents" / "GitHub",
        Path.home() / "Documents" / "git",
        Path.home() / "code",
        Path.home() / "projects",
        Path.home() / "repos",
        Path.home() / "dev",
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c

    # Prompt
    path = input("  Enter the path to your repos directory: ").strip()
    return Path(path).resolve()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Wire all git repos in a directory to the central wiki."
    )
    parser.add_argument(
        "repos_dir",
        nargs="?",
        help="Directory containing your repos (default: auto-detected)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be wired without making changes"
    )
    parser.add_argument(
        "--skip",
        nargs="+",
        help="Additional repo names to skip",
        default=[]
    )
    args = parser.parse_args()

    # Resolve directories
    repos_dir = Path(args.repos_dir).resolve() if args.repos_dir else find_repos_dir()
    wiki_root = get_wiki_root()

    skip = SKIP_REPOS | set(args.skip)

    # Add wiki repo itself to skip list
    skip.add(wiki_root.name)

    if not repos_dir.exists():
        print(f"❌ Repos directory not found: {repos_dir}")
        sys.exit(1)

    print(f"\n🔍 Scanning: {repos_dir}")
    print(f"   Wiki:     {wiki_root}")
    print()

    # Find eligible repos
    repos = sorted([
        d for d in repos_dir.iterdir()
        if d.is_dir()
        and d.name not in skip
        and is_git_repo(d)
    ], key=lambda p: p.name)

    already_wired = []
    to_wire = []

    for repo in repos:
        settings = repo / ".claude" / "settings.json"
        claude_md = repo / "CLAUDE.md"
        if settings.exists() and claude_md.exists():
            content = claude_md.read_text(encoding="utf-8", errors="ignore")
            if "Wiki Integration" in content:
                already_wired.append(repo)
                continue
        to_wire.append(repo)

    # Report
    if already_wired:
        print(f"  ✓ Already wired ({len(already_wired)}):")
        for r in already_wired:
            print(f"    • {r.name}")
        print()

    if not to_wire:
        print("  ✅ All repos already wired. Nothing to do.")
        return

    print(f"  📋 Will wire ({len(to_wire)}):")
    for r in to_wire:
        print(f"    • {r.name}")
    print()

    if args.dry_run:
        print("  (dry run — no changes made)")
        return

    confirm = input("  Proceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Aborted.")
        return

    # Wire each repo
    print()
    succeeded = []
    failed = []

    for repo in to_wire:
        ok = wire_project(repo, wiki_root)
        (succeeded if ok else failed).append(repo)

    # Final report
    print()
    print("=" * 60)
    print(f"✅ Wired: {len(succeeded)}  |  ❌ Failed: {len(failed)}  |  ⏭️  Skipped: {len(already_wired)}")
    print()

    if failed:
        print("Failed repos:")
        for r in failed:
            print(f"  • {r.name}")
        print()

    if succeeded:
        print("Next steps:")
        print("  1. Restart Claude Code in each wired project to activate hooks")
        print("  2. Sessions will export to:")
        print(f"     {wiki_root / 'sessions' / 'exports'}")
        print()
        print("  Commit the changes in each project:")
        for r in succeeded:
            print(f"    cd {r} && git add .claude/settings.json CLAUDE.md && git commit -m 'wire: connect to central wiki'")


if __name__ == "__main__":
    main()
