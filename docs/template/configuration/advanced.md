<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Advanced

To host your own template based on `opentemplate`, you can follow these steps:

1. [Fork the repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
    to your own GitHub account/organization
1. Make it a [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
1. Follow the steps in the [quick start guide](../quickstart/usage.md) (e.g. hardening)
1. Clone the repository, `pdm setup` and perform your changes

> [!TIP]
> Improvements to `opentemplate` are welcome! Please open an issue, discuss
> with the maintainers and your features might be upstreamed.

## General

Many of the adjustments will be tested as you develop them,
as __`opentemplate` is also a Python package__.

Caveats to remember:

- `.github/workflows/template-*` - files should be of special interest
    as they are used for `template` related functionality, e.g. testing
- `.github/workflows/release*.yml` - most complex workflow, a few parts
    __are not fully tested currently__.

## Tips

When adding a new feature (e.g. tool/check) you might consider the following
algorithm-like steps:

1. Check if the tool is available as a Python package
    (e.g. on [`PyPI`](https://pypi.org/))

1. __If yes and it fits in one of the categories (e.g. `dev-python`)__:

    1. Add the package to `pyproject.toml`
        (usually `dev-<category>` in `[dependency-groups]` section)

    1. Specify only the major version (e.g. `>=1`) if above `1.0.0`,
        or the exact version if below `1.0.0`

    1. Add the tool call to `[tool.pdm.scripts]` under `check-<category>`
        and `fix-<category>` if applicable

    1. Go to testing steps below

1. __If yes, but the appropriate category does not exist__:

    1. Create a new `dev-<category>` and put the package there

    1. Create appropriate entry in `.pre-commit-config.yaml`
        under the `- repo: "local"` section, `id: <category>`

    1. Create an entry in `.github/renovate.json` with appropriate
        [`matchPackageNames`](https://docs.renovatebot.com/configuration-options/#matchpackagenames)

    1. Create three workflows in `.github/workflows`
        (see `GitHub Actions` guide for more details):

        1. `<category>.yml` - checker run on human PRs

        1. `<category>-renovate.yml` - checker run on Renovate PRs

        1. `<category>-reusable.yml` - checker run used by the other two
            and which (probably) uses `.github/workflows/check-reusable.yml`

    1. Go to testing steps below

1. __If not__:

    1. Create appropriate entry in `.pre-commit-config.yaml`
        __if the tool is available as a `pre-commit` hook__
        (or try to create one if not)

    1. Add support for the tool in `.github/renovate.json/`
        (if applicable and available)

    1. Create three workflows in `.github/workflows`
        (see `GitHub Actions` guide for more details):

        1. `<category>.yml` - checker run on human PRs

        1. `<category>-update.yml` - if the tool requires updates,
            __but not supported by [`renovate`](https://docs.renovatebot.com/)__

> [!TIP]
> Order of the `.pre-commit-config.yaml` entries is important.
> Make sure to think about the implications of the changes done
> by your entry on the whole pipeline.

> [!CAUTION]
> This is a rough guide and in many specific cases you might
> have to consult specific functionalities and their implementation
> (start by consulting [details documentation](../details/index.md)).
