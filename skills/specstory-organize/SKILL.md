---
name: specstory-organize
description: Organizes SpecStory AI coding sessions in the project's .specstory/history directory into year and month subfolders.
allowed-tools: Bash, Read, Write
license: Apache-2.0
metadata:
  author: SpecStory, Inc.
  version: "1.0.0"
---

From the project root, run the following script with Python to organize the SpecStory history into .specstory/history/YYYY/MM/ subdirectories:

python scripts/organize.py