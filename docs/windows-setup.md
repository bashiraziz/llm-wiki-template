# Windows Setup Guide

Supplement to the main [SETUP-GUIDE.md](../SETUP-GUIDE.md) for Windows-specific setup.

---

## Prerequisites differences on Windows

### Python

Windows may have both `python` and `python3` commands.
Verify which one works:

```powershell
python --version
python3 --version
```

Use whichever returns a version. The scripts use `python` by default.
If only `python3` works, update the hook commands in `.claude/settings.json`.

### SQLite

SQLite is not pre-installed on Windows.

**Option A — Download sqlite3.exe directly (recommended):**
1. Go to sqlite.org/download.html
2. Download `sqlite-tools-win-x64-XXXXXXX.zip`
3. Extract `sqlite3.exe`
4. Copy `sqlite3.exe` to `C:\Windows\System32\` (requires admin)
5. Verify: `sqlite3 --version`

**Option B — Copy to Git Bash path (requires admin):**
```powershell
# Run PowerShell as Administrator:
cp C:\Windows\System32\sqlite3.exe "C:\Program Files\Git\usr\bin\sqlite3.exe"
```

### Git Bash vs PowerShell

The scripts are Python-based and work in both Git Bash and PowerShell.
Always use PowerShell for the `wikiexit` alias.

---

## Session export on Windows

The SessionEnd hook does not fire reliably on Windows when you type `exit`.
Use the `wikiexit` PowerShell alias instead.

### Setup wikiexit (one time)

```powershell
notepad $PROFILE
```

Add (replace `YOUR_WIKI_PATH` with your actual path):

```powershell
function wikiexit {
    python "YOUR_WIKI_PATH\.claude\scripts\export-session.py" `
           --trigger manual `
           --wiki-dir "YOUR_WIKI_PATH"
}
```

Save and close Notepad. Then reload your profile:

```powershell
. $PROFILE
```

### Using wikiexit

After every Claude Code session:

```
exit        ← close Claude Code, back to PowerShell
wikiexit    ← export session to wiki
```

`wikiexit` is a PowerShell function that:
- Works from any project directory
- Auto-detects the latest session transcript
- Exports with the project name in the filename
- Routes to your central wiki regardless of which project you're in

### Verifying it worked

```powershell
dir YOUR_WIKI_PATH\sessions\exports\
```

You should see a new file named:
```
YYYY-MM-DD_HHMMSS_sessionid_projectname_manual.md
```

The project name in the filename confirms which project it came from.

---

## Path differences

Windows uses backslashes in paths. The scripts handle both:
- `C:\Users\you\my-wiki` — Windows style (works)
- `C:/Users/you/my-wiki` — Forward slash (also works in Python)

In `settings.json`, use escaped backslashes:
```json
"C:\\Users\\you\\my-wiki\\.claude\\scripts\\export-session.py"
```

Or forward slashes (simpler, also works):
```json
"C:/Users/you/my-wiki/.claude/scripts/export-session.py"
```

---

## winget not available

If `winget` is not installed, use direct downloads instead:
- SQLite: sqlite.org/download.html
- Python: python.org/downloads
- Git: git-scm.com/download/win

---

## Emoji display as ?

Windows terminal (cp1252 encoding) shows emojis as `?` in script output.
This is cosmetic only — exports work correctly regardless.
The scripts use `safe_print()` which handles this gracefully.

---

## Confidentiality sentinel on Windows

The sentinel file approach works the same on Windows:

```powershell
# PowerShell — create sentinel before a confidential session:
New-Item .claude\no-export -ItemType File
# or shorter:
echo $null > .claude\no-export
```

Or just say `"This session is confidential"` at the first prompt —
the UserPromptSubmit hook creates the sentinel automatically.

---

## Troubleshooting

**`python` not recognized**

Add Python to your PATH, or use the full path:
```powershell
C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe --version
```

**wikiexit says "No transcript found"**

The script looks in `~\.claude\projects\` for the latest session.
Make sure Claude Code has been run at least once from a project directory.
Check:
```powershell
dir $HOME\.claude\projects\
```

**Hooks not activating**

Verify `.claude/settings.json` is valid JSON:
```powershell
python -c "import json; json.load(open('.claude/settings.json'))" && echo valid
```

Check the hook command uses `python` (not `python3` if that's not on your PATH):
```powershell
cat .claude/settings.json | python -m json.tool
```

---

*LLM Wiki Template · MIT License · github.com/bashiraziz/llm-wiki-template*
