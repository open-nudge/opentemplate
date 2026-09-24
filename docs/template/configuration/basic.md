<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Basic

This guide covers essential adjustments to the template.

> [!CAUTION]
> Keep changes minimal to simplify updates.
> If your changes relate to a specific section, you may want to
> consult [details documentation](../details/index.md).

## Project metadata

Declare package metadata directly in the `[project]` table of
`pyproject.toml`.

- __Runtime Dependencies__ – Add dependencies to `[project].dependencies`;
    PDM resolves them into `pdm.lock`.
- __Keywords__ – Edit `[project].keywords`.
- __Classifiers__ – Edit `[project].classifiers`.
- __Nested Metadata__ – Configure optional dependencies, scripts,
    GUI scripts, and entry points in the corresponding `[project]` fields.

## Tool configuration

Development and tool adjustments are made in `pyproject.toml`, which controls:

- __Developer Dependencies__ – Managed in `[dependency-groups]`
    (each dependency prefixed by `dev`).
- __Tool Settings__ – Configures tools like
    [`ruff`](https://docs.astral.sh/ruff/configuration/)
    section `[tool.<name-of-tool>]`.
- __Developer Commands__ – Defined under `[tool.pdm.scripts]`
    (usually `check-<type>` or `fix-<type>`).

> [!NOTE]
> Tool sections are ordered by importance and assumed frequency of change.

## `prek`

Some tools not integrated with `pyproject.toml` can be configured
by editing `prek.toml`.

> [!TIP]
> Non-`pyproject.toml` configurations are at the beginning of the file.

More details: [prek documentation](https://prek.j178.dev/configuration/)

## GitHub Actions

`opentemplate` minimizes manual GitHub Actions configuration, allowing
modifications through `pyproject.toml`.

To add or edit actions, edit files in `.github/workflows/` folder.

> [!TIP]
> See [GitHub Actions Guide](../details/github-actions.md) for more information.

## Other adjustments

For other modifications, check:

- Relevant documentation sections (mostly [details documentation](../details/index.md)).
- [FAQ](../about/faq.md) for general questions.
- [Tips and Tricks](../about/tips-and-tricks.md)

> [!IMPORTANT]
> __Need Help?__ Search the docs for specific files or directories.
> If you can’t find what you need, please
> [open an issue](https://github.com/open-nudge/opentemplate/issues).

## Code sources

- `pyproject.toml`
- `prek.toml`
- `.github/workflows/`
