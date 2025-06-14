from __future__ import annotations

from collections.abc import Mapping
import textwrap

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.footnote import footnote_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, adding the footnote plugin."""
    mdit.use(footnote_plugin)
    # Disable inline footnotes for now, since we don't have rendering
    # support for them yet.
    mdit.disable("footnote_inline")


def _footnote_ref_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"[^{node.meta['label']}]"


def _footnote_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    first_line = f"[^{node.meta['label']}]:"
    indent = " " * 4
    elements = []
    with context.indented(len(indent)):
        for child in node.children:
            if child.type == "footnote_anchor":
                continue
            elements.append(child.render(context))
    body = textwrap.indent("\n\n".join(elements), indent)
    # if the first body element is a paragraph, we can start on the first line,
    # otherwise we start on the second line
    if body and node.children and node.children[0].type != "paragraph":
        body = "\n" + body
    else:
        body = " " + body.lstrip()
    return first_line + body


def _render_children(node: RenderTreeNode, context: RenderContext) -> str:
    return "\n\n".join(child.render(context) for child in node.children)


RENDERERS: Mapping[str, Render] = {
    "footnote": _footnote_renderer,
    "footnote_ref": _footnote_ref_renderer,
    "footnote_block": _render_children,
}
