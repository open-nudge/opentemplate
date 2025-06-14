# Whitespace characters, as specified in
# https://github.github.com/gfm/#whitespace-character
# (spec version 0.29-gfm (2019-04-06)
WHITESPACE = frozenset(" \t\n\v\f\r")

BEFORE_AUTOLINK_CHARS = WHITESPACE | {"*", "_", "~", "("}
