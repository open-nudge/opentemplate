# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests of the package."""

from __future__ import annotations

import opentemplate

# enq: the smoke test is intentionally a small standalone module
# noqa-file: PYNUDGER46


def test_version() -> None:
    """Smoke test package version."""
    # nosemgrep
    # enq: this assertion verifies the public version API directly
    assert opentemplate.__version__ != ""  # noqa: PYNUDGER29
