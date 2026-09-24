<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# GitHub Actions

[GitHub Actions](https://github.com/features/actions) are used to run
CI/CD pipelines.

> [!IMPORTANT]
> No pipeline modifies the repository contents (e.g. no formatting is done),
> it only verifies the compliance (e.g. linting) of source code.

## Pipelines

> [!NOTE]
> Configuration is stored in `.github` directory and `.github/workflows` specifically

Pipelines run approximately the same steps as `prek` hooks, the specific
tooling functionality is located in various other documents such as
[legal](/docs/template/details/legal.md),
[python](/docs/template/details/python.md),
[other languages](/docs/template/details/other-languages.md),
[prose](/docs/template/details/prose.md), etc.

Features of note include:

- each workflow starts with a semantic prefix defining its purpose
    (e.g. `tests`, `security`, `docs`)

- most of the workflows from each semantic group comes in two flavors:

    - `<type>.yml` - analogous to check/linter of `type`, done for every push to
        the pull request (usually ran __only if files of interest where changed__
        in the pull request, e.g. `**.md` files for `markdown.yml`
    - `<type>-reusable.yml` - de facto implementation of the linter,
        called by `<type>.yml`

- `*-update.yml` workflows are ran periodically, see
    [scheduled jobs documentation](/docs/template/details/scheduled-jobs.md)
    for more details

> [!NOTE]
> This structure may not be present in all workflows, as some checks
> should not be run on every push, in these cases only
> `<type>.yml` might be present.

## Reusable workflows

[Reusable workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows):

- Improve security (as the source code is not modifiable
    by the repository owner)
- Keep workflow implementations centralized in the OpenTemplate repository.
    In generated repositories, reusable workflow references are pinned to the
    latest OpenTemplate commit SHA when `harden.yml` runs.

You might want to change the reusable workflows to local workflows
if you:

- want to fully control your pipelines
- want to host/adjust the pipeline yourself
- do not want the pipelines to change behavior without your consent

If so, check the [configuration](#configuration) section.

## Special workflows

These workflows might be of special interest:

- `check-run-reusable.yml` - runs __most of the checks__
    defined in `<type>-reusable.yml` as a sort of centralized runner
- `security-*` - ran on PRs and periodically to ensure the security
    of the project, see [security](/docs/template/details/security.md)
    section for more details

## Caching

Centralized caching (create from `main` branch) is used for all workflows,
after PR merge, the cache is updated (if needed) and stored.

> [!NOTE]
> Cache is optimized on a per-workflow basis, each
> having a minimal set of necessary dependencies.

> [!TIP]
> For source code check `cache.yml`

## Configuration

> [!IMPORTANT]
> Many of the features __can__ be controlled via `pyproject.toml` as described
> in [configuration](#configuration) section.

### Changing workflows reusability

Scripts provided in `.github/reusability`:

- `localize.sh` - changes pinned reusable workflow references
    (pointing to `open-nudge/opentemplate`) to local workflows
- `globalize.sh` - changes local workflows to reusable workflow references
    pinned to a commit SHA (by default, the latest `main` commit)

Run `.github/reusability/localize.sh` or
`.github/reusability/globalize.sh [directory] [skip_files] [repository] [commit_sha]`
to apply the changes. The globalize script resolves the latest `main` commit
when no SHA is supplied.

> [!CAUTION]
> While `localize.sh` is safe to run, `globalize.sh` should be used with
> caution, as it may incorrectly `globalize` local workflows/actions you have
> added on top of the template provided functionality.

## Code sources

- `pyproject.toml`
- `.github/workflows/*.yml`
- `.github/actions/*/action.yml`
