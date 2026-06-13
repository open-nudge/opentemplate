<!--
SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Pyproject's [project] metadata source

## General rules

- Each file in this directory represents a distinct metadata
    (e.g. `dependencies.txt` -> `project.dependencies` in `pyproject.toml`).
- Each folder represents a nested metadata section
    (e.g. `optional-dependencies/agents.txt` ->
    `project.optional-dependencies.agents` in `pyproject.toml`).
- Each value should be on a new line (e.g. `keywords.txt` might contain `library\npython\n`).
- Comments beginning with `#` are ignored.

## Additional resources

- See each file/folder for specific metadata details.
- See
    [Python packaging guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
    for a list of available fields and their meaning.
