"""Public Extension."""

from __future__ import annotations

from collections.abc import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render

from .mdit_plugins import GFM_ALERTS_PREFIX, gfm_alerts_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser to identify Alerts."""
    mdit.use(gfm_alerts_plugin)


def _render_alert(node: RenderTreeNode, context: RenderContext) -> str:
    if node.nester_tokens is not None:
        open_token = node.nester_tokens.opening
        close_token = node.nester_tokens.closing

        result = f"> [!{open_token.meta['title'].upper()}]"

        open_token.type = "blockquote_open"
        open_token.tag = "blockquote"
        open_token.meta = {}

        close_token.type = "blockquote_close"
        close_token.tag = "blockquote"

        # checking if inner node has non empty renderable
        for inner_node in node.walk(include_self=False):
            if not inner_node.is_nested and inner_node.render(context=context).strip():
                result += "\n" + node.render(context=context).lstrip()
                break
        return result
    raise ValueError("Alert node should have nester tokens.")


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {GFM_ALERTS_PREFIX: _render_alert}
