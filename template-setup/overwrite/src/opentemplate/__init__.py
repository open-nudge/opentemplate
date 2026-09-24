# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Official documentation."""

from __future__ import annotations

from importlib.metadata import version as _version

__version__ = _version("opentemplate")
"""Current opentemplate version."""

__all__: list[str] = [
    "__version__",
]
