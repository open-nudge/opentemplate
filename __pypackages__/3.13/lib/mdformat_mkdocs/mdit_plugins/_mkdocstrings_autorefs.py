"""Match 'markdown anchors' from the `mkdocs-autorefs` plugin.

Matches:

```md
[](){#some-anchor-name}
```

Docs: https://mkdocstrings.github.io/autorefs

"""

from __future__ import annotations

import re
from re import Match
from typing import TYPE_CHECKING

from mdformat_mkdocs._synced.admon_factories import new_token

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock
    from markdown_it.rules_inline import StateInline

_AUTOREFS_PATTERN = re.compile(r"\[\]\(<?>?\){#(?P<anchor>[^ }]+)}")
_HEADING_PATTERN = re.compile(r"(?P<markdown>^#{1,6}) (?P<content>.+)")
MKDOCSTRINGS_AUTOREFS_PREFIX = "mkdocstrings_autorefs"
MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX = f"{MKDOCSTRINGS_AUTOREFS_PREFIX}_heading"


def _mkdocstrings_autorefs_plugin(state: StateInline, silent: bool) -> bool:
    match = _AUTOREFS_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if silent:
        return True

    anchor = match["anchor"]
    with new_token(state, MKDOCSTRINGS_AUTOREFS_PREFIX, "a") as token:
        token.attrs = {"id": anchor, "href": ""}
        token.meta = {"content": f"[](){{#{anchor}}}"}

    state.pos += match.end()

    return True


def _mkdocstrings_heading_alias_plugin(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    """Identify when an autoref anchor is directly before a heading.

    Simplified heading parsing adapted from:
    https://github.com/executablebooks/markdown-it-py/blob/c10312e2e475a22edb92abede15d3dcabd0cac0c/markdown_it/rules_block/heading.py

    """
    if state.is_code_block(start_line):
        return False

    # Exit quickly if paragraph doesn't start with an autoref
    start = state.bMarks[start_line] + state.tShift[start_line]
    try:
        if state.src[start : start + 3] != "[](":
            return False
    except IndexError:
        return False

    matches: list[Match[str]] = []
    heading: Match[str] | None = None
    next_line = start_line
    while next_line <= end_line:
        start = state.bMarks[next_line] + state.tShift[next_line]
        maximum = state.eMarks[next_line]
        line = state.src[start:maximum]
        # Catch as many sequential autorefs as possible before a single heading
        if match := _AUTOREFS_PATTERN.match(line):
            matches.append(match)
        else:
            heading = _HEADING_PATTERN.match(line)
            break
        next_line += 1
    if heading is None:  # for pylint
        return False

    if silent:
        return True

    state.line = start_line + 1
    with new_token(state, MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX, "div"):
        for match in matches:
            anchor = match["anchor"]
            with new_token(state, MKDOCSTRINGS_AUTOREFS_PREFIX, "a") as a_token:
                a_token.attrs = {"id": anchor, "href": ""}
                a_token.meta = {"content": f"[](){{#{anchor}}}"}

        level = len(heading["markdown"])
        with new_token(state, "heading", f"h{level}") as h_token:
            h_token.markup = heading["markdown"]
            h_token.map = [start_line, state.line]

            inline = state.push("inline", "", 0)
            inline.content = heading["content"]
            inline.map = [start_line, state.line]
            inline.children = []

    state.line = next_line + 1

    return True


def mkdocstrings_autorefs_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.before(
        "link",
        MKDOCSTRINGS_AUTOREFS_PREFIX,
        _mkdocstrings_autorefs_plugin,
        {"alt": ["link"]},
    )
    md.block.ruler.before(
        "paragraph",
        MKDOCSTRINGS_HEADING_AUTOREFS_PREFIX,
        _mkdocstrings_heading_alias_plugin,
        {"alt": ["paragraph"]},
    )
