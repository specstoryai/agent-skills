# Contributing to Agent Skills

We welcome contributions! Whether it's a new skill, an improvement to an existing one, or documentation updates.

## Repository Structure

```
agent-skills/
├── .github/
│   ├── scripts/
│   │   └── sync-skills.js # Script to sync skills across files
│   └── workflows/
│       ├── sync-skills.yml     # Auto-sync workflow
│       └── validate-skill.yml  # Validation workflow
├── skills/
│   └── specstory-*/       # Individual skills
│       ├── SKILL.md       # Skill definition (required)
│       ├── scripts/       # Optional supporting scripts
│       └── LICENSE.txt    # Apache 2.0 license
├── AGENTS.md              # Guidelines for AI agents
├── CLAUDE.md              # Symlink to AGENTS.md
└── README.md              # Main documentation
```

## GitHub Workflows

### `sync-skills.yml`

**Triggers:** Push to `main` branch when files in `skills/` change

**What it does:**
- Runs `.github/scripts/sync-skills.js`
- Scans `skills/` directory for valid skills (directories with `SKILL.md`)
- Updates the README.md skills table between `<!-- SKILLS:START -->` and `<!-- SKILLS:END -->`
- Auto-commits changes if anything was updated

This means you don't need to manually update the README table when adding/removing skills.

### `validate-skill.yml`

**Triggers:** Push or PR to `main` when `SKILL.md` files change

**What it does:**
- Detects which skills were changed
- Validates each changed skill using [Flash-Brew-Digital/validate-skill](https://github.com/Flash-Brew-Digital/validate-skill)
- Checks frontmatter is valid (name, description fields)
- Ensures naming conventions are followed

## AGENTS.md

The `AGENTS.md` file provides guidelines for AI agents working in this repository. It covers:

- Repository structure and conventions
- Skill specification requirements
- Frontmatter field constraints
- Naming rules (all skills use `specstory-` prefix)
- Writing style guidelines
- Git workflow and commit conventions

`CLAUDE.md` is a symlink to `AGENTS.md` for Claude Code compatibility.

## Adding a New Skill

1. **Create the skill directory:**
   ```bash
   mkdir -p skills/specstory-your-skill-name
   ```

2. **Add `SKILL.md`** with required frontmatter:
   ```yaml
   ---
   name: specstory-your-skill-name
   description: What this skill does and when to use it. Include trigger phrases.
   license: Apache-2.0
   metadata:
     author: your-name
     version: "1.0.0"
   ---

   # Your skill instructions here
   ```

3. **Add `LICENSE.txt`** (copy from another skill - Apache 2.0)

4. **Optional: Add scripts** in a `scripts/` subdirectory

5. **Open a PR** - the validation workflow will check your skill

### Naming Rules

- All skills must use the `specstory-` prefix
- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Name must match directory name exactly

**Valid:** `specstory-yak`, `specstory-session-summary`
**Invalid:** `Specstory-Yak`, `session-summary`, `specstory--yak`

### PR Checklist

- [ ] Skill name has `specstory-` prefix
- [ ] `name` in frontmatter matches directory name
- [ ] `description` includes trigger phrases (1-1024 chars)
- [ ] `SKILL.md` is under 500 lines
- [ ] `LICENSE.txt` is included (Apache 2.0)
- [ ] No sensitive data or credentials

## Testing Locally

Don't run `npx skills add` from within this repo - it will install skills into the repo directory. Instead:

1. Clone this repo
2. Make your changes
3. Test by copying your skill to a separate project:
   ```bash
   cp -r skills/specstory-your-skill ~/.claude/skills/
   ```

## Technical Standards

The guidelines in [AGENTS.md](./AGENTS.md) apply equally to human contributors. Key points:

- Keep `SKILL.md` under 500 lines
- Use clear, direct language
- Include example usage where helpful
- Follow conventional commits for commit messages

## Code of Conduct

Be respectful and constructive in all project communication.
