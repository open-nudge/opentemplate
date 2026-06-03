---
# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

name: "dependencies-how-to"
description: "When where and how to add and update dependencies."
license: "Apache-2.0"
metadata:
    author: "Szymon Maszke"
---

As soon as possible you should define necessary dependencies for the project.

## When

Define needed dependencies soon as possible, first implementation step

## Where

Add them to `/project/requirements.txt`, DO NOT CHANGE ANYTHING ELSE.

## How

- Only add the dependencies IF THEY ARE INDISPENSABLE
- Only add well-known and maintained dependencies
- Single line specifying dependency like `requirements.txt`
