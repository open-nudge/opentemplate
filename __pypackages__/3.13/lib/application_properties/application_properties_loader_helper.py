"""
Module to provide helpers for the loaders to share.
"""

# pylint: disable=too-few-public-methods
from typing import Callable, Optional


class ApplicationPropertiesLoaderHelper:
    """
    Class to provide helpers for the loaders to share.
    """

    @staticmethod
    def set_error_handler_if_not_set(
        handle_error_fn: Optional[Callable[[str, Optional[Exception]], None]]
    ) -> Callable[[str, Optional[Exception]], None]:
        """
        If the error_handler is not set, make sure to set it to print to output.
        """
        if not handle_error_fn:

            def print_error_to_stdout(
                formatted_error: str, thrown_exception: Optional[Exception]
            ) -> None:
                _ = thrown_exception
                print(formatted_error)

            handle_error_fn = print_error_to_stdout
        return handle_error_fn


# pylint: enable=too-few-public-methods
