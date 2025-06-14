import io
import sys
from typing import Mapping

from markdown_it import MarkdownIt
import mdformat.renderer
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdit_py_plugins.front_matter import front_matter_plugin
import ruamel.yaml

yaml = ruamel.yaml.YAML()
# Make sure to always have `sequence >= offset + 2`
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = sys.maxsize


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.use(front_matter_plugin)


def _render_frontmatter(node: RenderTreeNode, context: RenderContext) -> str:
    # Safety check - parse and dump yaml to ensure it is correctly formatted
    dump_stream = io.StringIO()
    try:
        parsed = yaml.load(node.content)
        yaml.dump(parsed, stream=dump_stream)
    except ruamel.yaml.YAMLError as e:
        mdformat.renderer.LOGGER.warning(f"Invalid YAML in a front matter block: {e}.")
        formatted_yaml = node.content + "\n"
    else:
        formatted_yaml = dump_stream.getvalue()
        # Remove the YAML closing tag if added by `ruamel.yaml`
        if formatted_yaml.endswith("\n...\n"):
            formatted_yaml = formatted_yaml[:-4]

    return node.markup + "\n" + formatted_yaml + node.markup


# apply the render function to the block identified by the mdit plugin
RENDERERS: Mapping[str, Render] = {"front_matter": _render_frontmatter}
