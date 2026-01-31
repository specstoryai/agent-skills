# AGENTS.md

Guidelines for AI agents working in this repository.

## Repository Overview

This repository contains **Agent Skills** for AI agents following the [Agent Skills specification](https://agentskills.io/specification.md).

- **Name**: SpecStory Agent Skills
- **GitHub**: [specstoryai/agent-skills](https://github.com/specstoryai/agent-skills)
- **Creator**: SpecStory
- **License**: Apache-2.0

## Repository Structure

```
agent-skills/
├── skills/                # Agent Skills
│   └── specstory-*/
│       ├── SKILL.md       # Required skill file
│       ├── scripts/       # Optional Python scripts
│       └── LICENSE.txt    # Apache 2.0 license
├── LICENSE
└── README.md
```

## Build / Lint / Test Commands

Skills with Python scripts can be tested with:

```bash
# Test yak shave analyzer
python skills/specstory-yak/scripts/analyze.py --help

# Test link trail parser
python skills/specstory-link-trail/parse_webfetch.py --help
```

Verify skill files manually:
- YAML frontmatter is valid
- `name` field matches directory name exactly
- `name` is 1-64 chars, lowercase alphanumeric and hyphens only
- `description` is 1-1024 characters

## Agent Skills Specification

Skills follow the [Agent Skills spec](https://agentskills.io/specification.md).

### Required Frontmatter

```yaml
---
name: specstory-skill-name
description: What this skill does and when to use it. Include trigger phrases.
license: Apache-2.0
metadata:
  author: SpecStory
  version: "1.0.0"
---
```

### Frontmatter Field Constraints

| Field         | Required | Constraints                                                      |
|---------------|----------|------------------------------------------------------------------|
| `name`        | Yes      | 1-64 chars, lowercase `a-z`, numbers, hyphens. Must match dir.   |
| `description` | Yes      | 1-1024 chars. Describe what it does and when to use it.          |
| `license`     | No       | License name (default: Apache-2.0 for this repo)                 |
| `metadata`    | No       | Key-value pairs (author, version, etc.)                          |

### Name Field Rules

- All skills in this repo use the `specstory-` prefix
- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Must match parent directory name exactly

**Valid**: `specstory-yak`, `specstory-session-summary`, `specstory-guard`
**Invalid**: `Specstory-Yak`, `-specstory`, `specstory--yak`

### Skill Directory Structure

```
skills/specstory-*/
├── SKILL.md        # Required - main instructions (<500 lines)
├── scripts/        # Optional - Python scripts for analysis
│   ├── lib/        # Optional - shared library modules
│   └── *.py        # Entry point scripts
└── LICENSE.txt     # Apache 2.0 license
```

## Writing Style Guidelines

### Structure

- Keep `SKILL.md` under 500 lines (move details to `references/`)
- Use H2 (`##`) for main sections, H3 (`###`) for subsections
- Use bullet points and numbered lists liberally
- Short paragraphs (2-4 sentences max)

### Tone

- Direct and instructional
- Second person ("You will analyze...")
- Professional but approachable
- Humor is welcome (especially in yak shave reports)

### Formatting

- Bold (`**text**`) for key terms
- Code blocks for examples and CLI commands
- Tables for reference data
- Emojis allowed in output (especially for status indicators)

### Description Field Best Practices

The `description` is critical for skill discovery. Include:
1. What the skill does
2. When to use it (trigger phrases)
3. Related skills for scope boundaries

```yaml
description: Analyze your AI coding sessions for yak shaving - when your initial goal got derailed into rabbit holes. Run when user says "analyze my yak shaving", "check for rabbit holes", "how distracted was I", or "yak shave score".
```

## SpecStory-Specific Guidelines

### Working with .specstory/history

All skills in this repo work with the `.specstory/history` directory:

- Session files are markdown with timestamps, prompts, responses, tool calls
- Files are named with ISO timestamps: `YYYY-MM-DD_HH-MM-SS-{title}.md`
- User messages are marked with `_**User**_`
- Agent responses follow user messages
- Tool calls appear in code blocks with tool names

### Handling Missing SpecStory

When `.specstory/history` doesn't exist, provide helpful installation instructions:

```
No SpecStory session history found.

Install SpecStory:
- Cursor/VS Code: Search "SpecStory" in Extensions (Cmd/Ctrl+Shift+X)
- Claude Code/CLI: brew tap specstoryai/tap && brew install specstory
```

## Git Workflow

### Branch Naming

- New skills: `skill/specstory-skill-name`
- Improvements: `fix/specstory-skill-name-description`
- Documentation: `docs/description`

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat(skills): add specstory-skill-name skill`
- `fix(specstory-yak): improve scoring algorithm`
- `docs: update README`

### Pull Request Checklist

- [ ] Skill name has `specstory-` prefix
- [ ] `name` matches directory name exactly
- [ ] `name` follows naming rules (lowercase, hyphens, no `--`)
- [ ] `description` is 1-1024 chars with trigger phrases
- [ ] `SKILL.md` is under 500 lines
- [ ] `LICENSE.txt` is included (Apache 2.0)
- [ ] No sensitive data or credentials

## Skill Categories

### Session Analysis
- `specstory-yak` - Detect rabbit holes and scope creep
- `specstory-session-summary` - Generate standup-ready summaries
- `specstory-link-trail` - Track URLs fetched during sessions

### Organization & Maintenance
- `specstory-organize` - Organize history files by year/month
- `specstory-guard` - Pre-commit hook to catch secrets

See `README.md` for full descriptions and usage examples.
