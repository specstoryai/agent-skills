---
name: specstory-guard
description: Install a pre-commit guardrail for SpecStory AI coding sessions that scans .specstory/history for potential secrets and blocks commits until they are removed or redacted.
---

# SpecStory Guard

## When to use

- You want automatic protection against committing secrets that appear in SpecStory histories.
- You want a pre-commit hook that scans `.specstory/history` by default.

## What it does

- Scans `.specstory/history` for common secret patterns (tokens, keys, private key blocks).
- Fails the commit if matches are found and prints a redacted report.
- Uses no external dependencies.

## Setup

1. Install the pre-commit hook:

   ```zsh
   python3 skills/specstory-guard/scripts/setup.py install
   ```

2. The hook is installed at `.git/hooks/pre-commit` and runs on every commit.

## Manual scan

```zsh
python3 skills/specstory-guard/scripts/scan.py --root .
```

## Tuning

- Add extra allowlist regex patterns with `SPECSTORY_GUARD_ALLOWLIST`.
- The value is a comma-separated list of regular expressions.

Example:

```zsh
SPECSTORY_GUARD_ALLOWLIST='example-key,PLACEHOLDER_.*' \
  python3 skills/specstory-guard/scripts/scan.py --root .
```

## Remediation

- Redact or remove the secret from the history file.
- Re-run the scan or retry the commit.

## Verification

```zsh
python3 skills/specstory-guard/scripts/scan.py --root .
```
