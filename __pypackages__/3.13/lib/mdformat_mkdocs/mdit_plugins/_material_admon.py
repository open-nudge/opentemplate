"""Match `mkdocs-material` admonitions.

Matches:

```md
!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
```

Docs: <https://squidfunk.github.io/mkdocs-material/reference/admonitions/>

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mdformat_mkdocs._synced.admon_factories import (
    AdmonitionData,
    admon_plugin_factory,
    new_token,
    parse_possible_whitespace_admon_factory,
    parse_tag_and_title,
)

from ._pymd_admon import format_pymd_admon_markup

if TYPE_CHECKING:
    from markdown_it.rules_block import StateBlock

MATERIAL_ADMON_PREFIX = "admonition_mkdocs"
"""Prefix used to differentiate the parsed output."""

MATERIAL_ADMON_MARKERS = {"!!!", "???", "???+"}
"""All supported MkDocs Admonition markers."""


def format_admon_markup(
    state: StateBlock,
    start_line: int,
    admonition: AdmonitionData,
) -> None:
    """Format markup."""
    if admonition.marker == "!!!":
        format_pymd_admon_markup(state, start_line, admonition)
        return

    tags, title = parse_tag_and_title(admonition.meta_text)
    tag = tags[0]

    with new_token(state, MATERIAL_ADMON_PREFIX, "details") as token:
        token.markup = admonition.markup
        token.block = True
        attrs: dict[str, Any] = {"class": " ".join(tags)}
        if admonition.markup.endswith("+"):
            attrs["open"] = "open"
        token.attrs = attrs
        token.meta = {"tag": tag}
        token.info = admonition.meta_text
        token.map = [start_line, admonition.next_line]

        if title:
            title_markup = f"{admonition.markup} {tag}"
            with new_token(
                state,
                f"{MATERIAL_ADMON_PREFIX}_title",
                "summary",
            ) as tkn_title:
                tkn_title.markup = title_markup
                tkn_title.map = [start_line, start_line + 1]

                tkn_inline = state.push("inline", "", 0)
                tkn_inline.content = title
                tkn_inline.map = [start_line, start_line + 1]
                tkn_inline.children = []

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.blkIndent = admonition.old_state.blkIndent
    state.line = admonition.next_line


def admonition_logic(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    """Parse MkDocs-style Admonitions.

    `Such as collapsible blocks
    <https://squidfunk.github.io/mkdocs-material/reference/admonitions/#collapsible-blocks>`.

    .. code-block:: md

        ???+ note
            *content*

    """
    parse_possible_whitespace_admon = parse_possible_whitespace_admon_factory(
        markers=MATERIAL_ADMON_MARKERS,
    )
    result = parse_possible_whitespace_admon(state, start_line, end_line, silent)
    if isinstance(result, AdmonitionData):
        format_admon_markup(state, start_line, admonition=result)
        return True
    return result


material_admon_plugin = admon_plugin_factory(MATERIAL_ADMON_PREFIX, admonition_logic)
