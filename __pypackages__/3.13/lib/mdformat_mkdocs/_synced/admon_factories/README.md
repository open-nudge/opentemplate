# Admonition/Callout Factories

This code is useful to format and render admonitions similar to Python Markdown's format

If you are looking to add `mdformat` to your project to format a specific syntax, you will want to use one of the below plugins:

- [`mdformat-admon`](https://github.com/KyleKing/mdformat-admon)
    - [`python-markdown` admonitions](https://python-markdown.github.io/extensions/admonition)
- [`mdformat-mkdocs`](https://github.com/KyleKing/mdformat-mkdocs)
    - [MKDocs Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions)
- [`mdformat-gfm-alerts`](https://github.com/KyleKing/mdformat-gfm-alerts)
    - Primarily supports [Github "Alerts"](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts), but indirectly also supports
        - [Microsoft "Alerts"](https://learn.microsoft.com/en-us/contribute/content/markdown-reference#alerts-note-tip-important-caution-warning)
        - [Mozilla Callouts](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Howto/Markdown_in_MDN#notes_warnings_and_callouts)
- [`mdformat-obsidian`](https://github.com/KyleKing/mdformat-obsidian)
    - [Obsidian Callouts](https://help.obsidian.md/How+to/Use+callouts)

However, directive-style admonition formats are not known to be supported by an existing mdformat plugin nor by the utility code in this directory as it exists today:

- [node.js markdown-it-container](https://github.com/markdown-it/markdown-it-container)
- [MyST](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html)
- [Sphinx Directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html)
- [reStructuredText](https://docutils.sourceforge.io/docs/ref/rst/directives.html#specific-admonitions)
- [pymdown-extensions](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition)
- [PyMDown](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition)
