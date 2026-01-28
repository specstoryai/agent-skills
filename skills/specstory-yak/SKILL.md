---
name: specstory-yak
description: Analyze your AI coding sessions for yak shaving - when your initial goal got derailed into rabbit holes. Run when user says "analyze my yak shaving", "check for rabbit holes", "how distracted was I", or "yak shave score".
license: MIT
metadata:
  author: specstory
  version: "1.0.0"
  argument-hint: "[days|date-range]"
---

# Specstory Yak Shave Analyzer

Analyzes your `.specstory/history` to detect when coding sessions drifted off track from their original goal. Produces a "yak shave score" for each session.

## How It Works

1. **Parses** specstory history files from a date range (or all recent sessions)
2. **Extracts** the initial user intent from the first message
3. **Tracks** domain shifts: file references, tool call patterns, goal changes
4. **Scores** each session from 0 (laser focused) to 100 (maximum yak shave)
5. **Summarizes** your worst offenders and patterns

## What Is Yak Shaving?

> "I need to deploy my app, but first I need to fix CI, but first I need to update Node, but first I need to fix my shell config..."

Yak shaving is when you start with Goal A but end up deep in unrelated Task Z. This skill detects that pattern in your AI coding sessions.

## Usage

### Slash Command

When invoked via `/specstory-yak`, interpret the user's natural language:

| User says | Script args |
|-----------|-------------|
| `/specstory-yak` | `--days 7` (default) |
| `/specstory-yak last 30 days` | `--days 30` |
| `/specstory-yak this week` | `--days 7` |
| `/specstory-yak top 10` | `--top 10` |
| `/specstory-yak january` | `--from 2026-01-01 --to 2026-01-31` |
| `/specstory-yak from jan 15 to jan 20` | `--from 2026-01-15 --to 2026-01-20` |
| `/specstory-yak by modification time` | `--by-mtime` |
| `/specstory-yak last 14 days as json` | `--days 14 --json` |
| `/specstory-yak save to yak-report.md` | `-o yak-report.md` |
| `/specstory-yak last 90 days output to report` | `--days 90 -o report.md` |

### Direct Script Usage

```bash
python /path/to/skills/specstory-yak/scripts/analyze.py [options]
```

**Arguments:**
- `--days N` - Analyze last N days (default: 7)
- `--from DATE` - Start date (YYYY-MM-DD)
- `--to DATE` - End date (YYYY-MM-DD)
- `--path PATH` - Path to .specstory/history (auto-detects if not specified)
- `--top N` - Show top N worst yak shaves (default: 5)
- `--json` - Output as JSON
- `--verbose` - Show detailed analysis
- `--by-mtime` - Filter by file modification time instead of filename date
- `-o, --output FILE` - Write report to file (auto-adds .md or .json extension)

**Examples:**

```bash
# Analyze last 7 days
python scripts/analyze.py

# Analyze last 30 days, show top 10
python scripts/analyze.py --days 30 --top 10

# Analyze specific date range
python scripts/analyze.py --from 2026-01-01 --to 2026-01-28

# Filter by when files were modified (not session start time)
python scripts/analyze.py --days 7 --by-mtime

# JSON output for further processing
python scripts/analyze.py --days 14 --json

# Save report to a markdown file
python scripts/analyze.py --days 90 -o yak-report.md

# Save JSON to a file
python scripts/analyze.py --days 30 --json -o yak-data.json
```

## Output

```
Yak Shave Report (2026-01-21 to 2026-01-28)
==========================================

Sessions analyzed: 23
Average yak shave score: 34/100

Top Yak Shaves:
---------------
1. [87/100] "fix button alignment" (2026-01-25)
   Started: CSS fix for button
   Ended up: Rewriting entire build system
   Domain shifts: 4 (ui -> build -> docker -> k8s)

2. [72/100] "add logout feature" (2026-01-23)
   Started: Add logout button
   Ended up: Refactoring auth system + session management
   Domain shifts: 3 (ui -> auth -> database)

3. [65/100] "update readme" (2026-01-22)
   Started: Documentation update
   Ended up: CI pipeline overhaul
   Domain shifts: 2 (docs -> ci -> testing)

Most Focused Sessions:
----------------------
1. [5/100] "explain auth flow" (2026-01-26) - Pure analysis, no drift
2. [8/100] "fix typo in config" (2026-01-24) - Quick surgical fix

Patterns Detected:
------------------
- You yak shave most on: UI tasks (avg 58/100)
- Safest task type: Code review/explanation (avg 12/100)
- Peak yak shave hours: 11pm-2am (avg 71/100)
```

## Scoring Methodology

The yak shave score (0-100) is computed from:

| Factor | Weight | Description |
|--------|--------|-------------|
| Domain shifts | 40% | How many times file references jumped domains |
| Goal completion | 25% | Did the original stated goal get completed? |
| Session length ratio | 20% | Length vs. complexity of original ask |
| Tool type cascade | 15% | Read->Search->Edit->Create->Deploy escalation |

**Score interpretation:**
- 0-20: Laser focused
- 21-40: Minor tangents
- 41-60: Moderate drift
- 61-80: Significant yak shaving
- 81-100: Epic rabbit hole

## Present Results to User

When presenting results, highlight:
1. The **worst offenders** with before/after comparison
2. **Patterns** in when/what causes yak shaving
3. **Actionable insight** - what task types to watch out for
