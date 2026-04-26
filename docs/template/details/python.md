<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Python

> [!IMPORTANT]
> For testing details, see the [tests](tests.md) documentation.

As the project's core language, `Python` undergoes the most extensive linting.

## Checks and fixes

The following tools are used, in order:

- __Code formatting and linting:__ [`ruff`](https://github.com/astral-sh/ruff)
    (all checks enabled by default)
- __Type checking:__ [`basedpyright`](https://github.com/DetachHead/basedpyright)
    (run as a separate `typing` step)
- __Docstring coverage:__ [`interrogate`](https://github.com/econchick/interrogate)
    (checks all functions, classes, and modules, including private ones)

## Adjustments

You can configure most of the settings in `pyproject.toml`
(see [Configuration](../configuration/index.md)), for example:

- __Lower docstring coverage threshold:__ Adjust `fail-under`
    in `[tool.interrogate]`.

## Code sources

- `pyproject.toml`
- `.github/workflows/python*.yml`
