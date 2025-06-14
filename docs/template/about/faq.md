<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# FAQ

## Why use [`pdm`](https://github.com/pdm-project/pdm) instead of [`uv`](https://github.com/astral-sh/uv)?

`pdm` offers more flexibility, including:

- __PEP 582 support__ – Simplifies dependency management without virtual environments.
- __Custom commands__ – Enables unified workflows without extra tools ([more details](https://github.com/astral-sh/uv/issues/5903)).

> [!NOTE]
> `uv` is under evaluation and may be adopted in the future.

## Why use [`renovate`](https://github.com/renovatebot/renovate) instead of [`dependabot`](https://github.com/dependabot)?

`renovate` provides better support for:

- `pdm.lock` ([issue](https://github.com/dependabot/dependabot-core/issues/3190)).
- `[dev-dependencies]` ([issue](https://github.com/dependabot/dependabot-core/issues/10847)).

> [!NOTE]
> `dependabot` may be reconsidered once key issues are
> resolved and `uv` is used.

## Why is [`basedpyright`](https://docs.basedpyright.com/latest/) used?

`basedpyright` is a fork of [`pyright`](https://github.com/microsoft/pyright)\`
which:

- makes the package `pip` installable
    (unlike [`pyright`](https://github.com/microsoft/pyright))
- provides [LSP](https://microsoft.github.io/language-server-protocol/)
    implementation for Python (unlike [`mypy`](https://github.com/python/mypy))
- supports latest Python versions and features
    (unlike [`pytype`](https://github.com/google/pytype))

## Why use the rejected [`pep582`](https://peps.python.org/pep-0582/) standard?

This approach allows:

- __Local dependencies__ – Everything stays in the project directory.

- __Reusable installs__ – Simplifies scripting (e.g., running tests without
    `nox` or `tox`).

> [!NOTE]
> This may change as tools such as `uv` evolve.

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

## Feature does not work on Windows

Windows features are best-effort and may not be fully supported.

In terms of pre-commit hooks, more involved commands
(e.g. `sbom-*` scripts or `fix-legal`) use Linux/MacOS specific features
__and may not work__.

Upvote [this issue](https://github.com/fsfe/reuse-tool/issues/1108)
when it comes to `fix-legal` script.
