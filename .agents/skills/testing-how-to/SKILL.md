---
# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

name: "testing-how-to"
description: >
    How to test/validate your changes in this project. It defines the acceptance
    criteria, running tests and the retry flow when you have to fix something.
license: "Apache-2.0"
metadata:
    author: "Szymon Maszke"
---

# Testing

Use this skill to test changes in this project.

## Running

You should only ever run one command to test your changes:

```bash
pdm run harness
```

It will:

- validate **ALL** changed files
- return nothing if the validation succeeds
- return `git diff` if the validation fails

## Fixing

When your changes fail validation:

1. Read the error output from the `harness` command and
    the `git diff` reminder of the current state
1. Adjust the code to satisfy the failing checks
1. Rerun the same `pdm run harness` command
