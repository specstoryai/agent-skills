# Agent Skills for SpecStory

A collection of AI agent skills for working with [SpecStory](https://specstory.com) session histories. Built for developers who want Claude Code (or similar AI coding assistants) to help analyze, organize, and extract insights from their AI-assisted coding sessions.

**Contributions welcome!** Found a way to improve a skill or have a new one to add? [Open a PR](#contributing).

## What are Skills?

Skills are markdown files that give AI agents specialized knowledge and workflows for specific tasks. When you add these to your project, Claude Code (or agents like Codex, Cursor, Gemini, Copilot) can recognize relevant tasks and apply the right frameworks and analysis patterns.

## Prerequisites

These skills work with your local `.specstory/history` directory, which is created by [SpecStory](https://github.com/specstoryai/getspecstory) when capturing AI coding sessions.

**Install SpecStory for your tool:**

| Tool | Installation |
|------|--------------|
| **Cursor / VS Code** | Search "SpecStory" in Extensions (Cmd/Ctrl+Shift+X) |
| **Claude Code / CLI agents** | `brew tap specstoryai/tap && brew install specstory` |

Once installed, your AI conversations are automatically saved to `.specstory/history/` in each project.

> **Note for contributors:** Don't run `npx skills add` from within this repo - it will install skills into the repo directory. The `.gitignore` excludes these directories, but install skills in your actual projects instead.

## Available Skills

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [specstory-guard](skills/specstory-guard/) | Install a pre-commit guardrail for SpecStory AI coding sessions that scans .specstory/history for potential secrets and... |
| [specstory-link-trail](skills/specstory-link-trail/) | Review SpecStory AI coding sessions in .specstory/history and create a summary of all URLs that were fetched via... |
| [specstory-organize](skills/specstory-organize/) | Organizes SpecStory AI coding sessions in the project's .specstory/history directory into year and month subfolders. |
| [specstory-session-summary](skills/specstory-session-summary/) | Summarize recent SpecStory AI coding sessions in standup format. Use when the user wants to review sessions from... |
| [specstory-yak](skills/specstory-yak/) | Analyze your SpecStory AI coding sessions in .specstory/history for yak shaving - when your initial goal got derailed... |
<!-- SKILLS:END -->

## Installation

### Option 1: Skills CLI (Recommended)

Use [npx skills](https://skills.sh) to install skills directly:

```bash
# Install all skills
npx skills add specstoryai/agent-skills

# Install specific skills
npx skills add specstoryai/agent-skills --skill specstory-yak specstory-session-summary

# List available skills
npx skills add specstoryai/agent-skills --list
```

This installs skills to `.agents/skills/` and symlinks them to each detected agent's directory (`.claude/skills/`, `.cursor/skills/`, `.codex/skills/`, etc.). The CLI auto-detects which agents you have installed.

### Option 2: Claude Code Plugin

Install via Claude Code's built-in plugin system:

```bash
# Add the marketplace
/plugin marketplace add specstoryai/agent-skills

# Install all SpecStory skills
/plugin install specstory-skills
```

### Option 3: Clone and Copy

Clone the entire repo and copy the skills folder:

```bash
git clone https://github.com/specstoryai/agent-skills.git
cp -r agent-skills/skills/* .claude/skills/
```

### Option 4: Git Submodule

Add as a submodule for easy updates:

```bash
git submodule add https://github.com/specstoryai/agent-skills.git .claude/agent-skills
```

Then reference skills from `.claude/agent-skills/skills/`.

### Option 5: Fork and Customize

1. Fork this repository
2. Customize skills for your specific needs
3. Clone your fork into your projects

## Usage

Once installed, just ask Claude Code to help with SpecStory-related tasks:

```
"Analyze my yak shaving for the last 30 days"
→ Uses specstory-yak skill

"Summarize my coding sessions from this week"
→ Uses specstory-session-summary skill

"Organize my specstory history folder"
→ Uses specstory-organize skill

"What URLs did I visit in my last session?"
→ Uses specstory-link-trail skill

"Set up secret scanning for my specstory files"
→ Uses specstory-guard skill
```

You can also invoke skills directly:

```
/specstory-yak
/specstory-session-summary
/specstory-organize
/specstory-link-trail
/specstory-guard
```

## Skill Categories

### Session Analysis
- `specstory-yak` - Detect rabbit holes and scope creep in your coding sessions
- `specstory-session-summary` - Generate standup-ready summaries of recent work
- `specstory-link-trail` - Track all URLs fetched during sessions

### Organization & Maintenance
- `specstory-organize` - Keep history files organized by year/month
- `specstory-guard` - Pre-commit hook to catch secrets in history files

## Contributing

Found a way to improve a skill? Have a new skill to suggest? PRs and issues welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Repository structure and GitHub workflows
- How to add a new skill
- Naming conventions and PR checklist

## License

[Apache 2.0](LICENSE) - Use these however you want.
