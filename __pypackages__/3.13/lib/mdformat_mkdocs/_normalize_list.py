"""Normalize list indentation."""

from __future__ import annotations

import re
from contextlib import suppress
from enum import Enum
from itertools import starmap
from typing import TYPE_CHECKING, Any, Callable, Literal, NamedTuple, TypeVar

from more_itertools import unzip, zip_equal

from ._helpers import (
    EOL,
    FILLER_CHAR,
    MKDOCS_INDENT_COUNT,
    get_conf,
    rstrip_result,
    separate_indent,
)
from .mdit_plugins import MATERIAL_ADMON_MARKERS, MATERIAL_CONTENT_TAB_MARKERS

if TYPE_CHECKING:
    from collections.abc import Mapping

    from mdformat.renderer import RenderContext, RenderTreeNode

# ======================================================================================
# FP Helpers

Tin = TypeVar("Tin")
Tout = TypeVar("Tout")


def map_lookback(
    func: Callable[[Tout, Tin], Tout],
    items: list[Tin],
    initial: Tout,
) -> list[Tout]:
    """Modify each item based on the result of the modification to the prior item.

    Returns:
        list[Tout]: output of the function

    """
    results = [initial]
    for item in items:
        result = func(results[-1], item)
        results.append(result)
    return results[1:]


# ======================================================================================
# Parsing Operations

MARKERS = MATERIAL_CONTENT_TAB_MARKERS.union(MATERIAL_ADMON_MARKERS)
"""All block type markers."""

RE_LIST_ITEM = re.compile(r"(?P<bullet>[\-*]|\d+\.)\s+(?P<item>.+)")
"""Match `bullet` and `item` against `content`."""


class Syntax(Enum):
    """Non-standard line types."""

    CODE_BULLETED = "CODE_BULLETED"
    CODE_NUMBERED = "CODE_NUMBERED"
    LIST_BULLETED = "LIST_BULLETED"
    LIST_NUMBERED = "LIST_NUMBERED"
    START_MARKED = "START_MARKED"
    EDGE_CODE = "EDGE_CODE"
    HTML = "HTML"

    @classmethod
    def from_content(cls, content: str) -> Syntax | None:
        """Determine Syntax type from string.

        Returns:
            Syntax | None: Syntax if identified

        """
        if match := RE_LIST_ITEM.fullmatch(content):
            is_numbered = match["bullet"] not in {"-", "*"}
            if match["item"].startswith("```"):
                return cls.CODE_NUMBERED if is_numbered else cls.CODE_BULLETED
            return cls.LIST_NUMBERED if is_numbered else cls.LIST_BULLETED
        if any(content.startswith(f"{marker} ") for marker in MARKERS):
            return cls.START_MARKED
        if content.startswith("```"):
            return cls.EDGE_CODE
        if content.startswith("<"):
            return cls.HTML
        return None


SYNTAX_CODE_LIST = {Syntax.CODE_BULLETED, Syntax.CODE_NUMBERED}
"""The start of a code block, which is also the start of a list."""


class ParsedLine(NamedTuple):
    """Parsed Line of text."""

    line_num: int
    indent: str
    content: str
    syntax: Syntax | None


class LineResult(NamedTuple):
    """Parsed Line of text."""

    parsed: ParsedLine
    parents: list[ParsedLine]
    prev_list_peers: list[ParsedLine]  # Only applicable for lists


def _is_parent_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    """Return true if previous line has content and a lower indent (e.g. parent)."""
    return bool(prev_line.parsed.content) and len(parsed.indent) > len(
        prev_line.parsed.indent,
    )


def _is_peer_list_line(prev_line: LineResult, parsed: ParsedLine) -> bool:
    """Return True if two list items share the same scope and level."""
    list_types = {
        *SYNTAX_CODE_LIST,
        Syntax.LIST_BULLETED,
        Syntax.LIST_NUMBERED,
    }
    return (
        parsed.syntax in list_types
        and prev_line.parsed.syntax in list_types
        and len(parsed.indent) == len(prev_line.parsed.indent)
    )


def parse_line(line_num: int, content: str) -> ParsedLine:
    """Create summary object separating line from content.

    Returns:
        ParsedLine: summary object

    """
    indent, content = separate_indent(content)
    syntax = Syntax.from_content(content)
    return ParsedLine(
        line_num=line_num,
        indent=indent,
        content=content,
        syntax=syntax,
    )


def acc_line_results(parsed_lines: list[ParsedLine]) -> list[LineResult]:
    """Accumulate ParsedLines into summary LineResults.

    Returns:
        list[LineResult]: summary object

    """
    results: list[LineResult] = []
    for parsed in parsed_lines:
        parent_idx = 0
        parents = []
        with suppress(StopIteration):
            parent_idx, parent = next(
                (len(results) - idx, line)
                for idx, line in enumerate(results[::-1])
                if _is_parent_line(line, parsed)
            )
            parents = [*parent.parents, parent.parsed]

        prev_list_peers = [
            line.parsed
            for line in results[parent_idx:][::-1]
            if _is_peer_list_line(line, parsed)
        ]

        result = LineResult(
            parsed=parsed,
            parents=parents,
            prev_list_peers=prev_list_peers,
        )
        results.append(result)
    return results


