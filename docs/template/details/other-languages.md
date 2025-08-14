<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Other languages

> [!IMPORTANT]
> Although these checks are about other languages, the tooling
> is largely Python-based, and the configuration is in the `pyproject.toml`

Except Python a few other "complementary" languages (mostly markup)
are verified by both `pre-commit` and CI pipelines, namely:

- Generic text checks - [`codespell`](https://github.com/codespell-project/codespell)
    verifies spelling and compliance with [`editorconfig`](https://editorconfig.org/)
    is checked by
    [`editorconfig-checker`](https://github.com/editorconfig-checker/editorconfig-checker).
    Additionally `opentemplate` looks for merge conflict strings and whether
    scripts with `shebang` (`#`) is executable
- `yaml` - responsible for GitHub Actions workflows, `mkdocs.yml`,
    `.pre-commit-config.yaml`, performed by
    [adrienverge/yamllint](https://github.com/adrienverge/yamllint)
- `pyproject.toml` - responsible for Python project configuration,
    validated by [abravalheri/validate-pyproject](https://github.com/abravalheri/validate-pyproject)
- `json` - responsible mainly for `renovate.json`, performed by
    [pre-commit/pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
- `toml` - basic syntax correctness checks
- `ini` responsible for `.editorconfig` and `.vale.ini`,
    performed by [danieljrmay/pyinilint](https://gitlab.com/danieljrmay/pyinilint)
- `markdown` - any `markdown` files, see [prose](prose.md) for more information)
- `CITATION.cff` - checked by
    [citation-file-format/cffconvert](https://github.com/citation-file-format/cffconvert)

As with other commands, they have `check-<language>` and
(if available) `fix-<language>` variants and follow standard
procedure as outlined in the [configuration section](../configuration/index.md).

## Code Sources

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.github/workflows/<language>*.yml`
