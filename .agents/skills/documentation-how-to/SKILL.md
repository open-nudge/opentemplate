---
# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

name: "documentation-how-to"
description: "When and where to write and update documentation."
license: "Apache-2.0"
metadata:
    author: "Szymon Maszke"
---

## When

Do it AFTER creating implementation in `/src` and testing in `/tests`

## Where

Create documentation **ONLY** in the following paths in the following order:

1. Documentation FOR DEVELOPERS:

    1. `src/README.md` - source description
    2. `tests/README.md` - tests description
    3. `SECURITY-SELF-ASSESSMENT.md` - description of project's security
        posture (**ONLY** TBD sections)

2. Documentation FOR USERS:

    1. `README.md` - project description (**ONLY** sections
        "Features" and "Quick Start/Usage")
    2. `docs/tutorials` - tutorials FOR USERS, see `docs/tutorials/README.md`
    3. `docs/how-to` - how-to guides FOR USERS, see `docs/how-to/README.md`
    4. `docs/explanations` - explanatory guides FOR USERS, see `docs/explanations/README.md`

## Notes

- Public interface/API/Reference documentation will be CREATED
    AUTOMATICALLY FROM `/src` DOCSTRINGS

## Resources

- https://diataxis.fr/ - for `docs/tutorials`, `docs/how-to` and
    `docs/explanations`
