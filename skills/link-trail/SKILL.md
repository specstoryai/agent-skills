---
name: link-trail
description: Review SpecStory history transcripts and create a summary of all URLs that were fetched via WebFetch.
argument-hint: [history-file-or-pattern]
---

Run this command. The output IS the report - do not add any commentary or repeat the output.

```bash
uv run python .claude/skills/link-trail/parse_webfetch.py ${ARGUMENTS:-.specstory/history/*.md} 2>/dev/null | uv run python .claude/skills/link-trail/generate_report.py -
```
