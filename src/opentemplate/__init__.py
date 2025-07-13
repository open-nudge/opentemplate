# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Official documentation."""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("opentemplate")
"""Latest opentemplate version."""

del version

__all__: list[str] = [
    "__version__",
]
