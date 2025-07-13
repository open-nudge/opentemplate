# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Preprocess documentation files.

Script below does the following:

- Changes absolute GitHub links to mkdocs-compatible relative links,
    for example, `[link](/docs/file.txt)` to `[link](../file.txt)`
    if the file is located in `/docs/tutorials`.
- Allows users to remove block of markdown which look inconsistent
    between `GitHub` and `MkDocs` rendering (removes everything between
    `"<!-- mkdocs remove start -->"`
    and `"<!-- mkdocs remove end -->"`).
"""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re

import mkdocs_gen_files


@dataclasses.dataclass
class _LinkReplacer:
    """Replace absolute GitHub links with mkdocs-compatible relative links."""

    path: pathlib.Path

    def __post_init__(self) -> None:
        """Post-initialization method."""
        self._subpath()

    def __call__(self, match: re.Match[str]) -> str:
        """Replace the link with its path-local counterpart.

        Args:
            path: Path to the file.
            match: The match object.

        Returns:
            The preprocessed link

        """
        new_link = pathlib.Path(
            os.path.relpath(match.group(2), self.path),
        )

        return f"[{match.group(1)}]({pathlib.Path(*new_link.parts[1:])})"

    def _subpath(self) -> None:
        """Give a path, cuts it at the first occurrence of "docs".

        Args:
            path: The path to cut.

        Returns:
            The cut path.

        """
        subpath = []
        cut = False
        for part in self.path.parts:
            if part == "docs":
                cut = True
            if cut:
                subpath.append(part)

        self.path = pathlib.Path(
            "/",
            *subpath,  # pyright: ignore[reportUnknownArgumentType]
        )


def remove_blocks(content: str) -> str:
    """Remove blocks of markdown inconsistent between GitHub and MkDocs.

    Args:
        content: The content of the file.

    Returns:
        The preprocessed content.

    """
    return re.sub(
        r"<!-- mkdocs remove start -->(.|\n)*?<!-- mkdocs remove end -->",
        "",
        content,
    )


def main() -> None:
    """Change GitHub absolute links to mkdocs-compatible relative links."""
    pattern = re.compile(r"\[(.*?)\]\((/docs/.*?)\)")

    for path in sorted(pathlib.Path("docs").rglob("*.md")):
        with path.open() as file:
            content = file.read()

        updated_content = pattern.sub(_LinkReplacer(path), content)
        updated_content = remove_blocks(updated_content)

        with mkdocs_gen_files.open(
            path.relative_to("docs"), "w"
        ) as virtual_file:
            virtual_file.write(updated_content)


main()
