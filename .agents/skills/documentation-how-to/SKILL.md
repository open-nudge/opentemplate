---
# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

name: "documentation-how-to"
description: >
    How to write and update documentation in this project.
    It defines where authored docs live, how reference docs are produced,
    and what release-related documentation updates to make.
license: "Apache-2.0"
metadata:
    author: "Szymon Maszke"
---

# Documentation

Use this skill to create documentation of this project.

## Documentation locations

Create authored documentation **only** in these locations:

- `docs/explanations`
- `docs/tutorials`
- `docs/how-to`

## Reference documentation

Reference documentation will be automatically created from code docstrings
in `src` and `tests`.

## Release-related documentation

Before validating your work adjust:

- `README.md` (sections "Features", "Quick Start/Usage",
    and "Quick Start/Examples")
- complete **ALL** `TBD` sections in `SECURITY-SELF-ASSESSMENT.md`
