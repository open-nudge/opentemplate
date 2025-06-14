"""Python-Markdown Extensions Captions.

Matches:

```md
/// caption
Default values for config variables.
///
```

Docs:
https://github.com/facelessuser/pymdown-extensions/blob/main/pymdownx/blocks/caption.py


"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from mdit_py_plugins.utils import is_code_block

from mdformat_mkdocs._synced.admon_factories._whitespace_admon_factories import (
    new_token,
)

if TYPE_CHECKING:
    from markdown_it import MarkdownIt
    from markdown_it.rules_block import StateBlock

_CAPTION_START_PATTERN = re.compile(
    r"\s*///\s*(?P<type>figure-|table-|)caption\s*(\|\s*(?P<number>[\d\.]+))?",
)
_CAPTION_END_PATTERN = re.compile(r"^\s*///\s*$")
_CAPTION_ATTRS_PATTERN = re.compile(r"^s*(?P<attrs>attrs:\s*\{[^}]*\})\s*$")
PYMD_CAPTIONS_PREFIX = "mkdocs_caption"


def _src_in_line(state: StateBlock, line: int) -> tuple[str, int, int]:
    """Get the source in a given line number."""
    start_pos = state.bMarks[line] + state.tShift[line]
    end_pos = state.eMarks[line]
    return state.src[start_pos:end_pos], start_pos, end_pos


def _parse(
    state: StateBlock,
    first_line_max_pos: int,
    start_line: int,
    end_line: int,
) -> tuple[int, str, str | None]:
    """Parse a caption block: optionally read attrs and extract content."""
    end_match = None
    max_line = start_line + 1
    end_pos = -1
    attrs_text, _, attrs_max_pos = _src_in_line(state, max_line)
    caption_attrs_match = _CAPTION_ATTRS_PATTERN.match(attrs_text)
    content_start_pos = (
        first_line_max_pos + 1 if caption_attrs_match is None else attrs_max_pos + 1
    )
    attrs = (
        caption_attrs_match.group("attrs") if caption_attrs_match is not None else None
    )
    if not isinstance(attrs, str):
        attrs = None

    while end_match is None and max_line <= end_line:
        line_text, end_pos, _ = _src_in_line(state, max_line)
        if _CAPTION_END_PATTERN.match(line_text) is None:
            max_line += 1
        else:
            end_match = max_line

    return max_line, state.src[content_start_pos:end_pos], attrs


def _material_captions(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    """Detect caption blocks and wrap them in a token."""
    if is_code_block(state, start_line):
        return False

    first_line_text, _, first_line_max_pos = _src_in_line(state, start_line)
    start_match = _CAPTION_START_PATTERN.match(first_line_text)
    if start_match is None:
        return False

    if silent:
        return True

    max_line, content, attrs = _parse(state, first_line_max_pos, start_line, end_line)

    with (
        new_token(state, PYMD_CAPTIONS_PREFIX, "figcaption") as token,
        new_token(state, "", "p"),
    ):
        token.info = start_match.group("type") + "caption"
        token.meta = {"number": start_match.group("number")}
        if attrs is not None:
            token.meta["attrs"] = attrs
        tkn_inline = state.push("inline", "", 0)
        tkn_inline.content = content.strip()
        tkn_inline.map = [start_line, max_line]
        tkn_inline.children = []

    state.line = max_line + 1

    return True


def pymd_captions_plugin(md: MarkdownIt) -> None:
    md.block.ruler.before(
        "fence",
        PYMD_CAPTIONS_PREFIX,
        _material_captions,
        {"alt": ["paragraph"]},
    )
