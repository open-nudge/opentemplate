"""Matches `mkdocstrings` cross-references.

Matches:

```md
[package.module.object][]
[Object][package.module.object]
```

Docs: <https://mkdocstrings.github.io/usage/#cross-references>

"""

import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from mdformat_mkdocs._synced.admon_factories import new_token

_CROSSREFERENCE_PATTERN = re.compile(r"\[(?P<link>[^[|\]\n]+)\]\[(?P<href>[^\]\n]*)\]")
MKDOCSTRINGS_CROSSREFERENCE_PREFIX = "mkdocstrings_crossreference"


def _mkdocstrings_crossreference(state: StateInline, silent: bool) -> bool:
    match = _CROSSREFERENCE_PATTERN.match(state.src[state.pos : state.posMax])
    if not match:
        return False

    if silent:
        return True

    original_pos = state.pos
    original_pos_max = state.posMax
    state.pos += 1
    state.posMax = state.pos + len(match["link"])
    with new_token(state, MKDOCSTRINGS_CROSSREFERENCE_PREFIX, "a") as token:
        token.attrs = {"href": f"#{match['href'] or match['link']}"}
        token.meta = {"content": match.group()}

        state.linkLevel += 1
        state.md.inline.tokenize(state)
        state.linkLevel -= 1

    state.pos = original_pos
    state.posMax = original_pos_max
    state.pos += match.end()

    return True


def mkdocstrings_crossreference_plugin(md: MarkdownIt) -> None:
    md.inline.ruler.push(
        MKDOCSTRINGS_CROSSREFERENCE_PREFIX,
        _mkdocstrings_crossreference,
    )
