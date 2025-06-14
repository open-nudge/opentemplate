<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Comparing `opentemplate` to similar tools

This guide compares [`open-nudge/opentemplate`](https://github.com/open-nudge/opentemplate)
with similar technologies, including templates, libraries, and platforms.
While the overview is opinionated, we encourage you to verify details
independently.

> [!NOTE]
> If you spot inaccuracies, please open an issue or pull request with corrections.

## Feature comparison

The following table compares `opentemplate` to similar tools:

<!-- pyml disable-num-lines 15 line-length-->

| Feature                 | [`open-nudge/opentemplate`](https://github.com/open-nudge/opentemplate) | [`pyscaffold`](https://github.com/pyscaffold/pyscaffold) | [cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python) | [`microsoft/python-package-template`](https://github.com/microsoft/python-package-template) |
| ----------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Type**                | Template                                                                | Library                                                  | Template                                                                                        | Template                                                                                    |
| **Open Source**         | ✅                                                                      | ✅                                                       | ✅                                                                                              | ✅                                                                                          |
| **Free**                | ✅                                                                      | ✅                                                       | ✅                                                                                              | ✅                                                                                          |
| **Actively Maintained** | ✅                                                                      | ❌                                                       | ❌                                                                                              | ❌                                                                                          |
| **Security-Focused**    | ✅                                                                      | ❌                                                       | ❌                                                                                              | ❌                                                                                          |
| **Latest Tooling**      | ✅                                                                      | ❌                                                       | ❌                                                                                              | ❌                                                                                          |
| **Mature**              | ❌                                                                      | ✅                                                       | ❌                                                                                              | ✅                                                                                          |
| **Unified Config**      | ✅                                                                      | ❌                                                       | ❌                                                                                              | ❌                                                                                          |
| **GitHub-Centric**      | ✅                                                                      | ❌                                                       | ❌                                                                                              | ❌                                                                                          |

### Key notes

- **Free**: No extra cost for advanced features, but GitHub pricing may apply.
- **Latest Tooling**: Uses best-in-class tools
    (e.g., [`ruff`](https://github.com/astral-sh/ruff) for linting).
- **Unified Config**: Supports streamlined local and CI/CD setup via
    `pyproject.toml`.

## How `opentemplate` stands out

Compared to tools like [snyk](https://snyk.io/) or
[jit.io](https://www.jit.io/), `opentemplate` is:

- **DevSecOps-Inspired** – Security-aware but not solely focused on security.
- **Python-Centric** – Designed specifically for Python projects.
- **Truly Open-Source** – Unlike freemium or paid alternatives.
- **GitHub-Integrated** – Built to work seamlessly with GitHub, rather than
    being a standalone platform.

For developers seeking a modern, security-focused, and GitHub-native
Python template, `opentemplate` is a compelling choice.
