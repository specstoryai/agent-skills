---
name: specstory-project-stats
description: Get project statistics from SpecStory
allowed-tools: Bash(node *)
---

# SpecStory Project Stats

This skill fetches project statistics for the current project from SpecStory's cloud platform.

## Usage

When invoked, this skill will:
1. Determine the project ID by checking (in order):
   - `.specstory/.project.json` file (using `git_id` or `workspace_id`)
   - Git repository name from `.git/config` (remote "origin")
   - Current folder name as fallback
2. Fetch statistics from the SpecStory API at `http://localhost:5173` (local development default, configurable via `SPECSTORY_API_URL` environment variable)
3. Display the statistics to the user

## Instructions

When this skill is invoked, execute the following:

1. Run the stats script:
   ```bash
   node skills/specstory-project-stats/scripts/get-stats.js
   ```

2. Parse and present the statistics to the user in a clear, readable format.

3. Handle errors appropriately:
   - If the API returns a **404 status code**: Inform the user that the project doesn't exist on SpecStory yet. The project may need to be registered or synced first.
   - For other API failures: Suggest verifying the project ID calculation logic or checking the `SPECSTORY_API_URL` environment variable if using a custom endpoint

## Environment Variables

- `SPECSTORY_API_URL`: Override the default API endpoint (default: `http://localhost:5173` for local development, use `https://cloud.specstory.com` for production)

## Example Output

The script will output:
- The calculated project ID
- The API endpoint being called
- The JSON statistics returned from the API
