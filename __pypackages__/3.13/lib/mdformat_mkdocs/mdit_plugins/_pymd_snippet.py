"""Python-Markdown Extensions: Snippets.

WARNING: matches only the "scissors" portion, leaving the rest unparsed

```md
--8<-- ...
```

Docs: <https://facelessuser.github.io/pymdown-extensions/extensions/snippets>

"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from mdit_py_plugins.utils import is_code_block

from mdformat_mkdocs._synced.admon_factories import new_token

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock

_SNIPPET_MARKER = "--8<--"
_ABBREVIATION_PATTERN = re.compile(rf"^{_SNIPPET_MARKER}(?P<label>.*)")

PYMD_SNIPPET_PREFIX = "pymd_snippet"


def _content(state: StateBlock, start_line: int) -> str:
    """Content."""
    start = state.bMarks[start_line] + state.tShift[start_line]
    maximum = state.eMarks[start_line]
    return state.src[start:maximum]


def _parse(
    state: StateBlock,
    match: re.Match[str],
    start_line: int,
    end_line: int,
) -> tuple[int, str]:
    """Return the max line and matched content."""
    max_line = start_line + 1
    inline = f"{_SNIPPET_MARKER}{match['label']}"

    if not match["label"]:
        max_search = 20  # Upper limit of lines to search for multi-line snippet
        current_line = start_line + 1
        inner: list[str] = []
        while (current_line - start_line) < max_search:
            if max_line == end_line:
                break  # no 'label'
            line = _content(state, current_line)
            if _ABBREVIATION_PATTERN.match(line):
                max_line = current_line + 1
                inline = "\n".join([_SNIPPET_MARKER, *inner, _SNIPPET_MARKER])
                break
            if line:
                inner.append(line)
            current_line += 1

    return max_line, inline


def _pymd_snippet(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    if is_code_block(state, start_line):
        return False

    match = _ABBREVIATION_PATTERN.match(_content(state, start_line))
    if match is None:
        return False

    if silent:
        return True

    max_line, inline = _parse(state, match, start_line, end_line)

    with new_token(state, PYMD_SNIPPET_PREFIX, "p"):
        tkn_inline = state.push("inline", "", 0)
        tkn_inline.content = inline
        tkn_inline.map = [start_line, max_line]
        tkn_inline.children = []

    state.line = max_line

    return True


def pymd_snippet_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "reference",
        PYMD_SNIPPET_PREFIX,
        _pymd_snippet,
        {"alt": ["paragraph"]},
    )
