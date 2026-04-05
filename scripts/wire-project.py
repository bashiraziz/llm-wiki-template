#!/usr/bin/env python3
"""
wire-project.py — LLM Wiki Template
=====================================
Wires any project repository to your central wiki session export system.

Run this once on any existing or new project repo. It installs the Claude Code
hook configuration so every session in that project is automatically exported
to your central wiki session index — making all your projects searchable from
one place.

Usage:
    python wire-project.py <path-to-project>
    python wire-project.py .                          (current directory)
    python wire-project.py ~/code/my-app
    python wire-project.py C:\\Users\\you\\code\\my-app  (Windows)

What it does:
    1. Creates .claude/ directory in the project if it doesn't exist
    2. Writes .claude/settings.json with hooks pointing to central wiki
    3. Creates or appends Wiki Integration section to CLAUDE.md
    4. Does NOT overwrite existing CLAUDE.md content — appends only

Configuration:
    Set WIKI_ROOT to the absolute path of your personal wiki repo.
    On first run you will be prompted if WIKI_ROOT is not configured.

Requirements:
    Python 3.6+
    The wiki must already be set up (run setup.sh in the wiki repo first)
"""

import sys
import json
import shutil
import os
from pathlib import Path
from datetime import datetime


# ── CONFIGURATION ──────────────────────────────────────────────────────────────
#
# Set this to the absolute path of your personal wiki repo.
# Examples:
#   Mac/Linux:  Path.home() / "my-wiki"
#   Windows:    Path(r"C:\Users\YourName\Documents\GitHub\my-wiki")
#
# You can also set the environment variable WIKI_ROOT to override this.
#
WIKI_ROOT_DEFAULT = None  # Set this or use WIKI_ROOT environment variable


def get_wiki_root() -> Path:
    """Resolve wiki root from env var, config, or prompt."""
    # Check environment variable first
    env = os.environ.get("WIKI_ROOT")
    if env:
        return Path(env).resolve()

    # Check default
    if WIKI_ROOT_DEFAULT:
        return Path(WIKI_ROOT_DEFAULT).resolve()

    # Check for a .wiki-root file in common locations
    candidates = [
        Path.home() / ".wiki-root",
        Path.home() / "my-wiki",
        Path.home() / "Documents" / "GitHub" / "my-wiki",
        Path.home() / "Documents" / "my-wiki",
    ]
    for candidate in candidates:
        if candidate.exists() and (candidate / "CLAUDE.md").exists():
            print(f"  📍 Auto-detected wiki root: {candidate}")
            return candidate

    # Prompt
    print()
    print("  Wiki root not configured.")
    print("  Set WIKI_ROOT environment variable or edit WIKI_ROOT_DEFAULT in this script.")
    print()
    wiki_path = input("  Enter the absolute path to your wiki root: ").strip()
    if not wiki_path:
        print("  Aborted.")
        sys.exit(1)
    return Path(wiki_path).resolve()


# ── Hook configuration template ────────────────────────────────────────────────

def build_settings(wiki_scripts: Path) -> dict:
    """Build the .claude/settings.json hook configuration."""
    # Use forward slashes for cross-platform compatibility in commands
    export_script = str(wiki_scripts / "export-session.py").replace("\\", "/")
    index_script  = str(wiki_scripts / "index-sessions.py").replace("\\", "/")
    recall_script = str(wiki_scripts / "recall.py").replace("\\", "/")
    sentinel_path = str(wiki_scripts.parent / "no-export").replace("\\", "\\\\")

    return {
        "hooks": {
            "PreCompact": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python \"{export_script}\" --trigger precompact"
                        }
                    ]
                }
            ],
            "SessionEnd": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python \"{export_script}\" --trigger sessionend"
                        }
                    ]
                }
            ],
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python \"{index_script}\" && python \"{recall_script}\" --recent 3"
                        }
                    ]
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": (
                                f"python -c \"import json,sys,pathlib; "
                                f"d=json.load(sys.stdin); "
                                f"pathlib.Path('{sentinel_path}').touch() "
                                f"if 'this session is confidential' in d.get('prompt','').lower() else None\""
                            )
                        }
                    ]
                }
            ]
        }
    }


