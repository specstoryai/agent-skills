# Agent Skills for SpecStory

A collection of AI agent skills for working with [SpecStory](https://specstory.com) session histories. Built for developers who want Claude Code (or similar AI coding assistants) to help analyze, organize, and extract insights from their AI-assisted coding sessions.

Built by [SpecStory](https://specstory.com). SpecStory captures full AI conversation histories including timestamps, prompts, responses, tool calls, and file references.

**Contributions welcome!** Found a way to improve a skill or have a new one to add? [Open a PR](#contributing).

## What are Skills?

Skills are markdown files that give AI agents specialized knowledge and workflows for specific tasks. When you add these to your project, Claude Code can recognize relevant tasks and apply the right frameworks and analysis patterns.

## Available Skills

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [link-trail](skills/link-trail/) | Review SpecStory history transcripts and create a summary of all URLs that were fetched via WebFetch. |
| [session-summary](skills/session-summary/) | Summarize recent SpecStory sessions in standup format. Use when the user wants to review recent coding sessions, prepare for standups, or track work progress. |
| [specstory-guard](skills/specstory-guard/) | Install a pre-commit guardrail that scans .specstory/history for potential secrets and blocks commits until they are removed or redacted. |
| [specstory-organize](skills/specstory-organize/) | Organizes the project's .specstory/history directory into year and month subfolders. |
| [specstory-yak](skills/specstory-yak/) | Analyze your AI coding sessions for yak shaving - when your initial goal got derailed into rabbit holes. Get a "yak shave score" for each session. |
<!-- SKILLS:END -->

## Installation

### Option 1: Clone and Copy (Recommended)

Clone the entire repo and copy the skills folder:

```bash
git clone https://github.com/specstoryai/agent-skills.git
cp -r agent-skills/skills/* .claude/skills/
```

### Option 2: Git Submodule

Add as a submodule for easy updates:

```bash
git submodule add https://github.com/specstoryai/agent-skills.git .claude/agent-skills
```

Then reference skills from `.claude/agent-skills/skills/`.

### Option 3: Fork and Customize

1. Fork this repository
2. Customize skills for your specific needs
3. Clone your fork into your projects

## Usage

Once installed, just ask Claude Code to help with SpecStory-related tasks:

```
"Analyze my yak shaving for the last 30 days"
→ Uses specstory-yak skill

"Summarize my coding sessions from this week"
→ Uses session-summary skill

"Organize my specstory history folder"
→ Uses specstory-organize skill

"What URLs did I visit in my last session?"
→ Uses link-trail skill

"Set up secret scanning for my specstory files"
→ Uses specstory-guard skill
```

You can also invoke skills directly:

```
/specstory-yak
/session-summary
/specstory-organize
/link-trail
/specstory-guard
```

## Skill Categories

### Session Analysis
- `specstory-yak` - Detect rabbit holes and scope creep in your coding sessions
- `session-summary` - Generate standup-ready summaries of recent work
- `link-trail` - Track all URLs fetched during sessions

### Organization & Maintenance
- `specstory-organize` - Keep history files organized by year/month
- `specstory-guard` - Pre-commit hook to catch secrets in history files

## Prerequisites

These skills work with your local `.specstory/history` directory. To use them:

1. Install the [SpecStory VS Code extension](https://marketplace.visualstudio.com/items?itemName=SpecStory.specstory)
2. Have some coding sessions captured in `.specstory/history`
3. Install the skills using one of the methods above

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
