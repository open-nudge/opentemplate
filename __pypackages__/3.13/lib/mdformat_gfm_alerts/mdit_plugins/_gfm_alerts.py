"""GitHub Alerts."""

from __future__ import annotations

import re
from functools import cached_property
from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

GFM_ALERTS_PREFIX = "gfm_alert"
"""Prefix used to differentiate the parsed output."""

GFM_ALERT_OPEN = f"{GFM_ALERTS_PREFIX}_open"
GFM_ALERT_CLOSE = f"{GFM_ALERTS_PREFIX}_close"

DEFAULT_TITLES = ["TIP", "NOTE", "IMPORTANT", "WARNING", "CAUTION"]


class AlertRuleFactory:
    """Identifies blockquote tokens and transforms them to alert tokens."""

    def __init__(
        self,
        titles: list[str] | None = None,
        icons: dict[str, str] | None = None,
        class_prefix: str = "markdown-alert",
        *,
        parse_nested: bool = True,
        match_case_sensitive: bool = False,
    ) -> None:
        if titles is None:
            titles = DEFAULT_TITLES
        self.titles = titles
        if icons is None:
            icons = {}
        self.icons = icons

        self.class_prefix = class_prefix
        self.parse_nested = parse_nested
        self.match_case_sensitive = match_case_sensitive

    @cached_property
    def patterns(
        self,
    ) -> list[re.Pattern[str]]:
        marker_name_re = "\\w+" if self.titles == ["*"] else "|".join(self.titles)
        flags = 0 if self.match_case_sensitive else re.IGNORECASE
        return [
            re.compile(
                r"^(?P<marker>\*\*(?P<title>(Note|Warning))\*\*:?)\s*(?P<inline>[^\\n\\r]*)?",
                flags=flags,
            ),
            re.compile(
                rf"^(?P<marker>\\?\[!(?P<title>({marker_name_re}))\\?\])\s*(?P<inline>[^\\n\\r]*)?",
                flags=flags,
            ),
        ]

    @staticmethod
    def _get_first_inline(tokens: list[Token], start: int, end: int) -> Token | None:
        return next(
            (t for t in tokens[start : end + 1] if t.type == "inline"),
            None,
        )

    def _block_to_alerts_if_matched(
        self,
        tokens: list[Token],
        start_index: int,
        end_index: int,
    ) -> None:
        first_inline = self._get_first_inline(tokens, start_index, end_index)
        if not first_inline:
            return

        match = self.patterns[0].match(first_inline.content) or self.patterns[1].match(
            first_inline.content,
        )

        if not match:
            return

        title = match.group("title").strip()
        icon = self.icons.get(title.lower(), "")

        first_inline.content = first_inline.content[
            len(match.group("marker")) :
        ].lstrip()

        open_token = tokens[start_index]
        close_token = tokens[end_index]

        open_token.type = GFM_ALERT_OPEN
        open_token.tag = "div"
        open_token.meta = {
            "title": title,
            "icon": icon,
        }

        close_token.type = GFM_ALERT_CLOSE
        close_token.tag = "div"

    def get_rule(self) -> Callable[[StateCore], None]:
        def github_alerts_rule(state: StateCore) -> None:
            tokens = state.tokens
            i = 0
            start_indices = []
            while i < len(tokens):
                if tokens[i].type == "blockquote_open":
                    start_indices.append(i)
                elif tokens[i].type == "blockquote_close":
                    start_index = start_indices.pop()
                    if self.parse_nested or not start_indices:
                        self._block_to_alerts_if_matched(
                            tokens,
                            start_index,
                            end_index=i,
                        )
                i += 1

        return github_alerts_rule


def gfm_alerts_plugin(
    md: MarkdownIt,
    titles: list[str] | None = None,
    icons: dict[str, str] | None = None,
    class_prefix: str = "markdown-alert",
    *,
    parse_nested: bool = True,
    match_case_sensitive: bool = False,
) -> None:
    github_alerts_rule = AlertRuleFactory(
        titles=titles,
        icons=icons,
        class_prefix=class_prefix,
        parse_nested=parse_nested,
        match_case_sensitive=match_case_sensitive,
    ).get_rule()

    md.core.ruler.after("block", GFM_ALERTS_PREFIX, github_alerts_rule)

    def render_alert_open(
        self: RendererProtocol,  # noqa: ARG001
        tokens: list[Token],
        idx: int,
        options,  # noqa: ANN001,ARG001
        env,  # noqa: ANN001,ARG001
    ) -> str:
        meta = tokens[idx].meta
        return (
            f'<div class="{class_prefix} {class_prefix}-{meta["title"].lower()}">\n'
            f'<p class="{class_prefix}-title">'
            f"{meta['icon']}{meta['title'].title()}</p>\n"
        )

    def render_alert_close(
        self: RendererProtocol,  # noqa: ARG001
        tokens: list[Token],  # noqa: ARG001
        idx: int,  # noqa: ARG001
        options,  # noqa: ANN001,ARG001
        env,  # noqa: ANN001,ARG001
    ) -> str:
        return "</div>"

    md.add_render_rule("gfm_alert_open", render_alert_open)
    md.add_render_rule("gfm_alert_close", render_alert_close)
