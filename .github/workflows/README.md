<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
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

Pipelines run approximately the same steps as `pre-commit` hooks, the specific
tooling functionality is located in various other documents such as
[legal](/docs/template/details/legal.md),
[python](/docs/template/details/python.md),
[other languages](/docs/template/details/other-languages.md),
[prose](/docs/template/details/prose.md), etc.

Features of note include:

- each workflow starts with a semantic prefix defining its purpose
    (e.g. `tests`, `security`, `docs`)

- most of the workflows from each semantic group comes in three flavors:

    - `<type>.yml` - analogous to check/linter of `type`, done for every push to
        the pull request (usually ran __only if files of interest where changed__
        in the pull request, e.g. `**.md` files for `markdown.yml`
    - `<type>-renovate.yml` - checks run, when `renovate[bot]` makes an update
        to the checkers (e.g. `dev-markdown` in `pyproject.toml`'s `[dependency-groups]`
        gets updated, the markdown checks run on all `markdown` files in the repository).
        This allows verification of updates against currently accepted
        standards (e.g. no new checks were introduced without feedback)
    - `<type>-reusable.yml` - de facto implementation of the linter,
        will be called `<type>.yml` and `<type>-renovate.yml`

- `*-update.yml` workflows are ran periodically, see
    [scheduled jobs documentation](/docs/template/details/scheduled-jobs.md)
    for more details

> [!NOTE]
> This structure may not be present in all workflows, as some checks
> should not be ran on every push or renovate update, in these cases only
> `<type>.yml` might be present.

## Reusable workflows

[Reusable workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows):

- Improve security (as the source code is not modifiable
    by the repository owner)
- Streamline updates from the main template (as the reusable
    workflows are updated from the `opennudge/opentemplate` repository)

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

Scripts provided in `.github/workflows/reusability`:

- `localize.sh` - changes the reusable workflows
    (pointing to `opennudge/opentemplate`) to local workflows
- `globalize.sh` - changes the local workflows to reusable workflows
    (pointing to `opennudge/opentemplate`)

Run `./reusability/localize.sh` or `./reusability/globalize.sh` to
apply the changes. The script also allows you to specify the directory
where the changes should be applied as an argument.

> [!CAUTION]
> While `localize.sh` is safe to run, `globalize.sh` should be used with
> caution, as it may incorrectly `globalize` local workflows/actions you have
> added on top of the template provided functionality.

> [!WARNING]
> `release-package-reusable.yml` and `release-package-upload-reusable.yml`
> used by `release.yml` __should not be globalized__ as they are
> attested uploads to PyPI do not yet support reusable workflows
> (see [this GitHub issue](https://github.com/pypi/warehouse/issues/11096)).

## Code sources

- `pyproject.toml`
- `.github/workflows/*.yml`
- `.github/actions/*/action.yml`
