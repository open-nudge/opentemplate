"""Postprocess inline."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mdformat.renderer import WRAP_POINT

from ._helpers import FILLER_CHAR, MKDOCS_INDENT_COUNT, get_conf, rstrip_result

if TYPE_CHECKING:
    from mdformat.renderer import RenderContext, RenderTreeNode

FILLER = FILLER_CHAR * (MKDOCS_INDENT_COUNT - 2)  # `mdformat` default is two spaces
"""A spacer that is inserted and then removed to ensure proper word wrap."""


@rstrip_result
def postprocess_list_wrap(
    text: str,
    node: RenderTreeNode,
    context: RenderContext,
) -> str:
    """Postprocess inline tokens.

    Fix word wrap for lists to account for the change in indentation.
    We fool word wrap by prefixing an unwrappable dummy string of the same length.
    This prefix needs to be later removed (in `merge_parsed_text`).

    Adapted from:
    https://github.com/hukkin/mdformat-gfm/blob/cf316a121b6cf35cbff7b0ad6e171f287803f8cb/src/mdformat_gfm/plugin.py#L86-L111

    """
    if not context.do_wrap:
        return text
    wrap_mode = get_conf(context.options, "wrap")
    if (
        not isinstance(wrap_mode, int)  # noqa: PLR0916
        or FILLER_CHAR in text
        or (node.parent and node.parent.type != "paragraph")
        or (
            node.parent
            and node.parent.parent
            and node.parent.parent.type != "list_item"
        )
    ):
        return text

    counter_ = -1
    parent = node.parent
    while parent and parent.type == "paragraph":
        parent = parent.parent
        counter_ += 1
    indent_count = max(counter_, 0)

    text = text.lstrip(WRAP_POINT).lstrip()
    filler = (FILLER * indent_count)[:-1] if indent_count else ""
    newline_filler = filler + FILLER if indent_count else FILLER[:-1]
    if len(text) > wrap_mode:
        indent_length = MKDOCS_INDENT_COUNT * indent_count
        wrapped_length = -1 * wrap_mode
        words: list[str] = []
        split = text.split(WRAP_POINT)
        for idx, word in enumerate(split):
            next_length = wrapped_length + len(word)
            if not words:
                words = [filler, word]
                wrapped_length = indent_length + len(word)
            elif next_length > wrap_mode:
                if idx < len(split) - 1:
                    words += [word, newline_filler]
                    wrapped_length = indent_length + len(word)
                else:
                    words.append(word)
                    wrapped_length = len(word)
            else:
                words.append(word)
                wrapped_length = next_length + 1
        return WRAP_POINT.join(_w for _w in words if _w)
    return f"{filler}{WRAP_POINT}{text}" if filler else text
