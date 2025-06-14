<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Prose

This document covers non-code aspects of `opentemplate`,
including prose checks, documentation, and related files.

## Checks and Fixes

### Markdown

Markdown is the primary format for project documentation.
The following tools ensure consistency and quality:

- __Formatting:__ [`mdformat`](https://github.com/hukkin/mdformat)
- __Linting:__ [`pymarkdownlnt`](https://github.com/jackdewinter/pymarkdown)
    (similar to [`markdownlint`](https://github.com/DavidAnson/markdownlint))
- __Dead link checking:__ [`md-dead-link-check`](https://github.com/AlexanderDokuchaev/md-dead-link-check)

### `vale`

[`vale`](https://github.com/errata-ai/vale) checks writing style and grammar.
`pre-commit` and GitHub Actions run it on any text files
(__internet access is required__).

> [!TIP]
> To exclude specific checks, update `.vale.ini` instead of `pyproject.toml`.
> See [Vale's documentation](https://vale.sh/docs/vale-ini) for details.

> [!CAUTION]
> Many of the findings of type `suggestion` and `warning`
> __will be false positives__. Use your judgment when addressing them.

## Documentation Files

- __`ROADMAP.md`__ – Planned features and changes.
    __Update before each release or remove.__
- __`ADOPTERS.md`__ – List of project adopters, categorized.
- __`ANNOUNCEMENTS.md`__ – Updates on releases, discussions, and other project news.
- __`CONTRIBUTING.md`__ – Guidelines for contributing.
- __`SUPPORT.md`__ – Support channels and Code of Conduct information.

## Code Sources

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.github/workflows/prose.yml`
