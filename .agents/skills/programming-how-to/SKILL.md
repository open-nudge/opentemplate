---
# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

name: "programming-how-to"
description: >
    How to code features, tests, or specify dependencies  in this project.
    It defines where and how to do it.
license: "Apache-2.0"
metadata:
    author: "Szymon Maszke"
---

# Programming

Use this skill for implementation work in this project.

## Source Code

Write project code in `/src`.

## Tests

Write tests in `/tests`.

## Dependencies

Manage runtime dependencies in `/dependencies`.

- Append core dependencies to `dependencies/dependencies.txt`.
- Create optional dependency files as `dependencies/<optional>.txt`.

## Working style

Keep changes focused on the task and **ONLY** program in these directories:

- `/src` for implementation
- `/tests` for unit tests
- `/dependencies` for project dependency declarations
