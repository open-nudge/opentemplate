import re

from markdown_it import MarkdownIt
import mdformat.plugins
from mdformat.renderer import DEFAULT_RENDERERS, RenderContext, RenderTreeNode
from mdit_py_plugins.tasklists import tasklists_plugin

from mdformat_gfm._mdit_gfm_autolink_plugin import gfm_autolink_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    # Enable GFM autolink extension
    mdit.use(gfm_autolink_plugin)

    # Enable mdformat-tables plugin
    tables_plugin = mdformat.plugins.PARSER_EXTENSIONS["tables"]
    if tables_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(tables_plugin)
        tables_plugin.update_mdit(mdit)

    # Enable strikethrough markdown-it extension
    mdit.enable("strikethrough")

    # Enable tasklist markdown-it extension
    mdit.use(tasklists_plugin)


def _strikethrough_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    content = "".join(child.render(context) for child in node.children)
    return "~~" + content + "~~"


def _render_with_default_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    """Render the node using default renderer instead of the one in `context`.

    We don't use `RenderContext.with_default_renderer_for` because that
    changes the default renderer in context, where it's applied
    recursively to render functions of children.
    """
    syntax_type = node.type
    text = DEFAULT_RENDERERS[syntax_type](node, context)
    for postprocessor in context.postprocessors.get(syntax_type, ()):
        text = postprocessor(text, node, context)
    return text


def _is_task_list_item(node: RenderTreeNode) -> bool:
    assert node.type == "list_item"
    classes = node.attrs.get("class", "")
    assert isinstance(classes, str)
    return "task-list-item" in classes


def _list_item_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    if not _is_task_list_item(node):
        return _render_with_default_renderer(node, context)

    # Tasklists extension makes a bit weird token stream where
    # tasks are annotated by html. We need to remove the HTML.
    paragraph_node = node.children[0]
    inline_node = paragraph_node.children[0]
    assert inline_node.type == "inline"
    assert inline_node.children, "inline token must have children"
    html_inline_node = inline_node.children[0]
    assert 'class="task-list-item-checkbox"' in html_inline_node.content

    # This is naughty, shouldn't mutate and rely on `.remove` here
    inline_node.children.remove(html_inline_node)

    checkmark = "x" if 'checked="checked"' in html_inline_node.content else " "

    text = _render_with_default_renderer(node, context)

    if context.do_wrap:
        wrap_mode = context.options["mdformat"]["wrap"]
        if isinstance(wrap_mode, int):
            text = text[4:]  # Remove the "xxxx" added in `_postprocess_inline`
    # Strip leading space chars (numeric representations)
    text = re.sub(r"^(&#32;)+", "", text)
    text = text.lstrip()
    return f"[{checkmark}] {text}"


def _postprocess_inline(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    """Postprocess inline tokens.

    Fix word wrap of the first line in a task list item. It should be
    wrapped narrower than normal because of the "[ ] " prefix that
    indicates a task list item. We fool word wrap by prefixing an
    unwrappable dummy string of the same length. This prefix needs to be
    later removed (in `_list_item_renderer`).
    """
    if not context.do_wrap:
        return text
    wrap_mode = context.options["mdformat"]["wrap"]
    if not isinstance(wrap_mode, int):
        return text
    if (
        node.parent
        and node.parent.type == "paragraph"
        and not node.parent.previous_sibling
        and node.parent.parent
        and node.parent.parent.type == "list_item"
        and _is_task_list_item(node.parent.parent)
    ):
        text = text.lstrip("\x00")
        text = text.lstrip()
        text = "xxxx" + text
    return text


def _gfm_autolink_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return node.meta["source_text"]


def _escape_text(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    # Escape strikethroughs
    text = text.replace("~~", "\\~~")

    return text


_RE_GFM_TICK_BOX = re.compile(r"^\[([ xX])]", flags=re.MULTILINE)


def _escape_paragraph(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    # Escape tasklists
    text = _RE_GFM_TICK_BOX.sub(r"\[" + r"\g<1>" + r"\]", text)

    return text


RENDERERS = {
    "s": _strikethrough_renderer,
    "list_item": _list_item_renderer,
    "gfm_autolink": _gfm_autolink_renderer,
}
POSTPROCESSORS = {
    "text": _escape_text,
    "inline": _postprocess_inline,
    "paragraph": _escape_paragraph,
}