# ======================================================================================
# Block Parsing Operations


def _get_inner_indent(block_indent: BlockIndent, line_indent: str) -> str:
    """Return white space to the right of the outer indent block."""
    if block_indent.kind == "HTML":
        # PLANNED: Consider restoring some pretty indentation for HTML
        #   But the problem is that a single space is added to each line
        #       from somewhere else in mdformat that needs to be undone or
        #       accounted for
        #   This feature may require knowing when the HTML block ends
        return ""

    if (outer_indent_len := len(block_indent.raw_indent)) <= len(line_indent):
        return line_indent[outer_indent_len:]
    return block_indent.raw_indent


class BlockIndent(NamedTuple):
    """Track the parsed code block indentation."""

    start_line: int
    raw_indent: str
    indent_depth: int
    kind: Literal["code", "HTML"]


def _parse_code_block(last: BlockIndent | None, line: LineResult) -> BlockIndent | None:
    """Identify fenced or indented sections internally referred to as 'code blocks'."""
    result = last
    if line.parsed.syntax in {
        *SYNTAX_CODE_LIST,
        Syntax.EDGE_CODE,
    }:
        # On first edge, start tracking a code block
        #   on the second edge, stop tracking
        result = (
            None
            if last
            else BlockIndent(
                start_line=line.parsed.line_num,
                raw_indent=line.parsed.indent,
                indent_depth=len(line.parents),
                kind="code",
            )
        )
    return result


def _parse_html_line(last: BlockIndent | None, line: LineResult) -> BlockIndent | None:
    """Identify sections of HTML."""
    result = last
    if line.parsed.syntax == Syntax.HTML:
        # Start tracking an HTML block if not already
        result = last or BlockIndent(
            start_line=line.parsed.line_num,
            raw_indent=line.parsed.indent,
            indent_depth=len(line.parents),
            kind="HTML",
        )
    elif last and not line.parsed.content:
        # Stop tracking an HTML block on a line break
        result = None
    return result


# ======================================================================================
# Semantic Indent Handling


class SemanticIndent(Enum):
    """Possible states for evaluating semantic indents. The values aren't relevant."""

    INITIAL = "Hack for MyPy and map_lookack, which returns initial..."
    EMPTY = ""
    ONE_LESS_ON_NEXT = "⤓(←)"
    ONE_LESS_SPACE = "←"
    TWO_LESS_ON_NEXT = "⤓(←←)"  # Bulleted
    TWO_LESS_SPACE = "←←"


def _parse_semantic_indent(
    last: SemanticIndent,
    tin: tuple[LineResult, BlockIndent | None],
) -> SemanticIndent:
    """Conditionally evaluate when semantic indents are necessary."""
    # PLANNED: This works, but is very confusing
    line, code_indent = tin

    if (
        not line.parsed.content
        or code_indent is not None
        or line.parsed.syntax in SYNTAX_CODE_LIST
    ):
        result = SemanticIndent.EMPTY

    elif line.parsed.syntax == Syntax.LIST_BULLETED:
        result = SemanticIndent.TWO_LESS_ON_NEXT
    elif line.parsed.syntax == Syntax.LIST_NUMBERED:
        result = SemanticIndent.ONE_LESS_ON_NEXT

    elif last == SemanticIndent.TWO_LESS_ON_NEXT:
        result = SemanticIndent.TWO_LESS_SPACE
    elif last == SemanticIndent.ONE_LESS_ON_NEXT:
        result = SemanticIndent.ONE_LESS_SPACE
    else:
        result = last

    return result


def _trim_semantic_indent(indent: str, s_i: SemanticIndent) -> str:
    """Removes spaces based on SemanticIndent."""
    if s_i == SemanticIndent.ONE_LESS_SPACE:
        return indent[:-1]
    if s_i == SemanticIndent.TWO_LESS_SPACE:
        return indent[:-2]
    return indent


# ======================================================================================
# High-Level Accumulators

DEFAULT_INDENT = " " * MKDOCS_INDENT_COUNT
"""Default indent."""


def _format_new_indent(line: LineResult, block_indent: BlockIndent | None) -> str:
    """Normalize the list indent."""
    result = ""
    if line.parsed.content:
        if block_indent:
            depth = block_indent.indent_depth
            extra_indent = _get_inner_indent(
                block_indent=block_indent,
                line_indent=line.parsed.indent,
            )
            result = DEFAULT_INDENT * depth + extra_indent
        elif line.parents and line.parents[-1].syntax in SYNTAX_CODE_LIST:
            depth = len(line.parents) - 1
            match = RE_LIST_ITEM.fullmatch(line.parents[-1].content)
            assert match  # for pyright
            extra_indent = " " * (len(match["bullet"]) + 1)
            result = DEFAULT_INDENT * depth + extra_indent
        else:
            result = DEFAULT_INDENT * len(line.parents)
    return result


