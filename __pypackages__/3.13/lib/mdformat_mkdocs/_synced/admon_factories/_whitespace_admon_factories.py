"""Note, this is ported from `markdown-it-admon` <https://github.com/commenthol/markdown-it-admon>."""

from __future__ import annotations

import re
from contextlib import contextmanager, suppress
from typing import TYPE_CHECKING, Callable, NamedTuple

from mdit_py_plugins.utils import is_code_block

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

    from markdown_it import MarkdownIt
    from markdown_it.renderer import RendererProtocol
    from markdown_it.ruler import RuleOptionsType
    from markdown_it.rules_block import StateBlock
    from markdown_it.rules_inline import StateInline
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict


def _get_multiple_tags(meta_text: str) -> tuple[list[str], str]:
    """Check for multiple tags when the title is double quoted.

    Raises:
        ValueError: if no tags matched

    """
    re_tags = re.compile(r'^\s*(?P<tokens>[^"]+)\s+"(?P<title>.*)"\S*$')
    if match := re_tags.match(meta_text):
        tags = match["tokens"].strip().split(" ")
        return [tag.lower() for tag in tags], match["title"]
    raise ValueError("No match found for parameters")


def parse_tag_and_title(admon_meta_text: str) -> tuple[list[str], str]:
    """Separate the tag name from the admonition title."""
    if not (meta_text := admon_meta_text.strip()):
        return [""], ""

    with suppress(ValueError):
        return _get_multiple_tags(meta_text)

    tag, *title_ = meta_text.split(" ")
    joined = " ".join(title_)

    title = ""
    if not joined:
        title = tag.title()
    elif joined != '""':  # Specifically check for no title
        title = joined
    return [tag.lower()], title


def validate_admon_meta(meta_text: str) -> bool:
    """Validate the presence of the tag name after the marker."""
    tag = meta_text.strip().split(" ", 1)[-1] or ""
    return bool(tag)


class AdmonState(NamedTuple):
    """Frozen state using the same variable case."""

    parentType: str
    lineMax: int
    blkIndent: int


class AdmonitionData(NamedTuple):
    """AdmonitionData data for rendering."""

    old_state: AdmonState
    marker: str
    markup: str
    meta_text: str
    next_line: int


def search_admon_end(state: StateBlock, start_line: int, end_line: int) -> int:
    was_empty = False

    # Search for the end of the block
    next_line = start_line
    is_fenced = False
    while True:
        next_line += 1
        if next_line >= end_line:
            # unclosed block should be autoclosed by end of document.
            # also block seems to be autoclosed by end of parent
            break
        pos = state.bMarks[next_line] + state.tShift[next_line]
        maximum = state.eMarks[next_line]
        is_empty = state.sCount[next_line] < state.blkIndent

        # two consecutive empty lines autoclose the block, unless the block is fenced
        if not is_fenced and is_empty and was_empty:
            break
        was_empty = is_empty

        # Check if line starts with ```
        if state.src[pos : pos + 3] == "```":
            is_fenced = not is_fenced

        if pos < maximum and state.sCount[next_line] < state.blkIndent:
            # non-empty line with negative indent should stop the block:
            # - !!!
            #  test
            break

    return next_line


def parse_possible_whitespace_admon_factory(
    markers: set[str],
) -> Callable[[StateBlock, int, int, bool], AdmonitionData | bool]:
    expected_marker_len = 3  # Regardless of extra chars, block indent stays the same
    marker_first_chars = {_m[0] for _m in markers}
    max_marker_len = max(len(_m) for _m in markers)

    def parse_possible_whitespace_admon(
        state: StateBlock,
        start_line: int,
        end_line: int,
        silent: bool,
    ) -> AdmonitionData | bool:
        if is_code_block(state, start_line):
            return False

        start = state.bMarks[start_line] + state.tShift[start_line]
        maximum = state.eMarks[start_line]

        # Exit quickly on a non-match for first char
        if state.src[start] not in marker_first_chars:
            return False

        # Check out the rest of the marker string
        marker = ""
        marker_len = max_marker_len
        marker_pos = 0
        markup = ""
        while marker_len > 0:
            marker_pos = start + marker_len
            if (markup := state.src[start:marker_pos]) in markers:
                marker = markup
                break
            marker_len -= 1
        else:
            return False

        admon_meta_text = state.src[marker_pos:maximum]
        if not validate_admon_meta(admon_meta_text):
            return False
        # Since start is found, we can report success here in validation mode
        if silent:
            return True

        old_state = AdmonState(
            parentType=state.parentType,
            lineMax=state.lineMax,
            blkIndent=state.blkIndent,
        )
        state.parentType = "admonition"

        blk_start = marker_pos
        while blk_start < maximum and state.src[blk_start] == " ":
            blk_start += 1

        # Correct block indentation when extra marker characters are present
        marker_alignment_correction = expected_marker_len - len(marker)
        state.blkIndent += blk_start - start + marker_alignment_correction

        next_line = search_admon_end(state, start_line, end_line)

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = next_line
        return AdmonitionData(
            old_state=old_state,
            marker=marker,
            markup=markup,
            meta_text=admon_meta_text,
            next_line=next_line,
        )

    return parse_possible_whitespace_admon


@contextmanager
def new_token(
    state: StateBlock | StateInline,
    name: str,
    kind: str,
) -> Generator[Token, None, None]:
    """Create scoped token."""
    yield state.push(f"{name}_open", kind, 1)
    state.push(f"{name}_close", kind, -1)


def default_render(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    _options: OptionsDict,
    env: EnvType,
) -> str:
    """Render token if no more specific renderer is specified."""
    return self.renderToken(tokens, idx, _options, env)  # type: ignore[attr-defined]


RenderType = Callable[..., str]


def admon_plugin_factory(
    prefix: str,
    logic: Callable[[StateBlock, int, int, bool], bool],
) -> Callable[[MarkdownIt, RenderType | None], None]:
    def admon_plugin(md: MarkdownIt, render: RenderType | None = None) -> None:
        render = render or default_render

        md.add_render_rule(f"{prefix}_open", render)
        md.add_render_rule(f"{prefix}_close", render)
        md.add_render_rule(f"{prefix}_title_open", render)
        md.add_render_rule(f"{prefix}_title_close", render)

        options: RuleOptionsType = {
            "alt": ["paragraph", "reference", "blockquote", "list"],
        }
        md.block.ruler.before("fence", prefix, logic, options)

    return admon_plugin
