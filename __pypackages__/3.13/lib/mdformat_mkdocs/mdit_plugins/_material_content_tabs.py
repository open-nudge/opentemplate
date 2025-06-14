"""Match `mkdocs-material` Content Tabs.

Matches:

```md
=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```
```

Docs: <https://squidfunk.github.io/mkdocs-material/reference/content-tabs>

"""

from markdown_it.rules_block import StateBlock

from mdformat_mkdocs._synced.admon_factories import (
    AdmonitionData,
    admon_plugin_factory,
    new_token,
    parse_possible_whitespace_admon_factory,
)

MATERIAL_CONTENT_TAB_PREFIX = "content_tab_mkdocs"
"""Prefix used to differentiate the parsed output."""

MATERIAL_CONTENT_TAB_MARKERS = {"===", "===!", "===+"}
"""All supported content tab markers."""


def format_content_tab_markup(
    state: StateBlock,
    start_line: int,
    admonition: AdmonitionData,
) -> None:
    """WARNING: this is not the proper markup for MkDocs.

    Would require recursively calling the parser to identify all sequential
    content tabs

    """
    title = admonition.meta_text.strip().strip("'\"")

    with new_token(state, MATERIAL_CONTENT_TAB_PREFIX, "div") as token:
        token.markup = admonition.markup
        token.block = True
        token.attrs = {"class": "content-tab"}
        token.info = admonition.meta_text
        token.map = [start_line, admonition.next_line]

        with new_token(state, f"{MATERIAL_CONTENT_TAB_PREFIX}_title", "p") as tkn_inner:
            tkn_inner.attrs = {"class": "content-tab-title"}
            tkn_inner.map = [start_line, start_line + 1]

            tkn_inline = state.push("inline", "", 0)
            tkn_inline.content = title
            tkn_inline.map = [start_line, start_line + 1]
            tkn_inline.children = []

        state.md.block.tokenize(state, start_line + 1, admonition.next_line)

    state.parentType = admonition.old_state.parentType
    state.lineMax = admonition.old_state.lineMax
    state.blkIndent = admonition.old_state.blkIndent
    state.line = admonition.next_line


def content_tab_logic(
    state: StateBlock,
    start_line: int,
    end_line: int,
    silent: bool,
) -> bool:
    # Because content-tabs look like admonitions syntactically, we can
    #   reuse admonition parsing logic
    # Supported variations from: https://facelessuser.github.io/pymdown-extensions/extensions/tabbed
    parse_possible_whitespace_admon = parse_possible_whitespace_admon_factory(
        markers=MATERIAL_CONTENT_TAB_MARKERS,
    )
    result = parse_possible_whitespace_admon(state, start_line, end_line, silent)
    if isinstance(result, AdmonitionData):
        format_content_tab_markup(state, start_line, admonition=result)
        return True
    return result


material_content_tabs_plugin = admon_plugin_factory(
    MATERIAL_CONTENT_TAB_PREFIX,
    content_tab_logic,
)
