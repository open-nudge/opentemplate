"""An mdformat plugin for rendering tables."""

__version__ = "1.0.0"

from .plugin import (  # noqa: F401
    POSTPROCESSORS,
    RENDERERS,
    add_cli_options,
    update_mdit,
)
