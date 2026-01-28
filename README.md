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
| [specstory-guard](skills/specstory-guard/) | Install a pre-commit guardrail that scans .specstory/history for potential secrets and blocks commits until they are removed or redacted. |
| [specstory-link-trail](skills/specstory-link-trail/) | Review SpecStory history transcripts and create a summary of all URLs that were fetched via WebFetch. |
| [specstory-organize](skills/specstory-organize/) | Organizes the project's .specstory/history directory into year and month subfolders. |
| [specstory-session-summary](skills/specstory-session-summary/) | Summarize recent SpecStory sessions in standup format. Use when the user wants to review recent coding sessions, prepare for standups, or track work progress. |
| [specstory-yak](skills/specstory-yak/) | Analyze your AI coding sessions for yak shaving - when your initial goal got derailed into rabbit holes. Get a "yak shave score" for each session. |
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

This automatically installs to your `.claude/skills/` directory.

### Option 2: Claude Code Plugin

Install via Claude Code's built-in plugin system:

```bash
# Add the marketplace
/plugin marketplace add specstoryai/agent-skills

# Install all SpecStory skills
/plugin install specstory-skills
```

### Option 3: SkillKit (Multi-Agent)

Use [SkillKit](https://github.com/rohitg00/skillkit) to install skills across multiple AI agents (Claude Code, Cursor, Copilot, etc.):

```bash
# Install all skills
npx skillkit install specstoryai/agent-skills

# Install specific skills
npx skillkit install specstoryai/agent-skills --skill specstory-yak specstory-session-summary

# List available skills
npx skillkit install specstoryai/agent-skills --list
```

### Option 4: Clone and Copy

Clone the entire repo and copy the skills folder:

```bash
git clone https://github.com/specstoryai/agent-skills.git
cp -r agent-skills/skills/* .claude/skills/
```

### Option 5: Git Submodule

Add as a submodule for easy updates:

```bash
git submodule add https://github.com/specstoryai/agent-skills.git .claude/agent-skills
```

Then reference skills from `.claude/agent-skills/skills/`.

### Option 6: Fork and Customize

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

### Adding a New Skill

1. Create a new directory under `skills/` with your skill name
2. Add a `SKILL.md` file with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: Brief description of what the skill does
   license: Apache-2.0
   metadata:
     author: your-name
     version: "1.0.0"
   ---
   ```
3. Add any supporting scripts in a `scripts/` subdirectory
4. Include a `LICENSE.txt` file (Apache 2.0)
5. Open a PR!

## License

[Apache 2.0](LICENSE) - Use these however you want.