# ── Wiki integration section for CLAUDE.md ─────────────────────────────────────

def build_wiki_section(wiki_root: Path, project_name: str) -> str:
    scripts = wiki_root / ".claude" / "scripts"
    recall  = str(scripts / "recall.py").replace("\\", "/")
    wire    = str(wiki_root / "scripts" / "wire-project.py").replace("\\", "/")
    return f"""
---

## Wiki Integration

This project is wired to a central LLM Wiki at:
`{wiki_root}`

### What this means
Every Claude Code session in this repo is automatically exported to the
central wiki session index. All sessions across all wired projects are
searchable from one place.

### Querying the wiki from this project
Before starting a feature, get relevant wiki context:
```
> Check my wiki at {wiki_root}
  for everything relevant to [topic you are building]
```

### Updating the wiki after a session
At the end of any session where domain knowledge was established:
```
> Update the wiki at {wiki_root}
  with what we learned today. Update relevant pages and log.md.
```

### Confidential sessions
```
> This session is confidential
```
(The UserPromptSubmit hook will block export automatically)

### Recall past sessions across all projects
```bash
python "{recall}" "search terms"
python "{recall}" --recent 5
python "{recall}" --date YYYY-MM
```

### Re-wire this project (if hooks stop working)
```bash
python "{wire}" {project_name}
```
"""


# ── Main ───────────────────────────────────────────────────────────────────────

def wire_project(project_path: Path, wiki_root: Path):
    """Wire a single project to the central wiki."""

    if not project_path.exists():
        print(f"  ❌ Project not found: {project_path}")
        return False

    if not project_path.is_dir():
        print(f"  ❌ Not a directory: {project_path}")
        return False

    wiki_scripts = wiki_root / ".claude" / "scripts"

    # Verify wiki scripts exist
    if not wiki_scripts.exists():
        print(f"  ❌ Wiki scripts not found at: {wiki_scripts}")
        print(f"     Run setup.sh in your wiki root first.")
        return False

    print(f"\n  🔧 Wiring: {project_path.name}")

    # ── .claude/settings.json ──────────────────────────────────────────────
    claude_dir = project_path / ".claude"
    claude_dir.mkdir(exist_ok=True)

    settings_path = claude_dir / "settings.json"
    if settings_path.exists():
        backup = claude_dir / f"settings.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        shutil.copy2(settings_path, backup)
        print(f"     📦 Backed up existing settings.json")

    settings = build_settings(wiki_scripts)
    settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(f"     ✅ .claude/settings.json — hooks → central wiki")

    # ── CLAUDE.md ──────────────────────────────────────────────────────────
    claude_md = project_path / "CLAUDE.md"
    wiki_section = build_wiki_section(wiki_root, project_path.name)

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")
        if "Wiki Integration" in content:
            print(f"     ℹ️  CLAUDE.md already has Wiki Integration — skipping")
        else:
            with open(claude_md, "a", encoding="utf-8") as f:
                f.write(wiki_section)
            print(f"     ✅ CLAUDE.md — Wiki Integration section appended")
    else:
        claude_md.write_text(
            f"# CLAUDE.md — {project_path.name}\n"
            f"# Created: {datetime.now().strftime('%Y-%m-%d')}\n"
            f"#\n"
            f"# Add project-specific stack, structure, and conventions here.\n"
            f"# Run: claude → 'Read this project and document it in CLAUDE.md'\n"
            + wiki_section,
            encoding="utf-8"
        )
        print(f"     ✅ CLAUDE.md created with Wiki Integration section")
        print(f"     ⚠️  Open Claude Code and say 'document this project in CLAUDE.md'")

    print(f"     ✓  {project_path.name} wired successfully")
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    wiki_root = get_wiki_root()

    if not wiki_root.exists():
        print(f"❌ Wiki root not found: {wiki_root}")
        print(f"   Set up your wiki first: https://github.com/bashiraziz/llm-wiki-template")
        sys.exit(1)

    success = wire_project(project_path, wiki_root)

    if success:
        print()
        print("  ✅ Done. Restart Claude Code in that project to activate hooks.")
        print(f"     Sessions will export to: {wiki_root / 'sessions' / 'exports'}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
