<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Development dependencies (PEP582)

This folder contains project dependencies
as defined by (rejected) [PEP582 specification](https://peps.python.org/pep-0582/).

This approach allows us to:

- Manage dependencies in a well-defined manner
- Install/update dependencies for all Python versions
- Keep dependencies separated (within `.git` folder instead of `venv`)
- Test without using third party tools such as `tox` or `nox`
