<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Tips and tricks

This guide provides useful tips for working with the `opentemplate`-based projects.

## Committing

> [!IMPORTANT]
> You can use `git commit` normally; `pre-commit` will not allow you commit
> without passing all the checks.

`opentemplate` offers the following commit options:

- `pdm run commit` – Runs `git commit` with `--signoff --gpg-sign`.

- `pdm run commit-type` – Prompts for a commit message and type
    (`feat`, `fix`, `feat!`, `fix!`).

- `pdm run commit-guided` – Opens an editor with commit type options.

> [!IMPORTANT]
> This feature will likely be moved to a separate tool in the future.
