<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# FAQ

## Why is [`pyrefly`](https://github.com/facebook/pyrefly) used?

`pyrefly` is used for template type checking because it:

- makes the package `pip` installable
- supports local configuration from `pyproject.toml`
- emits JSON output consumed by [`mutmut`](https://mutmut.readthedocs.io/en/latest/)
    for type-aware mutation filtering

## Where are the dependencies installed?

In the `.venv` virtual environment inside the project directory
(managed by `uv`), so everything stays local to the project.
Tests run in separate environments per Python version (`.venvs/<version>`),
which install the package non-editable, as users would.

## Why is `CHANGELOG.md` empty?

It is not! It links to GitHub releases, which serve as the actual changelog.

Options considered:

- __Manual updates__ – Prone to being outdated.
- __Bot updates__ – Conflicts with branch protection ([details](https://github.com/orgs/community/discussions/25305)).
- __GitHub releases link__ – Automated and secure.

> [!TIP]
> You can manually copy release notes into `CHANGELOG.md`
> after a release.

## Why are there so many caches in GitHub Actions?

Cache per each `dev-dependency`, standard dependencies (including optional)
and even their combinations.

This optimizes download times, which speeds up the workflows.

> [!TIP]
> Check `.github/workflows/cache.yml` for cache settings.
