import re

from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline

from mdformat_gfm import _gfm
from mdformat_gfm._text_inline_rule import text_rule


def gfm_autolink_plugin(md: MarkdownIt) -> None:
    """Markdown-it plugin to parse GFM autolinks."""
    md.inline.ruler.before("linkify", "gfm_autolink", gfm_autolink)

    # The default "text" inline rule will skip starting characters of GFM
    # autolinks. It can be disabled, but that is disastrous for performance.
    # Instead, we replace it with a custom "text" inline rule that yields at
    # locations that can potentially be the beginning of a GFM autolink.
    md.inline.ruler.at("text", text_rule)


# A string that matches this must still be invalidated if it ends with "_" or "-"
RE_GFM_EMAIL = re.compile(r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+")
# A string that matches this must still be invalidated if last two segments contain "_"
RE_GFM_AUTOLINK_DOMAIN = re.compile(r"[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+")

RE_ENDS_IN_ENTITY_REF = re.compile(r"&[a-zA-Z0-9]+;\Z")

ASCII_ALPHANUMERICS = frozenset(
    "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "0123456789"
)


def gfm_autolink(state: StateInline, silent: bool) -> bool:  # noqa: C901
    """Markdown-it-py rule to parse GFM autolinks.

    This parser autolinks as specified here:
    https://github.github.com/gfm/#autolinks-extension-

    Args:
        state: Parse state object.
        silent: Disables token generation.
    Returns:
        bool: True if GFM autolink found.
    """
    # Prevents autolink parsing in link and image labels
    if state.level > 0:
        return False

    pos = state.pos
    src = state.src

    # Autolink can only be at the beginning of a line, after whitespace,
    # or any of the delimiting characters *, _, ~, and (.
    if pos:
        preceding_char = src[pos - 1]
        if preceding_char not in _gfm.BEFORE_AUTOLINK_CHARS:
            return False

    if src.startswith("www.", pos):
        pos += 4
        try:
            pos, domain, resource = read_domain_and_resource(src, pos)
        except NotFound:
            return False

        url = f"www.{domain}{resource}"
        full_url = "http://" + url
    elif src.startswith(("http://", "https://"), pos):
        scheme = "https://" if src[pos + 4] == "s" else "http://"
        pos += len(scheme)

        try:
            pos, domain, resource = read_domain_and_resource(src, pos)
        except NotFound:
            return False

        url = f"{scheme}{domain}{resource}"
        full_url = url
    elif src.startswith(("mailto:", "xmpp:"), pos):
        scheme = "xmpp:" if src[pos] == "x" else "mailto:"
        pos += len(scheme)

        try:
            pos, email = read_email(src, pos)
        except NotFound:
            return False

        if scheme == "xmpp:" and src[pos : pos + 1] == "/":
            pos += 1
            resource_start_pos = pos
            while pos < len(src) and src[pos] in ASCII_ALPHANUMERICS | {".", "@"}:
                pos += 1
            resource = src[resource_start_pos:pos]
            if resource.endswith("."):
                pos -= 1
                resource = resource[:-1]
            if not resource:
                return False
        else:
            resource = ""

        source_autolink = scheme + email
        if resource:
            source_autolink += "/" + resource

        url = source_autolink
        full_url = source_autolink
    else:
        try:
            pos, email = read_email(src, pos)
        except NotFound:
            return False

        url = email
        full_url = "mailto:" + email

    normalized_full_url = state.md.normalizeLink(full_url)
    if not state.md.validateLink(normalized_full_url):
        return False

    push_tokens(state, normalized_full_url, url, silent)
    state.pos = pos
    return True


def push_tokens(
    state: StateInline, full_url: str, source_url: str, silent: bool
) -> None:
    if silent:
        return
    token = state.push("gfm_autolink_open", "a", 1)
    token.attrs = {"href": full_url}
    token.meta = {"source_text": source_url}

    token = state.push("text", "", 0)
    token.content = state.md.normalizeLinkText(source_url)

    state.push("gfm_autolink_close", "a", -1)


def trim_resource(untrimmed: str) -> tuple[str, int]:
    """Trim illegal trailing chars from autolink resource.

    Trim trailing punctuation, parentheses and entity refs as per GFM
    spec. Also trim backslashes. The spec does not mention backslash,
    but I think it should. This is referred to as "extended autolink
    path validation" in the GFM spec. Return a tuple with the trimmed
    resource and the amount of characters removed.
    """
    i = len(untrimmed) - 1
    while i >= 0:
        c = untrimmed[i]
        if c == ";":
            ending_entity_match = RE_ENDS_IN_ENTITY_REF.search(untrimmed, endpos=i + 1)
            if not ending_entity_match:
                break
            i = ending_entity_match.start()
        elif c == ")":
            if untrimmed.count("(", 0, i + 1) >= untrimmed.count(")", 0, i + 1):
                break
        elif c in {"?", "!", ".", ",", ":", "*", "_", "~"}:
            pass
        elif c == "\\":  # not part of the spec, but should be
            pass
        else:
            break
        i -= 1

    trimmed = untrimmed[: i + 1]
    trim_count = len(untrimmed) - len(trimmed)
    return trimmed, trim_count


class NotFound(Exception):
    """Raised if a function didn't find what it was looking for."""


def read_domain_and_resource(src: str, pos: int) -> tuple[int, str, str]:
    """Read autolink domain and resource.

    Raise NotFound if not found. Return a tuple (pos, domain, resource).
    """
    domain_match = RE_GFM_AUTOLINK_DOMAIN.match(src, pos)
    if not domain_match:
        raise NotFound
    domain = domain_match.group()
    pos = domain_match.end()
    segments = domain.rsplit(".", 2)
    if "_" in segments[-2] or "_" in segments[-1]:
        raise NotFound

    resource_start_pos = pos
    while pos < len(src) and src[pos] not in _gfm.WHITESPACE | {"<"}:
        pos += 1
    resource = src[resource_start_pos:pos]

    resource, trim_count = trim_resource(resource)
    pos -= trim_count
    return pos, domain, resource


def read_email(src: str, pos: int) -> tuple[int, str]:
    """Read autolink email.

    Raise NotFound if not found. Return a tuple (pos, email).
    """
    email_match = RE_GFM_EMAIL.match(src, pos)
    email = email_match.group() if email_match else None
    if not email or email[-1] in {"-", "_"}:
        raise NotFound
    assert email_match is not None
    pos = email_match.end()

    # This isn't really part of the GFM spec, but an attempt to cover
    # up its flaws. If a trailing hyphen or underscore invalidates an
    # autolink, then an escaped hyphen or underscore should too.
    if src[pos : pos + 2] in {"\\-", "\\_"}:
        raise NotFound

    return pos, email
