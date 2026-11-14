# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

"""Generate the code reference pages and navigation.

Adjusted from:
https://mkdocstrings.github.io/recipes/#bind-pages-to-sections-themselves

Adjusted in order to:

- disregard files starting with `_` as these are considered private

__Please note:__

- This file might need to be edited to fit your needs.
- This file might need refactoring.
"""

from __future__ import annotations

import pathlib

# enq: MkDocs supplies this package only in the documentation environment
import mkdocs_gen_files  # pyrefly: ignore[missing-import]

# enq: this documentation generator is intentionally a small script module
# noqa-file: PYNUDGER46


def main() -> None:
    """Generate the code reference pages and navigation."""
    nav = mkdocs_gen_files.Nav()

    paths = (
        path
        for path in pathlib.Path("src").rglob("*.py")
        if not path.stem.startswith("_") or path.stem == "__init__"
    )
    for path in sorted(paths):
        module_path = path.relative_to("src").with_suffix("")
        doc_path = path.relative_to("src").with_suffix(".md")
        full_doc_path = pathlib.Path("reference", doc_path)

        parts = tuple(module_path.parts)

        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        nav[parts] = doc_path.as_posix()

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            ident = ".".join(parts)
            fd.write(f"::: {ident}")

        mkdocs_gen_files.set_edit_path(full_doc_path, path)

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())


main()
