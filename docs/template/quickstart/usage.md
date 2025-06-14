<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Usage

## Prerequisites

> [!WARNING]
> Follow the [installation instructions](installation.md) before proceeding.

## Overview

1. Create an issue for the task.
1. Create a new branch (`<issue-number>` or similar).
1. (Optional) Add dependencies to `pyproject.toml`.
1. Write code in `/src/<project_name>` and tests in `/tests`.
1. Use `git add`, `git commit` (following [semver](https://semver.org/)),
    and `git push`.
1. __`pre-commit` will guide you through the process.__
1. Create a pull request (following [semver](https://semver.org/)).
1. Wait for CI checks and code review approval.

> [!TIP]
> See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.

## Git workflow

`opentemplate` follows an extended [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow):

1. Create or pick up an issue (task tracker).
1. Create a branch (`<issue-number>` or similar) to track changes.
1. Push your changes to the remote repository.
1. Open a pull request (PR title should follow [semver](https://semver.org/),
    e.g., `feat: add feature`, `fix: bugfix`).

The `main` branch is protected and should always be in a releasable state.

> [!NOTE]
> If a PR has a few commits, its type should match the most significant
> one (`feat!` > `fix!` > `feat` > `fix`).

> [!TIP]
> The [`GitHub CLI`](https://cli.github.com/) simplifies this process.
> __A future extension will streamline it further.__

## Programming

### Source code

Place project source code in `src/<project_name>` or at least
`src` (e.g., `src/infrastructure`).
Some exceptions apply (e.g., `Dockerfile`, `Makefile`).

> [!NOTE]
> Before every commit and push `pre-commit` will run checks
> ensuring code quality and style.

### Tests

Tests should be in `/tests`. The default framework is `pytest`, but
you can change it in `dev-test` section inside `pyproject.toml`.

Key considerations:

- `100%` test coverage is the default (recommended).
- Fuzzing is encouraged ([OSSF Scorecard](https://github.com/ossf/scorecard/blob/main/docs/checks.md#fuzzing));
    [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/) is included
    by default.

> [!NOTE]
> `opentemplate` does not enforce a specific testing methodology (e.g., TDD, BDD).

## Commits

`opentemplate` follows simplified [semver](https://semver.org/):

- Allowed types: `fix`, `feat`, `BREAKING CHANGE`.
- No scopes (e.g., `feat(actions): ...` is incorrect).

Commits should be:

- `Signed-off` (agreeing to the [Developer Certificate of Origin](https://developercertificate.org/)).
- Signed via GPG, SSH, S/MIME, or [`gitsign`](https://github.com/sigstore/gitsign)
    ([learn more](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)).

## Pull requests

Pull request type is determined by the most significant type of commit:

- `BREAKING CHANGE` > `feat` > `fix`.
- Pull requests will be labeled automatically with scopes (additional labels
    may be added manually).

> [!WARNING]
> Predefined labels exist; avoid creating new ones unless necessary.

Each pull request undergoes CI testing (similar to local tests).
Depending on repository type and security settings, up to two reviewers
may be required (as defined during [installation](installation.md)).

## Code sources

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.github/pr-labeler.yml`
- `/.github/workflows/template_setup.yml`
- `.github/workflows/python-tests.yml`
