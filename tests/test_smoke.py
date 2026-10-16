# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Smoke tests of the package."""

from __future__ import annotations

from importlib import resources

import opentemplate

# enq: pytest requires the test_ prefix, which pynudger counts as a shared word
# noqa-file: PYNUDGER43


def test_version() -> None:
    """Smoke test package version."""
    # nosemgrep
    # enq: this assertion verifies the public version API directly
    assert opentemplate.__version__ != ""  # noqa: PYNUDGER29


def test_typed() -> None:
    """Installed package ships the py.typed marker (PEP 561)."""
    assert (resources.files(opentemplate) / "py.typed").is_file()
