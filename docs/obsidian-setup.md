# Obsidian Setup Guide

Obsidian is the reading interface for your LLM wiki. Claude Code writes the
wiki pages. You read, navigate, and explore using Obsidian's graph view,
backlinks, and search.

---

## Install Obsidian

Download from **obsidian.md** — available for Mac, Windows, Linux, iOS, Android.

---

## Open your wiki as a vault

- Open Obsidian
- Click **"Open folder as vault"**
- Navigate to `[your-wiki-root]/wiki/`
- Click **Select Folder**

> ⚠️ Select the `wiki/` **subdirectory**, not the repo root.
> The root contains scripts, sessions, and config files you
> don't want Obsidian indexing.

The vault name will show as "wiki" in the bottom-left corner.
You'll see your domain folders (research/, work/, personal/, etc.)
in the file explorer immediately.

---

## Recommended settings

### Files and links

Go to Settings → Files and links:

| Setting | Recommended value | Why |
|---|---|---|
| Default location for new notes | Your most-used domain folder | If you ever manually add a note |
| Attachment folder path | `../raw/assets/` | Web-clipped images go to raw/assets/ |
| Automatically update internal links | On | Keeps `[[wikilinks]]` valid when pages move |
| Use `[[Wikilinks]]` | On | Must match the format Claude Code uses |
| New link format | Shortest path when possible | Cleaner links |

### Editor

| Setting | Value | Why |
|---|---|---|
| Default view for new tabs | Reading view | Wiki pages are for reading, not editing |
| Vim key bindings | Your preference | |

---

## Hotkeys to configure

Go to Settings → Hotkeys:

| Search for | Bind to | Why |
|---|---|---|
| "Download attachments for current file" | `Ctrl+Shift+D` | After web clipping, downloads all images locally |
| "Open graph view" | `Ctrl+G` | Quick access to the knowledge graph |
| "Quick switcher" | `Ctrl+O` | Jump to any page by name |

---

## Core plugins to enable

Go to Settings → Core plugins:

| Plugin | Why |
|---|---|
| **Graph view** | See your wiki as a network. Hub pages have many connections. Orphan pages have none. Best way to find gaps and see what's growing. |
| **Backlinks** | Shows every page that links to the current one. Essential for understanding how concepts connect. |
| **Outline** | Navigate long concept pages by heading. |
| **Search** | Full-text search across all wiki pages. |
| **Templates** | Optional — useful if you want consistent page formats. |
| **Word count** | Optional — useful for tracking how much you've written. |

---

## Community plugins (optional)

Go to Settings → Community plugins → Browse:

| Plugin | Why |
|---|---|
| **Dataview** | Run queries over wiki frontmatter. Since every page has YAML frontmatter (domain, tags, date, source_count), you can generate dynamic tables like "all concepts updated this month" or "all sources from domain X". |
| **Marp** | Render Markdown as slide decks directly in Obsidian. Useful when Claude Code generates presentations from wiki content. |
| **Calendar** | Navigate wiki log entries by date. |

---

## Obsidian Web Clipper

Install the browser extension from **obsidian.md/clipper** (Chrome, Firefox, Safari).

Configure it:
- **Default save location**: `../raw/[your-main-domain]/` (relative to vault)
  Example: if your vault is `wiki/` and you want to save to `raw/research/`,
  set it to `../raw/research/`
- **Format**: Markdown
- **Include frontmatter**: Yes (captures date, URL, title automatically)

**Workflow:**
1. Find an article you want to add to your wiki
2. Click the Web Clipper extension
3. It saves a markdown file to `raw/[domain]/`
4. In Claude Code: `> ingest [domain] raw/[domain]/article-name.md`

After clipping, press `Ctrl+Shift+D` (the hotkey you configured) to download
all images locally — so Claude Code can reference them directly without relying
on URLs that may break.

---

## Graph view tips

Open graph view with the icon in the left sidebar or `Ctrl+G`.

**Filters** (top-left of graph view):
- Search box: filter to show only pages matching a term
- Show tags, attachments, orphans: toggle as needed

**Display** (top-right):
- Color nodes by path/folder to visually separate domains
- Increase node size to make hub pages more visible

**What to look for:**
- **Hub pages** (many connections) — your most important concepts
- **Orphan pages** (no connections) — need cross-referencing or may be stale
- **Clusters** — groups of related pages (often one per domain)
- **Bridges** — pages that connect two clusters (cross-domain concepts)

**Run lint when you see orphans:**
```
> lint
```
Claude Code will find orphans, missing cross-references, and suggest connections.

---

## Mobile setup

### iOS — Obsidian Mobile + iCloud

```bash
# On your Mac, create a symlink so wiki/ appears in iCloud:
ln -s ~/my-wiki/wiki \
  ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/my-wiki
```

Open that folder as a vault in Obsidian iOS. Full read access, graph view,
and search — syncs automatically via iCloud.

### Android — Obsidian Mobile + Git

Use the **MGit** app to sync the repo, then open `wiki/` as a vault
in Obsidian Android. Or use **Dropsync** with Dropbox.

### Phone workflow

Mobile is best for reading and quick reference. For adding content:

1. Take a voice note or type a quick note on your phone
2. At your next desktop session, tell Claude Code:
   ```
   > update [domain] [page] — add note from mobile: [paste your note]
   ```

---

## What Obsidian sees (and doesn't see)

Obsidian's vault is `wiki/` only. It does NOT see:

| Directory | Why excluded |
|---|---|
| `sessions/` | Raw transcripts — local only, gitignored |
| `raw/` | Source documents — often too large/noisy for the vault |
| `.claude/` | Scripts and hook configuration |
| `sessions.db` | SQLite binary — not a text file |

This is intentional. The wiki is the curated, structured knowledge.
Everything else is infrastructure.

---

## Dataview query examples

If you install the Dataview plugin, these queries work over wiki frontmatter:

```dataview
TABLE source_count, last_updated
FROM "govcon/concepts"
SORT last_updated DESC
LIMIT 10
```
*All GovCon concept pages, sorted by most recently updated*

```dataview
LIST
FROM "research/sources"
WHERE date_ingested >= date(today) - dur(7 days)
```
*Sources ingested in the last 7 days*

```dataview
TABLE domain, source_count
FROM ""
WHERE source_count = 0
SORT domain ASC
```
*All pages with no sources yet ingested — candidates for enrichment*

---

## Troubleshooting

**Wikilinks show as unresolved (red)**

Claude Code uses `[[page-name]]` format. If Obsidian shows these as broken:
- Settings → Files and links → Use `[[Wikilinks]]` → On
- Settings → Files and links → Shortest path when possible → On

**Images not showing**

Run the download hotkey (`Ctrl+Shift+D`) after clipping articles to
download images locally. Remote image URLs break over time.

**Vault is slow with many files**

Exclude large directories:
Settings → Files and links → Excluded files → add `sessions/` and `raw/`
(even though these aren't in the vault, this prevents any accidental inclusion)

**Graph view is too cluttered**

Use the search filter in graph view to focus on one domain at a time:
- Type `path:govcon` to see only govcon pages
- Type `path:research` to see only research pages

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