class ParsedText(NamedTuple):
    """Intermediary result of parsing the text."""

    new_lines: list[tuple[str, str]]
    # Used only for debugging purposes
    debug_original_lines: list[LineResult]
    debug_block_indents: list[BlockIndent | None]


def _format_new_content(line: LineResult, inc_numbers: bool, is_code: bool) -> str:
    """Normalize the list bullet or number."""
    new_content = line.parsed.content
    if not is_code and line.parsed.syntax in {
        Syntax.LIST_BULLETED,
        Syntax.LIST_NUMBERED,
    }:
        list_match = RE_LIST_ITEM.fullmatch(line.parsed.content)
        assert list_match  # for pyright
        new_bullet = "-"
        if line.parsed.syntax == Syntax.LIST_NUMBERED:
            first_peer = (
                line.prev_list_peers[-1] if line.prev_list_peers else line.parsed
            )
            base_num = 0 if first_peer.content.startswith("0.") else 1
            counter = len(line.prev_list_peers) + base_num if inc_numbers else base_num
            new_bullet = f"{counter}."
        new_content = f"{new_bullet} {list_match['item']}"

    return new_content


def _insert_newlines(
    parsed_lines: list[LineResult],
    zipped_lines: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Extend zipped_lines with newlines if necessary."""
    newline = ("", "")
    new_lines: list[tuple[str, str]] = []
    for line, zip_line in zip_equal(parsed_lines, zipped_lines):
        new_lines.append(zip_line)
        if (
            line.parsed.syntax == Syntax.EDGE_CODE
            and line.parents
            and line.parents[-1].syntax in SYNTAX_CODE_LIST
        ):
            new_lines.append(newline)

    return new_lines


def parse_text(*, text: str, inc_numbers: bool, use_sem_break: bool) -> ParsedText:
    """Post-processor to normalize lists.

    Returns:
        ParsedText: result of text parsing

    """
    parsed_lines = [*starmap(parse_line, enumerate(text.rstrip().split(EOL)))]
    lines = acc_line_results(parsed_lines)

    code_indents = map_lookback(_parse_code_block, lines, None)
    html_indents = [
        # Any indents initiated from within a `code_block_indents` should be ignored
        indent if (indent and code_indents[indent.start_line] is None) else None
        for indent in map_lookback(_parse_html_line, lines, None)
    ]
    # When both, code_indents take precedence
    block_indents = [_c or _h for _c, _h in zip_equal(code_indents, html_indents)]
    new_indents = [*starmap(_format_new_indent, zip_equal(lines, block_indents))]

    new_contents = [
        _format_new_content(line, inc_numbers, ci is not None)
        for line, ci in zip_equal(lines, code_indents)
    ]

    if use_sem_break:
        semantic_indents = map_lookback(
            _parse_semantic_indent,
            [*zip(lines, code_indents)],
            _parse_semantic_indent(SemanticIndent.INITIAL, (lines[0], code_indents[0])),
        )
        new_indents = [
            *starmap(
                _trim_semantic_indent,
                zip_equal(new_indents, semantic_indents),
            ),
        ]

    new_lines = _insert_newlines(lines, [*zip_equal(new_indents, new_contents)])
    return ParsedText(
        new_lines=new_lines,
        debug_original_lines=lines,
        debug_block_indents=block_indents,
    )


# ======================================================================================
# Outputs string result


def _join(*, new_lines: list[tuple[str, str]]) -> str:
    """Join ParsedText into a single string representation."""
    new_indents, new_contents = unzip(new_lines)

    new_indents_iter = new_indents

    # Remove filler characters added by inline formatting for 'wrap'
    new_contents_iter = (
        content.replace(f"{FILLER_CHAR} ", "").replace(FILLER_CHAR, "").rstrip()
        for content in new_contents
    )

    return "".join(
        f"{new_indent}{new_content}{EOL}"
        for new_indent, new_content in zip_equal(new_indents_iter, new_contents_iter)
    )


@rstrip_result
def normalize_list(
    text: str,
    node: RenderTreeNode,
    context: RenderContext,
    check_if_align_semantic_breaks_in_lists: Callable[[Mapping[str, Any]], bool],
) -> str:
    """Format markdown list.

    Returns:
        str: formatted text

    """
    if node.level > 1:
        # Note: this function is called recursively,
        #   so only process the top-level item
        return text

    # Retrieve user-options
    inc_numbers = bool(get_conf(context.options, "number"))

    parsed_text = parse_text(
        text=text,
        inc_numbers=inc_numbers,
        use_sem_break=check_if_align_semantic_breaks_in_lists(context.options),
    )
    return _join(new_lines=parsed_text.new_lines)
