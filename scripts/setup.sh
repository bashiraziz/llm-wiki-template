#!/bin/bash
# setup.sh — LLM Wiki Template
# ==============================
# One-time setup script. Run once after cloning the template.
# Creates directory structure, copies adapter files, initializes the database.
#
# Usage:
#   bash scripts/setup.sh [adapter]
#
#   adapter: claude-code (default) | codex | generic
#
# Example:
#   bash scripts/setup.sh
#   bash scripts/setup.sh codex

set -euo pipefail

ADAPTER="${1:-claude-code}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ""
echo "🌿 LLM Wiki Template — Setup"
echo "════════════════════════════"
echo "Adapter: $ADAPTER"
echo "Location: $REPO_ROOT"
echo ""

cd "$REPO_ROOT"

# ── Step 1: Verify prerequisites ──────────────────────────────────────────────
echo "Step 1/7 — Checking prerequisites..."

MISSING=()

command -v python3 &>/dev/null || MISSING+=("python3")
command -v sqlite3 &>/dev/null || MISSING+=("sqlite3")
command -v git &>/dev/null || MISSING+=("git")

if [ ${#MISSING[@]} -gt 0 ]; then
  echo ""
  echo "⚠️  Missing required tools: ${MISSING[*]}"
  echo ""
  echo "Install instructions:"
  echo "  Mac:   brew install ${MISSING[*]}"
  echo "  Linux: sudo apt install ${MISSING[*]}"
  echo "  Windows: see SETUP-GUIDE.md"
  echo ""
  exit 1
fi

# Optional: GPG
if command -v gpg &>/dev/null; then
  echo "  ✓ python3, sqlite3, git, gpg — all found"
else
  echo "  ✓ python3, sqlite3, git — found"
  echo "  ⚠️  gpg not found (optional — needed for encrypted confidential sessions)"
  echo "      Install: brew install gnupg  /  apt install gnupg"
fi

# ── Step 2: Create directory structure ────────────────────────────────────────
echo ""
echo "Step 2/7 — Creating directory structure..."

mkdir -p raw/{assets}
mkdir -p wiki/shared
mkdir -p sessions/{exports,confidential,wiki-digests}

# Create placeholder raw/ gitkeep
touch raw/.gitkeep

echo "  ✓ raw/, wiki/, sessions/ created"

# ── Step 3: Copy adapter files ────────────────────────────────────────────────
echo ""
echo "Step 3/7 — Copying adapter: $ADAPTER..."

case "$ADAPTER" in
  claude-code)
    if [ -d "adapters/claude-code" ]; then
      cp adapters/claude-code/CLAUDE.md ./CLAUDE.md
      mkdir -p .claude
      cp adapters/claude-code/.claude/settings.json .claude/settings.json 2>/dev/null || \
        echo "  ⚠️  settings.json not found in adapter — create manually from SETUP-GUIDE.md"
      echo "  ✓ CLAUDE.md and .claude/settings.json copied"
    else
      echo "  ⚠️  adapters/claude-code/ not found. Using CLAUDE.md in repo root."
    fi
    ;;
  codex)
    if [ -d "adapters/codex" ]; then
      cp adapters/codex/AGENTS.md ./AGENTS.md
      echo "  ✓ AGENTS.md copied"
      echo "  ℹ️  Codex: session export is manual. See adapters/codex/README.md"
    else
      echo "  ⚠️  adapters/codex/ not found."
    fi
    ;;
  generic)
    cp adapters/generic/WIKI-SCHEMA.md ./WIKI-SCHEMA.md 2>/dev/null || true
    echo "  ✓ WIKI-SCHEMA.md copied (generic adapter)"
    ;;
  *)
    echo "  ⚠️  Unknown adapter: $ADAPTER. Valid options: claude-code, codex, generic"
    exit 1
    ;;
esac

# ── Step 4: Copy scripts ──────────────────────────────────────────────────────
echo ""
echo "Step 4/7 — Installing scripts..."

if [ "$ADAPTER" = "claude-code" ]; then
  SCRIPTS_DEST=".claude/scripts"
else
  SCRIPTS_DEST="scripts"
fi

mkdir -p "$SCRIPTS_DEST"

cp scripts/export-session.py "$SCRIPTS_DEST/"
cp scripts/index-sessions.sh "$SCRIPTS_DEST/"
cp scripts/recall.sh "$SCRIPTS_DEST/"

chmod +x "$SCRIPTS_DEST"/*.py "$SCRIPTS_DEST"/*.sh

echo "  ✓ Scripts installed to $SCRIPTS_DEST/ (executable)"

# ── Step 5: Create .gitignore ─────────────────────────────────────────────────
echo ""
echo "Step 5/7 — Creating .gitignore..."

if [ -f ".gitignore" ]; then
  echo "  ℹ️  .gitignore already exists — skipping (check it includes sessions/ and sessions.db)"
else
  cat > .gitignore << 'GITIGNORE'
# LLM Wiki — gitignore
# Session exports — local only, never commit raw transcripts
sessions/exports/
sessions/confidential/
sessions/wiki-digests/

# SQLite index — regenerable from exports
sessions.db
sessions.db-shm
sessions.db-wal

# Confidentiality sentinel
.claude/no-export

# OS noise
.DS_Store
.DS_Store?
._*
Thumbs.db
*.swp
*.swo
.idea/
.vscode/
GITIGNORE
  echo "  ✓ .gitignore created"
fi

# ── Step 6: Create .exportignore ──────────────────────────────────────────────
echo ""
echo "Step 6/7 — Creating .exportignore..."

if [ -f ".exportignore" ]; then
  echo "  ℹ️  .exportignore already exists — skipping"
else
  cat > .exportignore << 'EXPORTIGNORE'
# .exportignore — LLM Wiki Template
# Patterns matched against export filenames.
# Files matching these patterns are excluded from the SQLite FTS5 index.
# They remain on disk but are never searchable.
# Add patterns for any sessions you want to archive but not index.

*_confidential_*.md
*_client_*.md
*_nda_*.md
*_personal_*.md
EXPORTIGNORE
  echo "  ✓ .exportignore created"
fi

# ── Step 7: Initialize SQLite database ────────────────────────────────────────
echo ""
echo "Step 7/7 — Initializing SQLite session index..."

bash "$SCRIPTS_DEST/index-sessions.sh"

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo ""

if [ "$ADAPTER" = "claude-code" ]; then
  echo "  1. Edit CLAUDE.md — replace DOMAIN_1, DOMAIN_2, DOMAIN_3 with your domains"
  echo "     See examples/domains/ for reference configurations"
  echo ""
  echo "  2. Create a private GitHub repo and push:"
  echo "     git remote set-url origin git@github.com:YOU/my-wiki.git"
  echo "     git push -u origin main"
  echo ""
  echo "  3. Open Claude Code and bootstrap:"
  echo "     cd $(pwd)"
  echo "     claude"
  echo "     > customize    ← interactive domain setup"
  echo "     > bootstrap    ← create wiki structure"
  echo ""
  echo "  4. Open wiki/ in Obsidian as a vault"
  echo ""
  echo "  5. Start ingesting:"
  echo "     > ingest research raw/research/my-first-article.md"
else
  echo "  1. Edit your schema file — replace DOMAIN_1, DOMAIN_2, DOMAIN_3"
  echo "  2. Push to a private GitHub repo"
  echo "  3. Open your LLM tool and run: bootstrap"
  echo "  4. See adapters/$ADAPTER/README.md for tool-specific notes"
fi

echo ""
echo "Full instructions: SETUP-GUIDE.md"
echo ""
