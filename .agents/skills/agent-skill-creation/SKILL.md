---
# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

name: "agent-skill-creation"
description: "When and where to write agents skill of the package"
license: "Apache-2.0"
metadata:
    author: "open-nudge" # templateskip
    documentation: "https://open-nudge.github.io/opentemplate" # templateskip
    repository: "https://github.com/open-nudge/opentemplate" # templateskip
---

Use this skill to DESCRIBE HOW AGENTS SHOULD USE THE PACKAGE.

## When

- AFTER creating implementation in `/src`, testing in `/tests` and documentation

## Where

Write agents documentation of the package **ONLY** in the following path:

- `/src/<pkg>/.agents/skills/<pkg>/SKILL.md`

## Notes

- It **SHOULD** be `SKILL.md` **ONLY** (no scripts, references or other files)
- Describe HOW TO USE the package, NOT how to develop it

## Resources

- https://agentskills.io/specification - `SKILL.md` format
