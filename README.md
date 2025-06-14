<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# opentemplate

<!-- mkdocs remove start -->

<!-- vale off -->

<!-- pyml disable-num-lines 30 line-length-->

<p align="center">
    <em>The simplest to use, yet the most comprehensive Python template</em>
</p>

<div align="center">

<a href="https://pypi.org/project/opentemplate">![PyPI - Python Version](https://img.shields.io/pypi/v/opentemplate?style=for-the-badge&label=release&labelColor=grey&color=blue)
</a>
<a href="https://pypi.org/project/opentemplate">![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fopen-nudge%2Fopentemplate%2Fmain%2Fpyproject.toml&style=for-the-badge&label=python&labelColor=grey&color=blue)
</a>
<a href="https://opensource.org/licenses/Apache-2.0">![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)
</a>
<a>![Coverage Hardcoded](https://img.shields.io/badge/coverage-100%25-green?style=for-the-badge)
</a>
<a href="https://scorecard.dev/viewer/?uri=github.com/open-nudge/opentemplate">![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/open-nudge/opentemplate?style=for-the-badge&label=OSSF)
</a>

</div>

<p align="center">
✨ <a href="#features">Features</a>
🚀 <a href="#quick-start">Quick start</a>
📚 <a href="https://open-nudge.github.io/opentemplate">Documentation</a>
🤝 <a href="#contribute">Contribute</a>
👍 <a href="https://github.com/open-nudge/opentemplate/blob/main/ADOPTERS.md">Adopters</a>
📜 <a href="#legal">Legal</a>
</p>
<!-- vale on -->

______________________________________________________________________

<!-- mkdocs remove end -->

## Features

__opentemplate__ is a Python template with the following features:

- [__Truly open source__](https://open-nudge.github.io/opentemplate/template/about/philosophy):
    no tokens, no fees, no premium plans, open source software only
- [__Ease of use__](https://open-nudge.github.io/opentemplate/template/quickstart/usage):
    clone templated repo, run `pdm setup` and __focus on your code__
- [__Consistency__](https://open-nudge.github.io/opentemplate/template/configuration/basic):
    `pre-commit` and `GitHub Actions` share the same config (`pyproject.toml`)
- [__Security__](https://open-nudge.github.io/opentemplate/template/details/security):
    [SLSA](https://slsa.dev/) L3+ (public/enterprise) or L2 (private),
    [OSSF Best Practices](https://github.com/ossf/scorecard)
- [__Batteries included__](https://open-nudge.github.io/opentemplate/template/details):
    multiple checkers for Python, YAML, Markdown, prose, etc.
- [__Performance__](https://open-nudge.github.io/opentemplate/template/details/github-actions):
    Parallel checks, builds, minimally-sized caches and checkouts

## Quick start

### Installation

> [!NOTE]
> [Install `pdm`](https://pdm-project.org/en/latest/#recommended-installation-method)
> (if you don't have it already), for Linux/MacOS:

```sh
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

1. Create a new GitHub repository using this template
    (green `Use this template` button)
1. Name your repo (__use underscore `_`, not hyphens `-`__)
1. Add project description (__necessary!__)
1. __Wait until the setup commit appears__
    (performed by `github-actions[bot]`, it may take a few minutes)
1. Clone the repository
1. Run `pdm setup` command locally to setup development environment

> [!IMPORTANT]
> For more details read the
> [documentation](https://open-nudge.github.io/opentemplate/template/quickstart/installation)

### Usage

1. Create a new branch
1. Optionally add dependencies to `pyproject.toml`
1. Write code in `/src/<project_name>` and tests in `/tests`
1. Use `git add`, `git commit` and `git push` your changes
1. `pre-commit` will guide you through the process

> [!IMPORTANT]
> For more details read the
> [documentation](https://open-nudge.github.io/opentemplate/template/quickstart/usage)

### Examples

<details>
  <summary><b><big>Run checkers or fixers manually</big></b> (click me)</summary>
&nbsp;

```sh
> pdm check-<group> # pdm fix-<group>
```

Note that all `check` and `fix` commands are grouped for your convenience:

```sh
> pdm check-all # pdm fix-all
```

</details>

<details>
  <summary><b><big>Adjust template</big></b> (click me)</summary>
&nbsp;

> Most of the adjustments can be done by __only__ editing `pyproject.toml`

Common changes to `pyproject.toml`:

- Add dev dependencies under `[dependency-groups]`
    (everything is named `dev-<group>`)
- Modify `[tool.pdm.scripts]` for custom command
    (`check-<group>` or `fix-<group>`, the latter modifies files)
- Use `[tool.<name>]` to adjust specific tool configuration

> __Adjusting these sections will affect `pre-commit` and `GitHub Actions`__

</details>

<details>
  <summary><b><big>Disable some pre-commit check</big></b> (click me)</summary>
&nbsp;

> Disabling checks should be done cautiously!

`pre-commit` checks are defined in `.pre-commit-config.yaml`.

Disable a check using `SKIP` environment variable:

```sh
SKIP='<group1>,<group2>` git commit -m <message>
```

For details, refer to the `id` fields in `.pre-commit-config.yaml`.

> Some commands have both `<group>-fix` and `<group>-check`
> for different actions!

</details>

<!-- mkdocs remove start -->

## Contribute

We welcome your contributions! Start here:

- [Code of Conduct](/CODE_OF_CONDUCT.md)
- [Contributing Guide](/CONTRIBUTING.md)
- [Roadmap](/ROADMAP.md)
- [Changelog](/CHANGELOG.md)
- [Report security vulnerabilities](/SECURITY.md)
- [Open an Issue](https://github.com/open-nudge/opentemplate/issues)

## Legal

- This project is licensed under the _Apache 2.0 License_ - see
    the [LICENSE](/LICENSE.md) file for details.
- This project is copyrighted by _open-nudge_ - the
    appropriate copyright notice is included in each file.

<!-- mkdocs remove end -->

<!-- md-dead-link-check: on -->
